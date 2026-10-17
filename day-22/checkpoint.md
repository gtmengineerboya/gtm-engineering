# Day 22 checkpoint

1. **Why use an in-memory SQLite database?** It keeps the lesson runnable
   offline without modifying the repository's historical database.
2. **What does GROUP BY do?** It calculates one aggregate result per group,
   such as source or lifecycle stage.
3. **What is PostgreSQL-specific?** Date/time arithmetic and several advanced
   features vary; verify them before porting a query.

Practice: add a synthetic `Partner` lead and compare source counts.
