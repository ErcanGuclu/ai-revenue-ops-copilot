from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def load_csv(file_name: str) -> pd.DataFrame:
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    return pd.read_csv(file_path)


def print_dataset_overview(name: str, df: pd.DataFrame) -> None:
    print("=" * 60)
    print(f"DATASET: {name}")
    print("=" * 60)

    print("\nİlk 5 satır:")
    print(df.head())

    print("\nKolonlar:")
    print(list(df.columns))

    print("\nSatır / Kolon sayısı:")
    print(df.shape)

    print("\nBoş değer sayıları:")
    print(df.isnull().sum())

    print("\nVeri tipleri:")
    print(df.dtypes)

    print("\n")


def main() -> None:
    sales_pipeline = load_csv("sales_pipeline.csv")
    marketing_leads = load_csv("marketing_leads.csv")
    weekly_targets = load_csv("weekly_targets.csv")

    print_dataset_overview("sales_pipeline.csv", sales_pipeline)
    print_dataset_overview("marketing_leads.csv", marketing_leads)
    print_dataset_overview("weekly_targets.csv", weekly_targets)


if __name__ == "__main__":
    main()