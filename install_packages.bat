@echo off
cd /d "%~dp0"
echo Installing WBRU Playlist Tracker packages...
echo This may take a minute...

python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Python not found or pip install failed
    echo Please install Python from python.org
    pause
    exit /b 1
)

echo Installation complete!
echo You can now run the tracker by double-clicking run_tracker.bat
pause