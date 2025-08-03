from flask import Blueprint, request, jsonify
from app.scraper.scraper_selenium import fetch_case_data
from app.db.models import get_db

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/fetch-case", methods=["POST"])
def fetch_case():
    data = request.json
    case_type = data.get("case_type")
    case_number = data.get("case_number")
    case_year = data.get("case_year")

    # Manual captcha scraping
    results = fetch_case_data(case_type, case_number, case_year)

    # Insert in DB
    db = get_db()
    cursor = db.cursor()
    for res in results:
        cursor.execute(
            "INSERT INTO cases (ctype, pet, orderdate, fetched_at) VALUES (?,?,?,datetime('now'))",
            (res["ctype"], res["pet"], res["orderdate"])
        )
    db.commit()

    return jsonify({"status": "success", "data": results})
