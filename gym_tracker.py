# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from datetime import datetime
# import pandas as pd
# import time
# import os
# import re
# import schedule

# # Set this to your actual ChromeDriver path
# CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"

# def fetch_occupancy():
#     print(f"\nRunning fetch at {datetime.now()}")

#     service = Service(CHROMEDRIVER_PATH)
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Optional: don't open a browser window
#     driver = webdriver.Chrome(service=service, options=options)

#     try:
#         driver.get("https://recreation.ucsd.edu/facilities/")
#         time.sleep(5)  # wait for JavaScript to load content

#         blocks = driver.find_elements(By.CSS_SELECTOR, "div.custom-html-widget div[style*='border']")
#         print(f"Found {len(blocks)} gym blocks")

#         data = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#         for block in blocks:
#             text = block.text.strip()
#             print("Block text:", text)

#             for gym in ["RIMAC Fitness Gym", "Main Gym Fitness Gym"]:
#                 if gym in text:
#                     match = re.search(r"(\d+)%\s+full", text)
#                     if match:
#                         data[gym] = int(match.group(1))

#         for gym in ["RIMAC Fitness Gym", "Main Gym Fitness Gym"]:
#             data.setdefault(gym, None)

#         print("Occupancy data:", data)

#         df = pd.DataFrame([data])
#         file_exists = os.path.exists("gym_occupancy_log.csv")
#         df.to_csv("gym_occupancy_log.csv", mode='a', header=not file_exists, index=False)

#     finally:
#         driver.quit()

# # Schedule every 30 minutes
# schedule.every(30).minutes.do(fetch_occupancy)

# print("Starting occupancy tracker...")
# fetch_occupancy()  # Run once at start

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# gym_tracker.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd
import time
import os
import re

CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"

def fetch_occupancy():
    print(f"\nRunning fetch at {datetime.now()}")

    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # run without opening browser
    driver = webdriver.Chrome(service=service, options=options)

    try:
        try:
            driver.set_page_load_timeout(20)  # Set timeout
            driver.get("https://recreation.ucsd.edu/facilities/")
        except Exception as e:
            print("Error loading page:", e)
            driver.quit()
            return
        time.sleep(5)

        blocks = driver.find_elements(By.CSS_SELECTOR, "div.custom-html-widget div[style*='border']")
        data = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        for block in blocks:
            text = block.text.strip()
            for gym in ["RIMAC Fitness Gym", "Main Gym Fitness Gym"]:
                if gym in text:
                    match = re.search(r"(\d+)%\s+full", text)
                    if match:
                        data[gym] = int(match.group(1))

        for gym in ["RIMAC Fitness Gym", "Main Gym Fitness Gym"]:
            data.setdefault(gym, None)

        df = pd.DataFrame([data])
        file_exists = os.path.exists("gym_occupancy_log.csv")
        log_path = "/Users/judemariadas/Documents/UCSD/gym_occupancy_log.csv"
        file_exists = os.path.isfile(log_path) and os.path.getsize(log_path) > 0
        df.to_csv(log_path, mode='a', header=not file_exists, index=False)

    finally:
        driver.quit()

fetch_occupancy()