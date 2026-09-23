Step 5 — Build your first GTM funnel

Now create:

notes/day-01-funnel.md

Put this inside:

# Day 1 GTM Funnel

Lead
  ↓
MQL
  ↓
SQL
  ↓
Opportunity
  ↓
Customer

Now add an example:

# Example

100 Leads
↓
20 MQL
↓
10 SQL
↓
5 Opportunities
↓
2 Customers

Calculate each conversion:

Lead → MQL
20 / 100 × 100
= 20%
MQL → SQL
10 / 20 × 100
= 50%
SQL → Opportunity
5 / 10 × 100
= 50%
Opportunity → Customer
2 / 5 × 100
= 40%

So your funnel is:

100 Leads
   ↓ 20%
20 MQL
   ↓ 50%
10 SQL
   ↓ 50%
5 Opportunities
   ↓ 40%
2 Customers
Step 6 — Think like an engineer

Now ask:

How could we automate this funnel?

Don't worry about building it yet.

Write this in your notes:

# Automation Idea

Incoming Lead
      ↓
Validate lead
      ↓
Enrich company
      ↓
Calculate ICP score
      ↓
Qualify lead
      ↓
Store in CRM
      ↓
Route to sales
      ↓
Track conversion
      ↓
Analytics

This is the fundamental pattern you will progressively build throughout the 30-day roadmap.

The later capstone ultimately expands this into:

Lead Source → Validation → Enrichment → ICP Scoring → AI Research → Personalization → HubSpot → Lead Routing → Analytics.

Step 7 — Your first engineering scenario

Imagine this company:

Company

AI Productivity SaaS

Target customers
Location: USA
Industry: SaaS
Employees: 50–1,000
Technology: Cloud/SaaS
Target buyer: CTO / VP Engineering

Now you receive:

Company: TechFlow
Industry: SaaS
Employees: 250
Location: USA
Technology: AWS
Contact: David
Job Title: CTO

Ask yourself:

Is this company potentially a good ICP match?

Look at:

Industry       → SaaS       ✅
Employees      → 250        ✅
Location       → USA        ✅
Technology     → AWS        ✅
Buyer          → CTO        ✅

So this is potentially a strong ICP match.

Important: today we're not building the scoring algorithm yet. The roadmap introduces the actual GTM data model and scoring implementation later in Project 1.

Step 8 — Your first GTM data model

Create:

notes/day-01-data-model.md

Put:

# GTM Data Model

## Company

- company_name
- website
- industry
- employee_count
- location
- technology

## Contact

- contact_name
- job_title
- email
- linkedin

## Lead

- lead_id
- company
- contact
- source
- status
- icp_score

## Qualification

- qualification_status
- qualification_reason

## Opportunity

- opportunity_id
- value
- stage
- probability

## Customer

- customer_id
- company
- revenue

This gives you your first mental model of GTM data.

Later, you'll make this substantially more technical.

Step 9 — Git

If Git is installed, open your terminal inside gtm-engineering.

Run:

git init

Then:

git add .

Then:

git commit -m "Day 1 - GTM engineering foundations"

Now you've made your first GTM Engineering Git commit.

Step 10 — Your Day 1 engineering checkpoint

Don't move to Day 2 yet.

Open your notes and answer these without looking at the answers above:

1.

A company submits a demo form.

Is it automatically an SQL?

Why or why not?

2.

What is the difference between:

ICP
vs
Buyer Persona
3.

What is the purpose of lead enrichment?

4.

Why would a company use lead scoring?

5.

Given:

1,000 Leads
200 MQL
50 SQL
20 Opportunities
5 Customers

Calculate:

Lead → MQL = ?
MQL → SQL = ?
SQL → Opportunity = ?
Opportunity → Customer = ?
6.

Explain this:

Lead
 ↓
Enrichment
 ↓
ICP Scoring
 ↓
Qualification
 ↓
CRM
 ↓
Sales
 ↓
Customer
7 — Interview question

"What does a GTM Engineer do?"

Answer it in 30–60 seconds, as if an interviewer asked you.

What I want you to do now

Don't just read this.

Actually create the folder and files.

Then send me your answers to Q1–Q7.

I'll review them, correct your terminology, and then we'll finish the remaining Day 1 practical work before moving to Day 2 — REST APIs, which is the next technical foundation in your roadmap.