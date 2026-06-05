from datetime import datetime
import json

from llm_provider import generate_text
from utils import load_json, save_text


def build_llm_prompt(
    kpi_summary: dict,
    anomaly_report: dict,
    action_recommendations: dict,
) -> str:
    return f"""
You are a senior Revenue Operations analyst.

Your task is to write a concise executive summary for a weekly B2B revenue operations report.

Use only the structured data provided below.
Do not invent numbers.
Do not mention information that is not present in the input data.
Write in a professional business tone.

Required output structure:

# LLM Executive Summary

## Executive Overview

Write 2-3 concise paragraphs summarizing the overall business performance.

## Key Risks

List the most important risks as bullet points.

## Recommended Management Actions

List the most important management actions as bullet points.

## Notes

Mention that this summary was generated from structured KPI, anomaly, and action recommendation outputs.

Input data:

KPI Summary:
{json.dumps(kpi_summary, indent=2, ensure_ascii=False)}

Anomaly Report:
{json.dumps(anomaly_report, indent=2, ensure_ascii=False)}

Action Recommendations:
{json.dumps(action_recommendations, indent=2, ensure_ascii=False)}
""".strip()


def add_metadata(summary: str) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""---
Generated at: {generated_at}
Source files:
- outputs/kpi_summary.json
- outputs/anomaly_report.json
- outputs/action_recommendations.json
---

{summary}
"""


def main() -> None:
    kpi_summary = load_json("kpi_summary.json")
    anomaly_report = load_json("anomaly_report.json")
    action_recommendations = load_json("action_recommendations.json")

    prompt = build_llm_prompt(
        kpi_summary=kpi_summary,
        anomaly_report=anomaly_report,
        action_recommendations=action_recommendations,
    )

    llm_summary = generate_text(prompt)
    final_summary = add_metadata(llm_summary)

    output_path = save_text("llm_executive_summary.md", final_summary)

    print(f"LLM executive summary oluşturuldu: {output_path}")


if __name__ == "__main__":
    main()