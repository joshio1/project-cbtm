import javalang
class JavaParser:
    def __init__(self):
        pass

    def get_common_methods(self, file_contents_base, file_contents_current):
        tree_base = javalang.parse.parse(file_contents_base);
        tree_current = javalang.parse.parse(file_contents_current);
        common_method_pairs = {};
        for base_type in tree_base.types:
            for current_type in tree_current.types:
                if(base_type.name == current_type.name):
                    for base_method in base_type.methods:
                        for current_method in current_type.methods:
                            if(self.check_if_methods_equal(base_method,current_method)):
                                common_method_pairs[base_method] = current_method;
                                break;
                    break;
        return common_method_pairs

    ###TODO
    ###This method will check whether the two methods declarations are equal or not.
    ### This method will not check the body of the method.
    ### This method will just check the signature to verify equality
    def check_if_methods_equal(self,method1,method2):
        return method1.name == method2.name and method1.parameters == method2.parameters and method1.return_type == method2.return_type