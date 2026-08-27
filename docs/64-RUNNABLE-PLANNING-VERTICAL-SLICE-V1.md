# 64 — Runnable Planning Vertical Slice V1

CAOS now has a concrete, dependency-free HTTP transport for the planning contract.

## Endpoint

`POST /api/v1/plan`

The stdlib server validates the request, delegates to `PlanningAPI`, validates successful responses, and returns JSON.

## Cost-aware design

The first runnable transport deliberately uses Python's standard library. This keeps the initial local/demo path free of framework dependencies while leaving the domain layer transport-independent.

## Error behavior

- unknown route → `404`;
- malformed request / schema validation → `400`;
- unexpected planning failure → `500`;
- successful planning response → `200`.

## Security boundary

The endpoint remains planning-only. No build execution, repository writes, provider credentials, deployment, or spending occurs through this route.

## Next milestone

Build the first browser-facing planning experience and connect it to `/api/v1/plan`. The UI should make the user's first interaction extremely simple: describe an idea, optionally set budget/time preferences, review the three plans, understand the recommendation, then explicitly choose `BUILD` or `DIY`.
