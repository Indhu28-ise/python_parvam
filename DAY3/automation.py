# Automation code 
import time
import csv
import logging
import os
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# ---------------- CONFIGURATION ---------------- #

BASE_DIR = Path(__file__).resolve().parent

CONFIG = {
    "url": "https://example.com/login",
    "username": "testuser",
    "password": "testpass",
    "driver_path": BASE_DIR / "chromedriver.exe",
    "timeout": 10,
    "retry": 3,
    "screenshot_path": BASE_DIR / "screenshots",
    "log_file": BASE_DIR / "automation.log",
    "csv_file": BASE_DIR / "testdata.csv"
}

# ---------------- LOGGING SETUP ---------------- #

logging.basicConfig(
    filename=CONFIG["log_file"],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- UTILITY FUNCTIONS ---------------- #

def create_screenshot_folder():
    os.makedirs(CONFIG["screenshot_path"], exist_ok=True)

def take_screenshot(driver, name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = CONFIG["screenshot_path"] / f"{name}_{timestamp}.png"
    driver.save_screenshot(str(file_path))
    logging.info(f"Screenshot saved: {file_path}")

def read_csv_data(file):
    data = []
    try:
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        logging.info("CSV data loaded successfully")
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
    return data

def write_csv_result(file, data):
    keys = data[0].keys()
    with open(file, 'w', newline='') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# ---------------- DRIVER SETUP ---------------- #

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver_path = Path(CONFIG["driver_path"])

    if driver_path.exists():
        service = Service(str(driver_path))
        return webdriver.Chrome(service=service, options=chrome_options)

    logging.info("Local chromedriver.exe not found. Falling back to Selenium Manager.")
    return webdriver.Chrome(options=chrome_options)

# ---------------- CORE AUTOMATION CLASS ---------------- #

class AutomationBot:

    def __init__(self):
        self.driver = init_driver()
        self.wait = WebDriverWait(self.driver, CONFIG["timeout"])

    def open_site(self):
        logging.info("Opening website")
        self.driver.get(CONFIG["url"])

    def login(self):
        try:
            logging.info("Attempting login")

            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

            username_field.send_keys(CONFIG["username"])
            password_field.send_keys(CONFIG["password"])
            login_button.click()

            self.wait.until(
                EC.presence_of_element_located((By.ID, "dashboard"))
            )

            logging.info("Login successful")

        except Exception as e:
            logging.error(f"Login failed: {e}")
            take_screenshot(self.driver, "login_failed")
            raise

    def navigate_to_section(self):
        try:
            logging.info("Navigating to data section")

            menu = self.wait.until(
                EC.element_to_be_clickable((By.ID, "menu_data"))
            )
            menu.click()

            self.wait.until(
                EC.presence_of_element_located((By.ID, "data_table"))
            )

        except Exception as e:
            logging.error(f"Navigation failed: {e}")
            take_screenshot(self.driver, "navigation_error")
            raise

    def extract_table_data(self):
        data = []
        try:
            logging.info("Extracting table data")

            rows = self.driver.find_elements(By.XPATH, "//table/tbody/tr")

            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                record = {
                    "name": cols[0].text,
                    "email": cols[1].text,
                    "status": cols[2].text
                }
                data.append(record)

        except Exception as e:
            logging.error(f"Data extraction failed: {e}")
            take_screenshot(self.driver, "data_error")

        return data

    def validate_data(self, extracted, expected):
        results = []

        for exp in expected:
            match = next((item for item in extracted if item["email"] == exp["email"]), None)

            if match:
                result = "PASS" if match["status"] == exp["status"] else "FAIL"
            else:
                result = "NOT FOUND"

            exp["result"] = result
            results.append(exp)

        return results

    def logout(self):
        try:
            logging.info("Logging out")

            logout_btn = self.wait.until(
                EC.element_to_be_clickable((By.ID, "logout"))
            )
            logout_btn.click()

        except Exception as e:
            logging.error(f"Logout failed: {e}")

    def close(self):
        self.driver.quit()

# ---------------- RETRY MECHANISM ---------------- #

def retry_operation(func):
    def wrapper(*args, **kwargs):
        for attempt in range(CONFIG["retry"]):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Retry {attempt + 1} failed: {e}")
                time.sleep(2)
        raise Exception("Max retries reached")
    return wrapper

# ---------------- MAIN EXECUTION ---------------- #

@retry_operation
def run_automation():
    create_screenshot_folder()

    bot = AutomationBot()

    try:
        bot.open_site()
        bot.login()
        bot.navigate_to_section()

        extracted_data = bot.extract_table_data()
        expected_data = read_csv_data(CONFIG["csv_file"])

        results = bot.validate_data(extracted_data, expected_data)

        write_csv_result(BASE_DIR / "results.csv", results)

        logging.info("Automation completed successfully")

    except Exception as e:
        logging.error(f"Automation failed: {e}")

    finally:
        bot.logout()
        bot.close()

# ---------------- ENTRY POINT ---------------- #

if __name__ == "__main__":
    run_automation()
# debug.log should NOT appear in the output!
    
w