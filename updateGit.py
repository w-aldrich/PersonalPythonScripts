# Author: William Aldrich
# Github: https://github.com/w-aldrich
# Created: 05-23-18
# Updated: 09-27-18

# Helpful sites / sites that code is from
# https://github.com/gitpython-developers/GitPython/issues/292
# http://gitpython.readthedocs.io/en/stable/tutorial.html
# https://stackoverflow.com/questions/11968976/list-files-in-only-the-current-directory?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa


import os, sys, argparse
from git import Repo
from git import remote

# Navigate to the folder that has your git repos inside of it
# Mine is in my home directory so this is where everything takes place

'''
Setup of program
Finds the home directory and all of the directories immediately inside that directory
calls goThroughFolders() to do the heavy work
Prints out whether or not all git repos are up to date or not after this program
if not, will print out all repos that need to be updated
'''
def main(additionalDirectory=""):
    # get home directory
    home = os.environ['HOME']
    # navigate to home directory
    if(additionalDirectory != ""):
        home = home + "/" + additionalDirectory
    os.chdir(home)

    # Get folders in current directory
    # This should be able to find all git repos even if you add a new one
    folders = [f for f in os.listdir('.') if not os.path.isfile(f)]

    # Get whether or not everything is up to date as well as the folders that are not up to date
    retVals = goThroughFolders(home, folders)

    # flag for everything up to date
    complete = retVals[0]
    # list of incomplete folders
    incompleteFolders = retVals[1]

    # final print message stating everything is updated or up to date
    if complete:
        print ("\nAll git accounts have been updated or are up to date\n")
    else:
        print ("\nThe following folders are not up to date:")
        for incomplete in incompleteFolders:
            print ("\t" + incomplete)

'''
This will loop through all of the folders for a given directory
skips directories that begin with a .
'''
def goThroughFolders(home, folders):
    # flag if skipping repos
    completeFlag = True
    # list of skipped repos
    incompleteFolders = []


    for pos, folder in enumerate(folders):
        # ignore . directories
        # Change this if your git repos have '.' inside of them or start with '.'
        if '.' in folder:
            continue

        # change directory to inside the file
        insideFile = os.chdir(home + "/" + str(folder))
        # get the files inside the directory
        files = [y for y in os.listdir('.') if os.path.isfile(y)]

        # go through all of the files in the folder
        retVals = goThroughFiles(files, insideFile, folder, completeFlag, incompleteFolders)

        # get the complete flag and list of incomplete folders
        completeFlag = retVals[0]
        incompleteFolders = retVals[1]

    return(completeFlag, incompleteFolders)

'''
This will loop through all of the files for a given folder
Checks for .git to know if it is a repo or not
***
MUST HAVE .git file to actually identify it as a github repo
***
Finds all of the untracked or changed files
'''
def goThroughFiles(files, insideFile, folder, completeFlag, incompleteFolders):
        # loop through the files
        for file in files:
            # if the files have a .git file they are a repository
            if ".git" in file:
                repo = Repo(insideFile)
                # check if anything is untracked or changed
                untracked = repo.untracked_files
                changedFiles = [repo.index.diff(None)]

                # if there are untracked or changed files
                if len(untracked) >= 1 or "<" in str(changedFiles[0]):
                    retVals = commitSteps(folder, untracked, changedFiles, repo, completeFlag, incompleteFolders)
                    completeFlag = retVals[0]
                    incompleteFolders = retVals[1]
        return (completeFlag, incompleteFolders)

'''
Used when have untracked or changed files to commit
Will print out the untracked or changed files
Gives option to add personal message, automated message, or skip committing anything
Will add all files to commit
'''
def commitSteps(folder, untracked, changedFiles, repo, completeFlag, incompleteFolders):
    print ("\n" + folder + " has untracked or changed files that will be committed.")

    if len(untracked) >= 1:
        print("Untracked Files:")
        for un in untracked:
            print ("\t" + un)
    if "<" in str(changedFiles[0]):
        print("Changed Files:")
        for ch in repo.index.diff(None):
            print ("\t" + ch.a_path)

    messageHelpFlag = True
    enterMessage = ""
    while(messageHelpFlag):
        # ask user if they want to add a commit message for the folder
        enterMessage = input("Would you like to add a custom commit message for: " + folder + "? \n")

        if ("y" in enterMessage or "sk" in enterMessage or "n" in enterMessage):
            messageHelpFlag = False
        else:
            print("\nEnter 'y' to add a custom commit message for: " + folder)
            print("Enter 'n' to have an automated message for your commit message for: " + folder)
            print("Enter 'sk' to skip committing for: " + folder + "\n")

    if("sk" in enterMessage or "SK" in enterMessage):
        completeFlag = False
        incompleteFolders.append(folder)
        print("Skipping commits for: " + folder + " \n")
        return (completeFlag, incompleteFolders)

    index = repo.index
    commitMessage = ""
    # add everything
    repo.git.add(A=True)

    # Check if ONLY master branch exists
    # Pull if ONLY master branch exists
    branches = repo.heads
    if (len(branches) <= 1):
        pullReq = repo.remotes.origin
        pullReq.pull()
        print("\n" + folder + ": was pulled before commit\n")

    # enter a commit message if the user entered y
    # If they didnt, it will give an automatic message
    if("y" in enterMessage or "Y" in enterMessage):
        commitMessage = input("Enter your commit message: ")
    else:
        commitMessage = ("Automatic Update via updateGit.py")

    # Commit all of the untracked or changed files
    index.commit(commitMessage)

    # Push
    repo.git.push('origin')
    print (folder + " Updated.\n")
    return (completeFlag, incompleteFolders)


def pullAllRepos(additionalDirectory=""):
    home = os.environ['HOME']

    if additionalDirectory != "":
        home = home + "/" + additionalDirectory

    os.chdir(home)
    folders = [f for f in os.listdir('.') if not os.path.isfile(f)]
    for pos, folder in enumerate(folders):
        if '.' in folder:
            continue
        insideFile = os.chdir(home + "/" + str(folder))
        files = [y for y in os.listdir('.') if os.path.isfile(y)]
        for file in files:
            # if the files have a .git file they are a repository
            if ".git" in file:
                repo = Repo(insideFile)
                branches = repo.heads
                currentBranch = repo.active_branch
                if (len(branches) > 1):
                    branches['master'].checkout()
                pullReq = repo.remotes.origin
                pullReq.pull()
                branches[str(currentBranch)].checkout()
                print("Pulled " + folder)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Update Github Repositories')
    parser.add_argument('-pa', '--pullall', help="Pull all Repositories", action="store_true")
    parser.add_argument('-pu', '--pullupdate', help="Pull all Repositories then check if need to update any", action="store_true")
    args = parser.parse_args()

    if args.pullall:
        pullAllRepos()
        # pullAllRepos("School")
    elif args.pullupdate:
        pullAllRepos()
        # pullAllRepos("School")
        main()
        # main("School")
    else:
        main()
        # main("School")
