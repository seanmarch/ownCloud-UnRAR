import os
import sys
import shutil
import subprocess
import PySimpleGUI as sg
from os.path import join,getsize
from pyunpack import Archive

pathOfRARFiles = os.path.expanduser('~\ownCloud\SMTV')
unRARTempFolder = os.path.expanduser('~\Videos\ownCloud Temp')
tvFolder = os.path.expanduser('~\Videos\TV Shows')
moviesFolder = os.path.expanduser('~\Videos\Movies')
#TVFolder = r'H:\to go on server\TV Shows'
#MoviesFolder = r'H:\to go on server\Movies'

def setFolders(folderPaths):
    global pathOfRARFiles
    global tvFolder
    global moviesFolder
    #global TVFolder
    #global MoviesFolder

    pathOfRARFiles = folderPaths[0]
    tvFolder = folderPaths[1]
    moviesFolder = folderPaths[2]

    startUnRAR()


def startUnRAR():
    createFileNameAndSizeList(pathOfRARFiles)

def createFileNameAndSizeList(pathOfRARFiles):
    fileNameList = []
    fileSizeList = []

    rarFilesList = os.listdir(pathOfRARFiles)
    rarFilesList.sort()
    
    for rarFile in rarFilesList:
        if rarFile.endswith(".rar") and ".part" in rarFile:
            fileNameList.append(rarFile)
            fileSizeList.append(getsize(join(pathOfRARFiles, rarFile)))

    createSmallestRARFileIndexList(fileNameList, fileSizeList)


def createSmallestRARFileIndexList(fileNameList, fileSizeList):
    smallestRARFileIndexList = []

    for index in range(len(fileNameList)):
        if fileNameList[index].endswith('.rar') and fileSizeList[index] < 50000000:
            smallestRARFileIndexList.append(index)

    getIndexOfAllFilesToUnRAR(smallestRARFileIndexList, fileNameList)


def getIndexOfAllFilesToUnRAR(smallestRARFileIndexList, fileNameList):
    indexOfFilesToUnRAR =[]
    for smallestRARFileIndex in smallestRARFileIndexList:
        fileTitleOfSmallestRARFile = getFileTitleOfSmallestRARFile(smallestRARFileIndex, fileNameList)
        partNumberOfSmallestRARFile = getPartNumberOfSmallestRARFile(smallestRARFileIndex, fileNameList)
        numberOfMatchingFileTitles = countNumberOfMatchingFileTitles(fileTitleOfSmallestRARFile, fileNameList)
        if partNumberOfSmallestRARFile == numberOfMatchingFileTitles:
            indexOfFilesToUnRAR.append(smallestRARFileIndex)
    unRARAllReadyRARs(indexOfFilesToUnRAR, smallestRARFileIndex, fileNameList)           
            

def unRARAllReadyRARs(indexOfFilesToUnRAR ,smallestRARFileIndexList, fileNameList):
    createUnRARTempFolderIfDoesntExist(unRARTempFolder)
    sg.Print('Wait ...')
    for fileToUnRAR in range(len(indexOfFilesToUnRAR)):
        sg.Print ("Processing " + str(fileToUnRAR + 1) + " of " + str(len(indexOfFilesToUnRAR)) + ": " + str(fileNameList[indexOfFilesToUnRAR[fileToUnRAR]].rsplit('.', 3) [0]))
        moveAllMatchingFilesToTempFolder(fileNameList[indexOfFilesToUnRAR[fileToUnRAR]].rsplit('.', 3) [0], fileNameList, pathOfRARFiles,unRARTempFolder)
        unRARFiles(unRARTempFolder, fileNameList, indexOfFilesToUnRAR[fileToUnRAR], smallestRARFileIndexList, fileNameList[indexOfFilesToUnRAR[fileToUnRAR]])
        fileTitleOfSmallestRARFile = fileNameList[indexOfFilesToUnRAR[fileToUnRAR]].rsplit('.', 3) [0]
        deleteRARFilesWhenUnRARComplete(fileTitleOfSmallestRARFile, fileNameList, unRARTempFolder)
        checkIfVideoIsFilmOrTV(tvFolder, moviesFolder, unRARTempFolder)
    deleteOwncloudTempFolder()

def getFileTitleOfSmallestRARFile(smallestRARFileIndexList, fileNameList):
    fileTitleOfSmallestRARFile = fileNameList[smallestRARFileIndexList].rsplit('.', 3) [0]
    return fileTitleOfSmallestRARFile


def getPartNumberOfSmallestRARFile(smallestRARFileIndex, fileNameList):
    partNumberOfSmallestRARFile = fileNameList[smallestRARFileIndex].split('.part', 1) [1]
    partNumberOfSmallestRARFile = partNumberOfSmallestRARFile[:-4]
    return int(partNumberOfSmallestRARFile)


def countNumberOfMatchingFileTitles(fileTitleOfSmallestRARFile, fileNameList):
    numberOfMatchingFileTitle = 0
    for index in range(len(fileNameList)):
        if fileTitleOfSmallestRARFile in fileNameList[index]:
            numberOfMatchingFileTitle = numberOfMatchingFileTitle + 1
    return numberOfMatchingFileTitle


def createUnRARTempFolderIfDoesntExist(unRARTempFolder):
    if not os.path.isdir(unRARTempFolder):
        os.mkdir(unRARTempFolder)


def moveAllMatchingFilesToTempFolder(fileTitleOfSmallestRARFile, fileNameList, pathOfRARFiles,unRARTempFolder):
    for index in range(len(fileNameList)):
        if fileTitleOfSmallestRARFile in fileNameList[index]:
            fileToMove = join(pathOfRARFiles, fileNameList[index])
            shutil.move(fileToMove, unRARTempFolder)


def unRARFiles(unRARTempFolder, fileNameList, smallestRARFileIndex, smallestRARFileIndexList, fileTitleOfSmallestRARFile):
    fileToUnRAR = join(unRARTempFolder, fileNameList[smallestRARFileIndex])
    Archive(fileToUnRAR).extractall(unRARTempFolder)


def deleteRARFilesWhenUnRARComplete(fileTitleOfSmallestRARFile, fileNameList, unRARTempFolder):
    for index in range(len(fileNameList)):
        if fileTitleOfSmallestRARFile in fileNameList[index]:
            if fileNameList[index].endswith('.rar'):
                fileToRemove = join(unRARTempFolder, fileNameList[index])
                os.remove(fileToRemove)


def checkIfVideoIsFilmOrTV(tvFolder, moviesFolder, unRARTempFolder):
    TVfolders = os.listdir(tvFolder)
    fileNameToMatch = os.listdir(unRARTempFolder)[0]
    mkvToMove = join(unRARTempFolder, fileNameToMatch)
    if '[' and ']' in fileNameToMatch: # Determine if TV or Movie ('[' and ']' meaning it's TV)
        mkvSeriesName = fileNameToMatch.split("-", 1) [0].strip()
        mkvDestination = join(tvFolder, mkvSeriesName)
        if mkvSeriesName not in TVfolders:
            os.mkdir(mkvDestination)
            TVfolders.append(mkvSeriesName)
    else:
        mkvDestination = moviesFolder
    moveVideoToTVOrFilmFolder(mkvToMove, mkvDestination)


def moveVideoToTVOrFilmFolder(mkvToMove, mkvDestination):
    shutil.move(mkvToMove, mkvDestination)
    

def deleteOwncloudTempFolder():
    os.rmdir(unRARTempFolder)
    print('Complete')


if __name__ == "__main__":
    startUnRAR()