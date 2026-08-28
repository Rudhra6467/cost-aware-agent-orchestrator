"""Concrete stdlib HTTP server for the CAOS planning endpoint.

Kept dependency-free so the first runnable vertical slice can operate at $0.
Production deployments can replace the transport without changing domain code.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .api_schema import validate_plan_request, validate_plan_response
from .http_api import PlanningAPI


WEB_INDEX = Path(__file__).resolve().parents[2] / "web" / "index.html"


class CAOSRequestHandler(BaseHTTPRequestHandler):
    api: PlanningAPI

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                body = WEB_INDEX.read_bytes()
            except OSError as exc:
                self._write(500, {"error": "web_ui_unavailable", "message": str(exc)})
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self._write(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/api/v1/plan":
            self._write(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            payload = validate_plan_request(payload)
            status, body = self.api.post_plan(payload)
            if status == 200:
                validate_plan_response(body)
            self._write(status, body)
        except (ValueError, json.JSONDecodeError) as exc:
            self._write(400, {"error": "invalid_request", "message": str(exc)})
        except Exception as exc:
            self._write(500, {"error": "internal_error", "message": str(exc)})

    def _write(self, status: int, body: dict):
        encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def create_server(api: PlanningAPI, host: str = "127.0.0.1", port: int = 8080):
    class Handler(CAOSRequestHandler):
        pass
    Handler.api = api
    return ThreadingHTTPServer((host, port), Handler)
