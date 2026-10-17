# Day 15 checkpoint

1. **Why not retry every POST?** A repeated create request can produce duplicate
   records unless the service honors an idempotency key.
2. **Which failures are retried?** Timeouts/connection errors for retry-safe
   methods, plus HTTP 429 and selected 5xx responses.
3. **What happens after the retry limit?** The original request exception or
   final HTTP error is raised for the caller to handle.

Practice: change `max_attempts` to 1 in a local test and confirm there is no
retry. Do not point the exercise at a paid or production endpoint.
