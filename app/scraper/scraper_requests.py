import requests
import re
import json
from bs4 import BeautifulSoup

BASE_URL = "https://delhihighcourt.nic.in/dhc_case_status_list_new.asp"
DETAIL_URL = "https://delhihighcourt.nic.in/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://delhihighcourt.nic.in/"
}

def clean_html(text):
    return re.sub(r'\s+', ' ', BeautifulSoup(text or "", "html.parser").get_text()).strip()

def parse_table_results(soup, case_type, case_number, case_year):
    results = []
    table_rows = soup.find_all("tr")
    for row in table_rows:
        cells = row.find_all("td")
        if len(cells) >= 4:
            pet_text = clean_html(cells[1].text)
            petitioner, respondent = "", ""
            match = re.split(r'\s+VS\.?\s+', pet_text, flags=re.IGNORECASE)
            if len(match) == 2:
                petitioner, respondent = match[0].strip(), match[1].strip()
            else:
                petitioner = pet_text.strip()
            results.append({
                "case_no": f"{case_type} {case_number}/{case_year}",
                "case_type": case_type,
                "case_number": case_number,
                "case_year": case_year,
                "status": clean_html(cells[0].text).upper() or "PENDING",
                "petitioner": petitioner,
                "respondent": respondent,
                "listing_date": clean_html(cells[2].text),
                "court_no": "",
                "orders_link": cells[3].find("a")["href"] if cells[3].find("a") else ""
            })
    return results

def parse_direct_detail(soup, case_type, case_number, case_year):
    results = []
    full_text = clean_html(soup.get_text())
    if "Case No" in full_text:
        results.append({
            "case_no": f"{case_type} {case_number}/{case_year}",
            "case_type": case_type,
            "case_number": case_number,
            "case_year": case_year,
            "status": "PENDING",
            "petitioner": "",
            "respondent": "",
            "listing_date": "",
            "court_no": "",
            "orders_link": ""
        })
    return results

def fetch_case_data(case_type, case_number, case_year):
    try:
        session = requests.Session()
        payload = {"ctype": case_type, "cnumber": case_number, "cyear": case_year}
        response = session.post(BASE_URL, headers=HEADERS, data=payload, timeout=20)

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = parse_table_results(soup, case_type, case_number, case_year)

        # If no results found, try parsing direct detail page
        if not results:
            results = parse_direct_detail(soup, case_type, case_number, case_year)

        return results
    except Exception as e:
        print("❌ Error in fetch_case_data:", str(e))
        return []

if __name__ == "__main__":
    payload = {"case_type": "W.P.(C)", "case_number": "11211", "case_year": "2023"}
    print(json.dumps(fetch_case_data(**payload), indent=4))
