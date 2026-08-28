import http.client

from caos.api_app import create_server
from caos.http_api import PlanningAPI


class Service:
    def request_from_dict(self, payload):
        return payload

    def create_plan(self, request):
        return {
            "idea": request["idea"],
            "blueprint_summary": "fixture",
            "assumptions": [],
            "plans": [],
            "recommendation": "zero-cost",
            "reasons": [],
            "explanation": "fixture",
            "next_actions": ["BUILD", "DIY"],
        }


def test_browser_vertical_slice_serves_ui_and_plan_endpoint():
    server = create_server(PlanningAPI(Service()), port=0)
    try:
        host, port = server.server_address
        server.server_activate()
        server_thread = __import__("threading").Thread(target=server.serve_forever, daemon=True)
        server_thread.start()

        conn = http.client.HTTPConnection(host, port)
        conn.request("GET", "/")
        response = conn.getresponse()
        html = response.read().decode("utf-8")
        assert response.status == 200
        assert "CAOS" in html
        assert "api/v1/plan" in html
        conn.close()

        conn = http.client.HTTPConnection(host, port)
        conn.request(
            "POST",
            "/api/v1/plan",
            '{"idea":"test"}',
            {"Content-Type": "application/json"},
        )
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        assert response.status == 200
        assert '"idea":"test"' in body
        conn.close()
    finally:
        server.shutdown()
        server.server_close()
