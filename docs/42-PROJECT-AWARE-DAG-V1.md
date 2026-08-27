# 42 — Project-Aware DAG V1

## Goal

Turn a raw product blueprint into a project-specific, dependency-aware task graph before cost optimization begins.

## V1 approach

CAOS uses transparent rules to detect broad capability signals such as:

- frontend;
- backend/application logic;
- database/persistence;
- authentication;
- AI/model integration;
- payments/billing;
- notifications.

The resulting graph adds only relevant capability tasks and connects them through explicit dependencies.

## Example

Input:

> Build a SaaS app with user login, AI chat and Stripe subscriptions.

Baseline graph:

```text
requirements
   ├── data ──┬── auth ───┐
   │          ├── ai ─────┤
   │          └── billing ┤
   │                      ↓
   └──────────────→ frontend
                          ↓
                     integration
                          ↓
                       verify
                          ↓
                       release
```

## Design principle

The rules engine is deliberately inspectable. Later an LLM can propose richer tasks, but CAOS should validate the proposed graph for missing dependencies, cycles, unsupported assumptions and acceptance criteria before allowing optimization or execution.

## Next step

Add LLM-assisted task enrichment while retaining deterministic validation. Each task should acquire explicit resource requirements, estimated consumption, quality/security constraints and testable acceptance criteria.
