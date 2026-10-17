# Day 26 checkpoint

1. **Why summarize instead of printing all details?** It provides operational
   signals while minimizing unnecessary personal data.
2. **What is the Day 13 durability limitation?** Run status exists only in the
   service process memory.
3. **Does this report mutate history?** No; it reads the CSV and writes a
   separate ignored report.

Practice: compare run count and failure count, then propose one recovery action
for a failed local run.
