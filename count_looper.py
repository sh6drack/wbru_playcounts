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

def extract_playlist_id(url):
    """Extract playlist ID from Spotify URL"""
    match = re.search(r'/playlist/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

def get_playlist_tracks(playlist_url):
    """
    Extract all track URLs from a Spotify playlist
    """
    # Setup Spotify API
    client_credentials_manager = SpotifyClientCredentials(
        client_id="7914f288d3fa40e08faa11a2af59c3b6",
        client_secret="b514416785af45dabb0f6bfaccdfd2cd"
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print(f"Could not extract playlist ID from: {playlist_url}")
        return []
    
    try:
        # Get playlist tracks
        results = sp.playlist_tracks(playlist_id)
        track_urls = []
        
        for item in results['items']:
            if item and item.get('track') and item['track'].get('id'):
                track_url = f"https://open.spotify.com/track/{item['track']['id']}"
                track_urls.append(track_url)
        
        # Handle pagination
        while results['next']:
            results = sp.next(results)
            for item in results['items']:
                if item and item.get('track') and item['track'].get('id'):
                    track_url = f"https://open.spotify.com/track/{item['track']['id']}"
                    track_urls.append(track_url)
        
        return track_urls
    
    except Exception as e:
        print(f"Error getting playlist tracks: {e}")
        return []

def process_playlist_to_chart(playlist_url):
    """
    Takes a Spotify playlist URL and returns a DataFrame with song names and playcounts
    """
    track_urls = get_playlist_tracks(playlist_url)
    if not track_urls:
        print("No tracks found in playlist")
        return pd.DataFrame()
    
    print(f"Found {len(track_urls)} tracks in playlist")
    return get_playcounts(track_urls)

def get_playcounts(urls):
    """
    Takes a list of Spotify track URLs and returns a DataFrame with song names and playcounts
    """
    # Setup Spotify API
    client_credentials_manager = SpotifyClientCredentials(
        client_id="7914f288d3fa40e08faa11a2af59c3b6",
        client_secret="b514416785af45dabb0f6bfaccdfd2cd"
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Setup Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    results = []
    
    for url in urls:
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
                    count_in_millions = count / 1_000_000
                    
                    results.append({
                        'Song': song_title,
                        'Artist': artist_name,
                        'URL': url,
                        'Playcounts (millions)': count_in_millions
                    })
                    
                except Exception as e:
                    print(f"Error processing {url}: {e}")
                    results.append({
                        'Song': 'Error',
                        'Artist': 'Error',
                        'URL': url,
                        'Playcounts (millions)': 0
                    })
            else:
                print(f"Could not extract track ID from: {url}")
        else:
            print(f"Skipping non-track URL: {url}")
    
    driver.quit()
    return pd.DataFrame(results)

# Example usage
if __name__ == "__main__":
    # Example 1: Process individual track URLs
    urls = [
        "https://open.spotify.com/track/76RAlQcfuQknnQFruYDj6Q?si=a1052891c545434f"
    ]
    
    df = get_playcounts(urls)
    print(df)
    
    # Example 2: Process entire playlist
    playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"  # Example playlist URL
    df_playlist = process_playlist_to_chart(playlist_url)
    print(df_playlist)
    
    # Save to Excel
    df.to_excel("spotify_playcounts.xlsx", index=False)
    print("Results saved to spotify_playcounts.xlsx")