import os
import requests
from dotenv import load_dotenv

load_dotenv("day-09/.env") #"Read the variables from .env."

token = os.getenv("HUBSPOT_ACCESS_TOKEN") #Give me the value stored under HUBSPOT_ACCESS_TOKEN."

if not token:
    print("ERROR: HubSpot token not found.")
    exit()

url = "https://api.hubapi.com/crm/v3/objects/contacts?limit=1"

headers = {
    "Authorization": f"Bearer {token}", #Bearer basically means:The person/system presenting this valid token is authorized to make this API request.
    "Content-Type": "application/json"
}

response = requests.get(
    url,
    headers=headers
)

print("Status Code:", response.status_code)

if response.status_code == 200:
    print("HubSpot authentication SUCCESS!")
    print(response.json())
else:
    print("HubSpot authentication FAILED!")
    print(response.text)