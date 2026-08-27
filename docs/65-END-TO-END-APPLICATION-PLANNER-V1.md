# 65 — End-to-End Application Planner V1

The CAOS planning stack now has an application-level composition boundary.

## Flow

```text
PlanningRequest
  ↓
Idea Analyzer
  ↓
Blueprint
  ↓
Variant Evaluation
  ├─ zero-cost
  ├─ lowest-practical-cost
  └─ fastest-practical (when configured)
  ↓
Variant Decision Engine
  ↓
PlanningResponse
```

`ApplicationPlanner` deliberately owns composition rather than duplicating optimization logic. Domain engines remain independently testable.

## End-user consequence

A future HTTP route can now call one application planner and receive the complete planning contract: blueprint summary, assumptions, evaluated options, recommendation, explanation, and explicit BUILD/DIY actions.

## Current boundary

This pass does not authorize build execution. BUILD remains an intent returned by planning and must be handled by a future execution/authorization service.

## Next milestone

Wire the concrete HTTP adapter to `ApplicationPlanner` using the repository's real analyzer/resource registry configuration, then add an end-to-end fixture demonstrating raw idea → response. After that, begin the browser-facing planning experience.
