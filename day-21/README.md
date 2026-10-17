# Day 21 — CRM association integrity

Contact/company associations depend on the association category and type ID
configured in the HubSpot account. The script refuses to guess those values.
Inspect your schema first; this demo does not run against HubSpot by default.

```powershell
$env:HUBSPOT_CONTACT_COMPANY_ASSOCIATION_CATEGORY = "<verified-category>"
$env:HUBSPOT_CONTACT_COMPANY_ASSOCIATION_TYPE_ID = "<verified-type-id>"
C:\gtm-engineering\.venv\Scripts\python.exe C:\gtm-engineering\day-21\association_demo.py --contact-id SYNTHETIC_CONTACT --company-id SYNTHETIC_COMPANY
```

To choose live mode, add `--apply`; read the plan and type `APPLY`. A real
write requires actual IDs, verified schema values, a token in the process
environment, and a deliberate confirmation. The live request is idempotent
PUT followed by read-back. The default command is a dry run. Tests:
`python -m unittest discover -s tests -p "test_days19_24.py" -v`.

Troubleshooting: the placeholder IDs above are for command shape only, not real
HubSpot IDs. Never run the live command with those placeholders.
