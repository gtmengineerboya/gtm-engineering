#How good is this lead according to our predefined ICP rules?”from advanced_scoring import calculate_score


companies = [

    {
        "company": "Company1",
        "industry": "SaaS",
        "employees": 750,
        "country": "USA",
        "job_title": "VP Sales",
        "technology": "AWS;Python;React",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company2",
        "industry": "Finance",
        "employees": 100,
        "country": "India",
        "job_title": "Developer",
        "technology": "Python;React",
        "buying_signal": "None"
    },

    {
        "company": "Company3",
        "industry": "SaaS",
        "employees": 600,
        "country": "USA",
        "job_title": "CTO",
        "technology": "Azure;Python",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company4",
        "industry": "Healthcare",
        "employees": 300,
        "country": "UK",
        "job_title": "CEO",
        "technology": "AWS;Python",
        "buying_signal": "None"
    },

    {
        "company": "Company5",
        "industry": "SaaS",
        "employees": 200,
        "country": "USA",
        "job_title": "VP Marketing",
        "technology": "GCP;React",
        "buying_signal": "None"
    },

    {
        "company": "Company6",
        "industry": "Retail",
        "employees": 800,
        "country": "USA",
        "job_title": "CTO",
        "technology": "Kubernetes;Python",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company7",
        "industry": "SaaS",
        "employees": 550,
        "country": "Canada",
        "job_title": "CEO",
        "technology": "AWS;React",
        "buying_signal": "None"
    },

    {
        "company": "Company8",
        "industry": "Finance",
        "employees": 900,
        "country": "USA",
        "job_title": "VP Sales",
        "technology": "Azure;SQL",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company9",
        "industry": "SaaS",
        "employees": 450,
        "country": "USA",
        "job_title": "CTO",
        "technology": "GCP;Python",
        "buying_signal": "None"
    },

    {
        "company": "Company10",
        "industry": "Education",
        "employees": 100,
        "country": "India",
        "job_title": "CEO",
        "technology": "AWS;Python",
        "buying_signal": "None"
    },

    {
        "company": "Company11",
        "industry": "SaaS",
        "employees": 1000,
        "country": "USA",
        "job_title": "Chief Growth Officer",
        "technology": "Kubernetes;Python",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company12",
        "industry": "Energy",
        "employees": 700,
        "country": "Germany",
        "job_title": "CTO",
        "technology": "GCP;Python",
        "buying_signal": "None"
    },

    {
        "company": "Company13",
        "industry": "SaaS",
        "employees": 300,
        "country": "UK",
        "job_title": "VP Sales",
        "technology": "AWS;React",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company14",
        "industry": "Cybersecurity",
        "employees": 600,
        "country": "USA",
        "job_title": "CTO",
        "technology": "Kubernetes;Python",
        "buying_signal": "None"
    },

    {
        "company": "Company15",
        "industry": "SaaS",
        "employees": 500,
        "country": "USA",
        "job_title": "Revenue Operations Manager",
        "technology": "Azure;Python",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company16",
        "industry": "Manufacturing",
        "employees": 250,
        "country": "India",
        "job_title": "Manager",
        "technology": "Java;SQL",
        "buying_signal": "None"
    },

    {
        "company": "Company17",
        "industry": "SaaS",
        "employees": 650,
        "country": "Canada",
        "job_title": "VP Marketing",
        "technology": "GCP;React",
        "buying_signal": "None"
    },

    {
        "company": "Company18",
        "industry": "Finance",
        "employees": 550,
        "country": "USA",
        "job_title": "CEO",
        "technology": "AWS;Python",
        "buying_signal": "Demo Request"
    },

    {
        "company": "Company19",
        "industry": "SaaS",
        "employees": 120,
        "country": "USA",
        "job_title": "CTO",
        "technology": "AWS;React",
        "buying_signal": "None"
    },

    {
        "company": "Company20",
        "industry": "Healthcare",
        "employees": 1000,
        "country": "USA",
        "job_title": "CEO",
        "technology": "Azure;Python",
        "buying_signal": "Demo Request"
    }
]


print("================================")
print("20 COMPANY SCORING TEST")
print("================================")

for company in companies:

    score = calculate_score(company)

    print(
        company["company"],
        "→",
        score,#we taking this value from --->advanced_scroring.py file
        "/ 100"
    )

print("\nTesting completed.")