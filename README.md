🏛️ Court Scraper Backend

Features
1.Case Data Scraper – Web scraper se live case details fetch karta hai.
2.SQLite Database Integration – Case data ko local DB mein store aur cache karta hai.
3.REST APIs – Data fetch aur list karne ke liye ready endpoints.
4.Logging System – Scraper activity aur errors ka detailed log rakhta hai.
5.Postman Collection – API testing ke liye ready-made Postman file.

🔗 API Endpoints
1.Get All Saved Cases (GET)
  http://127.0.0.1:5000/get-cases
  
2.Fetch Case Details (POST)
  http://127.0.0.1:5000/fetch-case
  
  Request Body (JSON):
  {
  "case_type": "W.P.(C)",
  "case_number": "12345",
  "case_year": "2024"
  }

  Response 
  "status": "success",
  "data": 
    {
         "case_no": "W.P.(C) 12345/2024",
         "status": "P",
         "petitioner": "HARI SHANKER VERMAVS. UNION OF INDIA AND ORS.",
         "respondent": "UNION OF INDIA AND ORS.",
         "listing_date": "02/05/2025",
         "court_no": "275",
         "orders_link": "https://delhihighcourt.nic.in/app/case-type-status-details/..."
    }

⚙️ Installation & Setup

1.Clone repository:
  git clone https://github.com/Amit-Jindar/court_scraper_backend.git
  cd court_scraper_backend

2.Create virtual environment:
  python3 -m venv venv
  source venv/bin/activate

3.Install dependencies:
  pip install -r requirements.txt

4.Run Flask server:
  python3 -m app.api.routes

🧪 Run Tests
python3 -m tests.test_routes
python3 -m tests.test_db_fetch

Sample Postman commands:
curl -X POST http://127.0.0.1:5000/fetch-case \
     -H "Content-Type: application/json" \
     -d '{"case_type": "W.P.(C)", "case_number": "11211", "case_year": "2023"}'

curl http://127.0.0.1:5000/get-cases


📜 License
This project is for educational & research purposes only.

