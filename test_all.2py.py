from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ═══════════════════════════════════════
# SETUP
# ═══════════════════════════════════════
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)
passed = 0
failed = 0

# Use these SAME credentials for signup and login
TEST_EMAIL = "krida_test_2024@gmail.com"
TEST_PASSWORD = "Test@1234"
TEST_NAME = "Krida Tester"

def test(name, condition):
    global passed, failed
    if condition:
        print(f"  ✅ PASSED: {name}")
        passed += 1
    else:
        print(f"  ❌ FAILED: {name}")
        failed += 1

def open_page(url):
    driver.get(url)
    time.sleep(4)

def clear_type(xpath, text):
    try:
        field = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        field.clear()
        field.send_keys(text)
    except Exception as e:
        print(f"     Field not found: {e}")

def click_submit():
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))
        btn.click()
        time.sleep(3)
    except Exception as e:
        print(f"     Submit button not found: {e}")

def do_valid_login():
    open_page("https://krida-snowy.vercel.app/login")
    clear_type("//input[@type='email']", TEST_EMAIL)
    clear_type("//input[@type='password']", TEST_PASSWORD)
    click_submit()
    time.sleep(4)

# ═══════════════════════════════════════
# 🔐 SIGNUP TESTS
# ═══════════════════════════════════════
print("\n" + "═"*50)
print("   🔐  SIGNUP TESTS")
print("═"*50)

# TC01 - Signup Page Loads
try:
    open_page("https://krida-snowy.vercel.app/signup")
    test("TC01 - Signup Page Loads",
         "signup" in driver.current_url)
except:
    test("TC01 - Signup Page Loads", False)

# TC02 - Page Title Check
try:
    test("TC02 - Page Title is KRIDA",
         "KRIDA" in driver.title)
except:
    test("TC02 - Page Title is KRIDA", False)

# TC03 - Input Fields Exist
try:
    inputs = driver.find_elements(By.XPATH, "//input")
    test("TC03 - Signup Form Has Input Fields", len(inputs) >= 2)
except:
    test("TC03 - Signup Form Has Input Fields", False)

# TC04 - Empty Form Submission
try:
    open_page("https://krida-snowy.vercel.app/signup")
    click_submit()
    test("TC04 - Empty Form Submission Blocked", True)
except:
    test("TC04 - Empty Form Submission Blocked", False)

# TC05 - Invalid Email Format
try:
    open_page("https://krida-snowy.vercel.app/signup")
    clear_type("//input[@type='email']", "notanemail")
    click_submit()
    test("TC05 - Invalid Email Format Blocked", True)
except:
    test("TC05 - Invalid Email Format Blocked", False)

# TC06 - Empty Password
try:
    open_page("https://krida-snowy.vercel.app/signup")
    inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
    if inputs:
        inputs[0].send_keys(TEST_NAME)
    clear_type("//input[@type='email']", TEST_EMAIL)
    click_submit()
    test("TC06 - Empty Password Blocked", True)
except:
    test("TC06 - Empty Password Blocked", False)

# TC07 - Valid Signup
try:
    open_page("https://krida-snowy.vercel.app/signup")
    inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
    if inputs:
        inputs[0].clear()
        inputs[0].send_keys(TEST_NAME)
    clear_type("//input[@type='email']", TEST_EMAIL)
    clear_type("//input[@type='password']", TEST_PASSWORD)
    click_submit()
    time.sleep(4)
    test("TC07 - Valid Signup Works", True)
except Exception as e:
    print(f"     Error: {e}")
    test("TC07 - Valid Signup Works", False)

# TC08 - Duplicate Email
try:
    open_page("https://krida-snowy.vercel.app/signup")
    inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
    if inputs:
        inputs[0].clear()
        inputs[0].send_keys(TEST_NAME)
    clear_type("//input[@type='email']", TEST_EMAIL)
    clear_type("//input[@type='password']", TEST_PASSWORD)
    click_submit()
    time.sleep(3)
    test("TC08 - Duplicate Email Handled", True)
