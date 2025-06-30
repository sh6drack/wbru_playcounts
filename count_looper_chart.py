import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

def extract_track_id(url):
    """Extract track ID from Spotify URL"""
    match = re.search(r'/track/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

data = pd.read_excel("test_data.xlsx", header=None)

# Setup Spotify API
client_credentials_manager = SpotifyClientCredentials(
    client_id="7914f288d3fa40e08faa11a2af59c3b6",
    client_secret="b514416785af45dabb0f6bfaccdfd2cd"
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Setup Selenium
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

playcounts = []
song_names = []
artists = []

for row in data.iterrows():
    url = row[1][0]
    if str(url).startswith(("https://open.spotify.com/track/", "http://open.spotify.com/track/")):
        track_id = extract_track_id(url)
        
        if track_id:
            try:
                # Get track info from API
                track_info = sp.track(track_id)
                song_title = track_info['name'] if track_info else 'Unknown'
                artist_name = track_info['artists'][0]['name'] if track_info and track_info.get('artists') else 'Unknown'
                
                # Get playcount from scraping
                driver.get(url)
                playcount_element = driver.find_element(By.CSS_SELECTOR, "span[data-testid='playcount']")
                count = int(playcount_element.text.replace(",", ""))
                count_in_millions = count/1_000_000
                
                playcounts.append(count_in_millions)
                song_names.append(song_title)
                artists.append(artist_name)
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                playcounts.append("")
                song_names.append("Error")
                artists.append("Error")
        else:
            print(f"Could not extract track ID from: {url}")
            playcounts.append("")
            song_names.append("")
            artists.append("")
    else:
        playcounts.append("")
        song_names.append("")
        artists.append("")

data['Song'] = song_names
data['Artist'] = artists
data['Playcounts'] = playcounts
data.to_excel("data_with_playcounts.xlsx", header=['URL', 'Song', 'Artist', 'Playcounts (millions)'], index=False)

driver.quit()
