import pandas as pd

from utils import load_csv


EXPECTED_COLUMNS = {
    "sales_pipeline.csv": [
        "deal_id",
        "company_name",
        "industry",
        "lead_source",
        "deal_stage",
        "deal_value",
        "probability",
        "owner",
        "created_date",
        "expected_close_date",
        "status",
    ],
    "marketing_leads.csv": [
        "lead_id",
        "lead_source",
        "campaign_name",
        "lead_date",
        "company_name",
        "industry",
        "lead_score",
        "converted_to_deal",
        "deal_id",
        "estimated_value",
    ],
    "weekly_targets.csv": [
        "week_start",
        "week_end",
        "target_revenue",
        "target_new_leads",
        "target_conversion_rate",
        "target_pipeline_value",
    ],
}


def validate_columns(file_name: str, df: pd.DataFrame) -> list[str]:
    errors = []
    expected = EXPECTED_COLUMNS[file_name]
    actual = list(df.columns)

    missing_columns = [col for col in expected if col not in actual]
    extra_columns = [col for col in actual if col not in expected]

    if missing_columns:
        errors.append(f"{file_name}: Eksik kolonlar: {missing_columns}")

    if extra_columns:
        errors.append(f"{file_name}: Beklenmeyen ekstra kolonlar: {extra_columns}")

    return errors


def validate_required_values(file_name: str, df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    errors = []

    for col in required_columns:
        if col not in df.columns:
            continue

        missing_count = df[col].isnull().sum()

        if missing_count > 0:
            errors.append(f"{file_name}: '{col}' kolonunda {missing_count} boş değer var.")

    return errors


def validate_numeric_range(
    file_name: str,
    df: pd.DataFrame,
    column: str,
    min_value: float,
    max_value: float,
) -> list[str]:
    errors = []

    if column not in df.columns:
        return errors

    numeric_series = pd.to_numeric(df[column], errors="coerce")

    invalid_numeric_count = numeric_series.isnull().sum()
    if invalid_numeric_count > 0:
        errors.append(f"{file_name}: '{column}' kolonunda sayıya çevrilemeyen değer var.")

    out_of_range = df[(numeric_series < min_value) | (numeric_series > max_value)]

    if not out_of_range.empty:
        errors.append(
            f"{file_name}: '{column}' kolonunda {min_value}-{max_value} aralığı dışında "
            f"{len(out_of_range)} kayıt var."
        )

    return errors


def validate_dates(file_name: str, df: pd.DataFrame, date_columns: list[str]) -> list[str]:
    errors = []

    for col in date_columns:
        if col not in df.columns:
            continue

        parsed_dates = pd.to_datetime(df[col], errors="coerce")
        invalid_date_count = parsed_dates.isnull().sum()

        if invalid_date_count > 0:
            errors.append(f"{file_name}: '{col}' kolonunda geçersiz tarih değeri var.")

    return errors


def validate_deal_id_relationship(
    sales_pipeline: pd.DataFrame,
    marketing_leads: pd.DataFrame,
) -> list[str]:
    errors = []

    sales_deal_ids = set(sales_pipeline["deal_id"].dropna())
    converted_leads = marketing_leads[
        marketing_leads["converted_to_deal"].str.lower() == "yes"
    ]

    lead_deal_ids = set(converted_leads["deal_id"].dropna())

    missing_deal_ids = lead_deal_ids - sales_deal_ids

    if missing_deal_ids:
        errors.append(
            "marketing_leads.csv: sales_pipeline.csv içinde bulunmayan deal_id değerleri var: "
            f"{sorted(missing_deal_ids)}"
        )

    return errors


def validate_sales_pipeline(df: pd.DataFrame) -> list[str]:
    file_name = "sales_pipeline.csv"
    errors = []

    errors.extend(validate_columns(file_name, df))

    errors.extend(
        validate_required_values(
            file_name,
            df,
            required_columns=[
                "deal_id",
                "company_name",
                "deal_stage",
                "deal_value",
                "probability",
                "created_date",
                "status",
            ],
        )
    )

    errors.extend(validate_numeric_range(file_name, df, "deal_value", 0, 10_000_000))
    errors.extend(validate_numeric_range(file_name, df, "probability", 0, 100))
    errors.extend(validate_dates(file_name, df, ["created_date", "expected_close_date"]))

    return errors


def validate_marketing_leads(df: pd.DataFrame) -> list[str]:
    file_name = "marketing_leads.csv"
    errors = []

    errors.extend(validate_columns(file_name, df))

    errors.extend(
        validate_required_values(
            file_name,
            df,
            required_columns=[
                "lead_id",
                "lead_source",
                "campaign_name",
                "lead_date",
                "company_name",
                "lead_score",
                "converted_to_deal",
                "estimated_value",
            ],
        )
    )

    errors.extend(validate_numeric_range(file_name, df, "lead_score", 0, 100))
    errors.extend(validate_numeric_range(file_name, df, "estimated_value", 0, 10_000_000))
    errors.extend(validate_dates(file_name, df, ["lead_date"]))

    return errors


def validate_weekly_targets(df: pd.DataFrame) -> list[str]:
    file_name = "weekly_targets.csv"
    errors = []

    errors.extend(validate_columns(file_name, df))

    errors.extend(
        validate_required_values(
            file_name,
            df,
            required_columns=[
                "week_start",
                "week_end",
                "target_revenue",
                "target_new_leads",
                "target_conversion_rate",
                "target_pipeline_value",
            ],
        )
    )

    errors.extend(validate_numeric_range(file_name, df, "target_revenue", 0, 10_000_000))
    errors.extend(validate_numeric_range(file_name, df, "target_new_leads", 0, 100_000))
    errors.extend(validate_numeric_range(file_name, df, "target_conversion_rate", 0, 100))
    errors.extend(validate_numeric_range(file_name, df, "target_pipeline_value", 0, 10_000_000))
    errors.extend(validate_dates(file_name, df, ["week_start", "week_end"]))

    return errors


def print_validation_result(errors: list[str]) -> None:
    print("=" * 70)
    print("DATA VALIDATION RESULT")
    print("=" * 70)

    if not errors:
        print("Tüm veri doğrulama kontrolleri başarıyla geçti.")
        return

    print(f"{len(errors)} adet doğrulama hatası bulundu:\n")

    for index, error in enumerate(errors, start=1):
        print(f"{index}. {error}")


def main() -> None:
    sales_pipeline = load_csv("sales_pipeline.csv")
    marketing_leads = load_csv("marketing_leads.csv")
    weekly_targets = load_csv("weekly_targets.csv")

    errors = []

    errors.extend(validate_sales_pipeline(sales_pipeline))
    errors.extend(validate_marketing_leads(marketing_leads))
    errors.extend(validate_weekly_targets(weekly_targets))
    errors.extend(validate_deal_id_relationship(sales_pipeline, marketing_leads))

    print_validation_result(errors)


if __name__ == "__main__":
    main()