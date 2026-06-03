import pandas as pd

from utils import load_csv


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