#!/bin/bash
cd "$(dirname "$0")"
echo "WBRU Playlist Tracker"
echo "====================="
echo ""
echo "This will track a playlist and add it to your master file."
echo ""
read -p "Enter playlist name (e.g., 'Weekly July 2025'): " playlist_name
read -p "Enter Spotify playlist URL: " playlist_url

if [ -z "$playlist_name" ] || [ -z "$playlist_url" ]; then
    echo "Name and URL are required. Exiting."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
echo "Processing playlist... This will take 5-10 minutes."
echo "Chrome will open automatically."
echo ""

# Try python3 first, then python
if command -v python3 &> /dev/null; then
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
"
elif command -v python &> /dev/null; then
    python -c "
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
else
    echo "ERROR: Python not found. Please run install_packages.command first."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
read -p "Press any key to close..."