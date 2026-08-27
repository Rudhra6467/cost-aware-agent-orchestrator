# 53 — DAG Execution Simulation V1

CAOS now has a dependency-aware execution simulation layer.

## Purpose

Before spending quota or invoking agents, CAOS should estimate how the task graph will actually execute.

V1 accepts tasks with:

- duration;
- dependencies;
- optional handoff overhead.

It produces:

- earliest start/finish for each task;
- total elapsed time under unlimited task-level parallelism;
- a critical path;
- cycle and missing-dependency validation.

## Example

```text
A (10m) ──► C (5m) ──┐
                     ├──► E (3m)
B (20m) ──► D (7m) ──┘
```

A and B can begin together. The critical path is B → D → E, giving 30 minutes rather than the 45 minutes required by sequential execution.

## Why this matters to the North Star

A resource that is technically free can still be a poor choice if it creates severe queueing, rate-limit waits or handoff overhead. Execution simulation gives the optimizer a time dimension.

## V1 limitations

The simulator currently assumes unlimited task-level parallelism and deterministic durations. It does not yet model provider concurrency limits, quota reset times, stochastic retries, task resource assignments, or context-transfer size.

## Next milestone

Connect simulated tasks to selected resource assignments and add **quota-reset / rate-limit scheduling**. CAOS should be able to answer not only "what is cheapest?" but also "when can this plan actually finish?".
