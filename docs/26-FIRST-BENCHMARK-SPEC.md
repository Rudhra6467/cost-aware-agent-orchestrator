# 26 — First CAOS Benchmark Specification

## Purpose

Measure whether CAOS can complete the same software task at lower practical cost than a fixed baseline while preserving functionality.

## Benchmark principle

The benchmark compares **policies**, not providers. Both policies receive the same frozen task specification, acceptance criteria, workspace constraints, and verification commands.

## Benchmark task: Todo API

Build a small REST API with:

1. Create a todo.
2. List todos.
3. Mark a todo complete.
4. Delete a todo.
5. Persist data locally.
6. Validate malformed input.
7. Include automated tests.
8. Include a README with run instructions.

The task is intentionally small enough to repeat while exercising decomposition, coding, persistence, testing, verification, and documentation.

## Frozen acceptance criteria

A run passes functional acceptance only when:

- the application starts successfully;
- all four required operations work;
- data survives process restart;
- malformed input returns a controlled validation response;
- the automated test suite passes;
- the documented start/test commands work;
- generated files remain inside the allowed workspace.

## Measurements

Record for every run:

- total provider cost;
- input/output/total tokens when available;
- number of provider calls;
- execution duration;
- retries;
- handoffs;
- task success rate;
- verification result;
- failure reason if unsuccessful.

## Baseline policy

Use one fixed capable execution resource and the same task prompt for every baseline repetition. Do not optimize provider selection during the baseline.

## CAOS policy

CAOS may decompose the task, select resources, use eligible free quota, hand off state, retry within configured limits, and choose a paid resource only when required by the optimizer's constraints.

## Fairness controls

- Freeze task requirements before running either policy.
- Use identical acceptance criteria.
- Reset the workspace before each run.
- Record actual outcomes rather than relying on published estimates.
- Keep provider credentials and private keys out of benchmark artifacts.
- Run enough repetitions to avoid drawing conclusions from one lucky execution.

## Primary outcome

A CAOS run is an **accepted cost optimization** only when it is verified and meets or exceeds the baseline's functional success/quality bar while costing no more than the baseline.

## Reporting language

Early experiments must say **"observed in this benchmark"**, not "CAOS is always cheaper." A broader product claim requires repeated evidence across different task classes and resource conditions.
