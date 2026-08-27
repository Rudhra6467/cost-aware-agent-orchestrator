# 62 — Planning HTTP API V1

CAOS now defines a framework-neutral HTTP adapter for the planning boundary.

## Endpoint contract

```text
POST /api/v1/plan
Content-Type: application/json
```

Request:

```json
{
  "idea": "I want to build a fitness app",
  "constraints": {
    "budget": 5,
    "quality_threshold": 0.8,
    "max_build_days": 7
  }
}
```

The adapter delegates to `PlanningService` and returns the stable planning response. It maps malformed input to HTTP 400 and unexpected planning failures to HTTP 500.

## Deliberate boundary

This endpoint is **planning-only**. It does not execute code, spend money, create infrastructure, or grant an agent repository write access.

Execution will require a separate explicit action and authorization boundary.

## Next milestone

Add a concrete web framework route, schema validation, request IDs, structured error codes, and integration tests. Then implement the first end-user planning screen against this contract.
