pyinstaller src/main.py --noconfirm --name MouseMover^
    --onefile --nowindow --noconsole^
    --add-data="./src/assets/ico.ico;./assets/ico.ico" ^
    --icon=./src/assets/ico.ico