from fastapi.testclient import TestClient

from backend.api import app


client = TestClient(app)


EXPECTED_OUTPUT_KEYS = {
    "kpi_summary",
    "anomaly_report",
    "action_recommendations",
    "weekly_revenue_report",
    "llm_executive_summary",
    "llm_quality_report",
}


def assert_output_status_shape(outputs: dict) -> None:
    assert set(outputs.keys()) == EXPECTED_OUTPUT_KEYS

    for output_exists in outputs.values():
        assert isinstance(output_exists, bool)


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
    assert_output_status_shape(response_json["outputs"])


def test_pipeline_run_endpoint_runs_core_pipeline_without_body():
    response = client.post("/pipeline/run")
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Pipeline completed successfully."
    assert response_json["mode"] == "core"
    assert_output_status_shape(response_json["outputs"])


def test_pipeline_run_endpoint_runs_core_pipeline_with_explicit_body():
    response = client.post(
        "/pipeline/run",
        json={
            "with_llm": False,
            "check_llm_quality": False,
        },
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["status"] == "success"
    assert response_json["message"] == "Pipeline completed successfully."
    assert response_json["mode"] == "core"
    assert_output_status_shape(response_json["outputs"])


def test_pipeline_run_endpoint_rejects_quality_check_without_llm():
    response = client.post(
        "/pipeline/run",
        json={
            "with_llm": False,
            "check_llm_quality": True,
        },
    )
    response_json = response.json()

    assert response.status_code == 400
    assert response_json["detail"]["status"] == "error"
    assert response_json["detail"]["message"] == "Invalid pipeline run request."
    assert (
        response_json["detail"]["details"]
        == "`check_llm_quality` requires `with_llm` to be true."
    )