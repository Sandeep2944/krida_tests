from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

# ═══════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)

bugs_found = []
no_bugs = []
test_results = []

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def record(name, condition, description, severity):
    status = "BUG FOUND" if condition else "NO BUG"
    test_results.append({
        "name": name,
        "status": status,
        "description": description,
        "severity": severity
    })
    if condition:
        print(f"  🐛 BUG FOUND [{severity}] : {name}")
        bugs_found.append(name)
    else:
        print(f"  ✅ NO BUG             : {name}")
        no_bugs.append(name)

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

def has_error():
    try:
        errors = driver.find_elements(By.XPATH,
            "//*[contains(@class,'error') or "
            "contains(@class,'alert') or "
            "contains(text(),'invalid') or "
            "contains(text(),'required') or "
            "contains(text(),'wrong')]")
        return len(errors) > 0
    except:
        return False

# ═══════════════════════════════════════════
# RUN ALL TESTS
# ═══════════════════════════════════════════
print("\n" + "═"*55)
print("   🔍  RUNNING ALL TESTS...")
print("═"*55)

# SIGNUP BUGS
print("\n  📋 Signup Tests...")

open_page("https://krida-snowy.vercel.app/signup")
url_before = driver.current_url
click_submit()
record("BUG01 - Empty Signup Form Submits",
       url_before != driver.current_url and not has_error(),
       "Empty form submitted with no validation",
       "HIGH")

open_page("https://krida-snowy.vercel.app/signup")
clear_type("//input[@type='email']", "notanemail")
click_submit()
record("BUG02 - Invalid Email Accepted",
       not has_error(),
       "Email without @ symbol was accepted",
       "HIGH")

open_page("https://krida-snowy.vercel.app/signup")
clear_type("//input[@type='email']", "123456789")
click_submit()
record("BUG03 - Numbers Only Email Accepted",
       not has_error(),
       "Numbers-only string accepted as email",
       "MEDIUM")

open_page("https://krida-snowy.vercel.app/signup")
inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
if inputs: inputs[0].send_keys("Test")
clear_type("//input[@type='email']", "test@test.com")
clear_type("//input[@type='password']", "1")
click_submit()
record("BUG04 - Weak Password Accepted",
       not has_error(),
       "Single character password was accepted",
       "CRITICAL")

open_page("https://krida-snowy.vercel.app/signup")
inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
if inputs: inputs[0].send_keys("     ")
clear_type("//input[@type='email']", "test@test.com")
clear_type("//input[@type='password']", "Test@1234")
click_submit()
record("BUG05 - Spaces Only Name Accepted",
       not has_error(),
       "Name field with only spaces accepted",
       "MEDIUM")

open_page("https://krida-snowy.vercel.app/signup")
clear_type("//input[@type='email']", "' OR '1'='1'; --")
clear_type("//input[@type='password']", "Test@1234")
click_submit()
record("BUG06 - SQL Injection Accepted",
       not has_error(),
       "SQL injection string accepted in email",
       "CRITICAL")

open_page("https://krida-snowy.vercel.app/signup")
clear_type("//input[@type='email']", "a"*200 + "@test.com")
click_submit()
record("BUG07 - Very Long Email Accepted",
       not has_error(),
       "Email with 200+ characters was accepted",
       "MEDIUM")

open_page("https://krida-snowy.vercel.app/signup")
inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
if inputs: inputs[0].send_keys("<script>alert('xss')</script>")
clear_type("//input[@type='email']", "xss@test.com")
clear_type("//input[@type='password']", "Test@1234")
click_submit()
record("BUG08 - XSS Injection in Name Field",
       "<script>" in driver.page_source,
       "XSS script reflected in page source",
       "CRITICAL")

# LOGIN BUGS
print("\n  📋 Login Tests...")

open_page("https://krida-snowy.vercel.app/login")
url_before = driver.current_url
click_submit()
record("BUG09 - Empty Login Form Submits",
       url_before != driver.current_url and not has_error(),
       "Empty login form submitted with no error",
       "HIGH")

open_page("https://krida-snowy.vercel.app/login")
clear_type("//input[@type='email']", "fake@fake.com")
clear_type("//input[@type='password']", "Test@1234")
click_submit()
record("BUG10 - Wrong Email Allows Login",
       "login" not in driver.current_url and not has_error(),
       "Wrong email was allowed to login",
       "CRITICAL")

open_page("https://krida-snowy.vercel.app/login")
clear_type("//input[@type='email']", "test@test.com")
clear_type("//input[@type='password']", "wrongpass")
click_submit()
record("BUG11 - Wrong Password Allows Login",
       "login" not in driver.current_url and not has_error(),
       "Wrong password allowed login",
       "CRITICAL")

# PAGE BUGS
print("\n  📋 Page Tests...")

open_page("https://krida-snowy.vercel.app/randompage999")
record("BUG12 - No 404 Error Page",
       "404" not in driver.page_source.lower() and
       "not found" not in driver.page_source.lower(),
       "No 404 page shown for invalid URL",
       "LOW")

