"""
Refactored version of count_looper.py with modular structure
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
    # Example 1: Process individual track URLs
    urls = [
        "https://open.spotify.com/track/76RAlQcfuQknnQFruYDj6Q?si=a1052891c545434f"
    ]
    
    print("=== Processing individual track URLs ===")
    df = get_playcounts(urls)
    print(df)
    
    # Example 2: Process entire playlist with playcounts
    playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"  # Example playlist URL
    
    print("\n=== Processing playlist with playcounts ===")
    df_playlist = process_playlist_to_chart(playlist_url)
    print(df_playlist)
    
    # Example 3: Extract playlist links only (no playcounts)
    print("\n=== Extracting playlist links only ===")
    df_links = process_playlist_to_links(playlist_url)
    print(df_links)
    df_links.to_excel("playlist_links.xlsx", index=False)
    print("Playlist links saved to playlist_links.xlsx")
    
    # Save to Excel
    df.to_excel("spotify_playcounts.xlsx", index=False)
    print("Results saved to spotify_playcounts.xlsx")