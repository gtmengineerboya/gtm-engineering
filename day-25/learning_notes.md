# Day 25 learning notes

Unit tests make deterministic rules reproducible. Integration boundaries are
replaced with fake sessions and fake CRM clients, so tests can simulate timeouts,
HTTP errors, and successful responses without making network calls.

The workflow runs tests on both Windows and Linux with Python 3.12 and 3.14.
This checks cross-platform behavior, including Windows file handling. CI does
not install a local CRM, Ollama model, or n8n instance.
