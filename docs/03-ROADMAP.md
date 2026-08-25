# 03 — Roadmap

## Phase 0 — Foundation

Repository, project doctrine, architecture, skill plan, progress tracking, research framework, budget policy.

**Exit:** project source of truth exists and development environment can be prepared.

## Phase 1 — Single-Agent Builder

User task → planner → coding agent → GitHub artifact.

**Exit:** a simple software task produces a functioning repository artifact.

## Phase 2 — Persistent State

Introduce SQLite orchestration state alongside Git/GitHub project state.

**Exit:** projects, tasks, executions, agents, tokens, costs, and outcomes are persisted.

## Phase 3 — Context Handoff

Build structured handoff state so Agent B can continue Agent A's work after failure or replacement.

**Exit:** controlled A→B continuation experiment succeeds.

## Phase 4 — Multi-Agent Workflow

Planner, Developer, Reviewer, Tester.

**Exit:** a complete development task passes through specialist roles.

## Phase 5 — Dynamic Agent Selection

Evaluate agents by capability, availability, reliability, context fit, and cost.

**Exit:** the orchestrator selects agents dynamically rather than using a fixed route.

## Phase 6 — Failure Recovery

Handle rate limits, timeouts, invalid output, build failures, test failures, context overflow, and budget exhaustion.

**Exit:** recoverable failures trigger retry/replan/fallback automatically.

## Phase 7 — Verification Engine

Automated build, lint, tests, review, and basic security checks.

**Exit:** completion is evidence-based rather than agent-asserted.

## Phase 8 — Cost Optimization

Token/call/cost telemetry and budget-aware planning.

**Exit:** system can demonstrate an economic decision for agent selection.

## Phase 9 — Research & Benchmarking

Compare single-agent, fixed multi-agent, cheapest-agent, and CAOS dynamic strategies.

**Exit:** reproducible dataset and benchmark results.

## Phase 10 — CAOS Alpha

End-to-end autonomous software-development prototype with controlled human oversight.

**Exit:** user requirement → working, tested artifact under explicit budget constraints.
