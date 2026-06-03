from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


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
}