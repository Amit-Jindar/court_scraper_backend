# test_selectors.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"))
driver.get("https://delhihighcourt.nic.in/case.asp")

try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "case_type")))
    print("✅ 'case_type' selector found")
except:
    print("❌ 'case_type' selector NOT found")

try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "case_number")))
    print("✅ 'case_number' selector found")
except:
    print("❌ 'case_number' selector NOT found")

input("⚠️ Press ENTER to close browser...")
driver.quit()
