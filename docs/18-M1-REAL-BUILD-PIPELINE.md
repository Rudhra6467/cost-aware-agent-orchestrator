# 18 — M1 Real Build Pipeline

## Objective

Move CAOS from deterministic orchestration into its first verifiable software-generation loop.

## Pipeline

```text
User request
  ↓
Plan / task DAG
  ↓
Free-first resource selection
  ↓
Provider executor
  ↓
Explicit FILE: artifact format
  ↓
Safe project workspace
  ↓
Verification command
  ↓
PASS → artifact delivery
FAIL → recorded failure → future recovery loop
```

## Safety Boundaries

Generated model text must never be treated as arbitrary shell commands. CAOS first parses explicit file artifacts. Verification commands are selected by the orchestration policy and executed inside the generated workspace.

## Current M1 Scope

- provider-neutral executor interface
- OpenAI-compatible HTTP adapter
- explicit file artifact parser
- safe workspace writes
- verification runner
- cost telemetry
- persistent task/execution state

## Next Extensions

1. Build an actual small reference application from model output.
2. Add Git worktree/commit artifact integration.
3. Add test-failure repair loop.
4. Add provider fallback on failure/429.
5. Add structured context handoff between agents.
6. Add resource-registry-driven dynamic selection.
7. Benchmark fixed-provider vs CAOS cost/quality.
