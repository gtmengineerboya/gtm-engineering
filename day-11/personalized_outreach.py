import csv
import requests


INPUT_FILE = "../day-10/scored_leads.csv"
OUTPUT_FILE = "personalized_leads.csv"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def generate_personalization(company):

    prompt = f"""
You are a B2B GTM assistant.

Analyze this company and write one short personalized
outreach message.

Company: {company["company_name"]}
Industry: {company["industry"]}
Country: {company["country"]}
Employees: {company["employees"]}
Technology: {company["technology"]}
ICP Score: {company["icp_score"]}

Requirements:
- Maximum 50 words
- Professional tone
- Mention one relevant company signal
- Do not invent information
- Do not use generic phrases
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    response.raise_for_status()

    result = response.json()

    return result["response"].strip() #.strip() removes unnecessary spaces/newlines.


def main():

    personalized_leads = []

    with open(
        INPUT_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for company in reader:

            qualification = company["qualification"]

            if qualification == "Not Qualified":
                continue       #Skip the current loop iteration and move to the next company.

            print(
                f"Generating personalization for "
                f"{company['company_name']}..."
            )

            message = generate_personalization(company)

            company["personalized_message"] = message

            personalized_leads.append(company)

    if not personalized_leads:
        print("No qualified leads found.")
        return

    fieldnames = personalized_leads[0].keys()

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(personalized_leads)

    print()
    print(
        f"Generated personalization for "
        f"{len(personalized_leads)} leads"
    )

    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()