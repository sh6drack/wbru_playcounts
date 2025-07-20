from count_looper import process_playlist_to_chart

# Test the full playlist processing
playlist_url = "https://open.spotify.com/playlist/1a9S07rNBB5EJq35uZ29bJ?si=42ebcaf59fa6496e"
print(f"Processing playlist: {playlist_url}")

# Process the entire playlist
df = process_playlist_to_chart(playlist_url)
print(f"Processed {len(df)} tracks")
print(df.head())

# Save to Excel
df.to_excel("playlist_results.xlsx", index=False)
print("Results saved to playlist_results.xlsx")