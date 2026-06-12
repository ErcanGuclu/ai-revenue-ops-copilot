import subprocess
import sys
from typing import Any

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


def get_output_status() -> dict[str, bool]:
    output_status = {}

    for output_name, file_name in OUTPUT_FILES.items():
        output_status[output_name] = (OUTPUT_DIR / file_name).exists()

    return output_status


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


def determine_pipeline_mode(request: PipelineRunRequest) -> str:
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


@app.get("/pipeline/status")
def pipeline_status() -> dict[str, Any]:
    return {
        "status": "ok",
        "outputs": get_output_status(),
    }


@app.post("/pipeline/run")
def run_pipeline(request: PipelineRunRequest | None = None) -> dict[str, Any]:
    if request is None:
        request = PipelineRunRequest()

    if request.check_llm_quality and not request.with_llm:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": "Invalid pipeline run request.",
                "details": "`check_llm_quality` requires `with_llm` to be true.",
            },
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

        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Pipeline failed.",
                "details": error_details,
            },
        )

    return {
        "status": "success",
        "message": "Pipeline completed successfully.",
        "mode": determine_pipeline_mode(request),
        "outputs": get_output_status(),
    }