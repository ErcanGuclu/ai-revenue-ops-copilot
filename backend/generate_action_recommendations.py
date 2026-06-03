
from utils import load_json, save_json



def map_severity_to_priority(severity: str) -> str:
    severity = severity.lower()

    if severity == "high":
        return "High"

    if severity == "medium":
        return "Medium"

    return "Low"


def infer_owner_team(category: str) -> str:
    category = category.lower()

    if "revenue" in category:
        return "Sales"

    if "lead" in category or "marketing" in category:
        return "Marketing"

    if "conversion" in category:
        return "Sales & Marketing"

    if "pipeline" in category:
        return "Sales"

    if "lost" in category:
        return "Sales Management"

    return "Revenue Operations"


def infer_time_horizon(priority: str) -> str:
    if priority == "High":
        return "This week"

    if priority == "Medium":
        return "Next 2 weeks"

    return "This month"


def build_recommendation_from_anomaly(anomaly: dict, index: int) -> dict:
    priority = map_severity_to_priority(anomaly["severity"])
    owner_team = infer_owner_team(anomaly["category"])
    time_horizon = infer_time_horizon(priority)

    return {
        "recommendation_id": f"REC-{index:03d}",
        "priority": priority,
        "business_area": anomaly["category"],
        "issue": anomaly["message"],
        "recommended_action": anomaly["recommendation"],
        "owner_team": owner_team,
        "time_horizon": time_horizon,
        "source": {
            "source_file": "anomaly_report.json",
            "source_category": anomaly["category"],
            "source_severity": anomaly["severity"],
        },
    }


def generate_action_recommendations(anomaly_report: dict) -> dict:
    anomalies = anomaly_report.get("anomalies", [])

    recommendations = []

    for index, anomaly in enumerate(anomalies, start=1):
        recommendation = build_recommendation_from_anomaly(anomaly, index)
        recommendations.append(recommendation)

    return {
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
    }


def save_action_recommendations(action_recommendations: dict) -> None:
    output_path = save_json("action_recommendations.json", action_recommendations)
    print(f"Aksiyon önerileri oluşturuldu: {output_path}")


def print_action_recommendations(action_recommendations: dict) -> None:
    print("=" * 70)
    print("ACTION RECOMMENDATIONS")
    print("=" * 70)

    recommendations = action_recommendations["recommendations"]

    if not recommendations:
        print("Aksiyon önerisi üretilmedi. Dikkat gerektiren anomali bulunmuyor.")
        return

    print(f"{len(recommendations)} adet aksiyon önerisi üretildi:\n")

    for recommendation in recommendations:
        print(f"{recommendation['recommendation_id']} - [{recommendation['priority']}]")
        print(f"Business Area: {recommendation['business_area']}")
        print(f"Issue: {recommendation['issue']}")
        print(f"Action: {recommendation['recommended_action']}")
        print(f"Owner Team: {recommendation['owner_team']}")
        print(f"Time Horizon: {recommendation['time_horizon']}")
        print()


def main() -> None:
    anomaly_report = load_json("anomaly_report.json")

    action_recommendations = generate_action_recommendations(anomaly_report)

    print_action_recommendations(action_recommendations)
    save_action_recommendations(action_recommendations)


if __name__ == "__main__":
    main()