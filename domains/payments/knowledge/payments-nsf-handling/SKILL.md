---
name: payments-nsf-handling
description: "Payments (sbc-pay) knowledge: what happens when a PAD payment is returned (freeze, lock, NSF fee) and what clears it, and checks NSF-01 to NSF-06 with their known causes. Use for a case whose check starts with NSF-, or for frozen or NSF-suspended accounts."
---

# NSF handling (PAD returns)

Payments domain knowledge (sbc-pay). Read [topic.yaml](topic.yaml):

- `how_it_works`: how the system behaves today, quirks included. Use it to read the evidence and explain
  what happened.
- `checks`: conditions that should hold. Each has known causes and how to confirm each one from the data.

Shared terms are in the `payments-primer` skill. This is knowledge, not permission: it never authorises
an action.
