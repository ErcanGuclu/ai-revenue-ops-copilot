from fastapi.testclient import TestClient

from backend.api import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ai-revenue-ops-copilot",
    }


def test_pipeline_status_endpoint_returns_output_status():
    response = client.get("/pipeline/status")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["status"] == "ok"

    expected_output_keys = {
        "kpi_summary",
        "anomaly_report",
        "action_recommendations",
        "weekly_revenue_report",
        "llm_executive_summary",
        "llm_quality_report",
    }

    assert set(response_json["outputs"].keys()) == expected_output_keys

    for output_exists in response_json["outputs"].values():
        assert isinstance(output_exists, bool)