@echo off
setlocal

python -m pip install pyinstaller
pyinstaller --onefile --windowed --name SimpleMacro app.py

echo.
echo Build complete. Find the exe in dist\SimpleMacro.exe
pause
