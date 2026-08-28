"""Dependency-free HTTP surface for the CAOS planning contract and web UI."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable

from .planning_api import plan_from_request

WEB_ROOT = Path(__file__).resolve().parents[2] / "web"


class CAOSRequestHandler(BaseHTTPRequestHandler):
    """Expose the planning API and the first CAOS browser experience."""

    pipeline_factory: Callable[[], Any] | None = None

    def _json(self, status: int, body: dict[str, Any]) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _static(self, path: str, content_type: str) -> None:
        file_path = WEB_ROOT / path
        if not file_path.is_file():
            self._json(404, {"error": "Not found"})
            return
        payload = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        if self.path != "/api/plan":
            self._json(404, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            if self.pipeline_factory is None:
                raise RuntimeError("CAOS pipeline is not configured")
            result = plan_from_request(payload, self.pipeline_factory())
            self._json(200, result)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._json(400, {"error": str(exc)})
        except Exception as exc:  # pragma: no cover - defensive HTTP boundary
            self._json(500, {"error": str(exc)})

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        if self.path == "/":
            self._static("index.html", "text/html; charset=utf-8")
            return
        if self.path == "/app.js":
            self._static("app.js", "text/javascript; charset=utf-8")
            return
        if self.path == "/health":
            self._json(200, {"status": "ok", "service": "caos"})
            return
        self._json(404, {"error": "Not found"})

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(pipeline_factory: Callable[[], Any], host: str = "127.0.0.1", port: int = 8080) -> None:
    CAOSRequestHandler.pipeline_factory = pipeline_factory
    server = ThreadingHTTPServer((host, port), CAOSRequestHandler)
    server.serve_forever()