open_page("https://krida-snowy.vercel.app")
links = driver.find_elements(By.XPATH, "//a[@href]")
broken = [l.get_attribute("href") for l in links
          if l.get_attribute("href") in ["", "#", None]]
record("BUG13 - Broken Links on Home Page",
       len(broken) > 0,
       f"Found {len(broken)} broken/empty links",
       "MEDIUM")

# UI BUGS
print("\n  📋 UI Tests...")

open_page("https://krida-snowy.vercel.app/signup")
btns = driver.find_elements(By.XPATH, "//button[@type='submit']")
record("BUG14 - Submit Button Missing on Signup",
       len(btns) == 0,
       "No submit button found on signup page",
       "HIGH")

open_page("https://krida-snowy.vercel.app/login")
btns = driver.find_elements(By.XPATH, "//button[@type='submit']")
record("BUG15 - Submit Button Missing on Login",
       len(btns) == 0,
       "No submit button found on login page",
       "HIGH")

driver.quit()

# ═══════════════════════════════════════════
# GENERATE HTML REPORT
# ═══════════════════════════════════════════
total = len(test_results)
total_bugs = len(bugs_found)
total_no_bugs = len(no_bugs)
score = round((total_no_bugs / total) * 100) if total > 0 else 0

severity_color = {
    "CRITICAL": "#ff4444",
    "HIGH":     "#ff8800",
    "MEDIUM":   "#ffcc00",
    "LOW":      "#44bb44"
}

rows = ""
for i, r in enumerate(test_results, 1):
    color = "#2d2d2d" if r["status"] == "NO BUG" else "#3a1a1a"
    icon = "✅" if r["status"] == "NO BUG" else "🐛"
    sev = r["severity"]
    sev_col = severity_color.get(sev, "#888")
    rows += f"""
    <tr style="background:{color}">
        <td>{i}</td>
        <td>{r['name']}</td>
        <td>{icon} {r['status']}</td>
        <td style="color:{sev_col};font-weight:bold">{sev}</td>
        <td>{r['description']}</td>
    </tr>"""

html = f"""<!DOCTYPE html>
<html>
<head>
<title>KRIDA Bug Report</title>
<style>
  body {{ font-family: Arial; background: #1a1a2e; color: #eee; padding: 20px; }}
  h1 {{ color: #00d4ff; text-align: center; }}
  h2 {{ color: #00d4ff; }}
  .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
  .card {{ background: #16213e; padding: 20px; border-radius: 10px;
           text-align: center; flex: 1; }}
  .card h3 {{ margin: 0; font-size: 2em; }}
  .bugs {{ color: #ff4444; }}
  .pass {{ color: #44ff44; }}
  .total {{ color: #00d4ff; }}
  .score {{ color: #ffcc00; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
  th {{ background: #0f3460; padding: 12px; text-align: left; color: #00d4ff; }}
  td {{ padding: 10px; border-bottom: 1px solid #333; }}
  .critical {{ color: #ff4444; font-weight: bold; }}
  .badge {{ padding: 3px 8px; border-radius: 5px; font-size: 0.8em; }}
  .footer {{ text-align: center; margin-top: 30px; color: #888; }}
</style>
</head>
<body>
<h1>🐛 KRIDA Website - Bug Report</h1>
<p style="text-align:center;color:#888">Generated: {now}</p>

<div class="summary">
  <div class="card">
    <p>Total Tests</p>
    <h3 class="total">{total}</h3>
  </div>
  <div class="card">
    <p>Bugs Found</p>
    <h3 class="bugs">{total_bugs}</h3>
  </div>
  <div class="card">
    <p>No Bugs</p>
    <h3 class="pass">{total_no_bugs}</h3>
  </div>
  <div class="card">
    <p>Health Score</p>
    <h3 class="score">{score}%</h3>
  </div>
</div>

<h2>📋 Detailed Bug Report</h2>
<table>
  <tr>
    <th>#</th>
    <th>Test Name</th>
    <th>Status</th>
    <th>Severity</th>
    <th>Description</th>
  </tr>
  {rows}
</table>

<h2>🔴 Critical Bugs Summary</h2>
<ul>
{"".join(f"<li style='color:#ff4444'>{r['name']} — {r['description']}</li>"
for r in test_results if r['severity'] == 'CRITICAL' and r['status'] == 'BUG FOUND')}
</ul>

<div class="footer">
  <p>🏁 KRIDA Automation Bug Report | Generated by Selenium Python</p>
</div>
</body>
</html>"""

with open("krida_bug_report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n" + "═"*55)
print("   📊  FINAL RESULTS")
print("═"*55)
print(f"  🐛  BUGS FOUND  : {total_bugs}")
print(f"  ✅  NO BUGS     : {total_no_bugs}")
print(f"  📋  TOTAL TESTS : {total}")
print(f"  🎯  HEALTH      : {score}%")
print("═"*55)
print("\n  📄 Report saved as: krida_bug_report.html")
print("  🏁 Open the HTML file in Chrome to see full report!")
