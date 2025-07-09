#!/bin/bash
cd "$(dirname "$0")"
echo "WBRU URL Extractor (Fast)"
echo "========================="
echo ""
echo "This will extract song URLs from your playlist (5 seconds)"
echo ""
echo "Paste your Spotify playlist URL below:"
read -p "URL: " playlist_url

if [ -z "$playlist_url" ]; then
    echo "No URL provided. Exiting."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
echo "Extracting URLs..."

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 -c "
import sys
sys.path.insert(0, 'src')
from enhanced_playlist_processor import process_playlist_to_links_with_logging
import datetime
filename = f'playlist_urls_{datetime.datetime.now().strftime(\"%Y-%m-%d\")}.xlsx'
process_playlist_to_links_with_logging('$playlist_url', filename)
print(f'URLs saved to logs/{filename}')
"
elif command -v python &> /dev/null; then
    python -c "
import sys
sys.path.insert(0, 'src')
from enhanced_playlist_processor import process_playlist_to_links_with_logging
import datetime
filename = f'playlist_urls_{datetime.datetime.now().strftime(\"%Y-%m-%d\")}.xlsx'
process_playlist_to_links_with_logging('$playlist_url', filename)
print(f'URLs saved to logs/{filename}')
"
else
    echo "ERROR: Python not found. Please run install_packages.command first."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
echo "Complete! Check the logs/ folder for your Excel file."
echo "You can copy/paste the URLs from there."
read -p "Press any key to close..."