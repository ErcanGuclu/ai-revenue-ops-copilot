import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def run_pipeline_command(args: list[str] | None = None) -> subprocess.CompletedProcess:
    pipeline_script = BACKEND_DIR / "run_pipeline.py"
    command = [sys.executable, str(pipeline_script)]

    if args:
        command.extend(args)

    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_core_pipeline_runs_successfully():
    result = run_pipeline_command()

    assert result.returncode == 0, result.stderr
    assert "PIPELINE COMPLETED SUCCESSFULLY" in result.stdout
    assert "Skipping optional LLM enrichment layer." in result.stdout
    assert (
        "LLM quality check is also skipped because LLM summary was not generated."
        in result.stdout
    )


def test_core_pipeline_generates_expected_output_files():
    expected_output_files = [
        "kpi_summary.json",
        "anomaly_report.json",
        "action_recommendations.json",
        "weekly_revenue_report.md",
    ]

    for file_name in expected_output_files:
        file_path = OUTPUT_DIR / file_name
        assert file_path.exists(), f"Missing output file: {file_path}"


def test_core_pipeline_does_not_list_llm_outputs_by_default():
    result = run_pipeline_command()

    assert result.returncode == 0, result.stderr
    assert "- outputs/llm_executive_summary.md" not in result.stdout
    assert "- outputs/llm_quality_report.json" not in result.stdout


def test_llm_quality_check_requires_llm_flag():
    result = run_pipeline_command(["--check-llm-quality"])

    assert result.returncode != 0
    assert "'--check-llm-quality' requires '--with-llm'." in result.stderr