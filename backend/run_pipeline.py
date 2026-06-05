import argparse
import subprocess
import sys

from config import BASE_DIR


BACKEND_DIR = BASE_DIR / "backend"


CORE_PIPELINE_STEPS = [
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


LLM_PIPELINE_STEPS = [
    {
        "name": "LLM executive summary üretimi",
        "script": "generate_llm_summary.py",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the AI Revenue Operations Copilot pipeline."
    )

    parser.add_argument(
        "--with-llm",
        action="store_true",
        help="Run optional LLM enrichment step after the core deterministic pipeline.",
    )

    return parser.parse_args()


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


def run_steps(steps: list[dict]) -> None:
    for step in steps:
        run_step(step["name"], step["script"])


def print_generated_outputs(with_llm: bool) -> None:
    print("\nGenerated outputs:")
    print("- outputs/kpi_summary.json")
    print("- outputs/anomaly_report.json")
    print("- outputs/action_recommendations.json")
    print("- outputs/weekly_revenue_report.md")

    if with_llm:
        print("- outputs/llm_executive_summary.md")


def main() -> None:
    args = parse_args()

    print("=" * 80)
    print("AI REVENUE OPS COPILOT - PIPELINE STARTED")
    print("=" * 80)

    print("\nRunning core deterministic pipeline...\n")
    run_steps(CORE_PIPELINE_STEPS)

    if args.with_llm:
        print("\nRunning optional LLM enrichment layer...\n")
        run_steps(LLM_PIPELINE_STEPS)
    else:
        print("\nSkipping optional LLM enrichment layer.")
        print("Use '--with-llm' to generate outputs/llm_executive_summary.md.")

    print("=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print_generated_outputs(with_llm=args.with_llm)


if __name__ == "__main__":
    main()