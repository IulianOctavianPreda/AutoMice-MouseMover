import PyInstaller.__main__
import os
import shutil
import platform

packageName = "MouseMover"
distPath = "./dist"
shortcutPath = "./systemShortcuts"
executableName = "MouseMover"
system = platform.system()
extension = ""
architecture = platform.architecture()[0]

if(architecture == "32bit"):
    architectureName = "x86"
else:
    architectureName = "x64"

command = [
    f'--name={packageName}',
    '--noconfirm',
    '--onedir',
]


def copyTree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def removeTree(src):
    if os.path.exists(src):
        if(os.path.isfile(src)):
            os.remove(src)
        elif(os.path.isdir(src)):
            shutil.rmtree(src)


def moveTree(src, dest):
    shutil.move(src, dest)


def copyFile(src, dest):
    shutil.copy(src, dest)


if __name__ == "__main__":
    # if(not os.path.exists(f'{shortcutPath}/{system}/MouseMover') or not os.path.exists(f'{shortcutPath}/{system}/MouseMover.exe')):
    #     os.system(
    #         f"gcc {shortcutPath}/MouseMover.cpp -o {shortcutPath}/{system}/MouseMover")

    if system == "Linux":
        command.append('--add-data=./src/assets/ico.ico:./assets/')
    elif system == "Windows":
        command.append('--windowed')
        command.append('--icon=./src/assets/ico.ico')
        command.append('--add-data=./src/assets/ico.ico;./assets/')
        command.append(
            f'--add-binary=C:/Program Files (x86)/Windows Kits/10/Redist/ucrt/DLLs/{architectureName};./')
        extension = ".exe"
    elif system == "Darwin":
        command.append('--windowed')
        command.append('--icon=./src/assets/ico.icns')
        command.append('--add-data=./src/assets/ico.ico:./assets/')

    command.append('src/main.py')

    removeTree(f'{distPath}/{system}_{architectureName}')
    PyInstaller.__main__.run(command)
    moveTree(f'{distPath}/{packageName}',
             f'{distPath}/{system}_{architectureName}/{packageName+"Data"}')
    copyFile(f'{shortcutPath}/{system}/{executableName}_{architectureName}{extension}',
             f'{distPath}/{system}_{architectureName}/{executableName}{extension}')
