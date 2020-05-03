# Mouse Mover

## Usage - No installation needed

-   Download the archive
-   Extract the executable
-   Move it in your desired place
-   Run the executable

## Preview

![image](https://user-images.githubusercontent.com/33485041/80921902-0d805300-8d82-11ea-8b35-ce1b6da80df0.png)

## Developer Instructions

### Requirements:

-   At least python 3.7+

### Run in the root folder in a terminal:

-   `pip3 install -r requirements.txt`

## Build

### Windows

#### Requirements

-   Visual studio <version> - installed
-   Build Tools for Visual Studio <version> - installed
-   Python 3.7+ - installed and added to path
-   Nuitka - installed in the python folder
-   requiements.txt - installed
-   Update the build command with the following template replacing <version> and <build version> to the installed ones and <repository path> to the current absolute path

Template:

```
set INCLUDE=C:\Program Files (x86)\Windows Kits\10\Include\<build version>\ucrt
set LIB=C:\Program Files (x86)\Windows Kits\10\Lib\<build version>\um\x64;C:\Program Files (x86)\Windows Kits\10\Lib\<build version>\ucrt\x64
"C:\Program Files (x86)\Microsoft Visual Studio\<version>\Community\VC\Auxiliary\Build\vcvars64.bat" && nuitka ./src/main.py  -o ./dist/MouseMover_Windows_x86_x64.exe  --remove-output  --windows-icon=<repository path>/MouseMover/src/assets/ico.ico --windows-disable-console  --warn-unusual-code --assume-yes-for-downloads --follow-imports

```

#### Instructions

-   Run the batch file build-win.cmd
