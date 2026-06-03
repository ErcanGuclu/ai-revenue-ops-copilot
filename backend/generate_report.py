
from datetime import datetime

from utils import load_json, save_text


def format_currency(value: float) -> str:
    return f"{value:,.2f}"


def format_percent(value: float) -> str:
    return f"{value:.2f}%"


def get_status_label(achievement_rate: float) -> str:
    if achievement_rate >= 100:
        return "Hedef üstü"
    if achievement_rate >= 80:
        return "Hedefe yakın"
    if achievement_rate >= 60:
        return "Riskli"
    return "Kritik"


def build_executive_summary(kpi_summary: dict, anomaly_report: dict) -> str:
    sales = kpi_summary["sales_kpis"]
    marketing = kpi_summary["marketing_kpis"]
    target = kpi_summary["target_comparison"]
    anomaly_count = anomaly_report["anomaly_count"]

    revenue_status = get_status_label(target["revenue"]["achievement_rate"])
    pipeline_status = get_status_label(target["pipeline_value"]["achievement_rate"])
    lead_status = get_status_label(target["new_leads"]["achievement_rate"])

    summary = [
        "## Yönetici Özeti",
        "",
        (
            f"Bu haftaki revenue performansı **{revenue_status}** seviyesindedir. "
            f"Kazanılan gelir {format_currency(sales['won_revenue'])} olarak gerçekleşmiştir."
        ),
        "",
        (
            f"Açık pipeline değeri {format_currency(sales['total_pipeline_value'])}, "
            f"weighted pipeline değeri ise {format_currency(sales['weighted_pipeline'])} seviyesindedir. "
            f"Pipeline durumu **{pipeline_status}** olarak değerlendirilmiştir."
        ),
        "",
        (
            f"Toplam {marketing['total_leads']} lead üretilmiş, "
            f"{marketing['converted_lead_count']} lead deal'a dönüşmüştür. "
            f"Lead üretim durumu **{lead_status}** seviyesindedir."
        ),
        "",
        (
            f"Sistem bu hafta {anomaly_count} adet dikkat noktası tespit etmiştir. "
            "Bu bulgular aşağıdaki anomali ve aksiyon bölümlerinde detaylandırılmıştır."
        ),
    ]

    return "\n".join(summary)


def build_sales_section(kpi_summary: dict) -> str:
    sales = kpi_summary["sales_kpis"]

    lines = [
        "## Satış KPI'ları",
        "",
        "| Metrik | Değer |",
        "|---|---:|",
        f"| Toplam açık pipeline değeri | {format_currency(sales['total_pipeline_value'])} |",
        f"| Açık fırsat sayısı | {sales['open_deal_count']} |",
        f"| Kazanılan gelir | {format_currency(sales['won_revenue'])} |",
        f"| Kaybedilen fırsat değeri | {format_currency(sales['lost_deal_value'])} |",
        f"| Weighted pipeline | {format_currency(sales['weighted_pipeline'])} |",
        f"| Ortalama deal değeri | {format_currency(sales['average_deal_value'])} |",
    ]

    return "\n".join(lines)


def build_marketing_section(kpi_summary: dict) -> str:
    marketing = kpi_summary["marketing_kpis"]

    lines = [
        "## Pazarlama KPI'ları",
        "",
        "| Metrik | Değer |",
        "|---|---:|",
        f"| Toplam lead sayısı | {marketing['total_leads']} |",
        f"| Deal'a dönüşen lead sayısı | {marketing['converted_lead_count']} |",
        f"| Lead-to-deal conversion rate | {format_percent(marketing['lead_to_deal_conversion_rate'])} |",
        f"| Ortalama lead skoru | {marketing['average_lead_score']:.2f} |",
        f"| Toplam tahmini lead değeri | {format_currency(marketing['total_estimated_lead_value'])} |",
        "",
        "### Lead Kaynak Performansı",
        "",
        "| Lead Kaynağı | Lead Sayısı | Ortalama Lead Skoru | Tahmini Değer |",
        "|---|---:|---:|---:|",
    ]

    for item in marketing["lead_source_summary"]:
        lines.append(
            f"| {item['lead_source']} | "
            f"{item['lead_count']} | "
            f"{item['average_lead_score']:.2f} | "
            f"{format_currency(item['estimated_value'])} |"
        )

    return "\n".join(lines)


