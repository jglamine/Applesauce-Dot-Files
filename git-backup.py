#! /usr/bin/env python
#
# James Lamine
#
# Script to copy dot files to a local git repository and push that repo to git-hub
# The list of files to backup is saved in a text file
#
# It would make more sense to write this as a bash script
# 	but I wanted more practice with writing Python code

import sys, shutil, subprocess, re, os

# Configuration variables
listFname = "backup-filelist"
gitRepoPath = "/home/james/git-repos/Applesauce-Dot-Files/"

# Open the file list.
try:
	listFile = open(listFname)
except IOError:
	print ("Error: Unable to open input file:", listFname)
	sys.exit(1)

# Copy files to the git repo directory, only if they have changed
changesMade = False
for path in listFile:
	path = path.strip()

	# initialize variables
	sourceMtime = 900000000000
	destMtime = 0
	try:
		# os.stat will throw OSError if the file doesn't exits
		sourceMtime = os.stat(path).st_mtime
		
		# find the name of the destination file
		fnameMatch = re.search(r"[^/]*$", path)
		if fnameMatch:
			destPath = gitRepoPath + fnameMatch.group()
			destMtime = os.stat(destPath).st_mtime
		
	except OSError:
		pass
	
	# only copy files if the source is newer than the destination file
	if destMtime < sourceMtime:
		shutil.copy(path, gitRepoPath)
		print (path, "-->", destPath)
		changesMade = True # Changes were made to the git repo

# Close the filelist file
listFile.close()


# only run git commands if changes were made to repo files
if changesMade:
	
	# Run git commands
	## git add
	print( "\nRunning command: git add\n")

	gitReturnCode = subprocess.call(["git", "--git-dir=" + gitRepoPath + ".git","--work-tree=" + gitRepoPath, "add", gitRepoPath + "*"])
	if gitReturnCode != 0:
		print ("Error: Unable to run git command: git add")
		sys.exit(1)
	
	## git commit
	print ( "\nRunning command: git commit\n")

	(gitReturnCode, gitOutput) = subprocess.getstatusoutput("git --git-dir=" + gitRepoPath + ".git --work-tree=" + gitRepoPath + " commit -m Commit")
	if gitReturnCode != 0:
		print (gitOutput)
		# Check if it failed because there were no changes to commit.
		match = re.search("nothing to commit \(working directory clean\)", gitOutput)
		if match:
			print ("Done: no changes to backup")
			sys.exit(0)
		else:
			print ("Error: Unable to run git command: git commit")
		sys.exit(1)
	
	## git push origin master
	print ("\nRunning command: git push origin master\n")

	gitReturnCode = subprocess.call(["git", "--git-dir=" + gitRepoPath + ".git","--work-tree=" + gitRepoPath, "push", "origin", "master"])
	if gitReturnCode != 0:
		print ("Error: Unable to run git command: git push origin master")
		sys.exit(1)
	
#if changes weren't made
else:
	print ("Done! Nothing to backup")
