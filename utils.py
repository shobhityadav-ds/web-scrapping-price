from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def clean_price(value):
    digits = re.sub(r"[^\d]", "", str(value))
    return int(digits) if digits else None


def save_dataframe(df, output_base_path):
    csv_path = output_base_path.with_suffix(".csv")
    xlsx_path = output_base_path.with_suffix(".xlsx")

    df.to_csv(csv_path, index=False)

    try:
        df.to_excel(xlsx_path, index=False)
    except PermissionError:
        fallback = output_base_path.with_name(f"{output_base_path.name}_new").with_suffix(".xlsx")
        df.to_excel(fallback, index=False)
