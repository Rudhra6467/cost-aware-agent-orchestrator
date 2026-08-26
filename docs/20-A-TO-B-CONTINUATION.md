# 20 — A→B Continuation

CAOS now contains the first complete provider-handoff path at the orchestration layer.

## Flow

```text
Agent A
  ↓
provider failure / quota signal
  ↓
ProviderHealthRegistry
  ↓
HandoffRouter
  ↓
HandoffManifest
  ↓
SHA-256 integrity validation
  ↓
Agent B
  ↓
restored manifest injected into continuation prompt
  ↓
continue existing task
```

## What this proves

The system can represent a continuation as portable state rather than depending on the original model's conversational context.

The current test uses mock providers intentionally. This isolates orchestration correctness from external API availability and cost.

## What is NOT claimed yet

- No automatic live free-tier discovery yet.
- No provider-specific quota scraping yet.
- No real second-provider call in CI.
- No guarantee that semantic continuity is lossless.
- No production autonomous deployment.

## Next research experiment

Measure whether Agent B can complete a task correctly after receiving only the structured handoff state, compared with the same task using the full Agent A transcript.

Metrics:

- task completion
- test pass rate
- architecture consistency
- files changed unnecessarily
- token/context size
- handoff latency
- total cost
