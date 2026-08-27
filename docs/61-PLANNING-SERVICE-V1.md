# 61 — Planning Service V1

CAOS now has an application-facing `PlanningService` boundary.

## Contract

```text
PlanningRequest
  idea
  constraints
       ↓
PlanningService
       ↓
Idea Analyzer
       ↓
Planning Engine
       ↓
PlanningResponse
```

The service validates the raw idea, converts external dictionaries into typed user constraints, delegates to domain components, and returns the stable planning response contract.

## Why this matters

The web UI, CLI, API, automation layer, or future agent interface should not know how the optimizer, simulator, quota ledger, or resource registry work internally. They should call the planning boundary.

## Next milestone

Expose this service through an HTTP API and add request/response schema validation. The API should support a planning-only request first; execution must remain a separate, explicit action.
