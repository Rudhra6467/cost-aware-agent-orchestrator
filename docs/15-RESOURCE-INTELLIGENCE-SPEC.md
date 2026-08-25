# 15 — Resource Intelligence Specification

## Purpose

Resource Intelligence is the evidence layer that lets CAOS answer:

> What legitimate resources can perform this task, under the user's constraints, and what is the lowest practical total cost?

## Resource Categories

- AI model/API
- Coding agent
- Research/search service
- UI/design generator
- Database
- Backend platform
- Frontend hosting
- Compute/runtime
- Storage
- Authentication
- Observability/testing service
- Open-source/local model
- Human/manual step

## Resource Profile

Each resource should eventually contain:

- resource_id
- provider
- model/service name
- category
- capabilities
- measured quality scores
- context limits
- input/output pricing
- free-tier description
- quota/rate-limit description
- trial/discount information
- availability
- reliability
- latency
- terms/eligibility notes
- source/evidence URL
- last_verified_at
- confidence level

## Important Distinction

CAOS must distinguish:

**Advertised availability** — what a provider says is available.

**Observed availability** — what CAOS has actually measured or successfully used.

**User eligibility** — whether the particular user can legitimately access it.

These should never be silently conflated.

## Free-Tier Tracking

The system may track remaining quota where the provider exposes it legitimately. It must not infer or manipulate hidden quota state, evade rate limits, rotate identities, or bypass eligibility restrictions.

## Resource Scoring

Initial score dimensions:

- capability fit,
- quality,
- reliability,
- availability,
- cost,
- latency,
- context fit,
- handoff risk,
- implementation effort.

The scoring formula will be experimental and versioned.

## Research Evolution

### V1
Curated registry entered manually.

### V2
Evidence-backed web/API-assisted updates.

### V3
Automated resource discovery and change detection.

### V4
Measured performance feedback updates resource profiles.

## Freshness Rule

Pricing, limits, trials, and availability are volatile. Every such field should have a last-verified timestamp and source evidence.
