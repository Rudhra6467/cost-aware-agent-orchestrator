import json
import threading
from http.client import HTTPConnection

from caos.http_api import CAOSRequestHandler
from caos.models import AgentProfile
from caos.pipeline import CostAwarePipeline
from http.server import ThreadingHTTPServer


def make_pipeline():
    return CostAwarePipeline([
        AgentProfile(
            agent_id="free-coder",
            name="Free Coder",
            capabilities={"coding": 0.8, "architecture": 0.6},
            context_window=8000,
            input_cost_per_million=0,
            output_cost_per_million=0,
            reliability=0.85,
            availability=0.95,
        ),
    ])


def test_health_and_plan_http_contract():
    CAOSRequestHandler.pipeline_factory = make_pipeline
    server = ThreadingHTTPServer(("127.0.0.1", 0), CAOSRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        conn = HTTPConnection("127.0.0.1", server.server_port)
        conn.request("GET", "/health")
        response = conn.getresponse()
        assert response.status == 200
        assert json.loads(response.read())["status"] == "ok"

        body = json.dumps({"idea": "Build a simple fitness tracking application"})
        conn.request("POST", "/api/plan", body=body, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        payload = json.loads(response.read())
        assert response.status == 200
        assert payload["recommendation"]["action"] == "BUILD"
        assert payload["recommendation"]["resource"] == "Free Coder"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