def build_target_section(kpi_summary: dict) -> str:
    target = kpi_summary["target_comparison"]
    period = target["target_period"]

    lines = [
        "## Hedef - Gerçekleşen Karşılaştırması",
        "",
        f"Rapor dönemi: **{period['week_start']} - {period['week_end']}**",
        "",
        "| Alan | Hedef | Gerçekleşen | Fark | Başarı Oranı | Durum |",
        "|---|---:|---:|---:|---:|---|",
    ]

    metric_labels = {
        "revenue": "Revenue",
        "new_leads": "Yeni Lead",
        "conversion_rate": "Conversion Rate",
        "pipeline_value": "Pipeline Değeri",
    }

    for key, label in metric_labels.items():
        item = target[key]
        status = get_status_label(item["achievement_rate"])

        if key == "conversion_rate":
            target_value = format_percent(item["target"])
            actual_value = format_percent(item["actual"])
            gap_value = format_percent(item["gap"])
        else:
            target_value = format_currency(item["target"])
            actual_value = format_currency(item["actual"])
            gap_value = format_currency(item["gap"])

        lines.append(
            f"| {label} | {target_value} | {actual_value} | "
            f"{gap_value} | {format_percent(item['achievement_rate'])} | {status} |"
        )

    return "\n".join(lines)


def build_anomaly_section(anomaly_report: dict) -> str:
    anomalies = anomaly_report["anomalies"]

    lines = [
        "## Tespit Edilen Anomaliler",
        "",
    ]

    if not anomalies:
        lines.append("Bu dönemde dikkat gerektiren anomali tespit edilmedi.")
        return "\n".join(lines)

    for index, anomaly in enumerate(anomalies, start=1):
        lines.extend(
            [
                f"### {index}. [{anomaly['severity']}] {anomaly['category']}",
                "",
                f"**Bulgu:** {anomaly['message']}",
                "",
                f"**Öneri:** {anomaly['recommendation']}",
                "",
            ]
        )

    return "\n".join(lines)


def build_action_section(anomaly_report: dict) -> str:
    anomalies = anomaly_report["anomalies"]

    lines = [
        "## Önerilen Aksiyonlar",
        "",
    ]

    if not anomalies:
        lines.append("- Mevcut performans izlenmeye devam edilmeli.")
        return "\n".join(lines)

    for anomaly in anomalies:
        lines.append(f"- **{anomaly['category']}**: {anomaly['recommendation']}")

    return "\n".join(lines)


def generate_report(kpi_summary: dict, anomaly_report: dict) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sections = [
        "# Weekly Revenue Operations Report",
        "",
        f"Generated at: {generated_at}",
        "",
        build_executive_summary(kpi_summary, anomaly_report),
        "",
        build_sales_section(kpi_summary),
        "",
        build_marketing_section(kpi_summary),
        "",
        build_target_section(kpi_summary),
        "",
        build_anomaly_section(anomaly_report),
        "",
        build_action_section(anomaly_report),
        "",
    ]

    return "\n".join(sections)


def save_report(report: str) -> None:
    output_path = save_text("weekly_revenue_report.md", report)
    print(f"Yönetici raporu oluşturuldu: {output_path}")


def main() -> None:
    kpi_summary = load_json("kpi_summary.json")
    anomaly_report = load_json("anomaly_report.json")

    report = generate_report(kpi_summary, anomaly_report)
    save_report(report)


if __name__ == "__main__":
    main()