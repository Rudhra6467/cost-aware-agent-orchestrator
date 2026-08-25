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

## DEC-006 — Provider-Neutral Adapter Boundary

**Decision:** CAOS core will communicate with AI providers through a normalized executor interface rather than importing provider SDKs into planning/selection logic.

**Reason:** Agent replacement, benchmarking and fallback behavior require provider independence.

## DEC-007 — Deterministic Selector as Baseline

**Decision:** Begin agent selection with an explicit deterministic utility function using capability, reliability, availability and estimated cost.

**Reason:** The baseline is explainable and measurable. More sophisticated learned or LLM-based routing can be compared against it later.

## DEC-008 — M1 Before Autonomy

**Decision:** Do not introduce multi-agent autonomy until single-agent execution is observable, testable and recoverable.

**Reason:** Layering autonomy onto an unverified execution core would make failures difficult to diagnose and weaken the research design.
