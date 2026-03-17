from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Headless Chrome Setup
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 15)
bugs = []
passed = []

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def bug(name, condition, description, severity):
    if condition:
        print(f"BUG [{severity}]: {name} - {description}")
        driver.save_screenshot(f"screenshots/{name}.png")
        bugs.append(name)
    else:
        print(f"OK: {name}")
        passed.append(name)

def open_page(url):
    driver.get(url)
    time.sleep(4)

def clear_type(xpath, text):
    try:
        f = wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)))
        f.clear()
        f.send_keys(text)
    except:
        pass

def click_submit():
    try:
        b = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))
        b.click()
        time.sleep(3)
    except:
        pass

def has_error():
    try:
        e = driver.find_elements(By.XPATH,
            "//*[contains(@class,'error') or "
            "contains(text(),'invalid') or "
            "contains(text(),'required')]")
        return len(e) > 0
    except:
        return False

print("="*50)
print("KRIDA CI/CD Automated Tests Starting...")
print("="*50)

# BUG01
open_page("https://krida-snowy.vercel.app/signup")
clear_type("//input[@type='email']", "notanemail")
click_submit()
bug("BUG01_Invalid_Email", not has_error(),
    "Invalid email accepted", "HIGH")

# BUG02
open_page("https://krida-snowy.vercel.app/signup")
inputs = driver.find_elements(
    By.XPATH, "//input[@type='text']")
if inputs:
    inputs[0].send_keys("Test")
clear_type("//input[@type='email']", "test@test.com")
clear_type("//input[@type='password']", "1")
click_submit()
bug("BUG02_Weak_Password", not has_error(),
    "Weak password accepted", "CRITICAL")

# BUG03
open_page("https://krida-snowy.vercel.app/signup")
clear_type("//input[@type='email']", "' OR '1'='1'")
clear_type("//input[@type='password']", "Test@1234")
click_submit()
bug("BUG03_SQL_Injection", not has_error(),
    "SQL injection accepted", "CRITICAL")

# BUG04
open_page("https://krida-snowy.vercel.app/randompage999")
bug("BUG04_No_404",
    "404" not in driver.page_source.lower(),
    "No 404 page", "LOW")

driver.quit()

total = len(bugs) + len(passed)
score = round((len(passed)/total)*100) if total > 0 else 0

print("="*50)
print(f"BUGS FOUND : {len(bugs)}")
print(f"PASSED     : {len(passed)}")
print(f"TOTAL      : {total}")
print(f"SCORE      : {score}%")
print("="*50)

if bugs:
    print("BUGS LIST:")
    for b in bugs:
        print(f"  - {b}")
    exit(1)
else:
    print("No bugs found!")
    exit(0)
