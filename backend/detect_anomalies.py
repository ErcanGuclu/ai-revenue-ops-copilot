import pandas as pd

from config import ANOMALY_THRESHOLDS
from utils import load_csv, load_json, save_json


def add_anomaly(anomalies: list[dict], category: str, severity: str, message: str, recommendation: str) -> None:
    anomalies.append(
        {
            "category": category,
            "severity": severity,
            "message": message,
            "recommendation": recommendation,
        }
    )


def detect_target_anomalies(kpi_summary: dict) -> list[dict]:
    anomalies = []
    target_comparison = kpi_summary["target_comparison"]

    revenue = target_comparison["revenue"]
    new_leads = target_comparison["new_leads"]
    conversion_rate = target_comparison["conversion_rate"]
    pipeline_value = target_comparison["pipeline_value"]

    if revenue["achievement_rate"] < ANOMALY_THRESHOLDS["revenue_achievement_rate_high_risk"]:
        add_anomaly(
            anomalies,
            category="Revenue",
            severity="High",
            message=f"Revenue achievement rate is low: {revenue['achievement_rate']:.2f}%",
            recommendation="Review stalled opportunities, accelerate high-probability deals, and check whether closed-won revenue is underreported.",
        )

    if new_leads["achievement_rate"] < ANOMALY_THRESHOLDS["new_leads_achievement_rate_high_risk"]:
        add_anomaly(
            anomalies,
            category="Lead Generation",
            severity="High",
            message=f"New lead achievement rate is low: {new_leads['achievement_rate']:.2f}%",
            recommendation="Review campaign performance and prioritize channels with higher lead quality.",
        )

    if conversion_rate["actual"] < conversion_rate["target"]:
        add_anomaly(
            anomalies,
            category="Conversion Rate",
            severity="Medium",
            message=(
                f"Conversion rate is below target. "
                f"Actual: {conversion_rate['actual']:.2f}%, Target: {conversion_rate['target']:.2f}%"
            ),
            recommendation="Analyze lead qualification criteria and review sales follow-up timing.",
        )

    if pipeline_value["achievement_rate"] < ANOMALY_THRESHOLDS["pipeline_value_achievement_rate_medium_risk"]:
        add_anomaly(
            anomalies,
            category="Pipeline Value",
            severity="Medium",
            message=f"Pipeline value achievement rate is below expected level: {pipeline_value['achievement_rate']:.2f}%",
            recommendation="Increase qualified opportunity generation and review open deal progression.",
        )

    return anomalies


def detect_sales_anomalies(sales_pipeline: pd.DataFrame) -> list[dict]:
    anomalies = []

    sales_pipeline["deal_value"] = pd.to_numeric(sales_pipeline["deal_value"], errors="coerce")
    sales_pipeline["probability"] = pd.to_numeric(sales_pipeline["probability"], errors="coerce")

    high_value_low_probability = sales_pipeline[
        (sales_pipeline["status"].str.lower() == "open")
        & (
            sales_pipeline["deal_value"]
            >= ANOMALY_THRESHOLDS["high_value_deal_threshold"]
        )
        & (
            sales_pipeline["probability"]
            < ANOMALY_THRESHOLDS["low_probability_threshold"]
        )
    ]

    for _, row in high_value_low_probability.iterrows():
        add_anomaly(
            anomalies,
            category="Sales Pipeline",
            severity="Medium",
            message=(
                f"High-value deal has low probability: "
                f"{row['deal_id']} - {row['company_name']} - {row['deal_value']} value, "
                f"{row['probability']}% probability."
            ),
            recommendation="Review blockers for this opportunity and define a next-step action plan.",
        )

    lost_deals = sales_pipeline[sales_pipeline["status"].str.lower() == "lost"]
    lost_value = lost_deals["deal_value"].sum()

    if lost_value >= ANOMALY_THRESHOLDS["notable_lost_deal_value_threshold"]:
        add_anomaly(
            anomalies,
            category="Lost Deals",
            severity="Medium",
            message=f"Lost deal value is notable: {lost_value:.2f}",
            recommendation="Review lost reasons and identify repeating objections or qualification issues.",
        )

    return anomalies


def detect_marketing_anomalies(marketing_leads: pd.DataFrame) -> list[dict]:
    anomalies = []

    marketing_leads["lead_score"] = pd.to_numeric(marketing_leads["lead_score"], errors="coerce")

    lead_source_summary = (
        marketing_leads
        .groupby("lead_source")
        .agg(
            lead_count=("lead_id", "count"),
            average_lead_score=("lead_score", "mean"),
        )
        .reset_index()
    )

    low_quality_sources = lead_source_summary[
    (lead_source_summary["lead_count"] >= 1)
    & (
        lead_source_summary["average_lead_score"]
        < ANOMALY_THRESHOLDS["low_quality_lead_score_threshold"]
    )
    ]

    for _, row in low_quality_sources.iterrows():
        add_anomaly(
            anomalies,
            category="Marketing Lead Quality",
            severity="Low",
            message=(
                f"Lead source has low average lead score: "
                f"{row['lead_source']} - {row['average_lead_score']:.2f}"
            ),
            recommendation="Review campaign targeting, messaging, and lead qualification rules for this source.",
        )

    return anomalies


def save_anomalies(anomalies: list[dict]) -> None:
    output_data = {
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
    }

    output_path = save_json("anomaly_report.json", output_data)
    print(f"Anomali raporu oluşturuldu: {output_path}")


def print_anomalies(anomalies: list[dict]) -> None:
    print("=" * 70)
    print("ANOMALY REPORT")
    print("=" * 70)

    if not anomalies:
        print("Dikkat gerektiren anomali bulunmadı.")
        return

    print(f"{len(anomalies)} adet anomali bulundu:\n")

    for index, anomaly in enumerate(anomalies, start=1):
        print(f"{index}. [{anomaly['severity']}] {anomaly['category']}")
        print(f"   Message: {anomaly['message']}")
        print(f"   Recommendation: {anomaly['recommendation']}")
        print()


def main() -> None:
    sales_pipeline = load_csv("sales_pipeline.csv")
    marketing_leads = load_csv("marketing_leads.csv")
    kpi_summary = load_json("kpi_summary.json")

    anomalies = []

    anomalies.extend(detect_target_anomalies(kpi_summary))
    anomalies.extend(detect_sales_anomalies(sales_pipeline))
    anomalies.extend(detect_marketing_anomalies(marketing_leads))

    print_anomalies(anomalies)
    save_anomalies(anomalies)


if __name__ == "__main__":
    main()