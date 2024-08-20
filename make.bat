@echo off
setlocal
set bat_dir=%~dp0
set target_dir=%bat_dir%\subdir
call venv\Scripts\activate

pyinstaller --noconfirm --onefile --windowed --icon "./static/favicon.ico" --name "RECAP" --splash "./static/PSDLogo.png" --add-data "./static;static/" --add-data "./templates;templates/"  "./app.py"