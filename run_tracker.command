#!/bin/bash
cd "$(dirname "$0")"
echo "WBRU Playlist Tracker"
echo "====================="
echo ""
echo "Paste your Spotify playlist URL below:"
read -p "URL: " playlist_url

if [ -z "$playlist_url" ]; then
    echo "No URL provided. Exiting."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
echo "Processing playlist... This will take 5-10 minutes."
echo "Chrome will open automatically. Please don't close it."
echo ""

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 -c "
import sys
sys.path.insert(0, 'src')
from enhanced_playlist_processor import process_playlist_to_chart_with_tracking
process_playlist_to_chart_with_tracking('$playlist_url')
"
elif command -v python &> /dev/null; then
    python -c "
import sys
sys.path.insert(0, 'src')
from enhanced_playlist_processor import process_playlist_to_chart_with_tracking
process_playlist_to_chart_with_tracking('$playlist_url')
"
else
    echo "ERROR: Python not found. Please run install_packages.command first."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
echo "Complete! Check the logs/ folder for your files."
read -p "Press any key to close..."