# Day 22 learning notes

Analytical SQL turns CRM activity into funnel and source reports. Aggregation
groups records by lifecycle stage or source; `CASE` can count only rows that
meet a stage condition.

SQLite is used locally because it ships with Python. PostgreSQL is commonly
used for shared analytics; the basic aggregates here are portable, while date
arithmetic, JSON operators, and some conflict-handling syntax vary by engine.
The stage-history table stores duration in days to avoid pretending SQLite and
PostgreSQL timestamp functions are identical.
