/* **********************************************************
 * Copyright (C) 2015 VMware, Inc. All rights reserved.
 * -- VMware Confidential
 * **********************************************************/

/*
 * WinEventCatcher.cpp --
 *
 * Instances of WinEventCatcher track activity on an arbitrary number of
 * Windows Event Handles.  This provides the basis for a replacement for
 * the Windows WaitForMultipleObjects[Ex] API call, which is limited to
 * dealing with only 64 Event Handles.  That's not sufficient for Blast on
 * an RDSH machine where we'd like to be able to manage hundreds of
 * sessions and therefore need to be able to wait on hundreds of worker
 * process event handles.
 */

#include <vm_assert.h>

#include "WinEventCatcher.h"


/*
 * The C callback trampoline function targeted by RegisterWaitForSingleObject
 * is passed only a single 'context' argument but in order to do its job it
 * must be able to obtain a reference to a WinEventCatcher instance and the
 * value of an individual event handle, so we pack those items into an
 * instance of this WECCallbackContext structure and specify a pointer to
 * that structure as the trampoline's 'context' argument'
 */

struct WECCallbackContext {
   WinEventCatcher *ccInstancePtr;
   HANDLE ccHandle;
};

/*
 * In addition to the per-event-handle information required by the callback
 * trampoline, we also need to store a cancellation handle for each event
 * handle.  Both of these things are packed into a WECHandleInfo structure,
 * which is stored in a map keyed by the associated event handle.
 */

struct WECHandleInfo {
   HANDLE hiCancelHandle;
   WECCallbackContext hiCtx;
};


/*
 *-----------------------------------------------------------------------------
 *
 * WinEventCatcher constructor.  Requires a logger and a 'notify' event
 * handle that will be signalled whenever one of the handles being watched
 * by this instance is signalled.  The 'notify' listener can discover which
 * of the watched handles has fired by repeatedly calling GetNextEvent().
 *
 *-----------------------------------------------------------------------------
 */

WinEventCatcher::WinEventCatcher(log4cxx::LoggerPtr log,    // IN
                                 HANDLE notify)             // IN
   :  mLog(log),
      mNotify(notify),
      mQueue(),
      mQueueLock(),
      mHandleMap(),
      mHandleMapLock()
{
}


/*
 *-----------------------------------------------------------------------------
 *
 * WinEventCatcher destructor.  Cancels any leftover watches, discards
 * the corresponding handle map entries empties any previously-notified
 * but not-yet-consumed handles.
 *
 *-----------------------------------------------------------------------------
 */

WinEventCatcher::~WinEventCatcher()
{
   /*
    * Cancel all Handle listeners and discard their map entries, then discard
    * any unconsumed queued events
    */

   {
      std::map<HANDLE, WECHandleInfo *>::iterator iter;
      AbAutoLock al(mHandleMapLock);
      for (iter = mHandleMap.begin(); iter != mHandleMap.end(); ++iter) {
         HANDLE handle = static_cast<HANDLE> (iter->first);
         WECHandleInfo *hip = static_cast<WECHandleInfo *> (iter->second);
         VERIFY(hip != NULL);
         HANDLE cancelHandle = hip->hiCancelHandle;
         CancelCatcher(handle, cancelHandle);
         log("Added comment for change");
         /*
          * Regardless of whether the cancel succeeded or not, go ahead and
          * discard this mapping -- there's nothing else useful we can do in
          * the failure case.
          */

         mHandleMap.erase(iter);
         delete hip;
      }
   }
   {
      AbAutoLock al(mQueueLock);
      while (!mQueue.empty()) {
         mQueue.pop();
      }
   }
}


/*
 *-----------------------------------------------------------------------------
 *
 * CancelCatcher -- an internal helper method that cancels the wait on an
 * individual handle.  Performing the actual cancellation is trivial but
 * wrapping it in this function lets us avoid duplication of the log
 * messages.
 *
 * Results:
 *    TRUE if the deregistration succeeds, FALSE otherwise.
 *
 *-----------------------------------------------------------------------------
 */

bool
WinEventCatcher::CancelCatcher(const HANDLE handle,         // IN
                               const HANDLE cancelHandle)   // IN
{
   bool retval = false;

   if (!UnregisterWait(cancelHandle)) {
      DWORD errcode = GetLastError();
      if (ERROR_IO_PENDING == errcode) {
         // unregister succeeded -- this is informational, not a real error
         retval = true;
         LOG_INFO(mLog,
                "Callback in progress on unregistering wait for handle %"
                              FMTHNDL " with cancel handle %" FMTHNDL,
                handle,
                cancelHandle);
      } else {
         LOG_ERROR(mLog,
                "Failed to unregister wait for handle %" FMTHNDL
                              " with cancel handle %" FMTHNDL ", error:0x%08lx",
                handle,
                cancelHandle,
                errcode);
      }
   } else {
      retval = true;
      LOG_TRACE(mLog,
                "Unregistered wait for handle %" FMTHNDL
                                 " with cancel handle %" FMTHNDL,
                handle,
                cancelHandle);
   }
   return retval;
}


