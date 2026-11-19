---
name: payments-primer
description: "Payments (sbc-pay) shared terms - pay-db, CFS (CAS), auth, invoice references and CFS invoice numbers, invoice statuses, credit card invoices, credit memos, account locks. Use with any payments topic skill or payments case."
---

# Payments primer

Terms shared by every payments topic. Each topic is its own `payments-<topic>` skill with its behaviour
and checks.

## Systems

- **pay-db:** sbc-pay's database. Invoices, their references to CFS, receipts, payments, credits, NSF
  records, payment accounts and their CFS accounts.
- **CFS (CAS):** the Province's receivables system and the ledger of record for what has been paid. pay-db
  follows it. CAS sends settlement files saying what was paid, returned or applied.
- **auth:** holds the account's status as customers see it (e.g. `NSF_SUSPENDED`). pay decides locks and
  auth mirrors them.

## Invoices and CFS invoice numbers

- A pay-db invoice reaches CFS through an invoice reference, which carries the **CFS invoice number** and a
  status: `ACTIVE` (waiting for CFS), `COMPLETED` (settled) or `CANCELLED`.
- One CFS invoice number can carry several pay-db invoices: consolidated PAD invoices, and after an NSF the
  fee invoice too. Most checks talk about "the invoices on the number" for this reason.
- Unsettled invoice statuses include `CREATED`, `APPROVED`, `SETTLEMENT_SCHED` and `PARTIAL_PAID`. Settled
  is `PAID`. `CREDITED` means refunded to a credit memo.
- **PAD** invoices are paid by pre-authorized debit from the customer's bank. A **CC** (credit card)
  invoice is paid by card through pay-api; the NSF fee invoice is one.

## Credits

- **Credit memos** (e.g. from refunds) become rows in `credits` with a remaining amount, which should
  match CFS.
- `applied_credits` records where a credit memo was applied.

## Account locks

- pay locks an account by setting `has_nsf_invoices` after a returned PAD debit, and tells auth, which
  sets the org to `NSF_SUSPENDED`. While locked, pay-api refuses new invoices.
- Unlocking clears the flag and tells auth again.
