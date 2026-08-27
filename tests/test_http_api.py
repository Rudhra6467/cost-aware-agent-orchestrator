from caos.http_api import PlanningAPI
from caos.planning_service import PlanningService


class Service:
    def request_from_dict(self, payload):
        return payload

    def create_plan(self, request):
        return {"idea": request["idea"], "plans": []}


def test_post_plan_returns_stable_success_shape():
    status, body = PlanningAPI(Service()).post_plan({"idea": "build an app"})
    assert status == 200
    assert body == {"idea": "build an app", "plans": []}


def test_post_plan_maps_invalid_request_to_400():
    class Bad:
        def request_from_dict(self, payload):
            raise ValueError("Idea is required")
    status, body = PlanningAPI(Bad()).post_plan({})
    assert status == 400
    assert body["error"] == "invalid_request"
