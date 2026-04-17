from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Open browser
driver = webdriver.Chrome()

# Open website
driver.get("https://scholar.parvam.in/student/login")

driver.maximize_window()

# Wait setup
wait = WebDriverWait(driver, 10)

# Take input from user
email_input = input("Enter your email: ")
password_input = input("Enter your password: ")

try:
    # ✅ Email field (better XPath)
    email = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='email']")
    ))
    email.send_keys(email_input)

    # ✅ Password field
    password = driver.find_element(By.XPATH, "//input[@type='password']")
    password.send_keys(password_input)

    # ✅ Login button
    login_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Sign')]")
    login_btn.click()

    print("Login attempted...")

except Exception as e:
    print("Error:", e)

input("Press Enter to close...")
driver.quit()
