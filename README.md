P## WBRU 360 UPDATES:
Now instead of overwriting columns, creates new columns showcasing playcounts. Also includes columns for song name and artist.

## What This Tool Does:

🎵 **Individual Track Processing:** Give it Spotify track URLs → Get back song names, artists, and playcount data  
🎵 **Playlist Link Extraction:** Give it a Spotify playlist URL → Get back all track info (FAST, ~5 seconds)  
🎵 **Full Playlist Processing:** Give it a Spotify playlist URL → Get back complete data with playcounts (SLOW, 5-10 minutes)

## Code Organization:

**Main Files:**
- `count_looper_chart.py` - processes Excel files with track URLs and adds playcounts
- `count_looper.py` - original monolithic implementation with all functions
- `playlist_processor.py` - **NEW** simplified interface for playlist processing

**Utility Modules:**
- `spotify_utils.py` - Spotify API functions (authentication, track/playlist extraction)
- `playcount_scraper.py` - web scraping functions to get playcount data from Spotify
- `logging_utils.py` - **NEW** logging system that creates logs in `logs/` folder
- `playcount_tracker.py` - **NEW** tracks playcounts over time with date-based columns
- `enhanced_playlist_processor.py` - **NEW** full-featured processor with logging and tracking

## Available Functions:

**For Processing Individual Tracks:**
- `get_playcounts(urls)` - takes list of Spotify track URLs, returns chart with song names, artists, URLs, and playcounts in millions

**For Processing Playlists:**
- `process_playlist_to_chart(playlist_url)` - **SLOW** - takes playlist URL, extracts all tracks, scrapes playcounts, returns complete chart with song/artist/URL/playcounts
- `process_playlist_to_links(playlist_url)` - **FAST** - takes playlist URL, extracts track info using Spotify API only, returns chart with song/artist/URL (no playcounts)

**NEW - For Tracking Playcounts Over Time:**
- `process_playlist_to_chart_with_tracking(playlist_url)` - processes playlist and saves to master tracking file with date-based columns
- `update_existing_tracks(urls_list)` - updates playcounts for specific tracks in the master file
- `PlaycountTracker.add_or_update_playcounts()` - adds new data to master file with columns like "Playcounts 06.07.2025"
- `PlaycountTracker.calculate_growth()` - automatically calculates growth between measurement dates


# wbru_playcounts

A tool used to automatically get the playcount numbers for a set of songs from Spotify. Used by the Indie team at [WBRU](https://www.wbru.com/) to decide which tracks will get added to the internet radio stream. WBRU is the Brown University affiliated radio station.

## Setup:

1. Clone the repo (`git clone <url>`)

2. Make sure you have python installed and Chrome browser

3. In your python environment install all of the packages in `requirements.txt`

## Usage:

### Option 1: Process individual track URLs (existing method)
1. Copy the column of song URLs (to the track on Spotify) from the current/recurrents sheet to the leftmost column (column A) in `data.xlsx`

2. Save and close `data.xlsx`

3. Run `python count_looper.py` (this may take a few minutes — if you get errors try running somewhere with faster internet connection)

4. `data.xlsx` now has the corresponding playcounts for the songs. Copy this data back into the current/recurrents sheet for today's date

### Option 2: Process entire Spotify playlist

**Method A: Quick Link Extraction (RECOMMENDED - takes ~5 seconds)**
1. Get the Spotify playlist URL you want to process
2. Run:
   ```python
   from playlist_processor import process_playlist_to_links
   df = process_playlist_to_links("YOUR_PLAYLIST_URL")
   df.to_excel("playlist_links.xlsx", index=False)
   ```
   - **Output:** Excel file with columns: Song, Artist, URL
   - **Use case:** When you need track links to paste into existing sheets
   - **Speed:** Very fast (API only, no web scraping)

**Method B: Full Processing with Playcounts (SLOW - takes 5-10 minutes)**
1. Get the Spotify playlist URL you want to process
2. Run:
   ```python
   from playlist_processor import process_playlist_to_chart
   df = process_playlist_to_chart("YOUR_PLAYLIST_URL")
   df.to_excel("playlist_with_playcounts.xlsx", index=False)
   ```
   - **Output:** Excel file with columns: Song, Artist, URL, Playcounts (millions)
   - **Use case:** When you need complete data including playcount numbers
   - **Speed:** Slow (requires web scraping each track)

**Method C: Using the standalone script**
1. Modify the `playlist_url` variable in `playlist_processor.py`
2. Run `python playlist_processor.py`
3. Uncomment the section you want (links only vs full processing)

### Option 3: Track Playcounts Over Time (NEW)

**For Weekly/Regular Updates:**
```python
from enhanced_playlist_processor import process_playlist_to_chart_with_tracking

# First run creates master_playcounts.xlsx with column "Playcounts 06.07.2025"
master_df = process_playlist_to_chart_with_tracking("YOUR_PLAYLIST_URL")

# Next week, running again adds "Playcounts 13.07.2025" column
# and calculates growth automatically
```

**For Updating Specific Tracks:**
```python
from enhanced_playlist_processor import update_existing_tracks

urls_to_update = [
    "https://open.spotify.com/track/76RAlQcfuQknnQFruYDj6Q",
    "https://open.spotify.com/track/3aSWXU6owkZeVhh94XxEWO"
]
update_existing_tracks(urls_to_update)
```

**Output Files:**
- `master_playcounts.xlsx` - main tracking file with date-based columns
- `playcounts_snapshot_YYYY-MM-DD.xlsx` - daily snapshots
- `logs/wbru_playcounts_YYYY-MM-DD.log` - detailed operation logs


<br>

---

<details>
<summary>Dev Notes:</summary>
<ul>
    <li>take artist/song or spotify link and every Tuesday update the stream count (automate python script on google sheets)</li>
    <li>stream count tracks the data of how popular songs are, Peter prefers stream numbers</li>
    - Indie has a guideline based on stream numbers to determine light/medium/heavy classification for songs; the different classifications determine how frequent to play a song
    - enhancement: use guideline to auto give classification to song
    - enhancement: they also like to see trends, so it would be useful to create a dashboard of song stream counts week by week (like trendy!)
        + this could be matplotlib
    <li>spreadsheet: https://docs.google.com/spreadsheets/d/16rxDbk8cNcZYGxYOze-zVlQgQwHU2ThSk-3rEeRrDuo/edit?usp=sharing</li>
    - songs being played are in col G-H, classification in col A, stream counts in col M (*unit: millions*)
        + isn't point of WBRU indie to play more underground stuff? Current apporach is to appeal popularly right now, team is trying to push back on threshold
    - like to have data for every song, which are the row entries
    - they like to keep songs on for max 20 weeks, but then after that if it's still streaming well they move down to recurrents, then after 52 weeks they move it to "E1" category (E cat is "gold")
    <li>ideas:</li>
    - could have an input to add songs to the set that get tracked, and different groups
</ul>
</details>