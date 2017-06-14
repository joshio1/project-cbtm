import linecache
import subprocess
import os
#This class is used to handle parsing of C/ C++ files.
#It currently used Universal Tags(ctags) to parse C++ files
class CParser:
    def __init__(self):
        pass

    def get_common_methods(self,actual_file_project_path, file_contents_base="", file_contents_current="", file_path_base="", file_path_current = "" ):
        '''Actual File Project Path is the path at which this file is located in the project
         Note that this is different from the file location on which we run the ctags command.
         Because, for ctags we create a dummy file at a temporary location.
         We need to store the actual file project path in the Functions object and not the dummy file path'''
        try:
            if not file_path_base:
                #Since we dont have a file, we need to create one and write its contents.
                new_file_path_base="file_path_base.cpp"
                with open(new_file_path_base, "w") as f:
                    f.write(file_contents_base)
                    file_path_base = os.path.realpath(f.name)#If Python is run from somewhere else, still running ctags on this file should work. Hence, take absolute path of this file.

            if not file_path_current:
                new_file_path_current = "file_path_current.cpp"
                with open(new_file_path_current, "w") as f:
                    f.write(file_contents_current)
                    file_path_current=os.path.realpath(f.name)

            base_function_list = self.create_functions_from_source(file_path_base,actual_file_project_path)
            current_function_list = self.create_functions_from_source(file_path_current,actual_file_project_path)
            common_method_pairs = {}
            for f in base_function_list:
                for cf in current_function_list:
                    if f.same_as(cf):
                        common_method_pairs[f]=cf
                        break
            return common_method_pairs
        except Exception as e:
            print("Error in getting common method names",e)
        finally:
            if new_file_path_base and os.path.exists(new_file_path_base):
                os.remove(new_file_path_base)
            if new_file_path_current and os.path.exists(new_file_path_current):
                os.remove(file_path_current)

            # Same as get_common_methods. Since uses same_as dummy method. This is also dummy. Used for testing
    def get_common_methods_dummy(self, file_contents_base="", file_contents_current="", file_path_base="", file_path_current = ""):
        base_function_list = self.create_functions_from_source(file_path_base)
        current_function_list = self.create_functions_from_source(file_path_current)
        common_method_pairs = {};
        for f in base_function_list:
            for cf in current_function_list:
                if f.same_as_dummy(cf):
                    common_method_pairs[f]=cf;
                    break;
        return common_method_pairs

    #This function is used to create a list of objects of class Functions from the C++ source files
    def create_functions_from_source(self, source, actual_file_project_path):
        '''Actual File Project Path is the path at which this file is located in the project
         Note that this is different from the file location on which we run the ctags command.
         Because, for ctags we create a dummy file at a temporary location.
         We need to store the actual file project path in the Functions object and not the dummy file path'''
        three_up = os.path.abspath(os.path.join(__file__, "../../.."))
        ctags_path=three_up+os.path.sep+"bin"+os.path.sep+"ctags"+os.path.sep+"ctags"
        output = subprocess.check_output([ctags_path,'--c++-kinds=f','--fields=+enftS-k', '-o','-','--sort=no', source]);
        output_string = output.decode("utf-8")
        result = []
        for row in output_string.split('\n'):
            f = Function.from_string(row, source, actual_file_project_path);
            if f:
                result.append(f);
        return result

    def get_line_function_mapping(self, source, actual_file_project_path):
        '''This function returns a mapping of line numbers versus methods. i.e. line numbers as keys and method at that particular line as value.
        If no method is present, simply Nothing will be stored
        Refer http://ctags.sourceforge.net/ctags.html for information about the tags'''
        three_up = os.path.abspath(os.path.join(__file__, "../../.."))
        ctags_path=three_up+os.path.sep+"bin"+os.path.sep+"ctags"+os.path.sep+"ctags"
        output = subprocess.check_output([ctags_path,'--c++-kinds=f','--fields=+enftS-k', '-o','-','--sort=no', source]);
        output_string = output.decode("utf-8")
        line_function_map = {}
        for row in output_string.split('\n'):
            f = Function.from_string(row, source, actual_file_project_path);
            if(f):
                for i in range(f.line_start, f.line_end):
                    line_function_map[i] = f;
        return line_function_map

