import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# Spotify API configuration
SPOTIFY_CLIENT_ID = "7914f288d3fa40e08faa11a2af59c3b6"
SPOTIFY_CLIENT_SECRET = "b514416785af45dabb0f6bfaccdfd2cd"

def get_spotify_client():
    """Create and return a Spotify client"""
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def extract_track_id(url):
    """Extract track ID from Spotify URL"""
    match = re.search(r'/track/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

def extract_playlist_id(url):
    """Extract playlist ID from Spotify URL"""
    match = re.search(r'/playlist/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

def get_playlist_tracks(playlist_url):
    """Extract all track URLs from a Spotify playlist"""
    sp = get_spotify_client()
    
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print(f"Could not extract playlist ID from: {playlist_url}")
        return []
    
    try:
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

def get_playlist_info_with_tracks(playlist_url):
    """Get playlist name and track data"""
    sp = get_spotify_client()
    
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print(f"Could not extract playlist ID from: {playlist_url}")
        return pd.DataFrame(), ""
    
    try:
        # Get playlist info
        playlist_info = sp.playlist(playlist_id)
        playlist_name = playlist_info['name']
        
        # Get playlist tracks with metadata
        results = sp.playlist_tracks(playlist_id)
        track_data = []
        
        for item in results['items']:
            if item and item.get('track') and item['track'].get('id'):
                track = item['track']
                track_url = f"https://open.spotify.com/track/{track['id']}"
                song_name = track.get('name', 'Unknown')
                artist_name = track['artists'][0]['name'] if track.get('artists') else 'Unknown'
                
                track_data.append({
                    'Song': song_name,
                    'Artist': artist_name,
                    'URL': track_url
                })
        
        # Handle pagination
        while results['next']:
            results = sp.next(results)
            for item in results['items']:
                if item and item.get('track') and item['track'].get('id'):
                    track = item['track']
                    track_url = f"https://open.spotify.com/track/{track['id']}"
                    song_name = track.get('name', 'Unknown')
                    artist_name = track['artists'][0]['name'] if track.get('artists') else 'Unknown'
                    
                    track_data.append({
                        'Song': song_name,
                        'Artist': artist_name,
                        'URL': track_url
                    })
        
        df = pd.DataFrame(track_data)
        print(f"Extracted {len(df)} tracks from playlist: {playlist_name}")
        return df, playlist_name
        
    except Exception as e:
        print(f"Error processing playlist: {e}")
        return pd.DataFrame(), ""