from caos.agents import MockAgentExecutor
from caos.models import TaskStatus, Task


def test_mock_executor_returns_normalized_result():
    task = Task(task_id="t1", description="build a hello world app")
    result = MockAgentExecutor().execute(task)
    assert result.status == TaskStatus.SUCCEEDED
    assert result.task_id == "t1"
    assert result.output_tokens > 0
