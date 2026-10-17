# Day 23 — GTM metrics and revenue analytics

Run the sample metric report:

```powershell
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-23\metrics_report.py
```

The CSV and Markdown outputs are under `day-23\output\`. The inputs are
synthetic. Conversion rates are ratios from 0 to 1; money is USD; ARR is MRR
times 12; CAC divides supplied sales/marketing spend by new customers; LTV
uses monthly revenue per customer times average lifetime. Missing denominators
produce `N/A`, not a fabricated zero.

Tests: `python -m unittest discover -s tests -p "test_days19_24.py" -v`.
Troubleshooting: check the funnel counts and input units before comparing
reports; never label these synthetic values as actual results.

Expected sample values include 30% Lead-to-MQL, 50% MQL-to-SQL, CAC
`$3,000/customer`, LTV `$38,400/customer`, ARR `$288,000/year`, pipeline
`$480,000`, and velocity `$2,000/day`.
