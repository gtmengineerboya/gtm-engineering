# Day 14 learning notes

## Why validation and normalization matter

CRM search depends on stable identifiers. `Jamie@Example.com` and
` jamie@example.com ` should be treated as the same email. Domains often arrive
with a protocol, `www`, or a page path, so the lesson normalizes them before
searching. Invalid records stop early rather than becoming bad CRM data.

## How the code works

`read_leads` checks the CSV headers and validates every row. `dry_run_plan`
describes an upsert without network access. Only the explicit `--apply` path
asks for `APPLY`, reads a token from the process environment, searches contacts
by email and companies by domain, then creates or updates a contact. The
contact is read back and compared. This prevents a success message from
standing in for verification.

The API uses HubSpot's standard contact fields `email`, `firstname`,
`lastname`, and `jobtitle`; the company lookup uses the standard `domain`
field. The exercise does not invent custom properties or create associations.
Its returned company ID is for review, not association.
