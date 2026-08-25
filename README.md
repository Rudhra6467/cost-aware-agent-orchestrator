# CAOS — Cost-Aware Agent Orchestration System

**Working title:** Autonomous Cost-Aware Multi-Agent Software Development Framework

CAOS is a research-oriented Meta-Agent orchestration framework designed to help budget-constrained developers turn software ideas into functioning, tested software by dynamically selecting and coordinating AI agents according to capability, availability, reliability, context requirements, and cost.

## North Star

> Build an autonomous software-development orchestration system that can transform a user's software idea into a functioning, tested application by dynamically selecting and coordinating AI agents while respecting a defined budget.

## Primary Research Question

Can cost-aware dynamic agent selection reduce AI execution cost while maintaining acceptable software-development quality, reliability, and task-success rates compared with fixed-agent approaches?

## Current Status

**Phase 0 — Foundation / Pre-development**

The repository currently contains the project's North Star, constitution, skill plan, roadmap, architecture, research plan, progress tracker, experiment framework, decision log, budget policy, and milestones.

## Core Principles

- Functionality before appearance.
- Cost is a first-class constraint.
- LLM claims must be verified by execution/tests.
- Project state must survive agent replacement.
- Agents are replaceable; orchestration is provider-agnostic.
- The Meta-Agent decides; specialist agents execute.
- Measure before optimizing.
- Free-first; paid services require measurable justification.
- Human approval precedes high-risk autonomy.
- Experiments must be reproducible.

## Initial Technical Direction

- Visual orchestration: n8n
- Decision/orchestration logic: Python
- Project artifact state: Git/GitHub
- Structured execution state: SQLite initially
- Verification: automated build/test/lint pipeline
- Initial agents: Planner, Developer, Reviewer, Tester

## Development Sequence

Foundation → Single-Agent Builder → Persistent State → Context Handoff → Multi-Agent → Dynamic Selection → Failure Recovery → Verification → Cost Optimization → Benchmarking → CAOS Alpha.

See `docs/` for the permanent project source of truth.
