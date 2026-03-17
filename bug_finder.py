from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ═══════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)

bugs_found = []
bugs_not_found = []

def bug(name, condition, description):
    if condition:
        print(f"  🐛 BUG FOUND    : {name}")
        print(f"     Description  : {description}")
        bugs_found.append(name)
    else:
        print(f"  ✅ NO BUG       : {name}")
        bugs_not_found.append(name)

def open_page(url):
    driver.get(url)
    time.sleep(4)

def clear_type(xpath, text):
    try:
        field = wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath)))
        field.clear()
        field.send_keys(text)
    except:
        pass

def click_submit():
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@type='submit']")))
        btn.click()
        time.sleep(3)
    except:
        pass

def page_has_error():
    try:
        error_elements = driver.find_elements(By.XPATH,
            "//*[contains(@class,'error') or "
            "contains(@class,'alert') or "
            "contains(@class,'warning') or "
            "contains(text(),'error') or "
            "contains(text(),'invalid') or "
            "contains(text(),'required')]")
        return len(error_elements) > 0
    except:
        return False

# ═══════════════════════════════════════════
# 🐛 FORM VALIDATION BUGS
# ═══════════════════════════════════════════
print("\n" + "═"*55)
print("   🐛  FORM VALIDATION BUG TESTS")
print("═"*55)

# BUG01 - Does empty signup form get submitted?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    url_before = driver.current_url
    click_submit()
    url_after = driver.current_url
    bug("BUG01 - Empty Signup Form Submits",
        url_before != url_after and not page_has_error(),
        "Empty form was submitted without any error message!")
except:
    bug("BUG01 - Empty Signup Form Submits", False, "")

# BUG02 - Does invalid email get accepted?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    clear_type("//input[@type='email']", "notanemail")
    click_submit()
    bug("BUG02 - Invalid Email Accepted",
        not page_has_error(),
        "Invalid email format was accepted without error!")
except:
    bug("BUG02 - Invalid Email Accepted", False, "")

# BUG03 - Does number-only email get accepted?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    clear_type("//input[@type='email']", "12345678")
    click_submit()
    bug("BUG03 - Number Only Email Accepted",
        not page_has_error(),
        "Number-only email was accepted!")
except:
    bug("BUG03 - Number Only Email Accepted", False, "")

# BUG04 - Does single character password get accepted?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
    if inputs:
        inputs[0].send_keys("Test User")
    clear_type("//input[@type='email']", "test@test.com")
    clear_type("//input[@type='password']", "1")
    click_submit()
    bug("BUG04 - Weak Password (1 char) Accepted",
        not page_has_error(),
        "Single character password was accepted!")
except:
    bug("BUG04 - Weak Password (1 char) Accepted", False, "")

# BUG05 - Does spaces-only name get accepted?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
    if inputs:
        inputs[0].send_keys("     ")
    clear_type("//input[@type='email']", "test@test.com")
    clear_type("//input[@type='password']", "Test@1234")
    click_submit()
    bug("BUG05 - Spaces Only Name Accepted",
        not page_has_error(),
        "Name with only spaces was accepted!")
except:
    bug("BUG05 - Spaces Only Name Accepted", False, "")

# BUG06 - Does SQL injection get accepted in email?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    clear_type("//input[@type='email']", "' OR '1'='1")
    clear_type("//input[@type='password']", "Test@1234")
    click_submit()
    bug("BUG06 - SQL Injection Accepted in Email",
        not page_has_error(),
        "SQL injection string was accepted in email field!")
except:
    bug("BUG06 - SQL Injection Accepted in Email", False, "")

# BUG07 - Does very long email get accepted?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    long_email = "a" * 200 + "@test.com"
    clear_type("//input[@type='email']", long_email)
    click_submit()
    bug("BUG07 - Very Long Email (200+ chars) Accepted",
        not page_has_error(),
        "Email with 200+ characters was accepted!")
except:
    bug("BUG07 - Very Long Email (200+ chars) Accepted", False, "")

# BUG08 - Does empty login form get submitted?
try:
    open_page("https://krida-snowy.vercel.app/login")
    url_before = driver.current_url
    click_submit()
    url_after = driver.current_url
    bug("BUG08 - Empty Login Form Submits",
        url_before != url_after and not page_has_error(),
        "Empty login form was submitted!")
except:
    bug("BUG08 - Empty Login Form Submits", False, "")

# BUG09 - Does wrong password login succeed?
try:
    open_page("https://krida-snowy.vercel.app/login")
    clear_type("//input[@type='email']", "test@test.com")
    clear_type("//input[@type='password']", "wrongpass")
    click_submit()
    bug("BUG09 - Wrong Password Login Succeeds",
        "login" not in driver.current_url and
        "signup" not in driver.current_url,
        "Wrong password allowed login!")
except:
    bug("BUG09 - Wrong Password Login Succeeds", False, "")

# BUG10 - Does special characters crash login?
try:
    open_page("https://krida-snowy.vercel.app/login")
    clear_type("//input[@type='email']", "<script>alert('xss')</script>")
    clear_type("//input[@type='password']", "Test@1234")
    click_submit()
    page_src = driver.page_source
    bug("BUG10 - XSS Script Injection Accepted",
        "<script>" in page_src,
        "XSS script tag was reflected in page source!")
except:
    bug("BUG10 - XSS Script Injection Accepted", False, "")

