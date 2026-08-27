# 58 — Variant Simulation Integration V1

CAOS now evaluates each policy-generated allocation through the execution and quota layers.

## Evaluation output

Each variant produces:

- policy identity;
- dependency-aware execution simulation;
- expected monetary/retry/handoff metrics;
- quota-aware task schedule;
- total quota waiting time.

This creates the missing bridge between **policy generation** and **plan comparison**.

## Current architecture

```text
Project DAG
   ↓
Variant Policy
   ↓
Resource Allocation
   ├──→ Execution Cost Model
   ├──→ DAG Simulator
   └──→ Quota Scheduler
             ↓
       Variant Evaluation
             ↓
       Plan Comparison
```

## Caveat

Quota scheduling currently evaluates assignments independently and does not reserve a global future quota schedule. The DAG simulator also assumes deterministic durations and unlimited task-level parallelism. These are deliberate V1 boundaries.

## Next milestone

Build the **Variant Decision Engine** that consumes all three evaluations and selects a recommendation using explicit user constraints, with a transparent breakdown of cost, waiting time, execution time, free coverage and risk.
