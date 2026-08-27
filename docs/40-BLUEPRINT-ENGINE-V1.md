# 40 — Blueprint Engine V1

CAOS now has a deterministic baseline for the first user-facing intelligence step: converting a plain-language idea into a reviewable product blueprint.

## User journey

```text
Raw idea
  ↓
Blueprint Engine
  ↓
Frontend | Backend | Database | Infrastructure | External Resources
  ↓
Assumptions + open questions
  ↓
User validation gate
  ├── Approve → cost planning when complete
  ├── Clarify → collect missing information
  └── Refine → revise scope
```

## Why this matters

Cost optimization is only meaningful after CAOS understands what the user is actually trying to build. The blueprint becomes the contract between natural-language intent and the downstream task/resource planner.

## V1 behavior

The baseline uses deterministic keyword heuristics to identify common external requirements such as AI, payments, and notifications. It deliberately labels this as an initial blueprint rather than pretending it has complete domain understanding.

## Next evolution

Connect the blueprint to the canonical task model and DAG builder. The LLM-backed analyzer should produce structured requirements, acceptance criteria, dependencies, uncertainty, and questions for the user while preserving a deterministic validation layer.
