from backend.api_models import (
    PipelineErrorDetail,
    PipelineOutputsStatus,
    PipelineRunRequest,
    PipelineRunSuccessResponse,
    PipelineStatusResponse,
)


def build_sample_outputs_status() -> PipelineOutputsStatus:
    return PipelineOutputsStatus(
        kpi_summary=True,
        anomaly_report=True,
        action_recommendations=True,
        weekly_revenue_report=True,
        llm_executive_summary=False,
        llm_quality_report=False,
    )


def test_pipeline_run_request_defaults_to_core_mode():
    request = PipelineRunRequest()

    assert request.with_llm is False
    assert request.check_llm_quality is False


def test_pipeline_outputs_status_model_contains_expected_fields():
    outputs = build_sample_outputs_status()

    assert outputs.kpi_summary is True
    assert outputs.anomaly_report is True
    assert outputs.action_recommendations is True
    assert outputs.weekly_revenue_report is True
    assert outputs.llm_executive_summary is False
    assert outputs.llm_quality_report is False


def test_pipeline_status_response_model():
    response = PipelineStatusResponse(
        status="ok",
        outputs=build_sample_outputs_status(),
    )

    assert response.status == "ok"
    assert response.outputs.kpi_summary is True


def test_pipeline_run_success_response_model():
    response = PipelineRunSuccessResponse(
        status="success",
        message="Pipeline completed successfully.",
        mode="core",
        outputs=build_sample_outputs_status(),
    )

    assert response.status == "success"
    assert response.message == "Pipeline completed successfully."
    assert response.mode == "core"


def test_pipeline_error_detail_model():
    error = PipelineErrorDetail(
        status="error",
        message="Invalid pipeline run request.",
        details="`check_llm_quality` requires `with_llm` to be true.",
    )

    assert error.status == "error"
    assert error.message == "Invalid pipeline run request."
    assert error.details == "`check_llm_quality` requires `with_llm` to be true."