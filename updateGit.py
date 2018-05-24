import os
from git import Repo

# https://github.com/gitpython-developers/GitPython/issues/292
# http://gitpython.readthedocs.io/en/stable/tutorial.html

# get home directory
home = os.environ['HOME']
# navigate to home directory
homeDir = os.chdir(home)

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
            # check if anything is untracked or changed
            untracked = repo.untracked_files
            changedFiles = [repo.index.diff()]

            for blah in changedFiles:
                print (blah)
            print (len(changedFiles))

            # if there is something untracked...
            # add everything to be commited
            # commit message is "Automatic Backup via python scripts"
            if len(untracked) >= 1 or len(changedFiles) >=1:
                print (f + " Has untracked files that will be commited.")
                repo.git.add(A=True)
                index = repo.index
                index.commit("Automatic Backup via python scripts")
                repo.git.push('origin')
                print (f + " Has been commited and pushed to github.")

print ("All git accounts have been updated")
