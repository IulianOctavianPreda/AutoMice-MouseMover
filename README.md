# Mouse Mover

![Build](https://github.com/IulianOctavianPreda/AutoMice-MouseMover/workflows/Build/badge.svg)

AutoMice(Automize?) is a free, no installation required, no admin right s required, user-friendly mouse auto-mover to keep your desktop active.
The latest version can always be downloaded from [here](https://github.com/IulianOctavianPreda/AutoMice-MouseMover/releases)

## Features:

-   Mouse auto-movement after a period of inactivity
-   Multiple movement patterns
-   Changeable start/stop key combination
-   Adjustable parameter as time, distance
-   Friendly GUI

## Usage - No installation needed

-   Download the archive
-   Extract the executable
-   Move it to your desired place
-   Run the executable

## Remarks

For windows:  
If you don't know what type of architecture your system uses (32-bit/x86 or 64-bit/x64), download the x86 version as it is compatible with both of them.

For both Linux and Windows:  
If for any reason the executable placed in the root folder doesn't work as expected, you can use a different executable that can be found in "MouseMoverData" folder. The executable in the root folder serves as a shortcut to the real one.

## Preview

![image](https://user-images.githubusercontent.com/33485041/80921902-0d805300-8d82-11ea-8b35-ce1b6da80df0.png)

## Developer Instructions

### Requirements:

-   At least python 3.7+

### Run in the root folder in a terminal:

-   `pip3 install -r requirements.txt`

## Build

### Requirements

-   Python 3.7+(32 bit, optionally 64 bit) - installed and added to path
-   requiements.txt - installed

### Instructions

-   run `python build.py` or `python3 build.py`

### Special mentions

-   If the "shortcuts" / executables are not created, compile them with `gcc MouseMover.cpp -o MouseMover -mwindows` for Windows and `gcc MouseMover.cpp -o MouseMover` for Linux. Optionally add the architecture in the name too.

Examples to compile for different architectures:

-   Windows:<br/> `gcc MouseMover.cpp -o Windows/MouseMover_x86 -mwindows -m32` <br/> `gcc MouseMover.cpp -o Windows/MouseMover_x64 -mwindows -m64`

-   Linux: <br/> `gcc MouseMover.cpp -o Linux/MouseMover_x86 -m32` <br/> `gcc MouseMover.cpp -o Linux/MouseMover_x64 -m64`

For linux you might need to run the command: `sudo apt-get install g++-multilib`
To add icons for the Windows executables you can use ResourceHacker.

#### Windows

-   Windows 10 SDK should be installed

#### Linux

-   Build on both x86 and x64 architectures using different OS installations

#### MacOs

-   Build for both architectures using different versions of Python(one for 32 bits and one for 64 bits)
