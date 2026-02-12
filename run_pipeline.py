# upload_pipeline.py

import sys
from selenium import webdriver
from comparator import comparator, log  
from up import uploader
from pathlib import Path

# Directory where the current .py file is located
current_dir = Path(__file__).resolve().parent

# DISCORD_URL = "https://discord.com/app"
fromD = current_dir.parent / "0delete afater uplaod"
UPLOAD_FOLDER = current_dir / "test"
UPLOAD_FOLDER = fromD
BATCH_SIZE = 10
UPLOAD_WAIT_TIMEOUT = 900  # 15 minutes max per batch

def get_files() -> List:
    discord_filenames, missing_locally, extra_locally, matched = comparator(current_dir.parent / "0delete afater uplaod")
    log(discord_filenames, missing_locally, extra_locally, matched)
    files = list(extra_locally)
    files = [fromD / x for x in extra_locally]
    return extra_locally, files
def main():
    _, files = get_files()
    while (len(files) > 0 ):
        try:
            uploader(files)

        except Exception as e:
            print(str(e))
        _, files = get_files()
            


if __name__ == "__main__":
    main()
