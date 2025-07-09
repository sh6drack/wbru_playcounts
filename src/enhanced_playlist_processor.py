"""
Enhanced playlist processor with logging and playcount tracking
"""
import pandas as pd
from .spotify_utils import get_playlist_tracks, get_playlist_info_with_tracks
from .playcount_scraper import get_playcounts
from .playcount_tracker import PlaycountTracker
from .logging_utils import setup_logger

def process_playlist_to_chart_with_tracking(playlist_url):
    """Process playlist and add to master tracking file"""
    logger = setup_logger("enhanced_processor")
    tracker = PlaycountTracker()
    
    # Get playlist name and tracks
    df_links, playlist_name = get_playlist_info_with_tracks(playlist_url)
    if df_links.empty:
        logger.error("No tracks found in playlist")
        return pd.DataFrame()
    
    # Get track URLs
    track_urls = df_links['URL'].tolist()
    
    # Get playcounts for all tracks
    chart_data = get_playcounts(track_urls)
    
    if not chart_data.empty:
        # Add to master tracking file
        master_df = tracker.add_or_update_playcounts(chart_data)
        master_df = tracker.calculate_growth()
        
        # Export snapshot with playlist name
        snapshot_file = tracker.export_playlist_snapshot(playlist_name)
        logger.info(f"Created snapshot: {snapshot_file}")
        
        return master_df
    
    return chart_data

def process_playlist_to_links_with_logging(playlist_url, save_file=None):
    """Extract playlist links and save to logs folder"""
    logger = setup_logger("enhanced_processor")
    
    result, playlist_name = get_playlist_info_with_tracks(playlist_url)
    
    if not result.empty:
        # Save to logs folder if filename provided
        if save_file:
            if not save_file.startswith("logs/"):
                save_file = f"logs/{save_file}"
            result.to_excel(save_file, index=False)
            logger.info(f"Saved playlist links to {save_file}")
        
    else:
        logger.error("Failed to extract any tracks")
    
    return result

def update_existing_tracks(urls_list):
    """
    Update playcounts for existing tracks in the master file
    """
    logger = setup_logger("enhanced_processor")
    tracker = PlaycountTracker()
    
    logger.info(f"Updating playcounts for {len(urls_list)} existing tracks")
    
    # Get playcounts for the URLs
    chart_data = get_playcounts(urls_list)
    
    if not chart_data.empty:
        # Add to master tracking file
        master_df = tracker.add_or_update_playcounts(chart_data)
        
        # Calculate growth
        master_df = tracker.calculate_growth()
        
        # Export snapshot
        snapshot_file = tracker.export_current_snapshot()
        logger.info(f"Updated master file and created snapshot: {snapshot_file}")
        
        return master_df
    
    return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    logger = setup_logger("main")
    
    # Example playlist URL
    playlist_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
    
    print("=== Option 1: Extract playlist links only (fast, with logging) ===")
    df_links = process_playlist_to_links_with_logging(playlist_url, "playlist_links_logged.xlsx")
    if not df_links.empty:
        logger.info("Playlist links saved to logs folder")
    
    print("\n=== Option 2: Process playlist with tracking (slow) ===")
    print("Note: This will take several minutes and update the master tracking file")
    
    # Uncomment to process with full tracking
    # master_df = process_playlist_to_chart_with_tracking(playlist_url)
    # if not master_df.empty:
    #     logger.info(f"Master file now contains {len(master_df)} tracks")
    #     print("Check master_playcounts.xlsx for the complete tracking data")
    
    print("\n=== Option 3: Update specific tracks ===")
    # Example of updating specific tracks
    # specific_urls = [
    #     "https://open.spotify.com/track/76RAlQcfuQknnQFruYDj6Q",
    #     "https://open.spotify.com/track/3aSWXU6owkZeVhh94XxEWO"
    # ]
    # update_existing_tracks(specific_urls)