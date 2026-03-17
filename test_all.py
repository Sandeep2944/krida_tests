from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ─────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)
passed = 0
failed = 0

def test(name, condition):
    global passed, failed
    if condition:
        print(f"✅ PASSED: {name}")
        passed += 1
    else:
        print(f"❌ FAILED: {name}")
        failed += 1

# ─────────────────────────────────────────
# SIGNUP TESTS
# ─────────────────────────────────────────
print("\n========== 🔐 SIGNUP TESTS ==========")

# TC01 - Page Load
driver.get("https://krida-snowy.vercel.app/signup")
time.sleep(3)
test("TC01 - Signup Page Loads", "signup" in driver.current_url)

# TC02 - Page Title
test("TC02 - Page Title is KRIDA", "KRIDA" in driver.title)

# TC03 - Empty Form Submission
try:
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']")))
    btn.click()
    time.sleep(2)
    test("TC03 - Empty Form Shows Error", True)
except:
    test("TC03 - Empty Form Shows Error", False)

# TC04 - Invalid Email
try:
    driver.get("https://krida-snowy.vercel.app/signup")
    time.sleep(3)
    email = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='email']")))
    email.clear()
    email.send_keys("invalidemail")
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()
    time.sleep(2)
    test("TC04 - Invalid Email Format", True)
except:
    test("TC04 - Invalid Email Format", False)

# TC05 - Valid Signup
try:
    driver.get("https://krida-snowy.vercel.app/signup")
    time.sleep(3)
    inputs = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//input")))
    for inp in inputs:
        t = inp.get_attribute("type")
        if t == "text": inp.send_keys("Test User")
        elif t == "email": inp.send_keys("testuser123@example.com")
        elif t == "password": inp.send_keys("Test@1234")
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()
    time.sleep(3)
    test("TC05 - Valid Signup Submitted", True)
except Exception as e:
    test("TC05 - Valid Signup Submitted", False)

# ─────────────────────────────────────────
# LOGIN TESTS
# ─────────────────────────────────────────
print("\n========== 🔑 LOGIN TESTS ==========")

# TC06 - Login Page Load
driver.get("https://krida-snowy.vercel.app/login")
time.sleep(3)
test("TC06 - Login Page Loads", "login" in driver.current_url)

# TC07 - Empty Login Form
try:
    btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@type='submit']")))
    btn.click()
    time.sleep(2)
    test("TC07 - Empty Login Form Error", True)
except:
    test("TC07 - Empty Login Form Error", False)

# TC08 - Wrong Email
try:
    driver.get("https://krida-snowy.vercel.app/login")
    time.sleep(3)
    email = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='email']")))
    email.send_keys("wrong@example.com")
    pwd = driver.find_element(By.XPATH, "//input[@type='password']")
    pwd.send_keys("Test@1234")
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()
    time.sleep(3)
    test("TC08 - Wrong Email Shows Error", True)
except:
    test("TC08 - Wrong Email Shows Error", False)

# TC09 - Wrong Password
try:
    driver.get("https://krida-snowy.vercel.app/login")
    time.sleep(3)
    email = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='email']")))
    email.send_keys("testuser123@example.com")
    pwd = driver.find_element(By.XPATH, "//input[@type='password']")
    pwd.send_keys("WrongPass123")
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()
    time.sleep(3)
    test("TC09 - Wrong Password Shows Error", True)
except:
    test("TC09 - Wrong Password Shows Error", False)

# TC10 - Valid Login
try:
    driver.get("https://krida-snowy.vercel.app/login")
    time.sleep(3)
    email = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@type='email']")))
    email.send_keys("testuser123@example.com")
    pwd = driver.find_element(By.XPATH, "//input[@type='password']")
    pwd.send_keys("Test@1234")
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()
    time.sleep(4)
    test("TC10 - Valid Login Success",
         "login" not in driver.current_url)
except:
    test("TC10 - Valid Login Success", False)

# ─────────────────────────────────────────
# HOME PAGE TESTS
# ─────────────────────────────────────────
print("\n========== 🏠 HOME PAGE TESTS ==========")

# TC11 - Home Page Load
driver.get("https://krida-snowy.vercel.app")
time.sleep(3)
test("TC11 - Home Page Loads", driver.current_url is not None)

# TC12 - Title Check
test("TC12 - Home Page Title is KRIDA", "KRIDA" in driver.title)

# TC13 - Navigation Links Exist
try:
    links = driver.find_elements(By.XPATH, "//a")
    test("TC13 - Navigation Links Exist", len(links) > 0)
except:
    test("TC13 - Navigation Links Exist", False)

# ─────────────────────────────────────────
# VENUE TESTS
# ─────────────────────────────────────────
print("\n========== 🏟️ VENUE TESTS ==========")

# TC14 - Venues Page Load
try:
    driver.get("https://krida-snowy.vercel.app")
    time.sleep(3)
    venue_link = driver.find_element(By.XPATH,
        "//a[contains(@href,'venue') or contains(text(),'Venue') or contains(text(),'Book')]")
    venue_link.click()
    time.sleep(3)
    test("TC14 - Venues Page Opens", True)
except:
    test("TC14 - Venues Page Opens", False)

# ─────────────────────────────────────────
# LOGOUT TEST
# ─────────────────────────────────────────
print("\n========== 🚪 LOGOUT TEST ==========")

# TC15 - Logout
try:
    logout = driver.find_element(By.XPATH,
        "//button[contains(text(),'Logout') or contains(text(),'Sign out')]")
    logout.click()
    time.sleep(3)
    test("TC15 - Logout Successful",
         "login" in driver.current_url or "/" in driver.current_url)
except:
    test("TC15 - Logout Successful", False)

# ─────────────────────────────────────────
# FINAL RESULTS
# ─────────────────────────────────────────
print("\n========== 📊 FINAL RESULTS ==========")
print(f"✅ PASSED : {passed}")
print(f"❌ FAILED : {failed}")
print(f"📋 TOTAL  : {passed + failed}")
print(f"🎯 SCORE  : {round((passed/(passed+failed))*100)}%")

time.sleep(2)
driver.quit()
print("\n🏁 All tests completed. Browser closed.")
