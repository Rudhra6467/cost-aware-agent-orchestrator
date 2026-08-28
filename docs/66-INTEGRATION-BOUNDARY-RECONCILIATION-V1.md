# 66 — Integration Boundary Reconciliation V1

This pass reconciles the application planner and planning service contracts.

## Final request flow

```text
HTTP payload
  ↓
PlanningService.request_from_dict
  ↓
PlanningRequest
  ↓
ApplicationPlanner.plan(request)
  ↓
Analyzer → Blueprint
  ↓
VariantSimulationEngine
  ↓
VariantDecisionEngine
  ↓
PlanningResponse
```

The planning service no longer duplicates blueprint composition. The application planner owns orchestration while the service remains the transport-facing boundary.

## Constraint propagation

The following user controls are preserved through the request boundary:

- budget;
- quality threshold;
- maximum build days;
- autonomy (`controlled`, `autonomous`, `diy`);
- free-first preference.

## Important verification note

This pass reconciles source-level contracts. Full repository CI still needs to be run before this is considered a verified end-to-end production path.

## Next milestone

Run the repository test suite and CI against the integrated branch, fix any import/signature failures, then expose a concrete browser/API fixture using the real planning components. Only after that should the first polished planning UI be built.
