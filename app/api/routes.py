import sqlite3
from flask import Flask, request, jsonify, g
from app.scraper.fetch_case_data_requests import fetch_case_data_requests
from app.db.models import get_db  # ✅ Updated import
from app.db import close_db   # ✅ Assuming close_db is in db.py

app = Flask(__name__)
app.teardown_appcontext(close_db)

@app.route('/fetch-case', methods=['POST'])
def fetch_case():
    try:
        data = request.get_json()
        case_type = data.get('case_type')
        case_number = data.get('case_number')
        case_year = data.get('case_year')

        if not all([case_type, case_number, case_year]):
            return jsonify({"status": "error", "message": "Missing input fields."}), 400

        db = get_db()

        # 1️⃣ Check if case already exists
        query = """
        SELECT * FROM cases 
        WHERE case_type=? AND case_number=? AND case_year=?
        """
        existing_case = db.execute(query, (case_type, case_number, case_year)).fetchone()

        if existing_case:
            print("📂 Data found in database, returning cached result.")
            return jsonify({
                "status": "success",
                "data": [dict(existing_case)]
            }), 200

        # 2️⃣ Fetch fresh data using scraper
        results = fetch_case_data_requests(case_type, case_number, case_year)

        if not results:
            return jsonify({"status": "error", "message": "No data found for given input."}), 404

        # 3️⃣ Ensure table has required columns (future-proof)
        db.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                case_year TEXT,
                status TEXT,
                petitioner TEXT,
                respondent TEXT,
                listing_date TEXT,
                court_no TEXT,
                orders_link TEXT,
                fetched_at TEXT
            )
        """)

        # 4️⃣ Save results in DB
        insert_query = """
        INSERT INTO cases (case_type, case_number, case_year, status, petitioner, respondent, listing_date, court_no, orders_link, fetched_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """
        for res in results:
            db.execute(insert_query, (
                case_type,
                case_number,
                case_year,
                res.get("status", "DISPOSED"),
                res.get("pet", ""),
                res.get("respondent", ""),
                res.get("orderdate", ""),
                res.get("court_no", ""),
                res.get("orders_link", "")
            ))
        db.commit()

        # 5️⃣ Return formatted data
        formatted_results = [
            {
                "case_no": f"{case_type} {case_number}/{case_year}",
                "status": res.get("status", "DISPOSED"),
                "petitioner": res.get("pet", ""),
                "respondent": res.get("respondent", ""),
                "listing_date": res.get("orderdate", ""),
                "court_no": res.get("court_no", ""),
                "orders_link": res.get("orders_link", "")
            }
            for res in results
        ]

        return jsonify({"status": "success", "data": formatted_results}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-cases', methods=['GET'])
def get_cases():
    try:
        db = get_db()
        rows = db.execute("SELECT * FROM cases ORDER BY fetched_at DESC").fetchall()
        data = [dict(row) for row in rows]
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
