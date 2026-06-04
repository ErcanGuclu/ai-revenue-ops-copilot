import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def test_pipeline_runs_successfully():
    pipeline_script = BACKEND_DIR / "run_pipeline.py"

    result = subprocess.run(
        [sys.executable, str(pipeline_script)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "PIPELINE COMPLETED SUCCESSFULLY" in result.stdout


def test_pipeline_generates_expected_output_files():
    expected_output_files = [
        "kpi_summary.json",
        "anomaly_report.json",
        "action_recommendations.json",
        "weekly_revenue_report.md",
    ]

    for file_name in expected_output_files:
        file_path = OUTPUT_DIR / file_name
        assert file_path.exists(), f"Missing output file: {file_path}"