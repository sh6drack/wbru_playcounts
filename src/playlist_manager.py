"""
Playlist management system for tracking multiple playlists
"""
import os
import json
import pandas as pd
from datetime import datetime
from logging_utils import setup_logger

class PlaylistManager:
    def __init__(self):
        self.logger = setup_logger("playlist_manager")
        self.config_file = "logs/playlist_config.json"
        self.master_file = "logs/master_playcounts.xlsx"
        self.ensure_logs_folder()
        self.config = self.load_config()
    
    def ensure_logs_folder(self):
        """Create logs folder if it doesn't exist"""
        if not os.path.exists("logs"):
            os.makedirs("logs")
    
    def load_config(self):
        """Load playlist configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
        
        return {"playlists": {}}
    
    def save_config(self):
        """Save playlist configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def add_playlist(self, name, url, description=""):
        """Add a new playlist to track"""
        playlist_id = name.lower().replace(" ", "_")
        
        self.config["playlists"][playlist_id] = {
            "name": name,
            "url": url,
            "description": description,
            "created": datetime.now().isoformat(),
            "last_updated": None,
            "file": f"logs/{playlist_id}_tracking.xlsx"
        }
        
        self.save_config()
        self.logger.info(f"Added playlist: {name}")
        return playlist_id
    
    def list_playlists(self):
        """List all tracked playlists"""
        return self.config["playlists"]
    
    def get_playlist(self, playlist_id):
        """Get playlist info by ID"""
        return self.config["playlists"].get(playlist_id)
    
    def update_playlist_timestamp(self, playlist_id):
        """Update last updated timestamp"""
        if playlist_id in self.config["playlists"]:
            self.config["playlists"][playlist_id]["last_updated"] = datetime.now().isoformat()
            self.save_config()
    
    def remove_playlist(self, playlist_id):
        """Remove a playlist from tracking"""
        if playlist_id in self.config["playlists"]:
            playlist_file = self.config["playlists"][playlist_id]["file"]
            
            # Remove the file if it exists
            if os.path.exists(playlist_file):
                os.remove(playlist_file)
                self.logger.info(f"Removed file: {playlist_file}")
            
            # Remove from config
            del self.config["playlists"][playlist_id]
            self.save_config()
            self.logger.info(f"Removed playlist: {playlist_id}")
            return True
        return False
    
    def get_playlist_file(self, playlist_id):
        """Get the tracking file path for a playlist"""
        playlist = self.get_playlist(playlist_id)
        return playlist["file"] if playlist else None
    
    def merge_to_master(self, playlist_data, playlist_name):
        """Merge playlist data into master file"""
        try:
            # Load existing master file or create new one
            if os.path.exists(self.master_file):
                master_df = pd.read_excel(self.master_file)
            else:
                master_df = pd.DataFrame()
            
            # Add playlist source column
            playlist_data = playlist_data.copy()
            playlist_data['Source_Playlist'] = playlist_name
            
            # Merge with master
            if master_df.empty:
                merged_df = playlist_data
            else:
                # Merge on URL to avoid duplicates
                merged_df = pd.concat([master_df, playlist_data], ignore_index=True)
                merged_df = merged_df.drop_duplicates(subset=['URL'], keep='last')
            
            # Save master file
            merged_df.to_excel(self.master_file, index=False)
            self.logger.info(f"Merged {len(playlist_data)} tracks to master file")
            
            return merged_df
            
        except Exception as e:
            self.logger.error(f"Error merging to master: {e}")
            return pd.DataFrame()
    
    def reset_playlist(self, playlist_id):
        """Reset a playlist's tracking data"""
        playlist_file = self.get_playlist_file(playlist_id)
        if playlist_file and os.path.exists(playlist_file):
            os.remove(playlist_file)
            self.logger.info(f"Reset playlist: {playlist_id}")
            return True
        return False