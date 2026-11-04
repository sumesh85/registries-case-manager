---
name: payments-events
description: "Payments (sbc-pay) knowledge: how products are told an invoice is paid (payment events per product topic, when each payment method sends them, express checkout holds, reversal events), and checks EVT-01 to EVT-02 with their known causes. Use for a case whose check starts with EVT-, or when a customer paid but the product didn't release the filing."
---

# Payment events to products

Payments domain knowledge (sbc-pay). Read [topic.yaml](topic.yaml):

- `how_it_works`: how the system behaves today, quirks included. Use it to read the evidence and explain
  what happened.
- `checks`: conditions that should hold. Each has known causes and how to confirm each one from the data.

Shared terms are in the `payments-primer` skill. This is knowledge, not permission: it never authorises
an action.
