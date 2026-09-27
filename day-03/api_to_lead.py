import requests


url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(url)

if response.status_code == 200:

    data = response.json()

    lead = {
        "name": data["name"],
        "email": data["email"],
        "company": data["company"]["name"]
    }

    print("Lead:")
    print(lead)

else:

    print("API request failed")
    print("Status:", response.status_code)