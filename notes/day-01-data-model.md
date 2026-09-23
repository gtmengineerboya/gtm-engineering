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