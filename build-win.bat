@RD /S /Q ".\dist\Windows\MouseMoverData"

python -OO -m PyInstaller src/main.py --noconfirm --name MouseMover ^
    --nowindow --noconsole ^
    --add-data="./src/assets/;./assets/" ^
    --icon=./src/assets/ico.ico 

move .\dist\MouseMover .\dist\Windows\MouseMoverData  