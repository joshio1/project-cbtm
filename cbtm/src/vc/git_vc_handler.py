# This class is for handling the communication with the Version Control system
# Either Perforce or Git
import os
from src import settings
from git import Repo
from git import Git

class GitVcHandler:

    def __init__(self, repository_url="", repo_folder="", branch = ""):
        self.repository_url = repository_url or settings.get("VersionControl","git_repo_url")
        self.branch = branch or settings.get("Product","branch")
        self.repo_folder_path = repo_folder or settings.get("VersionControl", "git_repo_url")

    def get_changed_files(self,base_build_hash, current_build_hash, extension = ""):
        repo = self.setup_repository()
        changed_files = []
        if repo is not None:
            # print ("Setup Successful")
            changed_files_path = self.get_changed_file_paths(repo, base_build_hash, current_build_hash,extension);
            for change_file_path,relative_path_for_git in changed_files_path:
                try:
                    file_contents_base = repo.git.show('{}:{}'.format(base_build_hash, relative_path_for_git))
                    file_contents_current = repo.git.show('{}:{}'.format(current_build_hash, relative_path_for_git))
                    relative_path_to_store = relative_path_for_git.replace("/", os.path.sep)
                    #The path we get from git has "/" separators. But we want "\" for windows, hence we use os.pathsep. So that it is similar to what is stored in the database
                    changed_files.append([change_file_path, file_contents_base, file_contents_current, relative_path_to_store])
                except Exception as e:
                    print("Could not get file contents for ",change_file_path,e)
        else:
            print ("Error while setting up code repository.")
        return changed_files;

    def setup_repository(self):
        """Create an empty repository in {#DIR_NAME}.
        For fetching the diffs, Git requires the repository to be locally checked out."""
        if not os.path.isdir(self.repo_folder_path):
            os.makedirs(self.repo_folder_path)
        repo = Repo.init(self.repo_folder_path)
        return repo

    def fetch_latest_repo(self,repo):
        """Fetches the latest update from the repository"""

        ###Check if there exists and remote origin already setup
        if any(x.name == "origin" for x in repo.remotes):
            origin = repo.remotes['origin']
        else:
            origin = repo.create_remote('origin', self.repository_url)

        key_path = 'C:/Users/joshio/.ssh/id_rsa'
        git_ssh_identity_file = os.path.expanduser(key_path)
        git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file

        with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
            origin.fetch()

        repo.head.ref.set_tracking_branch(origin.refs.master)
        origin.pull()

    def get_changed_file_paths(self,repo, base_build_hash,current_build_hash,extension = ""):
        """Fetches the file path of all the changed files from the previous build, i.e the current build to the base build"""
        diff = repo.git.diff('{}..{}'.format(base_build_hash, current_build_hash), name_status=True)
        changed_files_path = diff.split("\n")
        changed_selected_files_path=[]
        if(extension):
            for x in changed_files_path:
                split = x.split("\t")#x is of the form M\tFILE_NAME. We want only those file names which have "M", i.e. modified status
                if (split[0] == "M" and split[1].endswith(extension)):
                    changed_selected_files_path.append([repo.working_tree_dir+os.path.sep+split[1].replace("/",os.path.sep),split[1]])
                    # While returning, we return a list of tuples. Inside a tuple, the first column is the full abosulte path replacing forward slashes by the separator in the current OS.
                    # Second column in the tuple is the relative path from the project. This path is required for the further operation of retriving the file contents from the relative path and hash of the commit
            # Earlier Code -> changed_selected_files_path = [(repo.working_tree_dir+os.path.sep+x.replace("/","\\"),x) for x in changed_files_path if x.endswith(extension)]
            return changed_selected_files_path
        return changed_files_path

