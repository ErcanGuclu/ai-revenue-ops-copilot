import sys

from backend.config import BASE_DIR
from backend.pipeline_service import (
    build_pipeline_command,
    determine_pipeline_mode,
    get_output_status,
)


EXPECTED_OUTPUT_KEYS = {
    "kpi_summary",
    "anomaly_report",
    "action_recommendations",
    "weekly_revenue_report",
    "llm_executive_summary",
    "llm_quality_report",
}


def test_get_output_status_returns_expected_keys_and_boolean_values():
    output_status = get_output_status()

    assert set(output_status.keys()) == EXPECTED_OUTPUT_KEYS

    for output_exists in output_status.values():
        assert isinstance(output_exists, bool)


def test_build_pipeline_command_for_core_mode():
    command = build_pipeline_command()

    assert command == [
        sys.executable,
        str(BASE_DIR / "backend" / "run_pipeline.py"),
    ]


def test_build_pipeline_command_with_llm():
    command = build_pipeline_command(with_llm=True)

    assert command == [
        sys.executable,
        str(BASE_DIR / "backend" / "run_pipeline.py"),
        "--with-llm",
    ]


def test_build_pipeline_command_with_llm_quality_check():
    command = build_pipeline_command(
        with_llm=True,
        check_llm_quality=True,
    )

    assert command == [
        sys.executable,
        str(BASE_DIR / "backend" / "run_pipeline.py"),
        "--with-llm",
        "--check-llm-quality",
    ]


def test_determine_pipeline_mode_for_core():
    assert determine_pipeline_mode() == "core"


def test_determine_pipeline_mode_with_llm():
    assert determine_pipeline_mode(with_llm=True) == "core_with_llm"


def test_determine_pipeline_mode_with_llm_quality_check():
    assert (
        determine_pipeline_mode(
            with_llm=True,
            check_llm_quality=True,
        )
        == "core_with_llm_and_quality_check"
    )