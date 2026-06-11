from fastapi import FastAPI

from backend.config import OUTPUT_DIR, OUTPUT_FILES


app = FastAPI(
    title="AI Revenue Operations Copilot API",
    version="0.3.0",
    description="API layer for the AI Revenue Operations & Reporting Copilot.",
)


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "ai-revenue-ops-copilot",
    }


@app.get("/pipeline/status")
def pipeline_status() -> dict:
    output_status = {}

    for output_name, file_name in OUTPUT_FILES.items():
        output_status[output_name] = (OUTPUT_DIR / file_name).exists()

    return {
        "status": "ok",
        "outputs": output_status,
    }