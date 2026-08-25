# 08 — Decision Log

Historical architectural decisions are append-only. If a decision changes, record a new decision rather than silently rewriting the old rationale.

## DEC-001 — Working Project Name

**Decision:** Use `CAOS` (Cost-Aware Agent Orchestration System) as the working project name.

**Reason:** Short identifier for documentation and development; legal/product naming can be revisited later.

## DEC-002 — Primary Research Focus

**Decision:** Cost-aware dynamic agent selection is the primary research focus; context-preserving handoff is a supporting research track.

**Reason:** It provides a measurable economic optimization problem and differentiates the project from ordinary multi-agent workflows.

## DEC-003 — Initial Framework

**Decision:** Use n8n + Python rather than pure n8n or pure CrewAI for the first implementation.

**Reason:** n8n provides accessible visual orchestration while Python provides control over scoring, state transitions, cost logic, and experiments.

## DEC-004 — State Management

**Decision:** Use Git/GitHub for software/project artifacts and SQLite for structured orchestration state.

**Reason:** Each storage system is used for the type of state it handles best.

## DEC-005 — Free-First Economics

**Decision:** Do not introduce recurring paid infrastructure until a measured bottleneck justifies it.

**Reason:** Budget is a core constraint and a research variable.
