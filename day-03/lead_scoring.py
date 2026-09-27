leads = [
    {
        "company": "Acme AI",
        "industry": "SaaS",
        "employees": 250,
        "country": "USA"
    },
    {
        "company": "Beta Finance",
        "industry": "Finance",
        "employees": 50,
        "country": "USA"
    },
    {
        "company": "CloudTech",
        "industry": "SaaS",
        "employees": 500,
        "country": "USA"
    }
]


def calculate_score(lead):

    score = 0

    if lead["industry"] == "SaaS":
        score += 25

    if lead["employees"] >= 100:
        score += 20

    if lead["country"] == "USA":
        score += 15

    return score


def qualify_lead(score):

    if score >= 50:
        return "Qualified"

    elif score >= 30:
        return "Potential"

    else:
        return "Not Qualified"


for lead in leads:

    score = calculate_score(lead)
    qualification = qualify_lead(score)

    print("--------------------")
    print("Company:", lead["company"])
    print("ICP Score:", score)
    print("Qualification:", qualification)