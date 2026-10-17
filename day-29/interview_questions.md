# GTM Engineering interview practice

1. **What does GTM engineering automate?** Repetitive workflows across marketing,
   sales, and customer systems, with validation and auditability.
2. **Why normalize before CRM search?** Stable identifiers improve matching and
   reduce duplicate records.
3. **What is idempotency?** Repeating an operation has the same effect as
   performing it once.
4. **When may an HTTP POST be retried?** Only when the operation is safely
   repeatable, typically with a server-supported idempotency key.
5. **Why is a dry run useful?** It exposes planned changes before mutating an
   external system.
6. **What is a funnel stage?** A defined lifecycle state used to measure
   movement from lead through customer.
7. **Why separate qualification from routing?** Qualification determines fit;
   routing determines the owner or queue.
8. **How do you prevent unsupported AI claims?** Restrict evidence inputs,
   validate copied facts, label hypotheses, and retain human review.
9. **Does an automated copy pass guarantee quality?** No; it only passes
   specific checks and still needs a person.
10. **How do you handle API rate limits?** Honor `Retry-After`, apply bounded
    backoff, and avoid unsafe repeated writes.
11. **Why keep CRM associations separate from object creation?** They are
    distinct operations with account-specific schema and verification.
12. **How do you handle duplicate webhooks?** Persist event IDs with a unique
    key and return a duplicate response for repeat delivery.
13. **Why bind a local demo to loopback?** It avoids exposing an unauthenticated
    development service to other machines or the internet.
14. **What does CAC measure?** Acquisition spend divided by new customers for
    the chosen period and attribution assumptions.
15. **What makes a useful test for an API client?** Mock success, client/server
    errors, timeouts, retry limits, and idempotency conditions.
16. **What are the Day 13 API limitations?** Run state is in memory, not durable,
    and concurrent runs are rejected by a local lock.
17. **How do SQLite and PostgreSQL differ?** Core SQL aggregates are portable,
    while date/time, JSON, and concurrency features vary.
18. **Which capstone actions are intentionally absent?** Message sending and
    live CRM writes; human review is required and CRM mode stays dry-run.

Sample answers describe this repository's synthetic code only. Do not present
the sample metrics as business outcomes or claim production deployment.
