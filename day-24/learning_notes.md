# Day 24 learning notes

A webhook is an HTTP event notification. Receivers should validate the event,
limit input size, authenticate senders where appropriate, and deduplicate
retries. Event providers often resend when they do not receive a response.

This local FastAPI receiver accepts a small synthetic JSON event, optionally
checks an HMAC signature, and stores only its ID/type/time in SQLite. The
primary key makes duplicate event IDs idempotent across process restarts. It
binds to loopback in the documented command and does not expose a public
service by default.
