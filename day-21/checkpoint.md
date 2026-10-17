# Day 21 checkpoint

1. **Why not hard-code association type `1`?** The account's schema is the
   authority; guessing can create the wrong relationship.
2. **How does the lesson verify a write?** It reads the contact's company
   associations and checks the requested company ID.
3. **What do tests call?** A fake client, not the CRM.

Practice: run the dry-run command without association metadata; note the
explicit error asking you to inspect the schema.
