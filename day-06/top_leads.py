import csv

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent  # repo root, independent of the working folder

leads = []

if __name__ == "__main__":
    with open(str(ROOT_DIR / "day-06/enriched_leads.csv"), "r", newline="") as file:

        reader = csv.DictReader(file)

        for lead in reader:
            leads.append(lead)


    leads.sort(
        key=lambda lead: int(lead["icp_score"]), #(key=) --->Tell sort() what value it should use for sorting.
        reverse=True
    
    )


    print("===== TOP 10 GTM LEADS =====")

    for lead in leads[:10]:

        print("--------------------")
        print("Company:", lead["company"])
        print("ICP Score:", lead["icp_score"])
        print("Qualification:", lead["qualification"])
        print("Priority:", lead["priority"])
        print("Industry:", lead["industry"])
        print("Country:", lead["country"])