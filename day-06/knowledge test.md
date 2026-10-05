Good. I reviewed all 5 answers. Your understanding is mostly correct, with a few important corrections.

## Day 6 checkpoint review

### Q1 — `csv.DictReader()` ✅

Your answer:

> reads each row as a Python dictionary

**Correct.**

More precisely:

```python
reader = csv.DictReader(file)
```

reads the CSV header and uses the column names as dictionary keys.

Example:

```python
{
    "company": "Acme AI",
    "industry": "SaaS",
    "employees": "250"
}
```

---

### Q2 — `company["industry"]` ⚠️

Your answer is close, but the reason is slightly different.

`company` is a **Python dictionary**, because `DictReader` converts each CSV row into a dictionary.

Therefore:

```python
company["industry"]
```

means:

> Get the value associated with the `"industry"` key.

We don't use:

```python
company[1]
```

because that's **list-style/index-based access**, while dictionaries use **keys**.

Think:

```text
List:
company[1]

Dictionary:
company["industry"]
```

---

### Q3 — CSV vs JSON ✅

Your answer is good.

A clearer version:

**CSV** is tabular data organized into rows and columns:

```text
company,industry,employees
Acme AI,SaaS,250
CloudTech,SaaS,500
```

**JSON** is structured key-value data:

```json
{
    "company": "Acme AI",
    "industry": "SaaS",
    "employees": 250
}
```

In our GTM pipeline, CSV is useful as an input dataset, while JSON is useful for structured records and exchanging data with APIs.

---

### Q4 — Synthetic data ✅

Your answer:

> for practice and save money

Correct.

We're using synthetic data so we can safely build and test the pipeline without needing real prospect data or paid data-enrichment services.

This lets us test the workflow before connecting real GTM data sources.

---

### Q5 — Architecture ⚠️ **Good understanding, but one important correction**

You understood the overall flow correctly:

```text
CSV
 ↓
Python
 ↓
Processing
 ↓
Enrichment
 ↓
Scoring
 ↓
AI analysis
 ↓
JSON
 ↓
Database
```

One thing to correct: **AI analysis is not simply "for better analysis" and scoring isn't necessarily AI.**

We have two different stages:

### Rule-based scoring

Example:

```python
if employees >= 500:
    score += 20
```

This is deterministic Python logic.

### AI analysis

Later, AI can analyze information that is harder to handle with simple rules—for example, company descriptions, business context, or other research information.

So the complete idea is:

```text
Raw CSV
   ↓
Python reads data
   ↓
Process company records
   ↓
Enrich missing/additional information
   ↓
Calculate ICP score using rules
   ↓
AI analyzes the enriched company
   ↓
Create structured JSON
   ↓
Store/use the result
```

## ✅ Day 6 checkpoint passed

You understand the fundamental pipeline well enough to continue.

### Now we build the real project

Next task:

```text
10 companies
   ↓
Python CSV reader
   ↓
Process automatically
   ↓
Scale to 100 companies
```

**Don't jump to enrichment or AI yet.** We first need the 100-company dataset and a working Python processing script.

Your next step is to run:

```powershell
py day-06/lead_intelligence.py
```

If it successfully prints all 10 companies, send me the output/screenshot and we'll move to **Step 2: scaling the dataset to 100 companies**.