#!/bin/bash
cd "$(dirname "$0")"
echo "Installing WBRU Playlist Tracker packages..."
echo "This may take a minute..."

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 -m pip install -r requirements.txt
elif command -v python &> /dev/null; then
    python -m pip install -r requirements.txt
else
    echo "ERROR: Python not found. Please install Python from python.org"
    read -p "Press any key to close..."
    exit 1
fi

echo "Installation complete!"
echo "You can now run the tracker by double-clicking run_tracker.command"
read -p "Press any key to close..."