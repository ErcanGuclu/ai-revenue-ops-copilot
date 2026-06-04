import sys
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
sys.path.append(str(BACKEND_DIR))


from config import (  # noqa: E402
    ANOMALY_THRESHOLDS,
    DATA_DIR,
    INPUT_FILES,
    OUTPUT_DIR,
    OUTPUT_FILES,
)


def test_data_directory_exists():
    assert DATA_DIR.exists()


def test_output_directory_exists():
    assert OUTPUT_DIR.exists()


def test_input_files_exist():
    expected_keys = {
        "sales_pipeline",
        "marketing_leads",
        "weekly_targets",
    }

    assert set(INPUT_FILES.keys()) == expected_keys

    for file_name in INPUT_FILES.values():
        file_path = DATA_DIR / file_name
        assert file_path.exists()


def test_output_files_config_contains_expected_keys():
    expected_keys = {
        "kpi_summary",
        "anomaly_report",
        "action_recommendations",
        "weekly_revenue_report",
    }

    assert set(OUTPUT_FILES.keys()) == expected_keys


def test_anomaly_thresholds_contains_expected_keys():
    expected_keys = {
        "revenue_achievement_rate_high_risk",
        "new_leads_achievement_rate_high_risk",
        "pipeline_value_achievement_rate_medium_risk",
        "high_value_deal_threshold",
        "low_probability_threshold",
        "notable_lost_deal_value_threshold",
        "low_quality_lead_score_threshold",
    }

    assert set(ANOMALY_THRESHOLDS.keys()) == expected_keys


def test_anomaly_threshold_values_are_positive_numbers():
    for value in ANOMALY_THRESHOLDS.values():
        assert isinstance(value, int | float)
        assert value > 0