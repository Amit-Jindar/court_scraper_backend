import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

def human_like_delay(min_time=0.5, max_time=1.5):
    time.sleep(random.uniform(min_time, max_time))

def fetch_case_data(case_type, case_number, case_year):
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)
    driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

    print("⚠️ Page opened! Solve CAPTCHA manually.")
    input("⏳ Press ENTER here after solving CAPTCHA and page is ready...")

    results = []

    try:
        print("🔄 Attempting to auto-fill case details with human-like behavior...")

        # Fill Case Type
        human_like_delay()
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)
        human_like_delay()

        # Fill Case Number
        field_number = driver.find_element(By.ID, "case_number")
        for char in case_number:
            field_number.send_keys(char)
            human_like_delay(0.1, 0.3)
        
        # Fill Case Year
        human_like_delay()
        Select(driver.find_element(By.ID, "case_year")).select_by_visible_text(case_year)

        print("✅ Case details auto-filled successfully.")

        # Move mouse to search button before clicking (human-like)
        human_like_delay()
        search_btn = driver.find_element(By.ID, "search")
        driver.execute_script("arguments[0].scrollIntoView(true);", search_btn)
        human_like_delay()
        driver.execute_script("arguments[0].click();", search_btn)

        print("🖱️ Search button clicked... waiting for results.")

        # Wait for table results
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-bordered.table-hover tbody tr"))
            )
            print("✅ Table loaded.")
        except TimeoutException:
            print("⚠️ Table didn't load, possibly invalid CAPTCHA or detection triggered.")

        # Save page source for debugging
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Extract results
        rows = driver.find_elements(By.CSS_SELECTOR, "table.table.table-bordered.table-hover tbody tr")
        print(f"🔹 Found {len(rows)} rows.")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3 and "No data available" not in cols[0].text:
                results.append({
                    "ctype": cols[0].text.strip(),
                    "pet": cols[1].text.strip(),
                    "orderdate": cols[2].text.strip()
                })

        print(f"✅ Fetched {len(results)} results successfully.")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"❌ Error while scraping: {e}")
    except WebDriverException as e:
        print(f"❌ WebDriver error: {e}")
    finally:
        driver.quit()

    return results

if __name__ == "__main__":
    data = fetch_case_data("W.P.(C)", "11211", "2023")
    print("🔹 Data fetched:", data)
