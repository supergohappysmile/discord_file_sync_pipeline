import os
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============================
# CONFIGURATION
# ============================

CHANNEL_URL = "https://discord.com/channels/GUILD_ID/CHANNEL_ID"
DOWNLOAD_DIR = r"C:\discord_downloads"   # Change this

SCROLL_PAUSE = 1.5
WAIT_TIMEOUT = 30

# ============================
# SETUP
# ============================

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(CHANNEL_URL)

input("Log into Discord manually, then press ENTER...")

wait = WebDriverWait(driver, WAIT_TIMEOUT)

# Wait for chat container
wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '[data-list-id="chat-messages"]')
))

message_container = driver.find_element(By.CSS_SELECTOR, '[data-list-id="chat-messages"]')

# ============================
# SCROLL + COLLECT ATTACHMENTS
# ============================

print("Scrolling and collecting attachment URLs...")

attachment_urls = set()
last_height = 0

while True:
    # Find all attachment links
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="cdn.discordapp.com"]')

    for link in links:
        href = link.get_attribute("href")
        if href:
            attachment_urls.add(href.split("?")[0])

    # Scroll upward incrementally
    driver.execute_script("""
        const container = arguments[0];
        container.scrollBy(0, -1500);
    """, message_container)

    time.sleep(SCROLL_PAUSE)

    new_height = driver.execute_script(
        "return arguments[0].scrollHeight",
        message_container
    )

    if new_height == last_height:
        break

    last_height = new_height

print(f"Collected {len(attachment_urls)} attachment URLs.")

# ============================
# DOWNLOAD FILES
# ============================

print("Downloading files...")

session = requests.Session()

# Transfer cookies from Selenium to requests
for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])

for url in attachment_urls:
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(filepath):
        print(f"Skipping existing file: {filename}")
        continue

    try:
        response = session.get(url, stream=True)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Failed to download {filename}: {e}")

driver.quit()

print("Done.")