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

