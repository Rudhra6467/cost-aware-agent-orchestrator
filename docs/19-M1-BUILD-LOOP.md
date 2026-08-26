# 19 — M1 Build Loop

CAOS now has a bounded controlled build loop around the existing provider executor.

```text
Approved task
   ↓
Agent executor
   ↓
Explicit FILE artifacts
   ↓
Safe workspace
   ↓
Policy-selected verification
   ↓
PASS ─────────→ artifact ready
   │
   FAIL
   ↓
Failure classification
   ├── test/syntax/dependency → repair attempt
   ├── timeout → bounded retry
   └── provider 429/quota → future resource handoff
```

## Design rule

Model output is never treated as arbitrary shell execution. CAOS parses an explicit artifact contract and executes only verification commands selected by the build policy.

## Current limitation

The repair loop is now bounded and diagnosed, but it is not yet a full autonomous repair planner. Provider handoff is classified but not yet wired to a second provider.

## Next milestone

M1.5 — Multi-resource continuation:

1. Git-backed repository writer
2. Provider health/rate-limit monitor
3. Handoff manifest generation
4. Second-agent fallback
5. Context restoration test
6. Real provider integration test using injected credentials in CI/local only
7. Cost/quality/time telemetry
