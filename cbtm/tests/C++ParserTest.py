from smart_test_plan_generator.language_parser import CParser

cp = CParser()

file1 = []
with open('./../data/WinEventCatcher.cpp') as f:
    file1.append(f.readlines())

file2 = []
with open('./../data/WinEventCatcher-Copy.cpp') as f2:
    file1.append(f2.readlines())

common_method_dictionary = cp.get_common_methods_dummy(file_path_base="./../data/WinEventCatcher.cpp",file_path_current="./../data/WinEventCatcher-Copy.cpp");
print(common_method_dictionary);

# common_method_dictionary = cp.get_common_methods(file_contents_base,file_contents_current)
for [base_method,current_method] in common_method_dictionary.items():
    if(base_method == (current_method)):
        print (base_method.name+": True")
    else:
        print (base_method.name + ": False")