/*
 *-----------------------------------------------------------------------------
 *
 * OnEventCallback -- the instance-level callback for an event on a
 * watched handle.
 *
 *-----------------------------------------------------------------------------
 */

void
WinEventCatcher::OnEventCallback(HANDLE handle)    // IN
{
   {
      AbAutoLock al(mQueueLock);
      mQueue.push(handle);
   }
   SetEvent(mNotify);
}


/*
 *-----------------------------------------------------------------------------
 *
 * CallbackTrampoline -- a static callback function that forwards a
 * signalled handle to the OnEventCallback method in the appropriate
 * WinEventCatcher instance.
 *
 *-----------------------------------------------------------------------------
 */

static VOID CALLBACK
CallbackTrampoline(PVOID context,         // IN
                   BOOLEAN timerFired)    // IN
{
   WECCallbackContext *ccp = (WECCallbackContext *) context;
   VERIFY(NULL != ccp);
   WinEventCatcher *wec = ccp->ccInstancePtr;
   VERIFY(NULL != wec);
   wec->OnEventCallback(ccp->ccHandle);
}


/*
 *-----------------------------------------------------------------------------
 *
 * AddHandle -- accepts an event handle that is to be watched
 *
 * Results:
 *    TRUE if the handle is successfully placed on watch or is already
 *    being watched, otherwise FALSE.
 *
 *-----------------------------------------------------------------------------
 */

bool
WinEventCatcher::AddHandle(HANDLE handle)    // IN: a HANDLE to listen on
{
   bool retval = false;
   std::map<HANDLE, WECHandleInfo *>::iterator iter;
   do {  // do..while(0) lets us 'break' to skip to the end of this block
      AbAutoLock al(mHandleMapLock);
      iter = mHandleMap.find(handle);
      if (iter != mHandleMap.end()) {
         // We are already listening on this HANDLE
         retval = true;
         LOG_WARN(mLog,
                  "Already registered wait for handle %" FMTHNDL,
                  handle);
         break;
      }

      WECHandleInfo *hip = new WECHandleInfo;
      VERIFY(hip != NULL);
      hip->hiCtx.ccInstancePtr = this;
      hip->hiCtx.ccHandle = handle;
      if (!RegisterWaitForSingleObject(&hip->hiCancelHandle,
                                      handle,
                                      CallbackTrampoline,
                                      &hip->hiCtx,
                                      INFINITE,
                                      WT_EXECUTEONLYONCE)) {
         LOG_ERROR(mLog,
                   "Failed to register wait for handle %" FMTHNDL
                                 ", error:0x%08lx",
                   handle,
                   GetLastError());
         delete hip;
         break;
      }

      /*
       * Remember this handle's info (its registration cancellation cookie
       * and callback context) in our internal map
       */

      std::pair<HANDLE, WECHandleInfo *> handleMapInfo =
                        std::pair<HANDLE, WECHandleInfo *>(handle, hip);
      mHandleMap.insert(handleMapInfo);
      retval = true;
      LOG_TRACE(mLog,
                "Registered wait for handle %" FMTHNDL
                                 " with cancel handle %" FMTHNDL,
                handle,
                hip->hiCancelHandle);
   } while (0);
   /* Added comment for adding change*/

   return retval;
}


/*
 *-----------------------------------------------------------------------------
 *
 * RemoveHandle -- stops watching a handle that was previously placed on
 * watch by a call to AddHandle.
 *
 * Results:
 *    TRUE if the watch on the given handle is successfully cancelled,
 *    otherwise FALSE.
 *
 *-----------------------------------------------------------------------------
 */

bool
WinEventCatcher::RemoveHandle(HANDLE handle) // IN: a HANDLE being listened on
{
   bool retval = false;
   {
      std::map<HANDLE, WECHandleInfo *>::iterator iter;
      AbAutoLock al(mHandleMapLock);
      iter = mHandleMap.find(handle);
      if (iter != mHandleMap.end()) {
         HANDLE handle = static_cast<HANDLE> (iter->first);
         WECHandleInfo *hip = static_cast<WECHandleInfo *> (iter->second);
         VERIFY(hip != NULL);
         HANDLE cancelHandle = hip->hiCancelHandle;
         retval = CancelCatcher(handle, cancelHandle);

         /*
          * Regardless of whether the cancel succeeded or not, go ahead and
          * discard this mapping -- there's nothing else useful we can do in
          * the failure case.
          */

         mHandleMap.erase(iter);
         delete hip;
      }
   }
   return retval;
}


/*
 *-----------------------------------------------------------------------------
 *
 * GetNextEvent -- tells the caller the value of a handle that was
 * signalled at some time in the past.  Handles are reported in the
 * order that they were signalled.
 *
 * Results:
 *    The oldest unconsumed handle, or INVALID_HANDLE_VALUE if all
 *    previously-signalled handles have been consumed.
 *
 *-----------------------------------------------------------------------------
 */

HANDLE
WinEventCatcher::GetNextEvent()
{
   HANDLE retval = INVALID_HANDLE_VALUE;

   {
      AbAutoLock al(mQueueLock);
      if (!mQueue.empty()) {
         retval = mQueue.front();
		 /* Added comment for adding change*/
         mQueue.pop();
      }
   }

   return retval;
}
