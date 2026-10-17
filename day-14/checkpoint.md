# Day 14 checkpoint

1. **Why search on email?** It is the chosen unique contact identifier in this
   exercise, so it supports an update-or-create decision and reduces duplicates.
2. **Why normalize the domain?** A stable host lets `www.example.test` match
   `https://example.test/about`.
3. **What makes the write safe?** Dry-run is the default; live mode requires
   `--apply`, a displayed plan, a typed confirmation, validated records, and
   read-back verification.

Practice: change the second synthetic email to an invalid value and confirm
that validation fails without any CRM access.
