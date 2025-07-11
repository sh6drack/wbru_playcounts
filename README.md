# WBRU Playlist Tracker

Track Spotify playlist playcounts over time.

## Setup (One Time Only)

1. **Download this code:** Click green "Code" button → "Download ZIP" → Extract folder
2. **Install packages:** Double-click `install_packages.command` (Mac) or `install_packages.bat` (Windows)
3. **Ready to use:** `data.xlsx` is included - just paste your URLs in column A when needed

## **Key Points**

> **USE THE SAME NAME EACH WEEK** - For weekly playlists, enter the exact same name (e.g., "Weekly July 2025") every time. This creates a compounding chart that tracks the same playlist over time.

> **MASTER FILE COMBINES EVERYTHING** - All playlists merge into `logs/master_playcounts.xlsx` for one big chart with all your tracks.

> **EXPECT 5-10 MINUTES** - Tracking playlists takes time because it scrapes playcount data from each song.

## How to Use

**For tracking playlists (Weekly, Gold Library, etc.):**
- **Mac:** Double-click `track_playlist.command` 
- **Windows:** Double-click `track_playlist.bat`
- Enter playlist name like "Weekly July 2025"
- Paste Spotify playlist URL
- Wait for code to finish(extracting from a playlist link takes longer than from urls)

**For quick URL extraction:**
- **Mac:** Double-click `get_urls.command`
- **Windows:** Double-click `get_urls.bat`
- Paste Spotify playlist URL
- Get Excel file with URLs (5 seconds)

**For updating playcounts from Excel file:**
- Open `data.xlsx` and paste your Spotify URLs in column A
- **Mac:** Double-click `update_from_excel.command`
- **Windows:** Double-click `update_from_excel.bat`
- Wait for code to finish

## Common Workflows

**Weekly playlist tracking:**
1. Use `track_playlist` with your weekly playlist URL
2. **IMPORTANT: Use the exact same name each week** (e.g., "Weekly July 2025")
3. Gets playcounts and adds new date column each week to the same file
4. Creates compounding chart showing playlist growth over time

**Gold library updates:**
1. Use `get_urls` to extract URLs from your gold library playlist
2. Copy URLs from the output file to `data.xlsx` (column A)
3. Use `update_from_excel` to get playcounts for all songs

**Quick song lookup:**
1. Open `data.xlsx` and paste URLs in column A
2. Use `update_from_excel` to get playcounts

*Note: If you're in VS Code, you can also run these from the terminal, but double-clicking the files is easier.*

## Where to Find Your Files

**All files are saved in the `logs/` folder** (it creates automatically)

**Master file (everything combined):**
- `logs/master_playcounts.xlsx` - **ALL your playlists merged into one big chart**

**Individual playlist files:**
- `logs/weekly_july_2025_tracking.xlsx` - Just this playlist's history
- `logs/gold_library_tracking.xlsx` - Just this playlist's history

**Quick URL files:**
- `logs/playlist_name_urls_2025-07-09.xlsx` - Just the Spotify URLs

Each time you run the tracker, it adds a new date column to your files. Open the `logs/` folder to see all your Excel files!

That's it!
