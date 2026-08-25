# M1 — First Agent Implementation Specification

## Objective

Prove the smallest useful CAOS loop before introducing provider-specific complexity.

```text
User request
  -> Task planner
  -> Agent registry
  -> Cost-aware selector
  -> Agent executor
  -> Normalized execution result
  -> State store
  -> Verification
```

## Boundaries

### Git/GitHub
Owns software artifacts and version history.

### SQLite
Owns structured orchestration telemetry: tasks, executions, costs, failures and later handoffs.

### Agent adapter
Owns communication with a concrete LLM/provider. CAOS core must not depend on one provider SDK.

### Selector
Makes transparent routing decisions from agent profile + task requirements + remaining budget.

## M1 acceptance criteria

- [x] Python package can be installed.
- [x] Tasks have a normalized representation.
- [x] Agents have capability/economic profiles.
- [x] A deterministic baseline selector exists.
- [x] Selection respects context and budget constraints.
- [x] Execution state can be persisted in SQLite.
- [x] Agent execution has a provider-neutral adapter boundary.
- [x] Automated tests run in GitHub Actions.
- [ ] Real LLM provider adapter.
- [ ] Real code-generation task.
- [ ] Generated project committed to GitHub by CAOS.
- [ ] Build/test verification of generated project.

## Design rule

Do not add multi-agent autonomy until the single-agent execution path is observable, testable and recoverable.
