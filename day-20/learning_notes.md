# Day 20 learning notes

An automated quality screen is useful for obvious problems but cannot promise
that a message is relevant, polite, or appropriate. This exercise separates
deterministic rules (word count, company reference, known generic phrases, and
unsupported claims) from human judgment.

The report explains each decision and marks human review as required even for
a pass. No email, SMS, social message, or CRM send operation exists in this
module.

With `--ollama`, a local model returns separate 1–5 judgments for tone,
clarity, call-to-action quality, personalization, and grounding. These are
subjective model judgments, not verified facts or automatic approval.
