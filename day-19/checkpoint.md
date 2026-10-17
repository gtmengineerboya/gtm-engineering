# Day 19 checkpoint

1. **What is an observed fact here?** A value copied exactly from the supplied
   record and tied to its source field.
2. **What is a hypothesis?** An explicitly uncertain interpretation with
   evidence fields, not a verified company statement.
3. **What does the fallback do?** Returns available input facts, no hypotheses,
   and a reason; it does not fabricate an AI response.

Practice: change a returned observed industry to a value not in the input and
confirm validation rejects it.
