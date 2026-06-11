import subprocess
import sys

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.config import BASE_DIR, OUTPUT_DIR, OUTPUT_FILES


app = FastAPI(
    title="AI Revenue Operations Copilot API",
    version="0.3.0",
    description="API layer for the AI Revenue Operations & Reporting Copilot.",
)


def get_output_status() -> dict[str, bool]:
    output_status = {}

    for output_name, file_name in OUTPUT_FILES.items():
        output_status[output_name] = (OUTPUT_DIR / file_name).exists()

    return output_status


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "ai-revenue-ops-copilot",
    }


@app.get("/pipeline/status")
def pipeline_status() -> dict:
    return {
        "status": "ok",
        "outputs": get_output_status(),
    }


@app.post("/pipeline/run", response_model=None)
def run_pipeline():
    pipeline_script = BASE_DIR / "backend" / "run_pipeline.py"

    try:
        subprocess.run(
            [sys.executable, str(pipeline_script)],
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

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Core pipeline failed.",
                "details": error_details,
            },
        )

    return {
        "status": "success",
        "message": "Core pipeline completed successfully.",
        "mode": "core",
        "outputs": get_output_status(),
    }