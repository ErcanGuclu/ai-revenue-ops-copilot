from fastapi import FastAPI


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