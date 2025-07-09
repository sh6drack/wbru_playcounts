@echo off
cd /d "%~dp0"
echo WBRU Playlist Manager
echo ====================
echo.
echo Choose an option:
echo 1. List all tracked playlists
echo 2. Add/Track new playlist
echo 3. Update existing playlist
echo 4. Reset playlist data
echo 5. Remove playlist
echo 6. Quick URL extract (no tracking)
echo.
set /p choice=Enter choice (1-6): 

if "%choice%"=="1" (
    echo.
    echo Listing all playlists...
    python -c "import sys; sys.path.insert(0, 'src'); from multi_playlist_processor import MultiPlaylistProcessor; processor = MultiPlaylistProcessor(); processor.list_playlists()"
) else if "%choice%"=="2" (
    echo.
    set /p playlist_name=Enter playlist name: 
    set /p playlist_url=Enter Spotify playlist URL: 
    echo.
    echo Processing playlist... This will take 5-10 minutes.
    echo Chrome will open automatically.
    echo.
    python -c "import sys; sys.path.insert(0, 'src'); from multi_playlist_processor import MultiPlaylistProcessor; processor = MultiPlaylistProcessor(); playlist_df, playlist_id = processor.process_playlist_with_id('%playlist_url%', '%playlist_name%'); print(f'Successfully added playlist: {playlist_id}' if playlist_id else 'Failed to process playlist'); print('Check logs/ folder for files.') if playlist_id else None"
) else if "%choice%"=="3" (
    echo.
    set /p playlist_id=Enter playlist ID to update: 
    echo.
    echo Updating playlist... This will take 5-10 minutes.
    echo Chrome will open automatically.
    echo.
    python -c "import sys; sys.path.insert(0, 'src'); from multi_playlist_processor import MultiPlaylistProcessor; processor = MultiPlaylistProcessor(); playlist_df, updated_id = processor.update_playlist_by_id('%playlist_id%'); print(f'Successfully updated playlist: {updated_id}' if updated_id else 'Failed to update playlist'); print('Check logs/ folder for updated files.') if updated_id else None"
) else if "%choice%"=="4" (
    echo.
    set /p playlist_id=Enter playlist ID to reset: 
    python -c "import sys; sys.path.insert(0, 'src'); from multi_playlist_processor import MultiPlaylistProcessor; processor = MultiPlaylistProcessor(); print('Playlist data reset successfully' if processor.reset_playlist('%playlist_id%') else 'Failed to reset playlist')"
) else if "%choice%"=="5" (
    echo.
    set /p playlist_id=Enter playlist ID to remove: 
    python -c "import sys; sys.path.insert(0, 'src'); from multi_playlist_processor import MultiPlaylistProcessor; processor = MultiPlaylistProcessor(); print('Playlist removed successfully' if processor.remove_playlist('%playlist_id%') else 'Failed to remove playlist')"
) else if "%choice%"=="6" (
    echo.
    set /p playlist_url=Enter Spotify playlist URL: 
    echo.
    echo Extracting URLs...
    python -c "import sys; sys.path.insert(0, 'src'); from multi_playlist_processor import quick_url_extract; filename = quick_url_extract('%playlist_url%'); print(f'URLs extracted to: {filename}' if filename else 'Failed to extract URLs')"
) else (
    echo Invalid choice
)

echo.
pause