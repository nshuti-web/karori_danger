from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import sys
import shutil

# --- User configuration ---
PHONE_NUMBER = "0795507394"
PIN = "6664"
LOGIN_URL = "https://www.betpawa.rw/login"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # If you have a custom Chrome binary path, set it here:
    # chrome_options.binary_location = "/usr/bin/google-chrome"

    # Try to auto-detect chromedriver path (GitHub Actions installs it in /usr/bin)
    chromedriver_path = shutil.which("chromedriver")
    service = Service(executable_path=chromedriver_path) if chromedriver_path else None

    try:
        print("Starting Chrome WebDriver in headless mode...")
        driver = webdriver.Chrome(options=chrome_options, service=service)
    except WebDriverException as e:
        print(f"Error starting WebDriver: {e}")
        sys.exit(1)

    try:
        print(f"Navigating to login page: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        time.sleep(2)  # Wait for page to load

        print("Locating phone number input field...")
        phone_input = driver.find_element(By.ID, "login-form-phoneNumber")
        phone_input.clear()
        phone_input.send_keys(PHONE_NUMBER)
        print("Phone number entered.")

        print("Locating PIN input field...")
        pin_input = driver.find_element(By.ID, "login-form-password-input")
        pin_input.clear()
        pin_input.send_keys(PIN)
        print("PIN entered.")

        print("Locating login button...")
        login_button = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='logInButton']")
        login_button.click()
        print("Login button clicked.")

        print("Waiting for login to complete...")
        time.sleep(3)

        print("Looking for the 'Aviator' tab...")
        for _ in range(20):
            try:
                aviator_tab = driver.find_element(
                    By.XPATH,
                    "//li[contains(@class, 'tabs-selector')]//span[contains(@class, 'tab-text') and normalize-space(text())='Aviator']"
                )
                aviator_tab.click()
                print("'Aviator' tab clicked.")
                break
            except NoSuchElementException:
                time.sleep(0.5)
        else:
            print("'Aviator' tab not found.")
            driver.quit()
            sys.exit(1)

        print("Patiently waiting for claim buttons to appear (this may take a while)...")
        checks_per_second = 3
        interval = 1.0 / checks_per_second

        while True:
            claim_buttons = driver.find_elements(
                By.XPATH,
                "//button[contains(@class, 'btn-claim') and normalize-space(text())='Claim']"
            )
            if len(claim_buttons) >= 1:
                print(f"Found {len(claim_buttons)} claim button(s). Clicking all...")
                for btn in claim_buttons:
                    try:
                        btn.click()
                    except Exception as e:
                        print(f"Error clicking button: {e}")
                print("All visible claim buttons clicked. Waiting for new ones...")
            time.sleep(interval)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    main()
