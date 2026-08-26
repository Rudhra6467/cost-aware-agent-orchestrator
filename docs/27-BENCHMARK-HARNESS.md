# 27 — Benchmark Harness

The Benchmark Harness is the controlled execution boundary for CAOS experiments.

## Lifecycle

1. Create a unique run ID.
2. Reset an isolated workspace.
3. Execute the frozen benchmark task set.
4. Capture per-task cost, success, latency, retries, and handoffs.
5. Verify required artifacts.
6. Run declared verification commands.
7. Produce a structured pass/fail result.

## Design rule

The harness does not decide which provider is cheapest. It measures the outcome of an execution policy. Resource selection remains the responsibility of the optimizer.

## Safety boundary

Generated artifacts are confined to a disposable workspace. Artifact expectations are checked for workspace escape before verification. Future command execution should add explicit allowlists, environment isolation, resource/time limits, and network controls before arbitrary model-generated code is executed.

## Next integration

Connect the harness to the real builder and resource optimizer. Then run the same Benchmark 001 workload through baseline and CAOS policies and persist the results as experimental evidence.
