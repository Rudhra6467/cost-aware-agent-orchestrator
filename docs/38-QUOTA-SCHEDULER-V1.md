# 38 — Quota Scheduler V1

CAOS now has a scheduling primitive that can pack dependency-ordered work into available quota and, when a documented reset is known, wait for that reset rather than exceeding the limit.

## Scheduling principle

```text
Task sequence
    ↓
Known remaining quota
    ↓
Can task fit?
 ┌──YES───────────────┐
 ↓                    │
Schedule              │
                      │
 └──NO──→ Known reset? ──YES→ Wait → schedule
                 │
                 └──NO→ mark unscheduled
```

## Important limitation

V1 receives tasks in dependency order and schedules one resource assignment at a time. It is not yet a full DAG scheduler, does not concurrently execute independent tasks, and does not choose alternative resources itself.

## Next evolution

Combine the scheduler with the constrained optimizer so that each task can be assigned to the cheapest eligible resource while forecasting quota consumption across the whole DAG. The scheduler should then optimize provider switching, reset waits, parallelism, and expected practical cost together.
