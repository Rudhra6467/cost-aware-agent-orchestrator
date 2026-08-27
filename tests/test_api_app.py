import json
from caos.api_app import create_server
from caos.http_api import PlanningAPI


class Service:
    def request_from_dict(self, payload):
        return payload
    def create_plan(self, request):
        return {
            "idea": request["idea"], "blueprint_summary": "fixture",
            "assumptions": [], "plans": [], "recommendation": "zero-cost",
            "reasons": [], "explanation": "fixture", "next_actions": ["BUILD", "DIY"]
        }


def test_concrete_server_serves_plan_endpoint():
    server = create_server(PlanningAPI(Service()), port=0)
    try:
        import http.client
        server.server_activate()
        host, port = server.server_address
        conn = http.client.HTTPConnection(host, port)
        conn.request("POST", "/api/v1/plan", json.dumps({"idea": "test"}), {"Content-Type": "application/json"})
        response = conn.getresponse()
        body = json.loads(response.read())
        assert response.status == 200
        assert body["idea"] == "test"
        conn.close()
    finally:
        server.server_close()


def test_unknown_route_returns_404():
    server = create_server(PlanningAPI(Service()), port=0)
    try:
        import http.client
        host, port = server.server_address
        conn = http.client.HTTPConnection(host, port)
        conn.connect()
        conn.request("POST", "/nope", "{}", {"Content-Type": "application/json"})
        response = conn.getresponse()
        assert response.status == 404
        conn.close()
    finally:
        server.server_close()
