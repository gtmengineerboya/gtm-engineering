import csv
import os


INPUT_FILE = "../day-06/companies.csv"
OUTPUT_FILE = "enriched_leads.csv"


def enrich_company(company):
    """
    Add GTM intelligence to a company record.
    """

    employees = int(company.get("employees", 0))

    industry = company.get("industry", "").lower()

    country = company.get("country", "").lower()

    technology = company.get("technology", "").lower()

    enrichment = {
        "company_name": company.get("company_name", ""),
        "website": company.get("website", ""),
        "industry": company.get("industry", ""),
        "country": company.get("country", ""),
        "employees": employees,
        "technology": company.get("technology", ""),
    }

    # Employee segment
    if employees >= 1000:
        employee_segment = "Enterprise"
    elif employees >= 500:
        employee_segment = "Mid-Market"
    elif employees >= 100:
        employee_segment = "Growth"
    else:
        employee_segment = "SMB"

    enrichment["employee_segment"] = employee_segment

    # Technology signals
    if "ai" in technology:
        enrichment["ai_signal"] = "Yes"
    else:
        enrichment["ai_signal"] = "No"

    # Industry signal
    if industry == "saas":
        enrichment["saas_signal"] = "Yes"
    else:
        enrichment["saas_signal"] = "No"

    # Geography signal
    if country == "usa":
        enrichment["target_market"] = "Yes"
    else:
        enrichment["target_market"] = "No"

    return enrichment


def main():

    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    enriched_leads = []

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for company in reader:

            enriched_company = enrich_company(company)

            enriched_leads.append(enriched_company)

    fieldnames = enriched_leads[0].keys()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(enriched_leads)

    print(f"Enriched {len(enriched_leads)} companies")

    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()