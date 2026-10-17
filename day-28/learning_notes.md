# Day 28 learning notes

The capstone joins earlier lessons while keeping system boundaries visible.
Validation prevents malformed records from flowing forward; deterministic
rules make scoring/routing explainable; research records source facts;
automated copy checks provide reasons; a person approves before any action.

The CRM action is a plan only. The report says `DRY_RUN`, `HUMAN_APPROVAL_REQUIRED`,
and `message_sent=NO`. That is an intentional safety gate, not an incomplete
successful write. The offline fallback exercises the data flow without a
local model or paid enrichment service.
