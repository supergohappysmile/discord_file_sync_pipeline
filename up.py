import os
import glob
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

import os
from dotenv import load_dotenv

# Load environment variables from .env

# ============================
# CONFIGURATION
# ============================
load_dotenv()

EMAIL = os.getenv("email00")
PASSWORD = os.getenv("password00")

LOGIN_URL = "https://discord.com/app"

# Directory where the current .py file is located
current_dir = Path(__file__).resolve().parent

# DISCORD_URL = "https://discord.com/app"
fromD = current_dir.parent.parent / "0delete afater uplaod"
BATCH_SIZE = 10
UPLOAD_WAIT_TIMEOUT = 900  # 15 minutes max per batch


def wait_for_upload_100(driver, UPLOAD_FOLDER, timeout=900):
    """
    Waits until all Discord progress bars have aria-label="100 percent complete".
    """
    
    # ============================
    # CONFIGURATION
    # ============================


    LOGIN_URL = "https://discord.com/app"

    # Directory where the current .py file is located
    current_dir = Path(__file__).resolve().parent

    # DISCORD_URL = "https://discord.com/app"
    BATCH_SIZE = 10
    UPLOAD_WAIT_TIMEOUT = 900  # 15 minutes max per batch




    wait = WebDriverWait(driver, timeout)
    end_time = time.time() + timeout

    while time.time() < end_time:
        time.sleep(1)  # small polling interval

        # Find all progress bars that exist
        progress_elements = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'progress__') and @role='progressbar']"
        )

        if not progress_elements:
            # No progress bars = nothing uploading
            break

        all_complete = True
        for el in progress_elements:
            aria_label = el.get_attribute("aria-label")
            if aria_label != "100 percent complete":
                all_complete = False
                break

        if all_complete:
            # All progress bars reached 100%
            break

    # Buffer to ensure Discord finalizes upload
    time.sleep(1)
    print("All uploads reached 100%!")


def uploader(files, UPLOAD_FOLDER=current_dir.parent.parent / "0delete afater uplaod"):

    # ============================
    # CONFIGURATION
    # ============================
    load_dotenv()

    EMAIL = os.getenv("email00")
    PASSWORD = os.getenv("password00")

    LOGIN_URL = "https://discord.com/app"

    # Directory where the current .py file is located

    # DISCORD_URL = "https://discord.com/app"
    BATCH_SIZE = 10
    UPLOAD_WAIT_TIMEOUT = 900  # 15 minutes max per batch
    # ============================
    # SETUP DRIVER
    # ============================


    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 999999)


    driver.get(LOGIN_URL)

    # ============================
    # FILL LOGIN FORM
    # ============================

    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, "email"))
    )

    password_input = wait.until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    email_input.clear()
    email_input.send_keys(EMAIL)

    password_input.clear()
    password_input.send_keys(PASSWORD)

    # Click Login button
    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")
        )
    )

    login_button.click()

    print("Login submitted.")

    # ============================
    # HANDLE 2FA IF NEEDED
    # ============================

    time.sleep(5)  # allow redirect

    print("If you have 2FA, complete it now.")
    print("Navigate to the correct server/channel.")

    input("Press ENTER here once you are inside the target channel...")

    print("Ready to continue automation.")




    # ============================
    # UPLOAD LOOP
    # ============================
    len1 = len(files)
    files = [Path('D:/') / f.relative_to('D:/GITHUB') for f in files] # TODO make the input correct without this
    print(len1 == len(files))

    for i in range(0, len(files), BATCH_SIZE):
        batch = files[i:i + BATCH_SIZE]
        batch = list(map(str, batch))
        #breakpoint()
        print(f"\nUploading batch {i // BATCH_SIZE + 1} ({len(batch)} files)...")

        # Locate file input
        try:
            file_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )

            # Upload multiple files
            file_input.send_keys("\n".join(batch))
        except Exception as e:
            print(e)
            print("trying again after one full minute...")
            time.sleep(60)
            file_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            # Upload multiple files
            file_input.send_keys("\n".join(batch))


        # Wait for upload to complete
        # wait_for_upload_completion()
        # wait for upload box go away
        wait_for_upload_100(driver, UPLOAD_FOLDER)

        # Focus message input box
        message_box = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@role='textbox']")
            )
        )

        message_box.click()
        time.sleep(1)

        # Press Enter to send message
        message_box.send_keys(Keys.ENTER)

        print("Message sent.")

        # Wait a few seconds to ensure message posts
        time.sleep(8)

    print("\nAll files uploaded and sent successfully.")
    driver.quit()





if __name__ == "__main__":
    # ============================
    # GET FILES
    # ============================

    # files = sorted(glob.glob(os.path.join(UPLOAD_FOLDER, "*.part*")))

    # if not files:
    #     print("No .part files found.")
    #     driver.quit()
    #     exit()

    # print(f"Found {len(files)} files.")
    uploader(files)


