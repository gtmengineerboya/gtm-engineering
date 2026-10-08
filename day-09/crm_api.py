import requests

url = "https://jsonplaceholder.typicode.com/posts"

payload = { #payload is the lead data we send to the CRM API
    "company": "Acme AI",
    "job_title": "VP Sales",
    "icp_score": 85,
    "lead_status": "Hot"
}

response = requests.post(
    url,
    json=payload
)

print("Status Code:", response.status_code) #response is the answer returned by the API.

print("CRM Response:")
print(response.json())