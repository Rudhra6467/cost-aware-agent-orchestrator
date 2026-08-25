"""Optional OpenAI-compatible HTTP agent adapter.

This adapter keeps the CAOS core independent from a particular provider. The
provider must expose a compatible chat-completions endpoint. Credentials are
read from the environment and are never stored in the repository.
"""

import json
import os
from urllib import request

from .agents import AgentExecutor
from .models import ExecutionResult, Task, TaskStatus


class OpenAICompatibleExecutor(AgentExecutor):
    """Execute a CAOS task against an OpenAI-compatible chat API."""

    def __init__(
        self,
        agent_id: str,
        model: str,
        base_url: str,
        api_key: str,
        timeout_seconds: int = 120,
    ) -> None:
        self.agent_id = agent_id
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_environment(cls) -> "OpenAICompatibleExecutor":
        """Build an adapter from CAOS_API_KEY/BASE_URL/MODEL environment variables."""
        api_key = os.environ.get("CAOS_API_KEY")
        model = os.environ.get("CAOS_MODEL")
        base_url = os.environ.get("CAOS_API_BASE_URL")
        agent_id = os.environ.get("CAOS_AGENT_ID", "http-agent")
        if not api_key or not model or not base_url:
            raise ValueError(
                "CAOS_API_KEY, CAOS_MODEL and CAOS_API_BASE_URL must be configured."
            )
        return cls(agent_id, model, base_url, api_key)

    def execute(self, task: Task, context: str = "") -> ExecutionResult:
        prompt = task.description
        if context:
            prompt = f"PROJECT CONTEXT:\n{context}\n\nTASK:\n{prompt}"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a software-development worker inside CAOS. "
                        "Return precise, implementation-oriented output."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001 - normalized provider boundary
            return ExecutionResult(
                task_id=task.task_id,
                agent_id=self.agent_id,
                status=TaskStatus.FAILED,
                error=f"Provider request failed: {exc}",
            )

        try:
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            return ExecutionResult(
                task_id=task.task_id,
                agent_id=self.agent_id,
                status=TaskStatus.SUCCEEDED,
                output=content,
                input_tokens=int(usage.get("prompt_tokens", 0)),
                output_tokens=int(usage.get("completion_tokens", 0)),
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            return ExecutionResult(
                task_id=task.task_id,
                agent_id=self.agent_id,
                status=TaskStatus.FAILED,
                error=f"Invalid provider response: {exc}",
            )
