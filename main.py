import GUI
import ownCloudUnRAR

if __name__ == "__main__":
    while True:
        event, folderPaths = GUI.startBuildGUI()
        if event == 'Close' or event is None:
            break
        elif event == 'UnRAR':
            ownCloudUnRAR.setFolders(folderPaths)
            GUI.savePathsDirectories(folderPaths)