import csv

industries = [
    "SaaS",
    "Finance",
    "Healthcare",
    "Cybersecurity",
    "Retail",
    "Energy",
    "Education",
    "Manufacturing"
]

countries = [
    "USA",
    "India",
    "UK",
    "Canada",
    "Germany"
]

technologies = [
    "AWS;Python;React",
    "Azure;Power BI;SQL",
    "GCP;Kubernetes;Python",
    "AWS;Node.js;React",
    "Azure;Java;Spring Boot",
    "GCP;React;PostgreSQL"
]

job_titles = [
    "VP Sales",
    "CTO",
    "VP Marketing",
    "CEO",
    "Chief Growth Officer",
    "Revenue Operations Manager"
]

with open("day-06/companies.csv", "w", newline="") as file:
# writer--># the CSV writing tool     Imagine you have a blank notebook==> Notebook = companies.csv,  Pen  = writer
    writer = csv.writer(file) 
# .writerow()--># write ONE row into the CSV file.
    writer.writerow([ 
        "company",
        "website",
        "industry",
        "employees",
        "country",
        "technology",
        "job_title"
    ])

    for i in range(1, 101):

        company = f"Company{i}" #f"Company{i}"-->replace {i}-->Company1 ('f' tells Python to evaluate whatever is inside {}.)

        writer.writerow([
            company,
            f"company{i}.example.com",
            industries[(i - 1) % len(industries)],
            50 + (i * 25),
            countries[(i - 1) % len(countries)],
            technologies[(i - 1) % len(technologies)],
            job_titles[(i - 1) % len(job_titles)]
        ])

print("100 synthetic companies created successfully.")