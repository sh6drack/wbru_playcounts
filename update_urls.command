#!/bin/bash
cd "$(dirname "$0")"
echo "WBRU Playcount Updater"
echo "======================"
echo ""
echo "This will update playcounts for URLs you paste (5-10 minutes)"
echo ""
echo "Paste your Spotify URLs below (one per line, press Enter twice when done):"
echo ""

urls=""
while IFS= read -r line; do
    if [ -z "$line" ]; then
        break
    fi
    urls="$urls$line\n"
done

if [ -z "$urls" ]; then
    echo "No URLs provided. Exiting."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
echo "Processing URLs... Chrome will open automatically."
echo ""

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 -c "
import sys
sys.path.insert(0, 'src')
from enhanced_playlist_processor import update_existing_tracks

urls = '''$urls'''.strip().split('\n')
urls = [url.strip() for url in urls if url.strip()]
print(f'Processing {len(urls)} URLs...')
update_existing_tracks(urls)
print('Complete! Check logs/ folder for updated files.')
"
elif command -v python &> /dev/null; then
    python -c "
import sys
sys.path.insert(0, 'src')
from enhanced_playlist_processor import update_existing_tracks

urls = '''$urls'''.strip().split('\n')
urls = [url.strip() for url in urls if url.strip()]
print(f'Processing {len(urls)} URLs...')
update_existing_tracks(urls)
print('Complete! Check logs/ folder for updated files.')
"
else
    echo "ERROR: Python not found. Please run install_packages.command first."
    read -p "Press any key to close..."
    exit 1
fi

echo ""
read -p "Press any key to close..."