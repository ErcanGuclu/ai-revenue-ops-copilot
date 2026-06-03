from pathlib import Path
import json

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


def load_csv(file_name: str) -> pd.DataFrame:
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    return pd.read_csv(file_path)


def load_kpi_summary() -> dict:
    file_path = OUTPUT_DIR / "kpi_summary.json"

    if not file_path.exists():
        raise FileNotFoundError(
            "kpi_summary.json bulunamadı. Önce backend/calculate_kpis.py çalıştırılmalı."
        )

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


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

    if revenue["achievement_rate"] < 70:
        add_anomaly(
            anomalies,
            category="Revenue",
            severity="High",
            message=f"Revenue achievement rate is low: {revenue['achievement_rate']:.2f}%",
            recommendation="Review stalled opportunities, accelerate high-probability deals, and check whether closed-won revenue is underreported.",
        )

    if new_leads["achievement_rate"] < 70:
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

    if pipeline_value["achievement_rate"] < 80:
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
        & (sales_pipeline["deal_value"] >= 50000)
        & (sales_pipeline["probability"] < 50)
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

    if lost_value >= 30000:
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
        & (lead_source_summary["average_lead_score"] < 60)
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
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / "anomaly_report.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            {
                "anomaly_count": len(anomalies),
                "anomalies": anomalies,
            },
            file,
            indent=4,
            ensure_ascii=False,
        )

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
    kpi_summary = load_kpi_summary()

    anomalies = []

    anomalies.extend(detect_target_anomalies(kpi_summary))
    anomalies.extend(detect_sales_anomalies(sales_pipeline))
    anomalies.extend(detect_marketing_anomalies(marketing_leads))

    print_anomalies(anomalies)
    save_anomalies(anomalies)


if __name__ == "__main__":
    main()