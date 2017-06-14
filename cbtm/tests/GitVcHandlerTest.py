import git, os
from git import Repo
import subprocess
from git import Git

# key_path = 'C:/Users/joshio/.ssh/id_rsa'
repo_path = 'ssh://git@git.eng.vmware.com/appblast.git'

# ssh_cmd = 'ssh -i C:\\Users\\joshio\\.ssh\\id_rsa'
with Git().custom_environment(GIT_SSH_COMMAND="ssh -i C://Users//joshio//.ssh//id_rsa"):
    repo = Repo.clone_from(repo_path,"vc_appblast")

print("Here")
