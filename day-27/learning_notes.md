# Day 27 learning notes

Credentials belong in process environment variables or a local ignored
environment file, never in code, CSV fixtures, workflow exports, or Git. A
placeholder should fail validation just like a missing value. Error messages
name the setting but do not include the secret.

The redactor masks common bearer/token formats and email addresses before
text is stored in Day 13 logs or returned in run status. Redaction reduces
exposure but is not a substitute for minimizing logs in the first place.
Webhook requests are size-limited and can use an HMAC signature.

HubSpot access should use only the scopes required by the operation. Check
portal-specific properties and associations before writing. Never use the
offline tests as a reason to call live endpoints.
