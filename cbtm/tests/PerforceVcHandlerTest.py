from vc_handler.PerforceVcHandler import PerforceVcHandler

vc = PerforceVcHandler("perforce-qa.eng.vmware.com:1666", path="//depot/documentation/Availability/Tools/bugzilla/");
files = vc.get_changed_files(2194432,2226248);
for file in files:
    for item in file:
        print (item);