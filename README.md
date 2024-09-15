# wbru_playcounts

## Setup:

Make sure you have python installed and Chrome, and then in your python environment install selenium:
`pip install selenium`

Make sure you have the URLs to the song on Spotify.

Then run `python countLooper.py`

## Notes:
* take artist/song or spotify link and every Tuesday update the stream count
* stream count tracks the data of how popular songs are, Peter prefers stream numbers
    - Indie has a guideline based on stream numbers to determine light/medium/heavy classification for songs; the different classifications determine how frequent to play a song
    - enhancement: use guideline to auto give classification to song
    - enhancement: they also like to see trends, so it would be useful to create a dashboard of song stream counts week by week (like trendy!)
        + this could be matplotlib
* immediate todo: write README and share with Judd (has most CS experience), Morgan, & Tommy; can be run locally even on station computer too
    - then: host my script so that it can be viewed by indie team
    - on output page, display link, artist, song, stream count
* another way to get stream numbers is through spotify app
* spreadsheet: https://docs.google.com/spreadsheets/d/16rxDbk8cNcZYGxYOze-zVlQgQwHU2ThSk-3rEeRrDuo/edit?usp=sharing
    - songs being played are in col G-H, classification in col A, stream counts in col M (unit: millions)
        + isn't point of WBRU indie to play more underground stuff? Current apporach is to appeal popularly right now, team is trying to push back on threshold
    - like to have data for every song, which are the row entries
    - they like to keep songs on for max 20 weeks, but then after that if it's still streaming well they move down to recurrents, then after 52 weeks they move it to "E1" category (E cat is "gold")
* ideas:
    - could have like an input to add songs to the set that get tracked, and like different groups