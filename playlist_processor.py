"""
Main module for processing Spotify playlists and extracting playcounts
"""
import pandas as pd
from spotify_utils import get_playlist_tracks, get_playlist_info_with_tracks
from playcount_scraper import get_playcounts

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

def process_playlist_to_links(playlist_url):
    """
    Takes a Spotify playlist URL and returns a DataFrame with just the track links
    This is useful for creating a chart of links that can be processed later
    """
    return get_playlist_info_with_tracks(playlist_url)

# Example usage
if __name__ == "__main__":
    # Example playlist URL
    playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
    
    print("=== Option 1: Extract playlist links only (fast) ===")
    df_links = process_playlist_to_links(playlist_url)
    print(df_links.head())
    df_links.to_excel("playlist_links.xlsx", index=False)
    print("Playlist links saved to playlist_links.xlsx")
    
    print("\n=== Option 2: Extract playlist with playcounts (slow) ===")
    print("Note: This will take several minutes as it scrapes playcount data")
    
    # Uncomment the lines below to process playcounts
    # df_chart = process_playlist_to_chart(playlist_url)
    # print(df_chart.head())
    # df_chart.to_excel("playlist_with_playcounts.xlsx", index=False)
    # print("Playlist with playcounts saved to playlist_with_playcounts.xlsx")