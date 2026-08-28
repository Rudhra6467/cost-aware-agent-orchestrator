import json
import threading
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from caos.http_api import CAOSRequestHandler
from caos.models import AgentProfile
from caos.pipeline import CostAwarePipeline


def make_pipeline():
    return CostAwarePipeline([
        AgentProfile(
            agent_id="free-coder",
            name="Free Coder",
            coding_score=0.80,
            architecture_score=0.60,
            context_window=8_000,
            cost_per_1k_input=0,
            cost_per_1k_output=0,
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

        body = json.dumps({"idea": "Build a simple fitness tracking application for home workouts"})
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
