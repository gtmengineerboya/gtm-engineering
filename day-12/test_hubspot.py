
import os #os — reads environment variables, such as your HubSpot token.
import requests #requests — sends HTTP requests to the HubSpot API.
#Think of requests as the way Python communicates with HubSpot over the internet.
TOKEN = os.getenv("HUBSPOT_TOKEN") #os.getenv() reads the value of the HUBSPOT_TOKEN environment variable.

if not TOKEN:
    raise RuntimeError("HUBSPOT_TOKEN is not set")

url = "https://api.hubapi.com/crm/v3/objects/companies"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

response = requests.get(
    url,
    headers=headers,
    params={"limit": 3}, #this parameter only controls how many records are requested in this API call. It does not create, update, or delete any companies.
    timeout=30,#timeout=30 limits how long the request waits before timing out.
)

print("HTTP Status:", response.status_code)

if response.ok:
    data = response.json()
    print("HubSpot connection successful")
    print("Companies returned:", len(data.get("results", []))) #Here, data is a Python dictionary containing a list of three companies under "results" ,[]--->the default value ,if that' key' doesn't exist. it returns --->An empty list [].

else:
    print("HubSpot API request failed")
    print("Response:", response.text[:500])#This is called Python 'string slicing',  Why? Because [:500] takes 'characters' from the beginning up to, but not including, index 500.
