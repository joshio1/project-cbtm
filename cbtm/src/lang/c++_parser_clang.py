#!/usr/bin/env python
""" Usage: call with <filename> <typename>
"""

import sys
import clang.cindex
# clang.cindex.Config.set_library_path("/Library/Developer/CommandLineTools/usr/lib")

def find_typerefs(node, typename):
    """ Find all references to the type named 'typename'
    """
    if node.kind.is_reference():
        ref_node = clang.cindex.Cursor_ref(node)
        if ref_node.spelling == typename:
            print ('Found %s [line=%s, col=%s]' % (
                typename, node.location.line, node.location.column))
    # Recurse for children of this node
    for c in node.get_children():
        find_typerefs(c, typename)

def callexpr_visitor(node, parent, userdata):
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        print ('Found %s [line=%s, col=%s]' % (
            node.spelling, node.location.line, node.location.column))
    return 2  # means continue visiting recursively

# index = clang.cindex.Index.create()
clang.cindex.Config.set_library_path("/Library/Developer/CommandLineTools/usr/lib")
index = clang.cindex.Index(clang.cindex.conf.lib.clang_createIndex(False, True))

tu = index.parse("demo_code.cpp")
# print 'Translation unit:', tu.spelling
# # find_typerefs(tu.cursor, sys.argv[2])
# print 'Translation unit:', tu.spelling
for child in tu.cursor.get_children():
   print (child.spelling)

for node in tu.cursor:
   print ("pre-order-traversal",node.spelling,node.get_usr())

# clang.cindex.Cursor_visit(
#         tu.cursor,
#         clang.cindex.Cursor_visit_callback(callexpr_visitor),
#         None)