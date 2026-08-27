# 54 — Quota-Aware Scheduling V1

CAOS now has a time-aware quota scheduling primitive.

## What changed

The scheduler can reason about:

- currently available free capacity;
- known quota reset times;
- temporary cooldown/rate-limit windows;
- task duration;
- expected waiting time.

It selects the earliest feasible resource and prefers currently available capacity when schedules are otherwise equivalent.

## Example

```text
Agent A: 0 free units, reset in 45 min
Agent B: 2 free units, available now
Agent C: paid, available now

Task requires 2 units.

CAOS → Agent B now
```

If B is unavailable:

```text
Agent A → free again at 12:45
Agent C → $0.08 now

CAOS can compare waiting 45 minutes against paying $0.08.
```

## Important limitation

V1 is a scheduling primitive, not yet a full DAG scheduler. It does not reserve future quota across multiple tasks, model rolling windows, provider concurrency, stochastic reset behavior, or jointly optimize the whole project's monetary and time objectives.

## Next milestone

Integrate quota scheduling with the DAG simulator and global optimizer. The resulting planner should choose **resource + execution time + quota strategy** together rather than in separate stages.
