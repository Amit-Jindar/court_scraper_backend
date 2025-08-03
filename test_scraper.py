import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_case_data(case_type, case_number, case_year):
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

    print("⚠️ Page opened! Solve CAPTCHA manually.")
    input("⏳ Press ENTER here after solving CAPTCHA and page is ready...")

    results = []

    try:
        print("🔄 Attempting to auto-fill case details...")

        # Fill Case Type
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)

        # Fill Case Number
        driver.find_element(By.ID, "case_number").send_keys(case_number)

        # Fill Case Year
        Select(driver.find_element(By.ID, "case_year")).select_by_visible_text(case_year)

        print("✅ Case details auto-filled successfully.")

        # Click Search button
        search_btn = driver.find_element(By.ID, "search")
        driver.execute_script("arguments[0].click();", search_btn)
        print("🖱️ Search button clicked... waiting for results.")

        # Wait up to 10 seconds for table to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-bordered.table-hover"))
        )
        print("✅ Table loaded.")

        # Save page source for debugging
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📝 Saved page source to debug.html")

        # Extract results
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table.table-bordered.table-hover tbody tr")
        print(f"🔹 Found {len(rows)} rows.")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                results.append({
                    "ctype": cols[0].text.strip(),
                    "pet": cols[1].text.strip(),
                    "orderdate": cols[2].text.strip()
                })

        print(f"✅ Fetched {len(results)} results successfully.")

    except Exception as e:
        print(f"❌ Error while scraping: {e}")
    finally:
        driver.quit()

    return results

if __name__ == "__main__":
    data = fetch_case_data("W.P.(C)", "11211", "2023")
    print("🔹 Data fetched:", data)
