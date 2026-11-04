---
name: payments-primer
description: "Payments (sbc-pay) shared terms - pay-db, CFS (CAS), PayBC, CGI, BC Online, auth, invoice references and CFS invoice numbers, invoice statuses, credits, account locks. Use with any payments topic skill or payments case."
---

# Payments primer

Terms shared by every payments topic. Each topic is its own `payments-<topic>` skill with its behaviour
and checks.

## Systems

- **pay-db:** sbc-pay's database. Invoices, their references to CFS, receipts, payments, credits, NSF
  records, payment accounts and their CFS accounts.
- **CFS (CAS):** the Province's receivables system and the ledger of record for what has been paid. pay-db
  follows it.
- **auth:** holds the account's status as customers see it (e.g. `NSF_SUSPENDED`). pay decides locks and
  auth mirrors them.
- **PayBC:** the Province's card payment service, reached through pay-connector.
- **CGI:** the Province's financial system; journal vouchers (EJV) and payouts (AP) go to it as files.
- **BC Online:** the older system some accounts pay from by drawdown.

## Invoices and CFS invoice numbers

- A pay-db invoice reaches CFS through an invoice reference, which carries the **CFS invoice number** and a
  status: `ACTIVE` (waiting for CFS), `COMPLETED` (settled) or `CANCELLED`.
- One CFS invoice number can carry several pay-db invoices: consolidated PAD invoices, and after an NSF the
  fee invoice too. Most checks talk about "the invoices on the number" for this reason.
- Unsettled invoice statuses include `CREATED`, `APPROVED`, `SETTLEMENT_SCHED` and `PARTIAL_PAID`. Settled
  is `PAID`. `CREDITED` means refunded to a credit memo.
- Card payments go through PayBC: **DIRECT_PAY** pays one invoice on PayBC's direct sale page; **CC** pays
  a CFS invoice by card. "Credit card invoice" in other topics means a CC invoice, e.g. the NSF fee.

## Credits

- **Receipts on account** (e.g. an online banking overpayment) and **credit memos** (e.g. refunds) become
  rows in `credits` with a remaining amount, which should match CFS.
- `applied_credits` records where a credit memo was applied.
- The account's `pad_credit`, `ob_credit` and `eft_credit` are totals of its credits by payment method.

## Account locks

- pay locks an account by setting `has_nsf_invoices` (after a returned PAD debit) or
  `has_overdue_invoices` (after overdue EFT invoices), and tells auth, which sets the org to
  `NSF_SUSPENDED` with a reason (e.g. `OVERDUE_EFT`). While locked, pay-api refuses new invoices.
- Unlocking clears the flag and tells auth again. The messages to auth are sent once; a failure is only
  logged.
