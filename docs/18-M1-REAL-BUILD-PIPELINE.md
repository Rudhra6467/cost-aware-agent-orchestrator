# 18 — M1 Real Build Pipeline

## Objective

Move CAOS from deterministic orchestration into its first verifiable software-generation loop while establishing the end-user flow: idea → blueprint → approval → cost proposal → build/DIY.

## Pipeline

```text
User idea
  ↓
Blueprint Engine
  ↓
User Validation Gate
  ↓ approved
Task DAG
  ↓
Resource Intelligence
  ↓
Free-first Cost Optimizer
  ↓
Transparent Proposal
  ├── Let CAOS Build It
  └── Show Me How
          ↓
     Provider executor
          ↓
     Explicit FILE: artifacts
          ↓
     Safe project workspace
          ↓
     Verification command
          ↓
     PASS → delivery
     FAIL → repair/replan
```

## User Validation Gate

CAOS must not begin autonomous build execution until the user has approved the blueprint, unless the product later introduces an explicit auto-approve preference.

Supported decisions:

- **Approve** — proceed to cost planning.
- **Clarify** — request additional information/specifications.
- **Refine** — revise the blueprint instead of executing it.

## Safety Boundaries

Generated model text must never be treated as arbitrary shell commands. CAOS first parses explicit file artifacts. Verification commands are selected by the orchestration policy and executed inside the generated workspace.

## Cost Policy

The optimizer minimizes **lowest practical total cost**, not merely API price. It considers legitimate free capacity first, then open/local resources, then low-cost and premium options when required by capability, reliability, time or user constraints.

## Current M1 Scope

- provider-neutral executor interface
- OpenAI-compatible HTTP adapter
- idea blueprint engine
- user validation state
- free-first cost optimizer
- transparent build/DIY proposal primitives
- explicit file artifact parser
- safe workspace writes
- verification runner
- cost telemetry
- persistent task/execution state

## Next Extensions

1. Convert approved blueprints into richer domain-specific DAGs.
2. Connect the proposal engine to the full task-level cost optimizer.
3. Build an actual small reference application from real model output.
4. Add Git worktree/commit artifact integration.
5. Add test-failure classification and repair loop.
6. Add provider fallback on 429/failure/quota exhaustion.
7. Add structured context handoff between agents.
8. Add resource-registry-driven dynamic selection.
9. Benchmark fixed-provider vs CAOS cost/quality/time/reliability.
