import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

load_dotenv(BASE_DIR / ".env")


INPUT_FILES = {
    "sales_pipeline": "sales_pipeline.csv",
    "marketing_leads": "marketing_leads.csv",
    "weekly_targets": "weekly_targets.csv",
}


OUTPUT_FILES = {
    "kpi_summary": "kpi_summary.json",
    "anomaly_report": "anomaly_report.json",
    "action_recommendations": "action_recommendations.json",
    "weekly_revenue_report": "weekly_revenue_report.md",
    "llm_executive_summary": "llm_executive_summary.md",
    "llm_quality_report": "llm_quality_report.json",
}


ANOMALY_THRESHOLDS = {
    "revenue_achievement_rate_high_risk": 70,
    "new_leads_achievement_rate_high_risk": 70,
    "pipeline_value_achievement_rate_medium_risk": 80,
    "high_value_deal_threshold": 50_000,
    "low_probability_threshold": 50,
    "notable_lost_deal_value_threshold": 30_000,
    "low_quality_lead_score_threshold": 60,
}

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
