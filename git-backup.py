#! /usr/bin/env python
# Script to copy dot files to a local git repository and push that repo to git-hub
# The list of files to backup is saved in a text file

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
for path in listFile:
	path = path.strip()
	
	# initialize variables
	sourceMtime = 900000000000
	destMtime = 0
	try:
		# os.stat will throw OSError if the file doesn't exits
		sourceMtime = os.stat("path").st_mtime
		
		# find the name of the destination file
		fnameMatch = re.search(r"[^/]*$", path)
		if fnameMatch:
			destPath = path + fnameMatch.group()
			destMtime = os.stat(destPath).st_mtime
		
	except OSError:
		pass
	
	# only copy files if the source is newer than the destination file
	if destMtime < sourceMtime:
		shutil.copy(path, gitRepoPath)
	else:
		print ("No changes to copy")
		sys.exit(0)

# Close the filelist file
listFile.close()

# Run git commands
gitReturnCode = subprocess.call(["git", "--git-dir=" + gitRepoPath + ".git","--work-tree=" + gitRepoPath, "add", gitRepoPath + "*"])
if gitReturnCode != 0:
	print ("Error: Unable to run git command: git add")
	sys.exit(1)

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

gitReturnCode = subprocess.call(["git", "--git-dir=" + gitRepoPath + ".git","--work-tree=" + gitRepoPath, "push", "origin", "master"])
if gitReturnCode != 0:
	print ("Error: Unable to run git command: git push origin master")
	sys.exit(1)
