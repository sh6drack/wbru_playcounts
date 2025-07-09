@echo off
cd /d "%~dp0"
echo WBRU URL Extractor (Fast)
echo =========================
echo.
echo This will extract song URLs from your playlist (5 seconds)
echo.
set /p playlist_url=Paste your Spotify playlist URL: 

if "%playlist_url%"=="" (
    echo No URL provided. Exiting.
    pause
    exit /b 1
)

echo.
echo Extracting URLs...

for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "filename=playlist_urls_%YYYY%-%MM%-%DD%.xlsx"

python -c "import sys; sys.path.insert(0, 'src'); from enhanced_playlist_processor import process_playlist_to_links_with_logging; process_playlist_to_links_with_logging('%playlist_url%', '%filename%'); print('URLs saved to logs/%filename%')"
if %errorlevel% neq 0 (
    echo ERROR: Failed to run. Please run install_packages.bat first.
    pause
    exit /b 1
)

echo.
echo Complete! Check the logs/ folder for your Excel file.
echo You can copy/paste the URLs from there.
pause