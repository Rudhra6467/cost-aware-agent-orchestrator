# CAOS Benchmark 001 — Todo API

This directory defines the first frozen benchmark workload. It is intentionally provider-neutral.

## Objective

Compare a fixed single-agent baseline against CAOS on the same small software project.

## Required deliverable

A local REST API implementing create/list/complete/delete todo operations with persistence, validation, tests, and documentation.

## Acceptance gate

A run is functionally accepted only if all of the following are true:

- application starts;
- create works;
- list works;
- complete works;
- delete works;
- malformed input is handled safely;
- data persists across restart;
- automated tests pass;
- README start/test instructions work;
- generated artifacts stay within the benchmark workspace.

## Fair comparison

The baseline and CAOS must receive equivalent requirements and be verified using the same acceptance criteria. Reset the workspace between runs.

## What to record

`cost_usd`, `input_tokens`, `output_tokens`, `provider_calls`, `duration_ms`, `retries`, `handoffs`, `verification_passed`, `task_success_rate`, and failure reason.

## Experimental warning

This benchmark is evidence for this workload only. Do not generalize a single result into a universal claim that CAOS is always cheaper.
