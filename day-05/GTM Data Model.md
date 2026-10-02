Day 5 — GTM Data Model
Day 5 is about understanding how GTM data is structured before we build Project 1. Your roadmap defines this flow:
Company
   ↓
Contact
   ↓
Lead
   ↓
Qualification
   ↓
Opportunity

It also specifically covers company attributes, contact attributes, firmographic data, technographic data, intent signals, and buying signals.     GTM ENGINEER 30 days road map
The build for Day 5 is a JSON-based GTM lead record. The roadmap's structure contains:
company
website
industry
employee_count
location
technology
contact_name
job_title
email
linkedin
icp_score

1. First understand the GTM data model
Company
A Company is the organization you're targeting.
Example:
Acme AI
SaaS
250 employees
USA

Typical company attributes:
Company name
Website
Industry
Location
Employee count
Technologies

Contact
A Contact is a person working at the company.
Example:
John Smith
VP Sales
john@acme.ai

A company can have multiple contacts:
Acme AI
 ├── John → CEO
 ├── Sarah → VP Sales
 └── Mike → CTO

This connects directly to what you learned on Day 4 with:
companies
contacts

2. Firmographic data
Firmographic data = characteristics of a company.
Examples:
Industry
Company size
Revenue
Location
Number of employees
Company type

For example:
{
    "company": "Acme AI",
    "industry": "SaaS",
    "employee_count": 250,
    "location": "USA"
}

3. Technographic data
Technographic data = technologies a company uses.
Example:
{
    "technology": [
        "React",
        "Node.js",
        "AWS",
        "Salesforce"
    ]
}

Why does this matter in GTM?
Suppose you're selling a Salesforce integration.
A company already using Salesforce could be more relevant than a company that doesn't.
4. Intent signals
Intent signals = evidence that a company may be interested in a product/service.
Examples:
Visited pricing page
Downloaded an ebook
Requested a demo
Visited product page
Opened multiple emails

For example:
Company → Acme AI
Signal  → Demo Request

5. Buying signals
Buying signals are actions or events that indicate a potential purchasing opportunity.
Examples:
Hiring for a relevant role
Requesting a demo
Expanding into a new market
Increasing technology usage
Visiting pricing pages

For GTM engineering, these signals can later become inputs to your lead scoring and automation system.
6. Build your Day 5 JSON
Now let's actually build something.
Go to:
C:\gtm-engineering

Create:
day-05/

Inside it create:
gtm_data_model.json

Your structure should initially look like this:
{
    "company": "",
    "website": "",
    "industry": "",
    "employee_count": 0,
    "location": "",
    "technology": [],
    "contact_name": "",
    "job_title": "",
    "email": "",
    "linkedin": "",
    "icp_score": 0
}

This follows the roadmap's Day 5 data-model structure.     GTM ENGINEER 30 days road map
7. Now create a real example
Replace the empty values with:
{
    "company": "Acme AI",
    "website": "https://acme.ai",
    "industry": "SaaS",
    "employee_count": 250,
    "location": "USA",
    "technology": [
        "React",
        "Node.js",
        "AWS"
    ],
    "contact_name": "John Smith",
    "job_title": "VP Sales",
    "email": "john@acme.ai",
    "linkedin": "https://linkedin.com/in/johnsmith",
    "icp_score": 85
}

Now you have a structured GTM lead record.
8. Understand the complete record
Think of it like this:
                    GTM Lead
                       │
        ┌──────────────┴──────────────┐
        │                             │
     COMPANY                       CONTACT
        │                             │
   Acme AI                       John Smith
   SaaS                          VP Sales
   250 employees                 john@acme.ai
   USA
        │
   TECHNOLOGY
        │
 React / Node / AWS
        │
   ICP SCORE
        │
        85

This is important because later your automation will take records like this and perform actions.
For example:
Lead
 ↓
Enrichment
 ↓
ICP scoring
 ↓
AI research
 ↓
Personalization
 ↓
CRM
 ↓
Outreach

9. Your Day 5 practical task
Create 5 fake leads in one JSON file.
Use this structure:
[
    {
        "company": "",
        "website": "",
        "industry": "",
        "employee_count": 0,
        "location": "",
        "technology": [],
        "contact_name": "",
        "job_title": "",
        "email": "",
        "linkedin": "",
        "icp_score": 0
    }
]

Make 5 different companies.
For example:
1. Acme AI
2. CloudTech
3. Beta Finance
4. DataWorks
5. Nova Health

Give each one different:
- Industry
- Employee count
- Location
- Technologies
- Contact
- Job title
- ICP score
10. Day 5 checkpoint
The roadmap's checkpoint asks you to take 10 fake leads, manually identify 3 you would prioritize, and explain why.     GTM ENGINEER 30 days road map
We'll do that after you create your 5-lead JSON.
Your first task now
Create:
day-05
└── gtm_data_model.json

Put the 5 leads inside it.
Don't worry about Git yet. We'll complete the Day 5 practical work first, test it, then commit everything together.
When you've created the file, send me a screenshot or paste the JSON here.
