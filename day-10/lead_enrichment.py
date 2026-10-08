import csv
import os #os lets Python interact with the operating system.


INPUT_FILE = "../day-06/companies.csv"
OUTPUT_FILE = "enriched_leads.csv" #This means the new file will be created inside the current day-10 folder.


def enrich_company(company):
    """
    Add GTM intelligence to a company record.
    """

    employees = int(company.get("employees", 0)) #Why .get()? -->If the key exists:→ returns the value, If it doesn't exist:→ returns 0.

    industry = company.get("industry", "").lower()

    country = company.get("country", "").lower()

    technology = company.get("technology", "").lower()

    enrichment = { #Create a new dictionary -->Because we don't want to modify the original company record directly.We're creating a new enriched record.
        "company_name": company.get("company_name", ""),
        "website": company.get("website", ""),
        "industry": company.get("industry", ""),
        "country": company.get("country", ""),
        "employees": employees, #Notice employees is now an integer. earlier it is 'string' in csv file ,in this new 'enrichment' dictionary it enhanced to integer.
        "technology": company.get("technology", ""),
    }

    # Employee segment ,Now we start adding GTM intelligence.
    if employees >= 1000:
        employee_segment = "Enterprise"
    elif employees >= 500:
        employee_segment = "Mid-Market"
    elif employees >= 100:
        employee_segment = "Growth"
    else:
        employee_segment = "SMB"

    enrichment["employee_segment"] = employee_segment #Add the employee_segment to the 'enrichment' dictionary

    # Technology signals
    if "ai" in technology: #If technology were:React-->"ai" in "react"-->so false
        enrichment["ai_signal"] = "Yes" #Add the 'ai_signal' to the 'enrichment' dictionary
    else:
        enrichment["ai_signal"] = "No"

    # Industry signal
    if industry == "saas":
        enrichment["saas_signal"] = "Yes"
    else:
        enrichment["saas_signal"] = "No"

    # Geography signal
    if country == "usa":
        enrichment["target_market"] = "Yes" #means-->This company is in our target geography.
    else:
        enrichment["target_market"] = "No"

    return enrichment #The function has finished processing the company.-->It sends the final updated/complete 'enriched dictionary' back.


def main():#main()-->= process ALL companies   #This is where the actual pipeline starts.

    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return #return 'stops the function',This prevents --->the program from continuing and crashing.

    enriched_leads = []

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for company in reader:

            enriched_company = enrich_company(company)#enrich_company()-->process ONE company

            enriched_leads.append(enriched_company)

    fieldnames = enriched_leads[0].keys() #Get column names -->Get the dictionary's column names. #These become the CSV 'column headers'.

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(enriched_leads)

    print(f"Enriched {len(enriched_leads)} companies")

    print(f"Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__": #If this Python file is being executed directly, run main().  So when you execute:--->python lead_enrichment.py ,Python runs:--->main()
    main()


#The key distinction to remember is:
#enrich_company() processes one company. main() controls the entire pipeline.