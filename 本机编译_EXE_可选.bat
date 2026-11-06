@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3 -m pip install --upgrade pyinstaller
py -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name DailyEnglish --add-data "quotes.json;." english_widget.py
echo.
echo Build finished. Check dist\DailyEnglish.exe
pause
