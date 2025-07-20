"""
Multi-playlist processor that handles individual playlist tracking
"""
import pandas as pd
import os
from datetime import datetime
from spotify_utils import get_playlist_info_with_tracks
from playcount_scraper import get_playcounts
from playlist_manager import PlaylistManager
from logging_utils import setup_logger, get_playcount_column_name

class MultiPlaylistProcessor:
    def __init__(self):
        self.logger = setup_logger("multi_playlist_processor")
        self.manager = PlaylistManager()
    
    def process_playlist_with_id(self, playlist_url, playlist_name=None):
        """Process a playlist and track it individually"""
        if not playlist_name:
            # Try to get playlist name from Spotify
            _, playlist_name = get_playlist_info_with_tracks(playlist_url)
        
        # Add or update playlist in manager
        playlist_id = self.manager.add_playlist(playlist_name, playlist_url)
        
        # Get playlist tracks
        df_links, actual_name = get_playlist_info_with_tracks(playlist_url)
        if df_links.empty:
            self.logger.error("No tracks found in playlist")
            return pd.DataFrame(), None
        
        # Get playcounts
        track_urls = df_links['URL'].tolist()
        chart_data = get_playcounts(track_urls)
        
        if not chart_data.empty:
            # Save to playlist-specific file
            playlist_file = self.manager.get_playlist_file(playlist_id)
            current_date_column = get_playcount_column_name()
            
            # Load existing playlist data or create new
            if os.path.exists(playlist_file):
                existing_df = pd.read_excel(playlist_file)
                
                # Add new date column only if it doesn't exist
                if current_date_column not in existing_df.columns:
                    existing_df[current_date_column] = pd.NA
                
                # Update playcounts
                for _, new_row in chart_data.iterrows():
                    mask = existing_df['URL'] == new_row['URL']
                    if mask.any():
                        existing_df.loc[mask, current_date_column] = new_row[current_date_column]
                    else:
                        # Add new track
                        new_track = {
                            'Song': new_row['Song'],
                            'Artist': new_row['Artist'],
                            'URL': new_row['URL'],
                            current_date_column: new_row[current_date_column]
                        }
                        existing_df = pd.concat([existing_df, pd.DataFrame([new_track])], ignore_index=True)
                
                playlist_df = existing_df
            else:
                # Create new playlist file
                playlist_df = chart_data[['Song', 'Artist', 'URL']].copy()
                playlist_df[current_date_column] = chart_data[current_date_column]
            
            # Save playlist file
            playlist_df.to_excel(playlist_file, index=False)
            self.logger.info(f"Saved playlist data to {playlist_file}")
            
            # Update timestamp
            self.manager.update_playlist_timestamp(playlist_id)
            
            # Merge to master file
            master_df = self.manager.merge_to_master(chart_data, actual_name)
            
            return playlist_df, playlist_id
        
        return pd.DataFrame(), None
    
    def update_playlist_by_id(self, playlist_id):
        """Update an existing playlist by ID"""
        playlist_info = self.manager.get_playlist(playlist_id)
        if not playlist_info:
            self.logger.error(f"Playlist {playlist_id} not found")
            return pd.DataFrame()
        
        return self.process_playlist_with_id(playlist_info['url'], playlist_info['name'])
    
    def list_playlists(self):
        """List all tracked playlists"""
        playlists = self.manager.list_playlists()
        if not playlists:
            print("No playlists are currently being tracked.")
            return
        
        print("Currently tracked playlists:")
        print("-" * 50)
        for playlist_id, info in playlists.items():
            last_updated = info.get('last_updated', 'Never')
            if last_updated != 'Never':
                last_updated = datetime.fromisoformat(last_updated).strftime('%Y-%m-%d %H:%M')
            
            print(f"ID: {playlist_id}")
            print(f"Name: {info['name']}")
            print(f"Last Updated: {last_updated}")
            print(f"Description: {info.get('description', 'No description')}")
            print("-" * 50)
    
    def reset_playlist(self, playlist_id):
        """Reset a playlist's tracking data"""
        return self.manager.reset_playlist(playlist_id)
    
    def remove_playlist(self, playlist_id):
        """Remove a playlist from tracking"""
        return self.manager.remove_playlist(playlist_id)

def quick_url_extract(playlist_url, filename=None):
    """Quick URL extraction without tracking"""
    logger = setup_logger("quick_extract")
    
    df_links, playlist_name = get_playlist_info_with_tracks(playlist_url)
    
    if not df_links.empty:
        if not filename:
            date_str = datetime.now().strftime("%Y-%m-%d")
            clean_name = playlist_name.replace(" ", "_").replace("/", "-")[:30]
            filename = f"logs/{clean_name}_urls_{date_str}.xlsx"
        
        if not filename.startswith("logs/"):
            filename = f"logs/{filename}"
        
        df_links.to_excel(filename, index=False)
        logger.info(f"Extracted {len(df_links)} URLs to {filename}")
        return filename
    
    return None