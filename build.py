import PyInstaller.__main__
import os
import shutil
import platform

packageName = "MouseMover"
distPath = "./dist"
shortcutPath = "./systemShortcuts"
system = platform.system()

command = [
    '--name=%s' % packageName,
    '--noconfirm',
    '--onedir',
    '--add-data=src/assets/ico.ico;./assets/',
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


if __name__ == "__main__":
    if system == "Linux":
        pass
    elif system == "Windows":
        command.append('--windowed')
        command.append('--icon=./src/assets/ico.ico')
    elif system == "Darwin":
        command.append('--windowed')
        command.append('--icon=./src/assets/ico.icns')

    command.append('src/main.py')

    removeTree(f'{distPath}/{system}')
    PyInstaller.__main__.run(command)
    moveTree(f'{distPath}/{packageName}',
             f'{distPath}/{system}/{packageName+"Data"}')
    copyTree(f'{shortcutPath}/{system}', f'{distPath}/{system}/')
