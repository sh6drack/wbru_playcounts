@echo off
cd /d "%~dp0"
echo WBRU Playcount Updater
echo ======================
echo.
echo This will update playcounts for URLs you paste (5-10 minutes)
echo.
echo Paste your Spotify URLs below (one per line, press Ctrl+Z and Enter when done):
echo.

set "urls_file=%temp%\wbru_urls.txt"
copy con "%urls_file%" >nul

if not exist "%urls_file%" (
    echo No URLs provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Processing URLs... Chrome will open automatically.
echo.

python -c "
import sys
sys.path.insert(0, 'src')
from enhanced_playlist_processor import update_existing_tracks
urls = []
with open('%urls_file%', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            urls.append(line)
print(f'Processing {len(urls)} URLs...')
update_existing_tracks(urls)
print('Complete! Check logs/ folder for updated files.')
"
if %errorlevel% neq 0 (
    echo ERROR: Failed to run. Please run install_packages.bat first.
    pause
    exit /b 1
)

del "%urls_file%" >nul 2>&1
echo.
pause