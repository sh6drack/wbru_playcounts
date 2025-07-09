import pandas as pd
import os
from datetime import datetime
from .logging_utils import setup_logger, get_playcount_column_name

def ensure_logs_folder():
    """Ensure logs folder exists"""
    if not os.path.exists("logs"):
        os.makedirs("logs")

class PlaycountTracker:
    """Manages tracking and updating playcounts over time"""
    
    def __init__(self, master_file="logs/master_playcounts.xlsx"):
        ensure_logs_folder()
        self.master_file = master_file
        self.logger = setup_logger("playcount_tracker")
        
    def load_or_create_master_file(self):
        """Load existing master file or create new one"""
        if os.path.exists(self.master_file):
            self.logger.info(f"Loading existing master file: {self.master_file}")
            return pd.read_excel(self.master_file)
        else:
            self.logger.info(f"Creating new master file: {self.master_file}")
            return pd.DataFrame(columns=['Song', 'Artist', 'URL'])
    
    def add_or_update_playcounts(self, new_data):
        """
        Add new playcount data to the master file
        new_data should be a DataFrame with columns: Song, Artist, URL, Playcounts (millions)
        """
        master_df = self.load_or_create_master_file()
        current_date_column = get_playcount_column_name()
        
        self.logger.info(f"Adding playcounts for {len(new_data)} tracks with column: {current_date_column}")
        
        # If master file is empty, initialize with new data
        if master_df.empty:
            master_df = new_data[['Song', 'Artist', 'URL']].copy()
            master_df[current_date_column] = new_data['Playcounts (millions)']
        else:
            # Merge new data with existing data
            # First, ensure new tracks are added
            for _, new_row in new_data.iterrows():
                # Check if track already exists (by URL)
                existing_mask = master_df['URL'] == new_row['URL']
                
                if existing_mask.any():
                    # Update existing track
                    master_df.loc[existing_mask, current_date_column] = new_row['Playcounts (millions)']
                    self.logger.info(f"Updated playcount for existing track: {new_row['Song']}")
                else:
                    # Add new track
                    new_track = {
                        'Song': new_row['Song'],
                        'Artist': new_row['Artist'],
                        'URL': new_row['URL'],
                        current_date_column: new_row['Playcounts (millions)']
                    }
                    master_df = pd.concat([master_df, pd.DataFrame([new_track])], ignore_index=True)
                    self.logger.info(f"Added new track: {new_row['Song']}")
        
        # Save updated master file
        master_df.to_excel(self.master_file, index=False)
        self.logger.info(f"Saved updated master file with {len(master_df)} tracks")
        
        return master_df
    
    def get_playcount_history(self, url=None):
        """Get playcount history for a specific track or all tracks"""
        master_df = self.load_or_create_master_file()
        
        if url:
            track_data = master_df[master_df['URL'] == url]
            return track_data
        else:
            return master_df
    
    def calculate_growth(self):
        """Calculate playcount growth between dates"""
        master_df = self.load_or_create_master_file()
        
        # Get all playcount columns (those starting with "Playcounts")
        playcount_cols = [col for col in master_df.columns if col.startswith('Playcounts')]
        
        if len(playcount_cols) < 2:
            self.logger.info("Need at least 2 playcount measurements to calculate growth")
            return master_df
        
        # Sort columns by date
        playcount_cols.sort(key=lambda x: datetime.strptime(x.split(' ')[1], "%d.%m.%Y"))
        
        # Calculate growth between consecutive measurements
        for i in range(1, len(playcount_cols)):
            prev_col = playcount_cols[i-1]
            curr_col = playcount_cols[i]
            growth_col = f"Growth {curr_col.split(' ')[1]}"
            
            master_df[growth_col] = (master_df[curr_col] - master_df[prev_col]).fillna(0)
        
        master_df.to_excel(self.master_file, index=False)
        self.logger.info(f"Calculated growth metrics and saved to {self.master_file}")
        
        return master_df
    
    def export_playlist_snapshot(self, playlist_name="playlist"):
        """Export snapshot with playlist name"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        clean_name = playlist_name.replace(" ", "_").replace("/", "-")[:30]
        filename = f"logs/{clean_name}_{date_str}.xlsx"
        
        master_df = self.load_or_create_master_file()
        master_df.to_excel(filename, index=False)
        self.logger.info(f"Exported snapshot to {filename}")
        
        return filename