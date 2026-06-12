import subprocess
import sys
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.config import BASE_DIR, OUTPUT_DIR, OUTPUT_FILES


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


def get_output_status() -> PipelineOutputsStatus:
    output_status = {}

    for output_name, file_name in OUTPUT_FILES.items():
        output_status[output_name] = (OUTPUT_DIR / file_name).exists()

    return PipelineOutputsStatus(**output_status)


def build_pipeline_command(request: PipelineRunRequest) -> list[str]:
    command = [
        sys.executable,
        str(BASE_DIR / "backend" / "run_pipeline.py"),
    ]

    if request.with_llm:
        command.append("--with-llm")

    if request.check_llm_quality:
        command.append("--check-llm-quality")

    return command


def determine_pipeline_mode(
    request: PipelineRunRequest,
) -> Literal["core", "core_with_llm", "core_with_llm_and_quality_check"]:
    if request.with_llm and request.check_llm_quality:
        return "core_with_llm_and_quality_check"

    if request.with_llm:
        return "core_with_llm"

    return "core"


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
        outputs=get_output_status(),
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

    command = build_pipeline_command(request)

    try:
        subprocess.run(
            command,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True,
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
        mode=determine_pipeline_mode(request),
        outputs=get_output_status(),
    )