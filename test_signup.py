from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)

try:
    # TEST 1: Open signup page
    driver.get("https://krida-snowy.vercel.app/signup")
    time.sleep(3)
    print("✅ TEST 1 PASSED: Page opened")

    # TEST 2: Check title
    assert "KRIDA" in driver.title
    print("✅ TEST 2 PASSED: Title is correct")

    # TEST 3: Fill Name
    name_field = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='text']")))
    name_field.send_keys("Test User")
    print("✅ TEST 3 PASSED: Name entered")

    # TEST 4: Fill Email
    email_field = driver.find_element(By.XPATH, "//input[@type='email']")
    email_field.send_keys("testuser@example.com")
    print("✅ TEST 4 PASSED: Email entered")

    # TEST 5: Fill Password
    password_field = driver.find_element(By.XPATH, "//input[@type='password']")
    password_field.send_keys("Test@1234")
    print("✅ TEST 5 PASSED: Password entered")

    # TEST 6: Click Signup button
    signup_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    signup_btn.click()
    print("✅ TEST 6 PASSED: Signup button clicked")

    time.sleep(3)
    print("✅ ALL TESTS PASSED!")

except Exception as e:
    print(f"❌ TEST FAILED: {e}")

finally:
    time.sleep(2)
    driver.quit()
    print("🏁 Browser closed.")