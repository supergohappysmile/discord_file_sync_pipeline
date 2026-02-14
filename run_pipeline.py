# upload_pipeline.py

import sys
from selenium import webdriver
from comparator import comparator, log  
from up import uploader
from pathlib import Path
from parser import create_parser
# Directory where the current .py file is located
current_dir = Path(__file__).resolve().parent

# DISCORD_URL = "https://discord.com/app"
fromD = current_dir.parent / "0delete afater uplaod"
# TERMINAL_FILE = "mikubrit_02122026.log"
BATCH_SIZE = 10
UPLOAD_WAIT_TIMEOUT = 900  # 15 minutes max per batch

def get_files(driver, UPLOAD_FOLDER) -> List:
    discord_filenames, missing_locally, extra_locally, matched = comparator(driver,  UPLOAD_FOLDER)
    log(discord_filenames, missing_locally, extra_locally, matched)
    files = list(extra_locally)
    files = [UPLOAD_FOLDER / x for x in extra_locally]
    return extra_locally, files
def main():

    parser = create_parser()
    args = parser.parse_args()

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)


    UPLOAD_FOLDER = Path(args.source_folder).resolve()
    _, files = get_files(driver, UPLOAD_FOLDER)
    while (len(files) > 0 ):
        try:
            uploader(driver, files, UPLOAD_FOLDER=UPLOAD_FOLDER)

        except Exception as e:
            print(str(e))
        _, files = get_files(driver, UPLOAD_FOLDER)
            


if __name__ == "__main__":
    main()
