import requests
import json

# Base URL where your Flask app is running
BASE_URL = "http://127.0.0.1:5000"

def test_fetch_case():
    """
    ✅ This function tests the '/fetch-case' API.
    It sends case details to the backend and checks if data is fetched or cached.
    """
    payload = {
        "case_type": "W.P.(C)",      # Example: Case Type
        "case_number": "11211",      # Example: Case Number
        "case_year": "2023"          # Example: Case Year
    }

    # Sending POST request to backend
    response = requests.post(f"{BASE_URL}/fetch-case", json=payload)

    print("\n🔹 Testing /fetch-case endpoint")
    print("Status Code:", response.status_code)  # 200 = Success
    print("Response JSON:")
    print(json.dumps(response.json(), indent=4))  # Pretty-print JSON response


def test_get_cases():
    """
    ✅ This function tests the '/get-cases' API.
    It checks if stored cases are fetched from the database.
    """
    # Sending GET request to backend
    response = requests.get(f"{BASE_URL}/get-cases")

    print("\n🔹 Testing /get-cases endpoint")
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=4))


if __name__ == "__main__":
    print("🚀 Running API Tests...\n")
    test_fetch_case()   # Test fetching one case
    test_get_cases()    # Test retrieving all saved cases
