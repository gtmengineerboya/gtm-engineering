# Day 18 learning notes

Deduplication is a data-quality decision with business impact: two contacts
may share a name, and one contact can change companies. This lesson uses exact
normalized email as a contact match key and normalized company identity as a
fallback candidate key. It labels the result as a possible duplicate, not a
fact.

The output includes source row numbers, match key, review status, and a reason.
`safe_merge_candidate` remains `NO`: a collision alone is not enough evidence
to merge. This is intentionally conservative and never mutates source data.
