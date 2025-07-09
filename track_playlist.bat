@echo off
cd /d "%~dp0"
echo WBRU Playlist Tracker
echo =====================
echo.
echo This will track a playlist and add it to your master file.
echo.
set /p playlist_name=Enter playlist name (e.g., 'Weekly July 2025'): 
set /p playlist_url=Enter Spotify playlist URL: 

if "%playlist_name%"=="" (
    echo Name and URL are required. Exiting.
    pause
    exit /b 1
)

if "%playlist_url%"=="" (
    echo Name and URL are required. Exiting.
    pause
    exit /b 1
)

echo.
echo Processing playlist... This will take 5-10 minutes.
echo Chrome will open automatically.
echo.

python -c "import sys; sys.path.insert(0, 'src'); from multi_playlist_processor import MultiPlaylistProcessor; processor = MultiPlaylistProcessor(); playlist_df, playlist_id = processor.process_playlist_with_id('%playlist_url%', '%playlist_name%'); print(f'Successfully added playlist: {playlist_id}' if playlist_id else 'Failed to process playlist'); print('Check logs/ folder for individual playlist file and updated master file.') if playlist_id else None"
if %errorlevel% neq 0 (
    echo ERROR: Failed to run. Please run install_packages.bat first.
    pause
    exit /b 1
)

echo.
pause