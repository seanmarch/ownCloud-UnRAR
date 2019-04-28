import PySimpleGUI as sg 
import ownCloudUnRARRefactored
import os
import shelve

def startBuildGUI():
   ownCloudDir, tvFolder, filmFolder = loadPastPathDirectories()
   event, folderPaths = buildGUI(ownCloudDir, tvFolder, filmFolder)
   return event, folderPaths


def loadPastPathDirectories():
   folderPathsHistoryFile = shelve.open('folderPathsHistoryFile')

   if not folderPathsHistoryFile['ownCloudDir'] and not folderPathsHistoryFile['tvFolder'] and not folderPathsHistoryFile['filmFolder']:
      ownCloudDir = 'Enter your ownCloud Directory here'
      tvFolder = 'Enter your TV Folder Directory here'
      filmFolder = 'Enter your Film Folder here'
   else:
      ownCloudDir = folderPathsHistoryFile['ownCloudDir']
      tvFolder = folderPathsHistoryFile['tvFolder']
      filmFolder = folderPathsHistoryFile['filmFolder']
       
   folderPathsHistoryFile.close()
   return ownCloudDir, tvFolder, filmFolder
      

def buildGUI(ownCloudDir, tvFolder, filmFolder):
   layout = [[sg.Text('UnRAR Owncloud Files')],
            [sg.Text('Owncloud Directory', size=(15, 1)), sg.InputText(ownCloudDir), sg.FolderBrowse()],
            [sg.Text('TV Folder', size=(15, 1)), sg.InputText(tvFolder), sg.FolderBrowse()],
            [sg.Text('Film Folder', size=(15, 1)), sg.InputText(filmFolder), sg.FolderBrowse()],      
            [sg.RButton('UnRAR'), sg.CButton('Close')]]      
   window = sg.Window('UnRAR Owncloud Files')
     
   event, folderPaths = window.Layout(layout).Read()

   savePathsDirectories(folderPaths)

   return event, folderPaths


def savePathsDirectories(folderPaths):
   folderPathsHistoryFile = shelve.open('folderPathsHistoryFile')
   folderPathsHistoryFile['ownCloudDir'] = folderPaths[0]
   folderPathsHistoryFile['tvFolder'] = folderPaths[1]
   folderPathsHistoryFile['filmFolder'] = folderPaths[2]
   folderPathsHistoryFile.close()

   return

if __name__ == "__main__":
    startBuildGUI() 