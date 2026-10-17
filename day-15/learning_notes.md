# Day 15 learning notes

APIs fail temporarily because of network timeouts, rate limits, and server
outages. A timeout bounds how long a run waits. Exponential backoff spaces
retries farther apart so a client does not hammer an overloaded service.

The helper retries only a known set of transient conditions and only when the
request is safe to repeat. `Retry-After` is honored for rate limits and capped.
Bad client errors such as HTTP 400 are returned immediately. `requests` raises
the final error so the pipeline can log and handle failure explicitly.

The demo uses a fake session: it proves the retry behavior without depending on
the internet or a live CRM.
