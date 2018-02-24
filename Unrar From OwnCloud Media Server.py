import os, sys, shutil, subprocess
from os.path import join,getsize
from pyunpack import Archive

#       1 Declare OwnCloud Directory Source, Temporary Processing Folder and Destination
path = r'/store/ownCloud/SMTV'
dst = r'/store/OwnCloud Temp'
TVFolder = r'/store/media/TV Shows'
MoviesFolder = r'/store/media/Movies'


#       1.1     Create lists and variables
dirs = os.listdir(path)
dirs.sort()
TVfolders = os.listdir(TVFolder)
fileName = []
fileSize = []
smallestFileIndex = []
counter = 0


#       2       Add owncloud files to the lists
for file in dirs:
	if file.endswith(".rar") and ".part" in file:
        	fileName.append(file)
        	fileSize.append(getsize(join(path,file)))

#       3       Iterate through list and find files < 50 MB and is a rar file. Add their index to list
for index in range(len(fileName)):

        if fileName[index].endswith('.rar') and fileSize[index] < 50000000:
                smallestFileIndex.append(index)


#       4       Get File Title of this file
for index in range(len(smallestFileIndex)):
        fileNameToMatch = fileName[smallestFileIndex[index]].split('.', 1) [0]

        #       5       Get Part Number of this file
        partNumberToMatch = fileName[smallestFileIndex[index]].split('.part', 1) [1]
        partNumberToMatch = partNumberToMatch[:-4]


        #       6       Count how many titles in OwnCloud directory match this title
        for index in range(len(fileName)):
                if fileNameToMatch in fileName[index]:
                        counter = counter + 1

        #       7       Compare number of matches to Part Number. If the same move all these files to Temporary folder
        if counter == int(partNumberToMatch):
                if not os.path.isdir(dst):
                        os.mkdir(dst)
                for index in range(len(fileName)):
                        if fileNameToMatch in fileName[index]:
                                fileToMove = join(path, fileName[index])
                                shutil.move(fileToMove, dst)
                                fileToUnRAR = join(dst, fileName[index + 1 - counter])

        #       8       Unrar files and reset counter
	print ("Processing: " + fileNameToMatch)
        Archive(fileToUnRAR).extractall(dst)
        counter = 0

        #       9       Delete RAR files in Temp Folder
        for index in range(len(fileName)):
                if fileNameToMatch in fileName[index]:
                        if fileName[index].endswith('.rar'):
                                fileToRemove = join(dst, fileName[index])
                                os.remove(fileToRemove)

        #       10      Move .mkv file to respective videos folder. If folder doesn't exist, create it.
        fileNameToMatch = os.listdir(dst)[0]
        #fileNameToMatch = fileNameToMatch + ".mkv"
        mkvToMove = join(dst, fileNameToMatch)
        if '[' and ']' in fileNameToMatch: # Determine if TV or Movie (')' meaning it's a film) 
                mkvSeriesName = fileNameToMatch.split("-", 1) [0]
                mkvSeriesName = mkvSeriesName[:-1] # remove space
                mkvDestination = join(TVFolder, mkvSeriesName)
                if mkvSeriesName not in TVfolders:
                        os.mkdir(mkvDestination)
                        TVfolders.append(mkvSeriesName)
        else:
                mkvDestination = MoviesFolder

        shutil.move(mkvToMove, mkvDestination)

#os.rmdir(dst)
print('Complete')
