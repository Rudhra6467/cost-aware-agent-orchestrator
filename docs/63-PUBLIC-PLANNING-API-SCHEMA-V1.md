# 63 — Public Planning API Schema V1

The public planning boundary now has explicit input/output validation.

## Request

`POST /api/v1/plan`

Required:
- `idea`: non-empty string

Optional `constraints`:
- `budget`: non-negative number;
- `quality_threshold`: number from 0 to 1;
- `max_build_days`: positive number.

## Response

The response must contain:

- idea;
- blueprint summary;
- assumptions;
- plans;
- recommendation;
- reasons;
- explanation;
- next actions.

Next actions are restricted to explicit product actions such as `BUILD` and `DIY`.

## Why this matters

The end-user interface can now rely on a stable contract and reject malformed data before it reaches the planning engine. This also creates a clean boundary for future versioned API evolution.

## Next milestone

Build the concrete application route and first planning UI. Add request IDs, structured errors, and an end-to-end test from HTTP request through a deterministic fixture planner to the response contract.
