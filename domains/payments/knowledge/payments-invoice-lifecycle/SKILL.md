---
name: payments-invoice-lifecycle
description: "Payments (sbc-pay) knowledge: how invoices are created and reach CFS (starting status per payment method, the nightly CFS invoice job for PAD, EFT, online banking and routing slips, invoice references), and checks INV-01 to INV-03 with their known causes. Use for a case whose check starts with INV-, or for invoices never sent to CFS, online banking invoices left unpaid, or duplicate invoice references."
---

# Invoice lifecycle (creation, CFS invoices, references)

Payments domain knowledge (sbc-pay). Read [topic.yaml](topic.yaml):

- `how_it_works`: how the system behaves today, quirks included. Use it to read the evidence and explain
  what happened.
- `checks`: conditions that should hold. Each has known causes and how to confirm each one from the data.

Shared terms are in the `payments-primer` skill. This is knowledge, not permission: it never authorises
an action.
