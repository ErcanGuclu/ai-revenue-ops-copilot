import subprocess
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.pipeline_service import (
    determine_pipeline_mode,
    get_output_status,
    run_pipeline_process,
)


app = FastAPI(
    title="AI Revenue Operations Copilot API",
    version="0.3.0",
    description="API layer for the AI Revenue Operations & Reporting Copilot.",
)


class PipelineRunRequest(BaseModel):
    with_llm: bool = False
    check_llm_quality: bool = False


class PipelineOutputsStatus(BaseModel):
    kpi_summary: bool
    anomaly_report: bool
    action_recommendations: bool
    weekly_revenue_report: bool
    llm_executive_summary: bool
    llm_quality_report: bool


class PipelineStatusResponse(BaseModel):
    status: Literal["ok"]
    outputs: PipelineOutputsStatus


class PipelineRunSuccessResponse(BaseModel):
    status: Literal["success"]
    message: str
    mode: Literal[
        "core",
        "core_with_llm",
        "core_with_llm_and_quality_check",
    ]
    outputs: PipelineOutputsStatus


class PipelineErrorDetail(BaseModel):
    status: Literal["error"]
    message: str
    details: str


def build_outputs_status_response() -> PipelineOutputsStatus:
    return PipelineOutputsStatus(**get_output_status())


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ai-revenue-ops-copilot",
    }


@app.get("/pipeline/status", response_model=PipelineStatusResponse)
def pipeline_status() -> PipelineStatusResponse:
    return PipelineStatusResponse(
        status="ok",
        outputs=build_outputs_status_response(),
    )


@app.post("/pipeline/run", response_model=PipelineRunSuccessResponse)
def run_pipeline(
    request: PipelineRunRequest | None = None,
) -> PipelineRunSuccessResponse:
    if request is None:
        request = PipelineRunRequest()

    if request.check_llm_quality and not request.with_llm:
        error_detail = PipelineErrorDetail(
            status="error",
            message="Invalid pipeline run request.",
            details="`check_llm_quality` requires `with_llm` to be true.",
        )

        raise HTTPException(
            status_code=400,
            detail=error_detail.model_dump(),
        )

    try:
        run_pipeline_process(
            with_llm=request.with_llm,
            check_llm_quality=request.check_llm_quality,
        )

    except subprocess.CalledProcessError as error:
        error_details = (
            error.stderr.strip()
            or error.stdout.strip()
            or "Unknown pipeline execution error."
        )

        error_detail = PipelineErrorDetail(
            status="error",
            message="Pipeline failed.",
            details=error_details,
        )

        raise HTTPException(
            status_code=500,
            detail=error_detail.model_dump(),
        )

    return PipelineRunSuccessResponse(
        status="success",
        message="Pipeline completed successfully.",
        mode=determine_pipeline_mode(
            with_llm=request.with_llm,
            check_llm_quality=request.check_llm_quality,
        ),
        outputs=build_outputs_status_response(),
    )