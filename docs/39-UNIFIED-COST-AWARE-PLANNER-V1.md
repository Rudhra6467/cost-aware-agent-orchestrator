# 39 — Unified Cost-Aware Planner V1

CAOS now has a first integration layer that combines task constraints, resource discovery, historical performance, quota availability, and budget into an execution plan.

## Inputs

- ordered task requirements;
- discovered resources;
- quality/security evidence;
- historical execution evidence;
- current quota state;
- optional user budget.

## Output

Each planned task records:

- selected resource;
- estimated API cost;
- expected practical cost;
- quota available before execution.

The plan also reports total estimated API cost, total expected practical cost, feasibility, and a failure reason when planning cannot satisfy constraints.

## Current limitation

This is an integration baseline, not the final planner. It assumes one unit of quota per task and does not yet perform provider switching within a task, DAG-aware parallel scheduling, reset-window optimization, or automatic replanning.

## Next objective

Upgrade the planner into a project-level optimizer that can compare complete execution plans rather than making independent task-level choices. The optimizer should account for dependencies, quota forecasts, reset waits, parallelism, handoff overhead, verification risk, and total practical cost.
