from pathlib import Path
import json

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"


def load_csv(file_name: str) -> pd.DataFrame:
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"CSV dosyası bulunamadı: {file_path}")

    return pd.read_csv(file_path)


def load_json(file_name: str) -> dict:
    file_path = OUTPUT_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"JSON dosyası bulunamadı: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_name: str, data: dict) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / file_name

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return output_path


def save_text(file_name: str, content: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / file_name

    with output_path.open("w", encoding="utf-8") as file:
        file.write(content)

    return output_path