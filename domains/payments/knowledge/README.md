# Payments knowledge: how it works, and what to check

Each topic is an [Agent Skill](https://agentskills.io/specification) folder, `payments-<topic>/`:

- **`topic.yaml`:** the knowledge, per [the schema](../../../docs/schemas/knowledge-topic.schema.json).
  - **`how_it_works`:** how the system behaves today, quirks included, in terms of data and outcomes. The
    agent uses it to read the evidence and explain an anomaly.
  - **`checks`:** conditions on data that should hold. Each failure opens a case. Each check lists its known
    causes and how to confirm each one; a failure matching none goes to the unexplained queue. Once built,
    the check names its detector.
- **`SKILL.md`:** a short hand-written wrapper: `name` (same as the folder), a `description` naming the
  topic and its check prefix, and a pointer to `topic.yaml`. It carries no knowledge of its own.

Shared terms are the `payments-primer` skill ([payments-primer/SKILL.md](payments-primer/SKILL.md)). This
is domain knowledge, **not** action policy; it never authorises anything (see
[design](../../../docs/design.md#domain-knowledge-and-action-policy)).

## How it is loaded

The agent runtime loads the skills, not the model: for a case it loads `payments-primer` and the skill of
the case's check, by check prefix. The model doesn't choose. On a harness that supports Skills natively,
the same folders work as they are. Detectors read `topic.yaml` directly for checks and causes.

## Keep it small

The agent gets the primer, the topic of the case's failed check and the action catalogue. So:
- `how_it_works` covers what helps read the data and explain anomalies; nothing else. Aim for one screen.
- A check is something worth opening a case for. Mechanics that can't go wrong in a way anyone cares about
  aren't checks.
- No code locations (file paths, function names, line numbers); they drift. Describe behaviour and data.
- No open questions or plans. Questions go to the issue tracker. When an answer changes behaviour, update
  `how_it_works` after the change ships.

## Changing a topic

- Update `as_of` when `how_it_works` is re-checked against the running system.
- Check IDs are permanent: never reused or renumbered. A check that no longer applies gets `retired: true`.
- Git holds the history. Each run loads the domain's skill folders at one commit as a bundle and records
  its hash in the decision log; replays load the same bundle.

Checks before merging:
- `topic.yaml` matches the schema; check IDs are unique across the domain; no code locations in the text;
- `SKILL.md` front matter is valid, `name` matches the folder, and the description names the check prefix;
- a skill folder holds only `SKILL.md` and `topic.yaml`: no `scripts/`, no executables, nothing else.

## Topics

| Skill | Prefix | Topic |
|---|---|---|
| [payments-primer](payments-primer/SKILL.md) | | Shared terms |
| [payments-settlement-reconciliation](payments-settlement-reconciliation/topic.yaml) | `SET` | Applying CAS AR settlement files to pay-db |
| [payments-nsf-handling](payments-nsf-handling/topic.yaml) | `NSF` | PAD returns: freeze, lock, fee, and what clears them |
| [payments-refunds-credit-memos](payments-refunds-credit-memos/topic.yaml) | `REF` | Refund requests, approval, and what each payment method does |
| [payments-routing-slips](payments-routing-slips/topic.yaml) | `RSL` | Routing slips: balances, link/correction/void in CAS, refunds and write-offs |
| [payments-card-payments](payments-card-payments/topic.yaml) | `CRD` | Card payments through PayBC: transactions, re-checks, deletions |
| [payments-cgi-journals-disbursements](payments-cgi-journals-disbursements/topic.yaml) | `CGI` | EJV and AP files to CGI: government account payments, partner disbursements, feedback |
| [payments-invoice-lifecycle](payments-invoice-lifecycle/topic.yaml) | `INV` | Invoice creation, CFS invoices per payment method, references |
| [payments-cfs-accounts](payments-cfs-accounts/topic.yaml) | `CFA` | CFS accounts: setup, PAD activation, bank changes, freezes |
| [payments-events](payments-events/topic.yaml) | `EVT` | Payment events that tell products to release filings |
| [payments-bcol](payments-bcol/topic.yaml) | `BCL` | BC Online drawdown payments and refunds |
| [payments-eft](payments-eft/topic.yaml) | `EFT` | EFT accounts: bank files, short names, applying credit, overdue locks |

Still to write: online banking (credits, and bad payments sent to the wrong payee; waiting on the
bad-payment data source).
