# 31 — Budget Gate

CAOS must never spend money merely because a model or tool is available.

The Budget Gate sits between the proposed execution plan and execution.

```text
Execution Plan
    ↓
Estimated Cost
    ↓
Budget Policy
    ↓
┌───────────────┬──────────────────┐
│ Within budget │ Outside policy  │
│       ↓       │        ↓         │
│   APPROVE     │   REJECT/REPLAN  │
└───────────────┴──────────────────┘
```

## Supported policies V1

- maximum estimated spend;
- zero-cost-only execution.

## Product behavior

A rejected plan should not silently spend anyway. The next orchestration layer should either:

1. search for a cheaper plan;
2. ask the user to increase the budget;
3. switch to DIY mode;
4. explain that the requested quality/functionality cannot currently be achieved within the budget.

## Design principle

Cost optimization is not authorization. The user owns the spending decision.
