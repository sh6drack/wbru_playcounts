@echo off
cd /d "%~dp0"
echo WBRU Excel URL Updater
echo ======================
echo.
echo This will read URLs from an Excel file and update playcounts (5-10 minutes)
echo.
echo Default file: data.xlsx (paste your URLs in column A)
echo.
set /p excel_file=Enter Excel filename (press Enter for data.xlsx): 

if "%excel_file%"=="" set excel_file=data.xlsx

if not exist "%excel_file%" (
    echo File %excel_file% not found.
    pause
    exit /b 1
)

echo.
echo Processing URLs from %excel_file%...
echo Chrome will open automatically.
echo.

python -c "
import sys
sys.path.insert(0, 'src')
import pandas as pd
from enhanced_playlist_processor import update_existing_tracks

# Read Excel file
df = pd.read_excel('%excel_file%')

# Try to find URL column
url_col = None
for col in df.columns:
    if 'url' in col.lower() or 'link' in col.lower():
        url_col = col
        break

if url_col is None:
    # Try first column or column C
    if len(df.columns) >= 3:
        url_col = df.columns[2]  # Column C
    else:
        url_col = df.columns[0]  # Column A

urls = df[url_col].dropna().tolist()
urls = [url for url in urls if str(url).startswith('https://open.spotify.com/track/')]

if urls:
    print(f'Processing {len(urls)} URLs from {url_col}...')
    update_existing_tracks(urls)
    print('Complete! Check logs/ folder for updated files.')
else:
    print('No valid Spotify URLs found in the file.')
"
if %errorlevel% neq 0 (
    echo ERROR: Failed to run. Please run install_packages.bat first.
    pause
    exit /b 1
)

echo.
pause