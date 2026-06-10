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


LLM_QUALITY_CHECK_STEPS = [
    {
        "name": "LLM output quality check",
        "script": "check_llm_output_quality.py",
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

    parser.add_argument(
        "--check-llm-quality",
        action="store_true",
        help="Run LLM output quality check after generating the optional LLM summary.",
    )

    args = parser.parse_args()

    if args.check_llm_quality and not args.with_llm:
        parser.error("'--check-llm-quality' requires '--with-llm'.")

    return args


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


def print_generated_outputs(with_llm: bool, check_llm_quality: bool) -> None:
    print("\nGenerated outputs:")
    print("- outputs/kpi_summary.json")
    print("- outputs/anomaly_report.json")
    print("- outputs/action_recommendations.json")
    print("- outputs/weekly_revenue_report.md")

    if with_llm:
        print("- outputs/llm_executive_summary.md")

    if check_llm_quality:
        print("- outputs/llm_quality_report.json")


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

        if args.check_llm_quality:
            print("\nRunning optional LLM output quality check...\n")
            run_steps(LLM_QUALITY_CHECK_STEPS)
        else:
            print("\nSkipping LLM output quality check.")
            print(
                "Use '--with-llm --check-llm-quality' to generate "
                "outputs/llm_quality_report.json."
            )
    else:
        print("\nSkipping optional LLM enrichment layer.")
        print("Use '--with-llm' to generate outputs/llm_executive_summary.md.")
        print("LLM quality check is also skipped because LLM summary was not generated.")

    print("=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print_generated_outputs(
        with_llm=args.with_llm,
        check_llm_quality=args.check_llm_quality,
    )


if __name__ == "__main__":
    main()