from pathlib import Path

from caos.agents import MockAgentExecutor
from caos.builder import ControlledBuilder
from caos.models import AgentProfile, Task


def test_controlled_builder_generates_and_verifies(tmp_path: Path):
    agent = AgentProfile("mock", "Mock", coding_score=1.0)
    executor = MockAgentExecutor({"task-1": "FILE: app.py\n```python\nprint('ok')\n```"})
    builder = ControlledBuilder(executor, tmp_path / "project")
    task = Task("task-1", "Create a tiny Python application")

    result = builder.build(task, ["python", "-c", "import pathlib; assert pathlib.Path('app.py').exists()"])
    assert result.passed is True
    assert (tmp_path / "project" / "app.py").exists()
