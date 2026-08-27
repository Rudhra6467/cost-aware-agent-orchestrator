# 47 — Cost Plan Generator V1

## Product milestone

CAOS can now turn an enriched project DAG and ranked resource candidates into two explicit build options:

1. **Zero-Cost First** — maximize sufficient recorded free capacity.
2. **Lowest Practical Cost** — select the lowest reliability-adjusted unit-cost candidate per task.

## Output

Each plan contains:

- task-to-resource assignments;
- estimated resource units;
- available free units;
- estimated monetary cost;
- selection reason;
- total cost;
- free-coverage percentage;
- assumptions.

## Example user-facing explanation

> We can cover these tasks with recorded free capacity at $0. If a free quota is insufficient, CAOS identifies the remaining paid usage rather than pretending the whole build is free.

The hybrid option may deliberately cost a small amount if that produces a more practical route.

## Current limitation

V1 is a transparent greedy planner, not a global optimization solver. It does not yet model shared quotas across tasks, concurrency, retry consumption, time-to-build, provider switching, task-level quality thresholds, or multi-resource workflows.

Those constraints are necessary before making a strong claim of globally minimal cost.

## North Star connection

The planner is the first concrete implementation of the product promise:

> **Build your idea for the lowest practical cost.**

The system must always expose the assumptions and evidence behind the estimate rather than presenting a false guarantee of cheapest-possible execution.

## Next milestone

Add a **resource usage ledger and shared quota accounting layer**. This will prevent CAOS from counting the same free quota independently for multiple tasks and will make the $0 plan materially more realistic.