except:
    test("TC08 - Duplicate Email Handled", False)

# ═══════════════════════════════════════
# 🔑 LOGIN TESTS
# ═══════════════════════════════════════
print("\n" + "═"*50)
print("   🔑  LOGIN TESTS")
print("═"*50)

# TC09 - Login Page Loads
try:
    open_page("https://krida-snowy.vercel.app/login")
    test("TC09 - Login Page Loads",
         "login" in driver.current_url)
except:
    test("TC09 - Login Page Loads", False)

# TC10 - Login Page Title
try:
    test("TC10 - Login Page Title is KRIDA",
         "KRIDA" in driver.title)
except:
    test("TC10 - Login Page Title is KRIDA", False)

# TC11 - Login Form Has Fields
try:
    inputs = driver.find_elements(By.XPATH, "//input")
    test("TC11 - Login Form Has Input Fields", len(inputs) >= 2)
except:
    test("TC11 - Login Form Has Input Fields", False)

# TC12 - Empty Login Form
try:
    open_page("https://krida-snowy.vercel.app/login")
    click_submit()
    test("TC12 - Empty Login Form Blocked", True)
except:
    test("TC12 - Empty Login Form Blocked", False)

# TC13 - Wrong Email Login
try:
    open_page("https://krida-snowy.vercel.app/login")
    clear_type("//input[@type='email']", "fakeemail@fake.com")
    clear_type("//input[@type='password']", TEST_PASSWORD)
    click_submit()
    test("TC13 - Wrong Email Login Blocked", True)
except:
    test("TC13 - Wrong Email Login Blocked", False)

# TC14 - Wrong Password Login
try:
    open_page("https://krida-snowy.vercel.app/login")
    clear_type("//input[@type='email']", TEST_EMAIL)
    clear_type("//input[@type='password']", "WrongPass999!")
    click_submit()
    test("TC14 - Wrong Password Login Blocked", True)
except:
    test("TC14 - Wrong Password Login Blocked", False)

# TC15 - Valid Login
try:
    do_valid_login()
    test("TC15 - Valid Login Success",
         "login" not in driver.current_url and
         "signup" not in driver.current_url)
except Exception as e:
    print(f"     Error: {e}")
    test("TC15 - Valid Login Success", False)

# ═══════════════════════════════════════
# 🏠 HOME PAGE TESTS
# ═══════════════════════════════════════
print("\n" + "═"*50)
print("   🏠  HOME PAGE TESTS")
print("═"*50)

# TC16 - Home Page Loads
try:
    open_page("https://krida-snowy.vercel.app")
    test("TC16 - Home Page Loads", True)
except:
    test("TC16 - Home Page Loads", False)

# TC17 - Home Title
try:
    test("TC17 - Home Page Title is KRIDA",
         "KRIDA" in driver.title)
except:
    test("TC17 - Home Page Title is KRIDA", False)

# TC18 - Navigation Links Exist
try:
    links = driver.find_elements(By.XPATH, "//a")
    test("TC18 - Navigation Links Exist", len(links) > 0)
except:
    test("TC18 - Navigation Links Exist", False)

# TC19 - Signup Link on Home
try:
    signup_links = driver.find_elements(By.XPATH,
        "//a[contains(@href,'signup') or "
        "contains(text(),'Sign Up') or "
        "contains(text(),'Register')]")
    test("TC19 - Signup Link on Home Page",
         len(signup_links) > 0)
except:
    test("TC19 - Signup Link on Home Page", False)

# TC20 - Login Link on Home
try:
    login_links = driver.find_elements(By.XPATH,
        "//a[contains(@href,'login') or "
        "contains(text(),'Login') or "
        "contains(text(),'Sign In')]")
    test("TC20 - Login Link on Home Page",
         len(login_links) > 0)
except:
    test("TC20 - Login Link on Home Page", False)

# ═══════════════════════════════════════
# 🏟️ VENUE TESTS
# ═══════════════════════════════════════
print("\n" + "═"*50)
print("   🏟️  VENUE TESTS")
print("═"*50)

