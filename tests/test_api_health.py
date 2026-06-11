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


def test_pipeline_run_endpoint_runs_core_pipeline():
    response = client.post("/pipeline/run")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Core pipeline completed successfully."
    assert response_json["mode"] == "core"

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

    assert response_json["outputs"]["kpi_summary"] is True
    assert response_json["outputs"]["anomaly_report"] is True
    assert response_json["outputs"]["action_recommendations"] is True
    assert response_json["outputs"]["weekly_revenue_report"] is True