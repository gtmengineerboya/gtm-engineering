# Day 25 checkpoint

1. **Why mock external APIs?** Tests stay repeatable, offline, and cannot
   mutate a real CRM.
2. **What does the CI matrix cover?** Windows/Linux and two supported Python
   versions.
3. **How do you run tests locally?** `python -m unittest discover -s tests -v`
   from the repository root.

Practice: temporarily change a retry expectation in a test, observe the failing
assertion, then restore the expected behavior.
