#Merge the lead + enrichment topic

import requests

# Original lead
lead = {
    "company": "Acme",
    "website": "acme.com"
}

print("Original Lead:")
print(lead)

# Call enrichment API
response = requests.get(
    "https://jsonplaceholder.typicode.com/users/1"
)

print("API Status:", response.status_code)

# Convert JSON response
data = response.json()
print(data)

# Create enrichment data
enrichment = {
    "contact_name": data["name"],
    "email": data["email"],
    "source_company": data["company"]["name"]
}

# Merge enrichment into lead
lead.update(enrichment) #python update method ,add the elements at the end of list.

print("\nEnriched Lead:")
print(lead)