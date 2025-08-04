from app.scraper.scraper_requests import fetch_case_data

if __name__ == "__main__":
    print("🔄 Testing Request-Based Scraper...")
    
    # Sample input values
    case_type = "W.P.(C)"
    case_number = "11211"
    case_year = "2023"
    
    results = fetch_case_data(case_type, case_number, case_year)

    if results:
        print("\n✅ Results fetched successfully:")
        for idx, row in enumerate(results, start=1):
            print(f"{idx}. Case No: {row['case_no']} | "
                  f"Petitioner vs Respondent: {row['petitioner_vs_respondent']} | "
                  f"Listing Date: {row['listing_date']}")
    else:
        print("\n⚠️ No results found or request blocked.")
