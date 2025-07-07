# WBRU Playlist Tracker

Simple tool to track Spotify playlist playcounts over time for WBRU radio station.

## Setup (One Time Only)

1. **Download this code:** Click the green "Code" button above → "Download ZIP" → Extract the folder
2. **Install Chrome browser** (if you don't have it already)
3. **Install Python packages:**
   - Open Terminal/Command Prompt in the extracted folder
   - Type: `pip install -r requirements.txt`
   - Press Enter and wait for it to finish

## What It Does

🎵 **Track playcounts over time** - Each run adds a new date column like "Playcounts 06.07.2025"  
🎵 **Process playlists** - Give it a Spotify playlist URL, get back all track data  
🎵 **Calculate growth** - Automatically shows playcount changes between dates

## How to Get Spotify Playlist URL

1. Open Spotify (app or web)
2. Go to your playlist
3. Click the 3 dots (...) next to the playlist name
4. Click "Share" → "Copy link to playlist"
5. You'll get something like: `https://open.spotify.com/playlist/1a9S07rNBB5EJq35uZ29bJ`

## Quick Start

### Option 1: Get Just the Track Links (Fast - 5 seconds)

1. Get your Spotify playlist URL (see above)
2. Open Terminal/Command Prompt in this folder
3. Type: `python`
4. Copy and paste this (replace YOUR_PLAYLIST_URL with your actual URL):
```python
from enhanced_playlist_processor import process_playlist_to_links_with_logging
process_playlist_to_links_with_logging("YOUR_PLAYLIST_URL", "my_playlist.xlsx")
```
5. Press Enter and wait (you'll see "Extracted X tracks" message)
6. Find your file in the `logs/` folder

### Option 2: Track Playcounts Weekly (Slow - 5-10 minutes)

1. Get your Spotify playlist URL (see above)
2. Open Terminal/Command Prompt in this folder
3. Type: `python`
4. Copy and paste this (replace YOUR_PLAYLIST_URL with your actual URL):
```python
from enhanced_playlist_processor import process_playlist_to_chart_with_tracking
process_playlist_to_chart_with_tracking("YOUR_PLAYLIST_URL")
```
5. Press Enter and wait (Chrome browser will open automatically and visit each song)
6. Check the `logs/` folder for your files when done

## Files Created

All files save to `logs/` folder:
- `logs/master_playcounts.xlsx` - Main tracking file with date columns
- `logs/PLAYLIST_NAME_2025-07-06.xlsx` - Snapshot named after playlist
- `logs/wbru_playcounts_2025-07-06.log` - Operation logs

## How Master File Works

First run creates:
```
Song         | Artist | URL    | Playcounts 06.07.2025
SOMEBODY...  | PARTY  | link1  | 76.45
```

Next week adds new column:
```
Song         | Artist | URL    | Playcounts 06.07.2025 | Playcounts 13.07.2025 | Growth 13.07.2025
SOMEBODY...  | PARTY  | link1  | 76.45                  | 78.20                  | 1.75
```

## Functions

- `process_playlist_to_chart_with_tracking(url)` - Process playlist, add to master tracking
- `process_playlist_to_links_with_logging(url, filename)` - Extract just links, no playcounts
- `update_existing_tracks(url_list)` - Update specific tracks in master file

That's it! Simple playlist tracking with dated columns.