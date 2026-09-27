Day 3 Goal

By the end of today, you should be comfortable with:

Variables
Strings
Numbers
Lists
Dictionaries
if / elif / else
for loops
Functions
Working with JSON
Reading CSV data
Basic error handling
Combining these into a GTM lead-processing script

We will build, not just study.

Part 1 — Your GTM data is Python data

Yesterday you received JSON from an API:

data = response.json()

Suppose the API gives us:

{
    "company": "Acme",
    "industry": "SaaS",
    "employees": 250,
    "location": "USA"
}

Python can represent this as a dictionary:

lead = {
    "company": "Acme",
    "industry": "SaaS",
    "employees": 250,
    "location": "USA"
}

This is extremely important.

A GTM Engineer constantly transforms data like:

JSON → Python dictionary → process → JSON
Part 2 — Variables

Create:

day-03/
└── python-basics.py

Start with:

company = "Acme"
industry = "SaaS"
employees = 250
country = "USA"

print(company)
print(industry)
print(employees)
print(country)

Run:

py day-03/python-basics.py

You should get:

Acme
SaaS
250
USA
Part 3 — Lists

A list stores multiple values.

technologies = ["AWS", "Python", "React", "Docker"]

print(technologies)

Access an individual item:

print(technologies[0])
print(technologies[1])

Output:

AWS
Python

Remember:

Index:
0 → AWS
1 → Python
2 → React
3 → Docker
Part 4 — Dictionaries

This is more important for GTM work.

lead = {
    "company": "Acme",
    "industry": "SaaS",
    "employees": 250,
    "country": "USA"
}

Get values:

print(lead["company"])
print(lead["industry"])
print(lead["employees"])

Output:

Acme
SaaS
250

Add a new field:

lead["job_title"] = "CTO"

Now:

print(lead)

You have:

{
    "company": "Acme",
    "industry": "SaaS",
    "employees": 250,
    "country": "USA",
    "job_title": "CTO"
}

This is exactly the type of structure we'll use for leads.

Part 5 — if conditions

Now we start making GTM decisions.

employees = 250

if employees >= 100:
    print("Company fits employee criteria")
else:
    print("Company does not fit employee criteria")

Output:

Company fits employee criteria
Part 6 — GTM qualification

Let's make it realistic.

lead = {
    "company": "Acme",
    "industry": "SaaS",
    "employees": 250,
    "country": "USA"
}

if lead["industry"] == "SaaS" and lead["employees"] >= 100:
    print("Potential ICP match")
else:
    print("Not an ICP match")

This is your first piece of GTM qualification logic.

Part 7 — elif

Suppose we want three categories:

80+  → High
50–79 → Medium
<50 → Low

Python:

score = 85

if score >= 80:
    print("High")
elif score >= 50:
    print("Medium")
else:
    print("Low")

This will become your lead-prioritization logic.

Part 8 — Loops

Suppose we have multiple leads:

leads = [
    "Acme",
    "Beta",
    "Gamma",
    "Delta"
]

We can process every lead:

for company in leads:
    print(company)

Output:

Acme
Beta
Gamma
Delta

This is important because a GTM system rarely processes only one lead.

Part 9 — Loop through dictionaries

Now:

leads = [
    {
        "company": "Acme",
        "employees": 250
    },
    {
        "company": "Beta",
        "employees": 50
    },
    {
        "company": "Gamma",
        "employees": 500
    }
]

for lead in leads:
    print(lead["company"], lead["employees"])

Output:

Acme 250
Beta 50
Gamma 500

This is much closer to real GTM engineering.

Part 10 — Functions

A function lets us reuse logic.

def greet_company(company):
    print("Processing:", company)


greet_company("Acme")
greet_company("Beta")

Output:

Processing: Acme
Processing: Beta
Part 11 — Your first GTM function

Now we're getting into the actual project.

Create:

def calculate_score(lead):

    score = 0

    if lead["industry"] == "SaaS":
        score += 25

    if lead["employees"] >= 100:
        score += 20

    if lead["country"] == "USA":
        score += 15

    return score

Then:

lead = {
    "company": "Acme",
    "industry": "SaaS",
    "employees": 250,
    "country": "USA"
}

score = calculate_score(lead)

print("Company:", lead["company"])
print("ICP Score:", score)

Expected:

Company: Acme
ICP Score: 60

You have just built a basic deterministic ICP scoring function.