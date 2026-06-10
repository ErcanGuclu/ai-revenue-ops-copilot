from utils import load_json, load_text, save_json


REQUIRED_SECTIONS = [
    "# LLM Executive Summary",
    "## Executive Overview",
    "## Key Risks",
    "## Recommended Management Actions",
    "## Notes",
]

REQUIRED_SOURCE_REFERENCES = [
    "outputs/kpi_summary.json",
    "outputs/anomaly_report.json",
    "outputs/action_recommendations.json",
]

RISKY_PHRASES = [
    "I do not have access",
    "I don't have access",
    "cannot access",
    "not provided in the data",
    "as an AI language model",
    "I cannot verify",
]


def add_check(
    checks: list[dict],
    name: str,
    passed: bool,
    message: str,
) -> None:
    checks.append(
        {
            "check_name": name,
            "passed": passed,
            "message": message,
        }
    )


def check_required_sections(summary_text: str, checks: list[dict]) -> None:
    missing_sections = [
        section for section in REQUIRED_SECTIONS if section not in summary_text
    ]

    add_check(
        checks,
        name="required_sections",
        passed=not missing_sections,
        message=(
            "All required sections are present."
            if not missing_sections
            else f"Missing sections: {missing_sections}"
        ),
    )


def check_source_references(summary_text: str, checks: list[dict]) -> None:
    missing_references = [
        reference
        for reference in REQUIRED_SOURCE_REFERENCES
        if reference not in summary_text
    ]

    add_check(
        checks,
        name="source_references",
        passed=not missing_references,
        message=(
            "All source references are present."
            if not missing_references
            else f"Missing source references: {missing_references}"
        ),
    )


def check_minimum_length(summary_text: str, checks: list[dict]) -> None:
    minimum_length = 500
    passed = len(summary_text.strip()) >= minimum_length

    add_check(
        checks,
        name="minimum_length",
        passed=passed,
        message=(
            f"Summary length is acceptable: {len(summary_text)} characters."
            if passed
            else f"Summary is too short: {len(summary_text)} characters."
        ),
    )


def check_risky_phrases(summary_text: str, checks: list[dict]) -> None:
    found_phrases = [
        phrase for phrase in RISKY_PHRASES if phrase.lower() in summary_text.lower()
    ]

    add_check(
        checks,
        name="risky_phrases",
        passed=not found_phrases,
        message=(
            "No risky LLM phrases found."
            if not found_phrases
            else f"Risky phrases found: {found_phrases}"
        ),
    )


def check_structured_inputs_exist(checks: list[dict]) -> None:
    required_json_files = [
        "kpi_summary.json",
        "anomaly_report.json",
        "action_recommendations.json",
    ]

    missing_or_invalid_files = []

    for file_name in required_json_files:
        try:
            load_json(file_name)
        except Exception as error:
            missing_or_invalid_files.append(f"{file_name}: {error}")

    add_check(
        checks,
        name="structured_inputs",
        passed=not missing_or_invalid_files,
        message=(
            "All structured input JSON files are readable."
            if not missing_or_invalid_files
            else f"Missing or invalid JSON files: {missing_or_invalid_files}"
        ),
    )


def calculate_quality_status(checks: list[dict]) -> str:
    failed_checks = [check for check in checks if not check["passed"]]

    if not failed_checks:
        return "passed"

    return "failed"


def build_quality_report(summary_text: str) -> dict:
    checks = []

    check_structured_inputs_exist(checks)
    check_required_sections(summary_text, checks)
    check_source_references(summary_text, checks)
    check_minimum_length(summary_text, checks)
    check_risky_phrases(summary_text, checks)

    status = calculate_quality_status(checks)

    return {
        "status": status,
        "check_count": len(checks),
        "passed_count": len([check for check in checks if check["passed"]]),
        "failed_count": len([check for check in checks if not check["passed"]]),
        "checks": checks,
    }


def print_quality_report(report: dict) -> None:
    print("=" * 70)
    print("LLM OUTPUT QUALITY CHECK")
    print("=" * 70)

    print(f"Status: {report['status']}")
    print(f"Passed checks: {report['passed_count']}/{report['check_count']}")
    print()

    for check in report["checks"]:
        status_label = "PASSED" if check["passed"] else "FAILED"
        print(f"[{status_label}] {check['check_name']}")
        print(f"  {check['message']}")
        print()


def main() -> None:
    summary_text = load_text("llm_executive_summary.md")

    quality_report = build_quality_report(summary_text)

    print_quality_report(quality_report)

    output_path = save_json("llm_quality_report.json", quality_report)
    print(f"LLM kalite raporu oluşturuldu: {output_path}")

    if quality_report["status"] != "passed":
        raise SystemExit("LLM output quality check failed.")


if __name__ == "__main__":
    main()