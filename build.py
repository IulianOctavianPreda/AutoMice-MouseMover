import PyInstaller.__main__
import os
import shutil
import platform


class Build:

    name = "MouseMover"
    distPath = "./dist"
    shortcutPath = "./systemShortcuts"
    executableName = "MouseMover"
    system = platform.system()
    extension = ""
    architecture = platform.architecture()[0]
    command = [
        f'--name={name}',
        '--noconfirm',
        '--onedir',
    ]

    def __init__(self):
        if(self.architecture == "32bit"):
            self.architectureName = "x86"
        else:
            self.architectureName = "x64"

        self.packageName = f'{self.distPath}/{self.executableName}_'
        if self.system == "Darwin":
            self.packageName = self.packageName + \
                f'MacOS_{self.architectureName}'
        else:
            self.packageName = self.packageName + \
                f'{self.system}_{self.architectureName}'

    def copyTree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def removeTree(self, src):
        if os.path.exists(src):
            if(os.path.isfile(src)):
                os.remove(src)
            elif(os.path.isdir(src)):
                shutil.rmtree(src)

    def moveTree(self, src, dest):
        shutil.move(src, dest)

    def copyFile(self, src, dest):
        shutil.copy(src, dest)

    def build(self):
        if self.system == "Linux":
            self.command.append('--add-data=./src/assets/ico.ico:./assets/')
        elif self.system == "Windows":
            self.command.append('--windowed')
            self.command.append('--icon=./src/assets/ico.ico')
            self.command.append('--add-data=./src/assets/ico.ico;./assets/')
            self.command.append(
                f'--add-binary=C:/Program Files (x86)/Windows Kits/10/Redist/ucrt/DLLs/{self.architectureName};./')
            self.extension = ".exe"
        elif self.system == "Darwin":
            self.command.append('--windowed')
            self.command.append('--icon=./src/assets/ico.icns')
            self.command.append('--add-data=./src/assets/ico.ico:./assets/')

        self.command.append('src/main.py')

        self.removeTree(self.packageName)
        PyInstaller.__main__.run(self.command)
        self.moveTree(f'{self.distPath}/{self.name}',
                      f'{self.packageName}/{self.name+"Data"}')
        if self.system == "Darwin":
            self.copyFile(f'{self.shortcutPath}/Linux/{self.executableName}_{self.architectureName}{self.extension}',
                          f'{self.packageName}/{self.executableName}{self.extension}')
        else:
            self.copyFile(f'{self.shortcutPath}/{self.system}/{self.executableName}_{self.architectureName}{self.extension}',
                          f'{self.packageName}/{self.executableName}{self.extension}')


if __name__ == "__main__":
    appBuilder = Build()
    appBuilder.build()
