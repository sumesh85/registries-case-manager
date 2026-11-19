# Payments knowledge: how it works, and what to check

Each topic is an [Agent Skill](https://agentskills.io/specification) folder, `payments-<topic>/`:

- **`topic.yaml`:** the knowledge, per [the schema](../../../docs/schemas/knowledge-topic.schema.json).
  - **`how_it_works`:** how the system behaves today, quirks included, in terms of data and outcomes. The
    agent uses it to read the evidence and explain an anomaly.
  - **`checks`:** conditions on data that should hold. Each failure opens a case. Each check lists its known
    causes and how to confirm each one; the agent tests them when it diagnoses a case. A cause
    can have a short `id` so diagnoses and replays can cite it. Detectors only detect; they don't pick
    causes.
- **`SKILL.md`:** a short hand-written wrapper: `name` (same as the folder), a `description` naming the
  topic, and a pointer to `topic.yaml`. It carries no knowledge of its own.

Shared terms are the `payments-primer` skill ([payments-primer/SKILL.md](payments-primer/SKILL.md)). This
is domain knowledge, **not** action policy; it never authorises anything (see
[design](../../../docs/design.md#domain-knowledge-and-action-policy)).

## How it is loaded

For a case the agent runtime loads `payments-primer` and the skill of the topic that holds the case's
check. The other topics are listed to the model by their `SKILL.md` description, and the model fetches
one when the evidence points into it (e.g. `cfs-paid-means-paydb-paid`'s root cause is often an NSF), so a
description should say plainly what the topic covers. On a harness that supports Skills natively,
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
- Check IDs are short readable names (`one-live-reference`), unique within the domain. A check that no
  longer applies is removed; older cases keep their meaning through the bundle their run recorded.
- Git holds the history. Each run loads the domain's skill folders at one commit as a bundle and records
  its hash in the decision log; replays load the same bundle.

Checks before merging:
- `topic.yaml` matches the schema; check IDs are readable names, unique across the domain; no code locations in the text;
- `SKILL.md` front matter is valid, and `name` matches the folder;
- a skill folder holds only `SKILL.md` and `topic.yaml`: no `scripts/`, no executables, nothing else.

## Topics

Only the topics the demo use cases need are kept (2026-11-19). The removed ones are in the pre-cleanup backup.

| Skill | Topic |
|---|---|
| [payments-primer](payments-primer/SKILL.md) | Shared terms |
| [payments-settlement-reconciliation](payments-settlement-reconciliation/topic.yaml) | Applying CAS AR settlement files to pay-db (`cfs-paid-means-paydb-paid`, `no-flip-flop`) |
| [payments-nsf-handling](payments-nsf-handling/topic.yaml) | PAD returns: freeze, lock, fee, refunds to credit memos (`no-nsf-on-refunded-invoice`) |
