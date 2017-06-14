# This class is for handling the communication with the Version Control system
# Either Perforce or Git
from P4 import P4,P4Exception

class PerforceVcHandler:

    def __init__(self, repository_url, branch = "master", path=None):
        self.p4 = P4()  # Create the P4 instance
        self.p4.port = repository_url
        self.p4.user = "joshio"
        self.p4.client = "joshio_workspace"
        self.path = path;

    def get_changed_files(self,base_build_hash, current_build_hash):
        changed_files = []
        try:  # Catch exceptions with try/except
            self.p4.connect()  # Connect to the Perforce server
            file_1 = self.path+"...@"+str(base_build_hash)
            file_2 = self.path +"...@"+str(current_build_hash)
            files = self.p4.run("diff2", "-q", file_1, file_2);
            for file in files:
                try:
                    depot_file_string = file['depotFile']+"#"+(file['rev']);
                    depot_file2_string = file['depotFile2']+"#"+(file['rev2']);
                    file1_content = self.p4.run("print",depot_file_string);
                    file2_content = self.p4.run("print",depot_file2_string);
                    #Actual content is stored in the 1st index of the list. 0th index stores metadata.
                    changed_files.append([file['depotFile'], file1_content[1], file2_content[1]])
                except P4Exception:
                    for e1 in self.p4.errors:  # Display errors
                        print (e1)
            self.p4.disconnect()  # Disconnect from the server
        except P4Exception:
            for e in self.p4.errors:  # Display errors
                print (e)
        return changed_files;

    def setup_repository(self):
        try:  # Catch exceptions with try/except
            self.p4.connect()  # Connect to the Perforce server
            info = self.p4.run("info")  # Run "p4 info" (returns a dict)
            for key in info[0]:  # and display all key-value pairs
                print (key, "=", info[0][key])
            # self.p4.run("edit", "file.txt")  # Run "p4 edit file.txt"
            self.p4.disconnect()  # Disconnect from the server
            return True
        except P4Exception:
            for e in self.p4.errors:  # Display errors
                print (e)

    def get_changed_file_paths(self,repo, base_build_hash,current_build_hash):
        diff = repo.git.diff('{}..{}'.format(base_build_hash, current_build_hash), name_only=True)
        changed_files_path = diff.split("\n")
        #Filter only .java files
        changed_java_files_path = [x for x in changed_files_path if x.endswith(".java")]
        return changed_java_files_path