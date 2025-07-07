# WBRU Playlist Tracker

Simple tool to track Spotify playlist playcounts over time for WBRU radio station.

## Setup

1. Clone repo
2. Install Chrome browser  
3. Run: `pip install -r requirements.txt`

## What It Does

🎵 **Track playcounts over time** - Each run adds a new date column like "Playcounts 06.07.2025"  
🎵 **Process playlists** - Give it a Spotify playlist URL, get back all track data  
🎵 **Calculate growth** - Automatically shows playcount changes between dates

## Quick Start

### Get Playlist Links Only (Fast - 5 seconds)
```python
from enhanced_playlist_processor import process_playlist_to_links_with_logging
df = process_playlist_to_links_with_logging("PLAYLIST_URL", "my_playlist.xlsx")
```

### Track Playcounts Over Time (Slow - 5-10 minutes)
```python
from enhanced_playlist_processor import process_playlist_to_chart_with_tracking
master_df = process_playlist_to_chart_with_tracking("PLAYLIST_URL")
```

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