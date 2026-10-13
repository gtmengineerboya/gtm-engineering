
#os	Reads environment variables, such as your API token.
#Path	Builds file paths safely across operating systems.
#requests	Sends HTTP requests to HubSpot.
#load_dotenv	Loads environment variables from a .env file.
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

#__file__ — the path of the Python script currently running.
#.resolve() — converts the path into an absolute, resolved path.
#.parent — gets the directory containing the script.
#.parent.parent — moves up two directory levels.
##/ "day-09" / ".env" — builds the path to the environment file.
#load_dotenv(ENV_FILE) — loads the variables stored in that file.

# Load the token from the project's existing .env file.
PROJECT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_DIR / "day-09" / ".env"
load_dotenv(ENV_FILE)

TOKEN = (
    os.getenv("HUBSPOT_ACCESS_TOKEN")
    or os.getenv("HUBSPOT_TOKEN")
)

if not TOKEN:
    raise RuntimeError(f"HubSpot token not found: {ENV_FILE}")

URL = "https://api.hubapi.com/crm/v3/properties/companies"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get(URL, headers=HEADERS, timeout=30)

print("HTTP Status:", response.status_code)

if not response.ok:
    print(response.text[:1000])
    raise SystemExit(1) #SystemExit requests that Python terminate the program. 1 indicates an unsuccessful exit; 0 conventionally indicates success.
#raise is a Python keyword used to explicitly trigger an exception when a 'condition violates' the program's requirements. It helps prevent invalid data or failed operations from silently continuing through the application."
properties = response.json().get("results", [])
keywords = ("gtm", "icp", "outreach", "lead status") #a tuple is a collection of items that is ordered and immutable (cannot be changed after creation).

matches = [
    prop for prop in properties #1st prop Create a new list → check each item using 'if condition'→ add only matching items.
    if any(
        keyword in prop.get("name", "").lower()
        or keyword in prop.get("label", "").lower()
        for keyword in keywords
    )
]

if matches:
    print("\nMatching existing properties:")
    for prop in matches:
        print(
            f"Internal name: {prop.get('name')} | "
            f"Label: {prop.get('label')} | "
            f"Type: {prop.get('type')}"
        )
else:
    print("No matching custom properties found.")

print("\nNo CRM records were modified.")


#interview question:
#Explain this Python script and why you wrote it,

#I developed a Python-based diagnostic utility to validate company properties in HubSpot before running my GTM data synchronization pipeline. I use `python-dotenv` to load the API access token securely from an environment file and the `requests` library to call HubSpot's CRM Properties API. I validate the HTTP response, parse the JSON payload, and use a list comprehension with `any()` to filter properties based on keywords such as GTM, ICP, outreach, and lead status. Finally, I print each matching property's internal name, label, and type. This is a read-only operation that helps identify existing fields and reduces configuration errors during downstream lead synchronization.