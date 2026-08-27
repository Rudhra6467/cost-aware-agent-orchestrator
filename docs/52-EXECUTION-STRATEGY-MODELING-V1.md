# 52 — Execution Strategy Modeling V1

CAOS now distinguishes nominal resource cost from **practical execution cost**.

## Why

The cheapest API allocation is not necessarily the cheapest successful build. A plan can consume additional resources through retries, agent handoffs and provider switching, while parallel execution can reduce elapsed time.

## V1 assumptions

`ExecutionAssumptions` models:

- expected retry rate;
- expected handoff rate;
- handoff resource cost;
- average task execution time;
- available parallelism;
- provider-switching time penalty.

`ExecutionCostModel` returns:

- expected retries;
- expected handoffs;
- estimated monetary cost including expected retry/handoff spend;
- estimated elapsed minutes;
- a practical cost score.

## Important modeling principle

CAOS must separate **observed facts** from **assumptions**. Provider pricing and quota data should come from evidence; retry probabilities and execution times are estimates until CAOS has telemetry.

## Current limitation

V1 does not yet calculate a full expected-success probability, dependency-aware critical path, context-token overhead, or quality-adjusted utility. The monetary score intentionally remains interpretable rather than inventing a false universal dollar value for developer time.

## Next milestone

Build **execution simulation / critical-path modeling** over the DAG. Use task dependencies and parallelism to estimate completion time, handoff points and expected resource consumption before execution begins.
