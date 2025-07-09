#!/bin/bash
cd "$(dirname "$0")"
echo "WBRU Playlist Manager"
echo "===================="
echo ""
echo "Choose an option:"
echo "1. List all tracked playlists"
echo "2. Add/Track new playlist"
echo "3. Update existing playlist"
echo "4. Reset playlist data"
echo "5. Remove playlist"
echo "6. Quick URL extract (no tracking)"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Listing all playlists..."
        python3 -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
processor.list_playlists()
" 2>/dev/null || python -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
processor.list_playlists()
"
        ;;
    2)
        echo ""
        read -p "Enter playlist name: " playlist_name
        read -p "Enter Spotify playlist URL: " playlist_url
        echo ""
        echo "Processing playlist... This will take 5-10 minutes."
        echo "Chrome will open automatically."
        echo ""
        python3 -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
playlist_df, playlist_id = processor.process_playlist_with_id('$playlist_url', '$playlist_name')
if playlist_id:
    print(f'Successfully added playlist: {playlist_id}')
    print('Check logs/ folder for individual playlist file and updated master file.')
else:
    print('Failed to process playlist')
" 2>/dev/null || python -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
playlist_df, playlist_id = processor.process_playlist_with_id('$playlist_url', '$playlist_name')
if playlist_id:
    print(f'Successfully added playlist: {playlist_id}')
    print('Check logs/ folder for individual playlist file and updated master file.')
else:
    print('Failed to process playlist')
"
        ;;
    3)
        echo ""
        read -p "Enter playlist ID to update: " playlist_id
        echo ""
        echo "Updating playlist... This will take 5-10 minutes."
        echo "Chrome will open automatically."
        echo ""
        python3 -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
playlist_df, updated_id = processor.update_playlist_by_id('$playlist_id')
if updated_id:
    print(f'Successfully updated playlist: {updated_id}')
    print('Check logs/ folder for updated files.')
else:
    print('Failed to update playlist')
" 2>/dev/null || python -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
playlist_df, updated_id = processor.update_playlist_by_id('$playlist_id')
if updated_id:
    print(f'Successfully updated playlist: {updated_id}')
    print('Check logs/ folder for updated files.')
else:
    print('Failed to update playlist')
"
        ;;
    4)
        echo ""
        read -p "Enter playlist ID to reset: " playlist_id
        python3 -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
if processor.reset_playlist('$playlist_id'):
    print('Playlist data reset successfully')
else:
    print('Failed to reset playlist')
" 2>/dev/null || python -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
if processor.reset_playlist('$playlist_id'):
    print('Playlist data reset successfully')
else:
    print('Failed to reset playlist')
"
        ;;
    5)
        echo ""
        read -p "Enter playlist ID to remove: " playlist_id
        python3 -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
if processor.remove_playlist('$playlist_id'):
    print('Playlist removed successfully')
else:
    print('Failed to remove playlist')
" 2>/dev/null || python -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import MultiPlaylistProcessor
processor = MultiPlaylistProcessor()
if processor.remove_playlist('$playlist_id'):
    print('Playlist removed successfully')
else:
    print('Failed to remove playlist')
"
        ;;
    6)
        echo ""
        read -p "Enter Spotify playlist URL: " playlist_url
        echo ""
        echo "Extracting URLs..."
        python3 -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import quick_url_extract
filename = quick_url_extract('$playlist_url')
if filename:
    print(f'URLs extracted to: {filename}')
else:
    print('Failed to extract URLs')
" 2>/dev/null || python -c "
import sys
sys.path.insert(0, 'src')
from multi_playlist_processor import quick_url_extract
filename = quick_url_extract('$playlist_url')
if filename:
    print(f'URLs extracted to: {filename}')
else:
    print('Failed to extract URLs')
"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

echo ""
read -p "Press any key to close..."