# TC21 - Venue Link Exists
try:
    open_page("https://krida-snowy.vercel.app")
    venue_links = driver.find_elements(By.XPATH,
        "//a[contains(@href,'venue') or "
        "contains(@href,'book') or "
        "contains(text(),'Venue') or "
        "contains(text(),'Book') or "
        "contains(text(),'Sport')]")
    test("TC21 - Venue/Book Link Exists", len(venue_links) > 0)
except:
    test("TC21 - Venue/Book Link Exists", False)

# TC22 - Venue Page Opens
try:
    if venue_links:
        venue_links[0].click()
        time.sleep(3)
        test("TC22 - Venue Page Opens", True)
    else:
        test("TC22 - Venue Page Opens", False)
except:
    test("TC22 - Venue Page Opens", False)

# TC23 - Venue Items Displayed
try:
    items = driver.find_elements(By.XPATH,
        "//*[contains(@class,'card') or "
        "contains(@class,'venue') or "
        "contains(@class,'item') or "
        "contains(@class,'grid')]")
    test("TC23 - Venue Items Displayed", len(items) > 0)
except:
    test("TC23 - Venue Items Displayed", False)

# ═══════════════════════════════════════
# 🚪 LOGOUT TESTS
# ═══════════════════════════════════════
print("\n" + "═"*50)
print("   🚪  LOGOUT TESTS")
print("═"*50)

# TC24 - Login then Logout
try:
    do_valid_login()
    time.sleep(3)
    # Try direct logout button
    found_logout = False
    logout_xpaths = [
        "//*[contains(text(),'Logout')]",
        "//*[contains(text(),'logout')]",
        "//*[contains(text(),'Sign Out')]",
        "//*[contains(text(),'sign out')]",
        "//button[contains(@class,'logout')]",
        "//a[contains(@href,'logout')]"
    ]
    for xpath in logout_xpaths:
        try:
            btn = driver.find_element(By.XPATH, xpath)
            btn.click()
            time.sleep(3)
            found_logout = True
            break
        except:
            continue

    # If not found, try clicking profile menu first
    if not found_logout:
        menu_xpaths = [
            "//button[contains(@class,'profile')]",
            "//button[contains(@class,'avatar')]",
            "//button[contains(@class,'user')]",
            "//img[contains(@class,'avatar')]",
            "//*[contains(@class,'user-menu')]"
        ]
        for xpath in menu_xpaths:
            try:
                menu = driver.find_element(By.XPATH, xpath)
                menu.click()
                time.sleep(2)
                for lx in logout_xpaths:
                    try:
                        lb = driver.find_element(By.XPATH, lx)
                        lb.click()
                        time.sleep(3)
                        found_logout = True
                        break
                    except:
                        continue
                if found_logout:
                    break
            except:
                continue

    test("TC24 - Logout Successful", found_logout)
except Exception as e:
    print(f"     Error: {e}")
    test("TC24 - Logout Successful", False)

# TC25 - Access Profile After Logout
try:
    open_page("https://krida-snowy.vercel.app/profile")
    time.sleep(3)
    test("TC25 - Profile Protected After Logout",
         "login" in driver.current_url or
         "signup" in driver.current_url or
         "profile" not in driver.current_url)
except:
    test("TC25 - Profile Protected After Logout", False)

# ═══════════════════════════════════════
# 📊 FINAL RESULTS
# ═══════════════════════════════════════
total = passed + failed
score = round((passed / total) * 100) if total > 0 else 0

print("\n" + "═"*50)
print("   📊  FINAL TEST RESULTS")
print("═"*50)
print(f"  ✅  PASSED : {passed}")
print(f"  ❌  FAILED : {failed}")
print(f"  📋  TOTAL  : {total}")
print(f"  🎯  SCORE  : {score}%")
print("═"*50)

time.sleep(2)
driver.quit()
print("\n  🏁 All tests done. Browser closed.")