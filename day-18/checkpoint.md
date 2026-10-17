# Day 18 checkpoint

1. **Why is an email match only a review candidate?** Shared inboxes, recycled
   addresses, and source errors still need human checking.
2. **What does the script do to source rows?** Nothing; it writes a separate
   review CSV.
3. **Which fields are normalized?** Email case/whitespace and website host
   format; company names are compared after removing punctuation.

Practice: add two different contacts at one company and ensure they are not
classified as the same contact when their emails differ.
