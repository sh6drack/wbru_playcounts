@echo off
cd /d "%~dp0"
echo WBRU Playlist Tracker
echo =====================
echo.
set /p playlist_url=Paste your Spotify playlist URL: 

if "%playlist_url%"=="" (
    echo No URL provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Processing playlist... This will take 5-10 minutes.
echo Chrome will open automatically. Please don't close it.
echo.

python -c "import sys; sys.path.insert(0, 'src'); from enhanced_playlist_processor import process_playlist_to_chart_with_tracking; process_playlist_to_chart_with_tracking('%playlist_url%')"
if %errorlevel% neq 0 (
    echo ERROR: Failed to run. Please run install_packages.bat first.
    pause
    exit /b 1
)

echo.
echo Complete! Check the logs/ folder for your files.
pause