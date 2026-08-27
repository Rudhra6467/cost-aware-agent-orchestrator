# 48 — Shared Usage Ledger V1

## Problem

A free-tier resource has one quota, but a project can contain many tasks. Independent task estimates can incorrectly count the same free capacity more than once.

## Solution

`UsageLedger` tracks, per resource:

- total recorded free units;
- consumed units;
- reserved units;
- remaining units.

Reservations let the planner allocate capacity before execution. Consumption records actual usage after execution.

## Example

```text
Free quota = 100

Task A reserves 70
Remaining = 30

Task B needs 60
30 can be free
30 must use another resource / paid capacity
```

## Architectural rule

Quota is a **shared project constraint**, not a property that each task may independently spend.

## Current limitation

V1 is an in-memory ledger. It does not yet persist across processes, model providers, quota-reset windows or projects. It also does not reconcile provider-reported usage automatically.

## Next milestone

Integrate the ledger directly into `CostPlanGenerator` so the generated plans allocate shared free capacity correctly and expose exactly which tasks spill into paid capacity.
