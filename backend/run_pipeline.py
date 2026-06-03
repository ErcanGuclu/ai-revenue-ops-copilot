from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = BASE_DIR / "backend"


PIPELINE_STEPS = [
    {
        "name": "Veri doğrulama",
        "script": "validate_data.py",
    },
    {
        "name": "KPI hesaplama",
        "script": "calculate_kpis.py",
    },
    {
        "name": "Anomali tespiti",
        "script": "detect_anomalies.py",
    },
    {
        "name": "Aksiyon önerileri üretimi",
        "script": "generate_action_recommendations.py",
    },
    {
        "name": "Markdown yönetici raporu üretimi",
        "script": "generate_report.py",
    },
]


def run_step(step_name: str, script_name: str) -> None:
    script_path = BACKEND_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(f"Pipeline adımı bulunamadı: {script_path}")

    print("=" * 80)
    print(f"RUNNING STEP: {step_name}")
    print("=" * 80)

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        check=True,
    )

    print(f"\nSTEP COMPLETED: {step_name}\n")


def main() -> None:
    print("=" * 80)
    print("AI REVENUE OPS COPILOT - PIPELINE STARTED")
    print("=" * 80)

    for step in PIPELINE_STEPS:
        run_step(step["name"], step["script"])

    print("=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print("\nGenerated outputs:")
    print("- outputs/kpi_summary.json")
    print("- outputs/anomaly_report.json")
    print("- outputs/action_recommendations.json")
    print("- outputs/weekly_revenue_report.md")


if __name__ == "__main__":
    main()