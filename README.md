## WBRU 360 UPDATES:
now instead of overwriting column, creates a new column showcasing playcounts.


# wbru_playcounts

A tool used to automatically get the playcount numbers for a set of songs from Spotify. Used by the Indie team at [WBRU](https://www.wbru.com/) to decide which tracks will get added to the internet radio stream. WBRU is the Brown University affiliated radio station.

## Setup:

1. Clone the repo (`git clone <url>`)

2. Make sure you have python installed and Chrome browser

3. In your python environment install all of the packages in `requirements.txt`

## Usage:

1. Copy the column of song URLs (to the track on Spotify) from the current/recurrents sheet to the leftmost column (column A) in `data.xlsx`

2. Save and close `data.xlsx`

3. Run `python count_looper.py` (this may take a few minutes — if you get errors try running somewhere with faster internet connection)

4. `data.xlsx` now has the corresponding playcounts for the songs. Copy this data back into the current/recurrents sheet for today's date


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