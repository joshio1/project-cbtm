from src.lang.c_parser import  CParser
from src.vc.git_vc_handler import GitVcHandler

class DeltaFetcher:

    def __init__(self, repo_folder = ""):
        self.vc = GitVcHandler(repo_folder=repo_folder)
        self.language_parser = CParser()
        self.extension = ".cpp"

    def get_changed_methods_for_current_build(self, base_build_hash, current_build_hash):
        changed_files_path = self.vc.get_changed_files(base_build_hash,current_build_hash,extension = self.extension)
        # Filter only .java files
        changed_methods =[]
        changed_java_files_path = [x for x in changed_files_path if x[0].endswith(self.extension)]
        for [change_file_path, file_contents_base, file_contents_current, relative_path_to_store] in changed_java_files_path:
            common_method_dictionary = self.language_parser.get_common_methods(relative_path_to_store, file_contents_base,file_contents_current)
            # print ("File - "+change_file_path+":")
            for [base_method,current_method] in common_method_dictionary.items():
                if(base_method != (current_method)):
                    # print (base_method.name + ": False")
                    changed_methods.append(base_method)
        return changed_methods