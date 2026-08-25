import json

from caos.http_agent import OpenAICompatibleExecutor
from caos.models import Task, TaskStatus


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_openai_compatible_adapter_normalizes_response(monkeypatch):
    def fake_urlopen(request, timeout):
        assert request.method == "POST"
        assert request.headers["Authorization"] == "Bearer test-key"
        assert timeout == 120
        return FakeResponse(
            {
                "choices": [{"message": {"content": "hello"}}],
                "usage": {"prompt_tokens": 12, "completion_tokens": 8},
            }
        )

    monkeypatch.setattr("caos.http_agent.request.urlopen", fake_urlopen)

    executor = OpenAICompatibleExecutor(
        agent_id="test-agent",
        model="test-model",
        base_url="https://example.test/v1",
        api_key="test-key",
    )
    result = executor.execute(Task(task_id="t", description="Say hello"))

    assert result.status == TaskStatus.SUCCEEDED
    assert result.output == "hello"
    assert result.total_tokens == 20
