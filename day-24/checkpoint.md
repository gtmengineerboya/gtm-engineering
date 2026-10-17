# Day 24 checkpoint

1. **Why persist event IDs?** A restarted service can still recognize retries.
2. **What does the signature cover?** The exact raw request body, authenticated
   with HMAC-SHA256 and a shared secret.
3. **What data is retained?** Only event ID, event type, and receive time.

Practice: post the same synthetic event twice, observe `accepted` then
`duplicate`, and do not send real personal data.
