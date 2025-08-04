import requests
import json
import re
from bs4 import BeautifulSoup

BASE_URL = "https://delhihighcourt.nic.in/app/get-case-type-status"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://delhihighcourt.nic.in/app/get-case-type-status"
}

def clean_html(text):
    return re.sub(r'\s+', ' ', BeautifulSoup(text or "", "html.parser").get_text()).strip()

def fetch_case_data_requests(case_type, case_number, case_year):
    try:
        # ✅ Step 1: Load main page to get cookies
        session = requests.Session()
        home_url = "https://delhihighcourt.nic.in/"
        home_resp = session.get(home_url, timeout=15)
        print("🔹 Initial cookie grab status:", home_resp.status_code)  # 🔹 Added
        print("🔹 Cookies grabbed:", session.cookies.get_dict())        # 🔹 Added

        # ✅ Step 2: Prepare payload (DataTables format)
        params = {
            "draw": 2,
            "columns[0][data]": "DT_RowIndex",
            "columns[0][name]": "DT_RowIndex",
            "columns[0][searchable]": "true",
            "columns[0][orderable]": "false",
            "columns[0][search][value]": "",
            "columns[0][search][regex]": "false",
            "columns[1][data]": "ctype",
            "columns[1][name]": "ctype",
            "columns[1][searchable]": "true",
            "columns[1][orderable]": "true",
            "columns[1][search][value]": "",
            "columns[1][search][regex]": "false",
            "columns[2][data]": "pet",
            "columns[2][name]": "pet",
            "columns[2][searchable]": "true",
            "columns[2][orderable]": "true",
            "columns[2][search][value]": "",
            "columns[2][search][regex]": "false",
            "columns[3][data]": "orderdate",
            "columns[3][name]": "orderdate",
            "columns[3][searchable]": "true",
            "columns[3][orderable]": "true",
            "columns[3][search][value]": "",
            "columns[3][search][regex]": "false",
            "order[0][column]": 0,
            "order[0][dir]": "asc",
            "order[0][name]": "DT_RowIndex",
            "start": 0,
            "length": 50,
            "search[value]": "",
            "search[regex]": "false",
            "case_type": case_type,
            "case_number": case_number,
            "case_year": case_year
        }

        # ✅ Step 3: GET request
        response = session.get(BASE_URL, headers=HEADERS, params=params, timeout=15)
        print("🔹 Final Request Status:", response.status_code)  # 🔹 Added
        print("🔹 Response Content-Type:", response.headers.get("content-type"))  # 🔹 Added
        print("🔹 Raw Response (first 300 chars):", response.text[:300])  # 🔹 Added

        if response.status_code != 200:
            print("❌ Error:", response.status_code)
            return []

        data = response.json()
        results = []

        for row in data.get("data", []):
            petitioner_raw = clean_html(row.get("pet", ""))
            petitioner, respondent = "", ""
            match = re.split(r'\s+VS\.?\s+', petitioner_raw, flags=re.IGNORECASE)
            if len(match) == 2:
                petitioner, respondent = match[0].strip(), match[1].strip()
            else:
                petitioner = petitioner_raw.strip()

            listing_info = row.get("orderdate", "")
            last_date = re.search(r'Last Date:?\s*([0-9/-]+)', listing_info, re.IGNORECASE)
            listing_date = last_date.group(1) if last_date else ""

            # ✅ Extract orders link (handles both quoted & unquoted href)
            orders_raw = row.get("ctype", "")
            link_match = re.search(r'href\s*=\s*["\']?([^"\'\s>]+)', orders_raw)
            if link_match:
                orders_link = link_match.group(1).strip()
                if not orders_link.startswith("http"):
                    orders_link = "https://delhihighcourt.nic.in" + orders_link
            else:
                orders_link = ""

            results.append({
                "case_no": f"{case_type} {case_number}/{case_year}",
                "court_no": row.get("courtno", ""),
                "listing_date": listing_date,
                "orders_link": orders_link,
                "petitioner": petitioner,
                "respondent": respondent or row.get("res", ""),
                "status": row.get("status", "").strip().upper()
            })

        return results

    except Exception as e:
        print("❌ Error in fetch_case_data:", str(e))
        return []

if __name__ == "__main__":
    payload = {
        "case_type": "W.P.(C)",
        "case_number": "11211",
        "case_year": "2023"
    }
    print(json.dumps(fetch_case_data_requests(**payload), indent=4))