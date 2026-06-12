import subprocess
import sys
from typing import Literal

from backend.config import BASE_DIR, OUTPUT_DIR, OUTPUT_FILES


PipelineMode = Literal[
    "core",
    "core_with_llm",
    "core_with_llm_and_quality_check",
]


def get_output_status() -> dict[str, bool]:
    output_status = {}

    for output_name, file_name in OUTPUT_FILES.items():
        output_status[output_name] = (OUTPUT_DIR / file_name).exists()

    return output_status


def build_pipeline_command(
    with_llm: bool = False,
    check_llm_quality: bool = False,
) -> list[str]:
    command = [
        sys.executable,
        str(BASE_DIR / "backend" / "run_pipeline.py"),
    ]

    if with_llm:
        command.append("--with-llm")

    if check_llm_quality:
        command.append("--check-llm-quality")

    return command


def determine_pipeline_mode(
    with_llm: bool = False,
    check_llm_quality: bool = False,
) -> PipelineMode:
    if with_llm and check_llm_quality:
        return "core_with_llm_and_quality_check"

    if with_llm:
        return "core_with_llm"

    return "core"


def run_pipeline_process(
    with_llm: bool = False,
    check_llm_quality: bool = False,
) -> None:
    command = build_pipeline_command(
        with_llm=with_llm,
        check_llm_quality=check_llm_quality,
    )

    subprocess.run(
        command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        check=True,
    )