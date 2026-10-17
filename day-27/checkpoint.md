# Day 27 checkpoint

1. **Why does `.env.example` use placeholders?** It documents configuration
   without exposing any credential.
2. **Why redact and minimize logs?** Logs can be copied, retained, and accessed
   by more people than the original CRM data.
3. **What does HMAC authenticate?** It verifies that a request body was signed
   by a party holding the shared secret; it does not encrypt the body.

Practice: add a synthetic email and bearer token to the redaction example and
confirm neither appears in output.