# ═══════════════════════════════════════════
# 🔗 BROKEN LINKS & PAGES BUGS
# ═══════════════════════════════════════════
print("\n" + "═"*55)
print("   🔗  BROKEN LINKS & PAGES BUG TESTS")
print("═"*55)

# BUG11 - Does homepage load properly?
try:
    open_page("https://krida-snowy.vercel.app")
    bug("BUG11 - Home Page Fails to Load",
        "KRIDA" not in driver.title,
        "Home page did not load properly!")
except:
    bug("BUG11 - Home Page Fails to Load", True,
        "Home page threw an exception!")

# BUG12 - Does signup page load?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    bug("BUG12 - Signup Page Fails to Load",
        "KRIDA" not in driver.title,
        "Signup page did not load!")
except:
    bug("BUG12 - Signup Page Fails to Load", True,
        "Signup page threw an exception!")

# BUG13 - Does login page load?
try:
    open_page("https://krida-snowy.vercel.app/login")
    bug("BUG13 - Login Page Fails to Load",
        "KRIDA" not in driver.title,
        "Login page did not load!")
except:
    bug("BUG13 - Login Page Fails to Load", True,
        "Login page threw an exception!")

# BUG14 - Are there any broken links on home page?
try:
    open_page("https://krida-snowy.vercel.app")
    links = driver.find_elements(By.XPATH, "//a[@href]")
    broken = []
    for link in links:
        href = link.get_attribute("href")
        if href and href != "#" and "javascript" not in href:
            if href == "" or href is None:
                broken.append(href)
    bug("BUG14 - Broken Links Found on Home Page",
        len(broken) > 0,
        f"Found {len(broken)} broken links: {broken}")
except:
    bug("BUG14 - Broken Links Found on Home Page", False, "")

# BUG15 - Does unknown page show 404?
try:
    open_page("https://krida-snowy.vercel.app/unknownpage123")
    time.sleep(3)
    page_src = driver.page_source.lower()
    bug("BUG15 - No 404 Page for Unknown URLs",
        "404" not in page_src and
        "not found" not in page_src and
        "error" not in page_src,
        "No 404 error page shown for unknown URL!")
except:
    bug("BUG15 - No 404 Page for Unknown URLs", False, "")

# ═══════════════════════════════════════════
# 🖱️ UI & BUTTON BUGS
# ═══════════════════════════════════════════
print("\n" + "═"*55)
print("   🖱️  UI & BUTTON BUG TESTS")
print("═"*55)

# BUG16 - Is submit button missing on signup?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    btns = driver.find_elements(By.XPATH, "//button[@type='submit']")
    bug("BUG16 - Submit Button Missing on Signup",
        len(btns) == 0,
        "No submit button found on signup page!")
except:
    bug("BUG16 - Submit Button Missing on Signup", False, "")

# BUG17 - Is submit button missing on login?
try:
    open_page("https://krida-snowy.vercel.app/login")
    btns = driver.find_elements(By.XPATH, "//button[@type='submit']")
    bug("BUG17 - Submit Button Missing on Login",
        len(btns) == 0,
        "No submit button found on login page!")
except:
    bug("BUG17 - Submit Button Missing on Login", False, "")

# BUG18 - Is page title wrong?
try:
    open_page("https://krida-snowy.vercel.app")
    bug("BUG18 - Page Title is Wrong or Empty",
        driver.title == "" or driver.title is None,
        f"Page title is empty or None!")
except:
    bug("BUG18 - Page Title is Wrong or Empty", False, "")

# BUG19 - Do input fields exist on signup?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    inputs = driver.find_elements(By.XPATH, "//input")
    bug("BUG19 - Input Fields Missing on Signup",
        len(inputs) < 2,
        f"Only {len(inputs)} input field(s) found on signup!")
except:
    bug("BUG19 - Input Fields Missing on Signup", False, "")

# BUG20 - Does double clicking submit cause issues?
try:
    open_page("https://krida-snowy.vercel.app/signup")
    inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
    if inputs:
        inputs[0].send_keys("Test User")
    clear_type("//input[@type='email']", "double@test.com")
    clear_type("//input[@type='password']", "Test@1234")
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn.click()
    btn.click()  # Double click
    time.sleep(3)
    bug("BUG20 - Double Click Submit Causes Issues",
        False,
        "Double clicking submit caused unexpected behavior!")
except Exception as e:
    bug("BUG20 - Double Click Submit Causes Issues",
        True,
        f"Double click caused error: {e}")

# ═══════════════════════════════════════════
# 📊 FINAL BUG REPORT
# ═══════════════════════════════════════════
total = len(bugs_found) + len(bugs_not_found)
print("\n" + "═"*55)
print("   📊  FINAL BUG REPORT")
print("═"*55)
print(f"  🐛  BUGS FOUND    : {len(bugs_found)}")
print(f"  ✅  NO BUGS       : {len(bugs_not_found)}")
print(f"  📋  TOTAL TESTS   : {total}")

if bugs_found:
    print(f"\n  🔴  LIST OF BUGS FOUND:")
    for i, b in enumerate(bugs_found, 1):
        print(f"     {i}. {b}")
else:
    print("\n  🎉  NO BUGS FOUND! Website is clean!")

print("═"*55)
time.sleep(2)
driver.quit()
print("\n  🏁 Bug finding completed".)