import csv


INPUT_FILE = "enriched_leads.csv"
OUTPUT_FILE = "scored_leads.csv"


def calculate_icp_score(company):

    score = 0

    employees = int(company.get("employees", 0))

    # Industry
    if company.get("saas_signal") == "Yes":
        score += 25

    # Company size
    if employees >= 500:
        score += 20
    elif employees >= 100:
        score += 10

    # Geography
    if company.get("target_market") == "Yes":
        score += 15

    # AI signal
    if company.get("ai_signal") == "Yes":
        score += 15

    return score


def qualify_lead(score):

    if score >= 60:
        return "Highly Qualified"

    elif score >= 40:
        return "Qualified"

    else:
        return "Not Qualified"


def main():

    scored_leads = []

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for company in reader:

            score = calculate_icp_score(company)

            company["icp_score"] = score

            company["qualification"] = qualify_lead(score)

            scored_leads.append(company)

    fieldnames = scored_leads[0].keys()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(scored_leads)

    print(f"Scored {len(scored_leads)} leads")

    print(f"Output saved to: {OUTPUT_FILE}")

    print("\nTOP 10 LEADS:")

    sorted_leads = sorted(
        scored_leads,
        key=lambda x: int(x["icp_score"]),
        reverse=True
    )

    for lead in sorted_leads[:10]:

        print(
            lead["company_name"],
            "| Score:",
            lead["icp_score"],
            "|",
            lead["qualification"]
        )


if __name__ == "__main__":
    main()