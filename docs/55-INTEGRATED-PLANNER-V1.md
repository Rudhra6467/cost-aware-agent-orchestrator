# 55 — Integrated Planner V1

CAOS now has a single orchestration facade connecting the planning primitives built so far.

## Flow

```text
Tasks + Resources + Shared Quota + User Constraints
                    ↓
             Global Optimizer
                    ↓
          Execution Cost Model
                    ↓
             Quota Scheduler
                    ↓
          Plan Comparison (optional)
                    ↓
              Integrated Plan
```

## Why this milestone matters

Before this pass, the components existed but a caller had to coordinate them independently. `IntegratedPlanner` establishes the first coherent planning API and gives the future application layer one entry point.

## Output

An `IntegratedPlan` contains:

- resource assignments and estimated monetary cost;
- execution assumptions and expected practical cost;
- optional alternative-plan comparison and recommendation;
- quota-aware scheduled task starts.

## Architectural rule

This facade is orchestration, not business-policy replacement. Individual engines remain independently testable and can evolve without coupling the entire system.

## Known limitation

Plan variants are currently supplied to the facade rather than generated automatically from a single project definition. DAG scheduling is also not yet dependency-aware inside the quota scheduler. The next stage should unify project DAG + resource assignment + quota windows into one simulation rather than running these concerns independently.

## Next milestone

Build **Unified Execution Planner V1**: generate the Zero-Cost, Lowest-Practical-Cost and Fastest-Practical variants automatically from the same DAG, simulate their schedules, and expose a single evidence-backed recommendation.
