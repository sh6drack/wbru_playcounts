import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from spotify_utils import get_spotify_client, extract_track_id
from logging_utils import setup_logger, get_playcount_column_name

def get_playcounts(urls):
    """
    Takes a list of Spotify track URLs and returns a DataFrame with song names and playcounts
    """
    logger = setup_logger("playcount_scraper")
    sp = get_spotify_client()
    playcount_column = get_playcount_column_name()
    
    logger.info(f"Starting playcount extraction for {len(urls)} tracks")
    logger.info(f"Using column name: {playcount_column}")
    
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
                    # Get track info from API first
                    track_info = sp.track(track_id)
                    song_title = track_info['name'] if track_info else 'Unknown'
                    artist_name = track_info['artists'][0]['name'] if track_info and track_info.get('artists') else 'Unknown'
                    
                    # Try to get playcount from scraping
                    count_in_millions = 0
                    try:
                        driver.get(url)
                        playcount_element = driver.find_element(By.CSS_SELECTOR, "span[data-testid='playcount']")
                        count = int(playcount_element.text.replace(",", ""))
                        count_in_millions = count / 1_000_000
                        logger.info(f"Successfully processed: {song_title} by {artist_name} - {count_in_millions:.2f}M plays")
                    except Exception as scrape_error:
                        logger.warning(f"No playcount data found for '{song_title}' by {artist_name} - using 0 (likely WBRU production track)")
                    
                    results.append({
                        'Song': song_title,
                        'Artist': artist_name,
                        'URL': url,
                        playcount_column: count_in_millions
                    })
                    
                except Exception as e:
                    logger.error(f"Error getting track info for {url}: {e}")
                    results.append({
                        'Song': 'Error',
                        'Artist': 'Error',
                        'URL': url,
                        playcount_column: 0
                    })
            else:
                logger.warning(f"Could not extract track ID from: {url}")
        else:
            logger.warning(f"Skipping non-track URL: {url}")
    
    driver.quit()
    logger.info(f"Completed playcount extraction. Processed {len(results)} tracks")
    return pd.DataFrame(results)