class Function:

    def __init__(self, name="", file="", scope = ""):
        self.name = name
        self.file = file
        self.scope = scope
        self.line_start = None
        self.line_end = None
        self.parameter_list = None
        self.return_type = None

    @classmethod
    def from_string(self,ctag_input,file_source, actual_file_project_path):
        '''Actual File Project Path is the path at which this file is located in the project
        Note that this is different from the file location on which we run the ctags command.
        Because, for ctags we create a dummy file at a temporary location.
        We need to store the actual file project path in the Functions object and not the dummy file path'''
        try:
            split_input = ctag_input.split("\t")
            if(len(split_input) >6):
                f = self(split_input[0],actual_file_project_path)
                for fields in split_input[3:]: #split_input[3:] will start iterate from the fourth element. If we iterate also for first and second element, we may get a false positive hit in field_split[0] in if..elif..elif for the first and second index, even though our actual fields start from the third index
                    field_split = fields.split(":",1)
                    if(len(field_split)>1):
                        if("class" in field_split[0]):
                            f.scope = field_split[1]
                        elif("typeref" in field_split[0]):
                            f.return_type = field_split[1]
                        elif("signature" in field_split[0]):
                            f.parameter_list = field_split[1]
                        elif("end" in field_split[0]):
                            f.line_end = int(field_split[1].strip())
                        elif ("line" in field_split[0]):
                            f.line_start = int(field_split[1].strip())
                body = []
                linecache.clearcache()
                try:
                    '''Get function body by parsing the source file and extracting lines from start to end'''
                    for i in range(f.line_start,f.line_end):
                        body.append(linecache.getline(file_source, i))
                    body.append(linecache.getline(file_source,f.line_end))
                except Exception as e:
                    print("Error in getting function body for "+file_source,e);
                f.body = body;
                return f;
        except Exception as e1:
            print("Error in decoding a Function object from string for : "+str(file_source),e1)
        return None

    def same_as_dummy(self,other):
        '''This method is a dummy method which does not check the file. Currently it is only for testing when file names are ought to be different.
        This method will check if two methods are same, i.e. without comparing their body.
        A method can be uniquely identified by the file path in which the method is, and its class(scope), its name, its parameter list, its return type'''
        return \
            self.scope == other.scope\
            and self.name == other.name\
            and self.parameter_list == other.parameter_list\
            and self.return_type == other.return_type;

    def same_as(self, other):
        '''This method will check if two methods are same, i.e. without comparing their body.
        A method can be uniquely identified by the file path in which the method is, and its class(scope), its name, its parameter list, its return type'''
        return \
            self.file == other.file \
            and self.scope == other.scope \
            and self.name == other.name \
            and self.parameter_list == other.parameter_list \
            and self.return_type == other.return_type;

    def __eq__(self, other):
        '''A method is said to be equal when its fully qualified method name(which is checked by same_as) and its content(body) are equal'''
        if(self.same_as(other)):
            if(len(self.body)==len(other.body)):
                for self_line,other_line in zip(self.body, other.body):
                    if(self_line != other_line):
                        return False;
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Function(name='%s', file='%s', scope='%s')>" % (self.name, self.file, self.scope)

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        value = hash(self.name) ^ hash(self.file) ^ hash(self.name);
        if(self.scope):
            value = value ^ hash(self.scope);
        if(self.parameter_list):
            value = value ^ hash(self.parameter_list)
        if(self.return_type):
            value = value ^ hash(self.return_type)
        for line in self.body:
            value = value ^ hash(line)
        return value


