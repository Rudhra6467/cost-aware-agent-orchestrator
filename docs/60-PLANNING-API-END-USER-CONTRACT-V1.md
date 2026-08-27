# 60 — Planning API / End-User Contract V1

CAOS now defines a stable response contract between the planning brain and future UI/API clients.

## User-facing shape

```text
Raw idea
  ↓
Blueprint summary
  ↓
Assumptions
  ↓
Three plan summaries
  ↓
Recommendation + reasons
  ↓
Explanation
  ↓
BUILD / DIY
```

## Contract fields

- `idea`: original user idea;
- `blueprint_summary`: plain-language decomposition;
- `assumptions`: facts/estimates the planner relied on;
- `plans`: normalized cost/time/wait/critical-path summaries;
- `recommendation`: selected plan ID;
- `reasons`: structured decision reasons;
- `explanation`: human-readable rationale;
- `next_actions`: explicit user actions.

## Product boundary

The contract deliberately separates **planning** from **execution**. `BUILD` means the user can request autonomous/controlled construction; it does not itself execute arbitrary code. `DIY` means CAOS should produce the detailed build roadmap.

## Why this matters

Frontend development can now proceed against a stable contract without depending on the internal implementation of the optimizer, scheduler or simulator.

## Next milestone

Build the **Planning Service** that orchestrates idea ingestion → blueprint → resource discovery → variant generation → simulation → decision → this response contract, with provenance attached to every material cost/capability claim.
