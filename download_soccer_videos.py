import os
import time
import logging
from SoccerNet.Downloader import SoccerNetDownloader
import urllib.error

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize the downloader
mySoccerNetDownloader = SoccerNetDownloader(LocalDirectory="./SoccerNet_videos")
mySoccerNetDownloader.password = "s0cc3rn3t"

# Function to handle retries with exponential backoff
def download_with_retries(files: list[str], split: list[str], max_retries: int = 5):
    for file in files:
        for sp in split:
            # Construct the local file path
            local_file_path = os.path.join(mySoccerNetDownloader.LocalDirectory, sp, file)
            
            # Check if the file already exists
            if os.path.exists(local_file_path):
                logging.info(f"{local_file_path} already exists. Skipping download.")
                continue  # Skip to the next file

            attempt = 0
            backoff = 5  # Initial backoff time in seconds
            
            while attempt < max_retries:
                try:
                    logging.info(f"Attempt {attempt + 1} to download {file} for split {sp}...")
                    mySoccerNetDownloader.downloadGames(files=[file], split=[sp])
                    logging.info(f"Download successful: {file} for split {sp}!")
                    break  # Exit if successful
                except (urllib.error.ContentTooShortError, urllib.error.URLError, ConnectionResetError) as e:
                    attempt += 1
                    logging.error(f"Download failed: {e}")
                    if attempt < max_retries:
                        wait_time = backoff * (2 ** (attempt - 1))  # Exponential backoff
                        logging.info(f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        logging.error(f"Maximum retries reached for {file} in split {sp}. Download failed.")
                        break  # Stop retrying after max attempts

# Download 720p videos
download_with_retries(files=["1_720p.mkv", "2_720p.mkv"], split=["train", "valid", "test", "challenge"])
