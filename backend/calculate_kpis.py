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


def calculate_sales_kpis(sales_pipeline: pd.DataFrame) -> dict:
    sales_pipeline["deal_value"] = pd.to_numeric(sales_pipeline["deal_value"], errors="coerce")
    sales_pipeline["probability"] = pd.to_numeric(sales_pipeline["probability"], errors="coerce")

    open_deals = sales_pipeline[sales_pipeline["status"].str.lower() == "open"]
    won_deals = sales_pipeline[sales_pipeline["status"].str.lower() == "won"]
    lost_deals = sales_pipeline[sales_pipeline["status"].str.lower() == "lost"]

    total_pipeline_value = open_deals["deal_value"].sum()
    open_deal_count = len(open_deals)
    won_revenue = won_deals["deal_value"].sum()
    lost_deal_value = lost_deals["deal_value"].sum()

    weighted_pipeline = (open_deals["deal_value"] * open_deals["probability"] / 100).sum()

    average_deal_value = (
        sales_pipeline["deal_value"].mean()
        if not sales_pipeline.empty
        else 0
    )

    return {
        "total_pipeline_value": float(total_pipeline_value),
        "open_deal_count": int(open_deal_count),
        "won_revenue": float(won_revenue),
        "lost_deal_value": float(lost_deal_value),
        "weighted_pipeline": float(weighted_pipeline),
        "average_deal_value": float(average_deal_value),
    }


def calculate_marketing_kpis(marketing_leads: pd.DataFrame) -> dict:
    marketing_leads["lead_score"] = pd.to_numeric(marketing_leads["lead_score"], errors="coerce")
    marketing_leads["estimated_value"] = pd.to_numeric(marketing_leads["estimated_value"], errors="coerce")

    total_leads = len(marketing_leads)

    converted_leads = marketing_leads[
        marketing_leads["converted_to_deal"].str.lower() == "yes"
    ]

    converted_lead_count = len(converted_leads)

    lead_to_deal_conversion_rate = (
        converted_lead_count / total_leads * 100
        if total_leads > 0
        else 0
    )

    average_lead_score = marketing_leads["lead_score"].mean()
    total_estimated_lead_value = marketing_leads["estimated_value"].sum()

    lead_source_summary = (
        marketing_leads
        .groupby("lead_source")
        .agg(
            lead_count=("lead_id", "count"),
            average_lead_score=("lead_score", "mean"),
            estimated_value=("estimated_value", "sum"),
        )
        .reset_index()
        .to_dict(orient="records")
    )

    return {
        "total_leads": int(total_leads),
        "converted_lead_count": int(converted_lead_count),
        "lead_to_deal_conversion_rate": float(lead_to_deal_conversion_rate),
        "average_lead_score": float(average_lead_score),
        "total_estimated_lead_value": float(total_estimated_lead_value),
        "lead_source_summary": lead_source_summary,
    }


def calculate_target_comparison(
    sales_kpis: dict,
    marketing_kpis: dict,
    weekly_targets: pd.DataFrame,
) -> dict:
    latest_target = weekly_targets.iloc[-1]

    target_revenue = float(latest_target["target_revenue"])
    target_new_leads = int(latest_target["target_new_leads"])
    target_conversion_rate = float(latest_target["target_conversion_rate"])
    target_pipeline_value = float(latest_target["target_pipeline_value"])

    actual_revenue = sales_kpis["won_revenue"]
    actual_new_leads = marketing_kpis["total_leads"]
    actual_conversion_rate = marketing_kpis["lead_to_deal_conversion_rate"]
    actual_pipeline_value = sales_kpis["total_pipeline_value"]

    return {
        "target_period": {
            "week_start": str(latest_target["week_start"]),
            "week_end": str(latest_target["week_end"]),
        },
        "revenue": {
            "target": target_revenue,
            "actual": actual_revenue,
            "gap": actual_revenue - target_revenue,
            "achievement_rate": actual_revenue / target_revenue * 100 if target_revenue > 0 else 0,
        },
        "new_leads": {
            "target": target_new_leads,
            "actual": actual_new_leads,
            "gap": actual_new_leads - target_new_leads,
            "achievement_rate": actual_new_leads / target_new_leads * 100 if target_new_leads > 0 else 0,
        },
        "conversion_rate": {
            "target": target_conversion_rate,
            "actual": actual_conversion_rate,
            "gap": actual_conversion_rate - target_conversion_rate,
            "achievement_rate": actual_conversion_rate / target_conversion_rate * 100 if target_conversion_rate > 0 else 0,
        },
        "pipeline_value": {
            "target": target_pipeline_value,
            "actual": actual_pipeline_value,
            "gap": actual_pipeline_value - target_pipeline_value,
            "achievement_rate": actual_pipeline_value / target_pipeline_value * 100 if target_pipeline_value > 0 else 0,
        },
    }


def save_kpis_to_json(kpi_summary: dict) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / "kpi_summary.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(kpi_summary, file, indent=4, ensure_ascii=False)

    print(f"KPI özeti oluşturuldu: {output_path}")


def print_kpi_summary(kpi_summary: dict) -> None:
    print("=" * 70)
    print("KPI SUMMARY")
    print("=" * 70)

    print("\nSALES KPIs")
    for key, value in kpi_summary["sales_kpis"].items():
        if key != "lead_source_summary":
            print(f"{key}: {value}")

    print("\nMARKETING KPIs")
    for key, value in kpi_summary["marketing_kpis"].items():
        if key != "lead_source_summary":
            print(f"{key}: {value}")

    print("\nTARGET COMPARISON")
    for category, values in kpi_summary["target_comparison"].items():
        print(f"\n{category}:")
        if isinstance(values, dict):
            for key, value in values.items():
                print(f"  {key}: {value}")


def main() -> None:
    sales_pipeline = load_csv("sales_pipeline.csv")
    marketing_leads = load_csv("marketing_leads.csv")
    weekly_targets = load_csv("weekly_targets.csv")

    sales_kpis = calculate_sales_kpis(sales_pipeline)
    marketing_kpis = calculate_marketing_kpis(marketing_leads)
    target_comparison = calculate_target_comparison(
        sales_kpis,
        marketing_kpis,
        weekly_targets,
    )

    kpi_summary = {
        "sales_kpis": sales_kpis,
        "marketing_kpis": marketing_kpis,
        "target_comparison": target_comparison,
    }

    print_kpi_summary(kpi_summary)
    save_kpis_to_json(kpi_summary)


if __name__ == "__main__":
    main()