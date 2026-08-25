# 16 — Cost Optimizer Specification

## Objective

Select an execution strategy that minimizes practical total cost while satisfying user constraints.

## Inputs

- task graph
- user budget
- deadline
- quality target
- reliability target
- project/platform constraints
- resource registry
- current resource availability
- historical execution metrics
- estimated handoff/retry costs

## Candidate Strategy Types

1. Single-provider execution
2. Cheapest-capable execution
3. Free-first execution
4. Hybrid free + paid execution
5. Parallel execution
6. Sequential execution
7. Local + API hybrid
8. Agent handoff strategy
9. Human-assisted strategy

## Cost Model

Estimated total cost should consider:

`direct service cost + expected retries + infrastructure cost + execution-time cost + handoff cost + expected failure cost`

The first implementation may use simplified monetary estimates. The model should become evidence-based as telemetry accumulates.

## Quality Constraint

The optimizer must reject strategies expected to fall below the user's minimum acceptable quality/reliability threshold, even if they are cheaper.

## Budget Modes

### Zero-Cost Target
Attempt a legitimate $0 execution path first. Report limitations and expected additional time.

### Budget-Constrained
Maximize outcome within a user-specified budget.

### Balanced
Optimize quality-adjusted cost and time.

### Speed-Constrained
Allow additional spend when it materially reduces delivery time while remaining within budget.

## Output

The optimizer should return:

- recommended strategy,
- alternatives,
- estimated cost range,
- estimated duration,
- expected quality,
- assumptions,
- risks,
- resources required,
- reasons for rejecting alternatives.

## Research Question

A central CAOS research question is:

> Can dynamic task-level resource selection achieve comparable or better software outcomes at materially lower cost than a fixed-provider or strongest-model baseline?

