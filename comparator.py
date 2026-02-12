import os
import time
import glob
from datetime import datetime
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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

DISCORD_URL = "https://discord.com/app"
UPLOAD_FOLDER = current_dir / "test"
BATCH_SIZE = 10
UPLOAD_WAIT_TIMEOUT = 900  # 15 minutes max per batch

def comparator(UPLOAD_FOLDER = current_dir / "test"):
    # ==============================
    # SELENIUM SETUP
    # ==============================

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    driver.get(DISCORD_URL)
    # ============================
    # FILL LOGIN FORM
    # ============================
    wait = WebDriverWait(driver, 60)

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


    print("If you have 2FA, complete it now.")
    print("Navigate to the correct server/channel.")

    input("Press ENTER here once you are inside the target channel...")

    print("Ready to continue automation.")



    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*=scroller]"))
    )

    # ==============================
    # SCROLL TO LOAD HISTORY
    # ==============================

    message_container = driver.find_element(By.CSS_SELECTOR, "div[class*=scroller]")

    last_height = 0
    while True:
        driver.execute_script("arguments[0].scrollTop = 0", message_container)
        time.sleep(2)
        new_height = driver.execute_script(
            "return arguments[0].scrollHeight", message_container
        )
        if new_height == last_height:
            break
        last_height = new_height


    # ==============================
    # COLLECT DISCORD FILENAMES
    # ==============================

    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='cdn.discordapp.com']")

    discord_filenames = set()

    for link in links:
        href = link.get_attribute("href")
        if href:
            parsed = urlparse(href)
            filename = parsed.path.split("/")[-1]
            if filename:
                discord_filenames.add(filename)

    driver.quit()


    # ==============================
    # GLOB LOCAL DIRECTORY
    # ==============================

    local_files = set()

    for filepath in glob.glob(os.path.join(UPLOAD_FOLDER, "*part*")):
        if os.path.isfile(filepath):
            local_files.add(os.path.basename(filepath))


    # ==============================
    # COMPARE
    # ==============================

    missing_locally = discord_filenames - local_files
    extra_locally = local_files - discord_filenames
    matched = discord_filenames & local_files
    return discord_filenames, missing_locally, extra_locally, matched


# ==============================
# SAFE OUTPUT FILE (NO OVERWRITE)
# ==============================

def get_unique_filename(base_name):
    if not os.path.exists(base_name):
        return base_name

    counter = 1
    while True:
        new_name = f"{base_name.rsplit('.',1)[0]}_{counter}.txt"
        if not os.path.exists(new_name):
            return new_name
        counter += 1

def log(discord_filenames, missing_locally, extra_locally, matched):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_output = f"discord_filename_report_{timestamp}.txt"
    output_file = get_unique_filename(base_output)


    # ==============================
    # WRITE REPORT
    # ==============================

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("DISCORD FILENAMES:\n")
        f.write("-" * 50 + "\n")
        for name in sorted(discord_filenames):
            f.write(name + "\n")

        f.write("\n\nMATCHED FILES:\n")
        f.write("-" * 50 + "\n")
        for name in sorted(matched):
            f.write(name + "\n")

        f.write("\n\nMISSING LOCALLY (on Discord only):\n")
        f.write("-" * 50 + "\n")
        for name in sorted(missing_locally):
            f.write(name + "\n")

        f.write("\n\nEXTRA LOCALLY (not on Discord):\n")
        f.write("-" * 50 + "\n")
        for name in sorted(extra_locally):
            f.write(name + "\n")


    print(f"\nReport written to: {output_file}")
if __name__ == "__main__":
    discord_filenames, missing_locally, extra_locally, matched = comparator(current_dir.parent / "0delete afater uplaod")
    log(discord_filenames, missing_locally, extra_locally, matched)

