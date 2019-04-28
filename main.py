import GUI
import ownCloudUnRARRefactored

if __name__ == "__main__":
    while True:
        event, folderPaths = GUI.startBuildGUI()
        if event == 'Close':
            break
        elif event == 'UnRAR':
            ownCloudUnRARRefactored.setFolders(folderPaths)