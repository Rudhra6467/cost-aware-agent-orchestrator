from caos.benchmark_harness import execute_harness
from caos.benchmark_manifest import ArtifactExpectation, BenchmarkManifest
from caos.benchmark_runner import BenchmarkTask, ExecutionMeasurement
from caos.benchmark_workspace import BenchmarkWorkspaceManager


def test_harness_runs_tasks_and_verifies_output(tmp_path):
    tasks = [BenchmarkTask("t1", "generate app"), BenchmarkTask("t2", "generate docs")]
    manifest = BenchmarkManifest(
        artifacts=(ArtifactExpectation("app.py"), ArtifactExpectation("README.md")),
        verification_commands=(("python", "app.py"),),
    )

    def executor(task, workspace):
        if task.task_id == "t1":
            (workspace.path / "app.py").write_text("print('ok')")
        else:
            (workspace.path / "README.md").write_text("run app")
        return ExecutionMeasurement(cost=0.0, success=True, latency_ms=10)

    result = execute_harness("run-001", tasks, manifest, executor, BenchmarkWorkspaceManager(tmp_path))
    assert result.passed
    assert len(result.measurements) == 2
    assert result.verification.artifacts_present
