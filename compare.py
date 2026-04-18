from difflib import SequenceMatcher
import re

import pandas as pd

from utils import ensure_data_dir, save_dataframe


OUTPUT_COLUMNS = [
    "Amazon Product",
    "Flipkart Product",
    "Amazon Price",
    "Flipkart Price",
    "Best Platform",
    "Price Difference",
    "Match Score",
]


def normalize_name(value):
    text = re.sub(r"[^a-z0-9\s]", " ", str(value).lower())
    tokens = [token for token in text.split() if len(token) > 1]
    return " ".join(tokens)


def match_score(left, right):
    left_text = normalize_name(left)
    right_text = normalize_name(right)

    if not left_text or not right_text:
        return 0.0

    seq_score = SequenceMatcher(None, left_text, right_text).ratio()
    left_tokens = set(left_text.split())
    right_tokens = set(right_text.split())
    overlap_score = len(left_tokens & right_tokens) / max(len(left_tokens | right_tokens), 1)

    return max(seq_score, overlap_score)


def compare_products(amazon_df, flipkart_df):
    final_data = []
    used_flipkart_indexes = set()

    for _, amazon_row in amazon_df.iterrows():
        best_match = None
        best_score = 0.0

        for flipkart_index, flipkart_row in flipkart_df.iterrows():
            if flipkart_index in used_flipkart_indexes:
                continue

            score = match_score(amazon_row["Name"], flipkart_row["Name"])
            if score > best_score:
                best_score = score
                best_match = (flipkart_index, flipkart_row)

        if best_match is None or best_score < 0.42:
            continue

        flipkart_index, flipkart_row = best_match

        try:
            amazon_price = int(amazon_row["Price"])
            flipkart_price = int(flipkart_row["Price"])
        except Exception:
            continue

        used_flipkart_indexes.add(flipkart_index)

        if amazon_price <= flipkart_price:
            best_platform = "Amazon"
            difference = flipkart_price - amazon_price
        else:
            best_platform = "Flipkart"
            difference = amazon_price - flipkart_price

        final_data.append({
            "Amazon Product": amazon_row["Name"],
            "Flipkart Product": flipkart_row["Name"],
            "Amazon Price": amazon_price,
            "Flipkart Price": flipkart_price,
            "Best Platform": best_platform,
            "Price Difference": difference,
            "Match Score": round(best_score, 3),
        })

    comparison_df = pd.DataFrame(final_data, columns=OUTPUT_COLUMNS)
    data_dir = ensure_data_dir()
    save_dataframe(comparison_df, data_dir / "comparison")

    return comparison_df
