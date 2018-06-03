# Author: William Aldrich
# Created: 05-23-18
# Updated: 06-03-18

# Helpful sites / sites that code is from
# https://github.com/gitpython-developers/GitPython/issues/292
# http://gitpython.readthedocs.io/en/stable/tutorial.html
# https://stackoverflow.com/questions/11968976/list-files-in-only-the-current-directory?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa


import os, time
from git import Repo
import progressbar


# Uses GitPython must download
# Uses progressbar2 must download

# Navigate to the folder that has your git repos inside of it
# Mine is in my home directory so this is where everything takes place

# get home directory
home = os.environ['HOME']

# navigate to home directory
homeDir = os.chdir(home)


# Get folders in current directory
# This should be able to find all git repos even if you add a new one
folders = [f for f in os.listdir('.') if not os.path.isfile(f)]

widgets = ["Percentage: ", progressbar.Percentage(), progressbar.Bar()]
fileLen = len(folders)
bar = progressbar.ProgressBar(widgets=widgets, max_value=fileLen).start()

for pos, folder in enumerate(folders):
    # ignore . directories
    # Change this if your git repos have '.' inside of them
    if '.' in folder:
        continue

    # change directory to inside the file
    insideFile = os.chdir(home + "/" + str(folder))
    # get the files inside the directory
    files = [y for y in os.listdir('.') if os.path.isfile(y)]

    for file in files:
        # if the files have a .git file they are a repository
        if ".git" in file:
            repo = Repo(insideFile)
            # check if anything is untracked or changed
            untracked = repo.untracked_files
            changedFiles = [repo.index.diff(None)]

            # if there are untracked or changed files
            if len(untracked) >= 1 or "<" in str(changedFiles[0]):
                print ("\n\n" + folder + " has untracked or changed files that will be commited.")

                # ask user if they want to add a commit message for the folder
                enterMessage = input("Would you like to add a commit message for: " + folder + "? (y/n) ")

                # add everything
                repo.git.add(A=True)
                index = repo.index

                commitMessage = ""

                # enter a commit message if the user entered y
                # If they didnt, it will give an automatic message
                if("y" in enterMessage or "Y" in enterMessage):
                    commitMessage = input("Enter your message: ")
                else:
                    commitMessage = ("Automatic Update via updateGit.py")

                # Commit all of the untracked or changed files
                index.commit(commitMessage)

                # Push
                repo.git.push('origin')
                print (folder + " Updated.\n")

    # sleep to watch progress bar actually do something
    # if you want it to run faster, get rid of this sleep or the progress bar
    time.sleep(0.1)

    #update the progress bar
    bar.update(pos + 1)

# This will say that the progress bar is finished 100%
bar.finish()

# final print message stating everything is updated or up to date
print ("\nAll git accounts have been updated or are up to date\n")
