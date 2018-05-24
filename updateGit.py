import os
from git import Repo

# https://github.com/gitpython-developers/GitPython/issues/292
# http://gitpython.readthedocs.io/en/stable/tutorial.html

# get home directory
home = os.environ['HOME']
# navigate to home directory
homeDir = os.chdir(home)

print ("\n\n")

# https://stackoverflow.com/questions/11968976/list-files-in-only-the-current-directory?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

# Get folders in current directory
folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
for f in folders:
    # ignore . directories
    if '.' in f:
        continue
    # change directory to inside the file
    insideFile = os.chdir(home + "/" + str(f))
    # get the files inside the directory
    files = [y for y in os.listdir('.') if os.path.isfile(y)]

    for x in files:
        # if the files have a .git file they are a repository
        if ".git" in x:
            repo = Repo(insideFile)
            # check if anything is untracked
            untracked = repo.untracked_files
            # if there is something untracked...
            # add everything to be commited
            # commit message
            if len(untracked) >= 1:
                repo.git.add(A=True)
                index = repo.index
                index.commit("Automatic Backup via python scripts")
                repo.git.push('origin')
