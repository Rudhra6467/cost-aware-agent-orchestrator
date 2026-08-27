import pytest

from caos.api_schema import validate_plan_request, validate_plan_response


def test_valid_request_is_normalized():
    value = validate_plan_request({"idea": "  build app  ", "constraints": {"budget": 5}})
    assert value["idea"] == "build app"


@pytest.mark.parametrize("payload", [None, {}, {"idea": ""}, {"idea": "x", "constraints": []}, {"idea": "x", "constraints": {"budget": -1}}, {"idea": "x", "constraints": {"quality_threshold": 2}}])
def test_invalid_requests_are_rejected(payload):
    with pytest.raises(ValueError):
        validate_plan_request(payload)


def test_response_contract_requires_expected_fields():
    with pytest.raises(ValueError):
        validate_plan_response({})


def test_response_actions_are_whitelisted():
    body = {k: [] for k in ("assumptions", "plans", "reasons", "next_actions")}
    body.update({"idea": "x", "blueprint_summary": "x", "recommendation": "x", "explanation": "x"})
    body["next_actions"] = ["DELETE_EVERYTHING"]
    with pytest.raises(ValueError):
        validate_plan_response(body)
