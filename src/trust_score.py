import pandas as pd
import numpy as np


def calculate_completeness(raw_df):
    total_cells = raw_df.shape[0] * raw_df.shape[1]
    missing_cells = raw_df.isnull().sum().sum()

    completeness = (1 - (missing_cells / total_cells)) * 100
    return round(completeness, 2)


def calculate_uniqueness(raw_df):
    duplicate_rows = raw_df.duplicated().sum()
    uniqueness = (1 - duplicate_rows / len(raw_df)) * 100
    return round(uniqueness, 2)


def calculate_consistency(clean_df):
    score = 0
    checks = 0

    for col in clean_df.columns:
        try:
            col_data = clean_df[col]

            # Skip completely empty columns
            if col_data.dropna().empty:
                continue

            # =========================
            # NUMERIC CHECKS
            # =========================
            if pd.api.types.is_numeric_dtype(col_data):
                checks += 1

                # negative values penalty
                negative_ratio = (col_data < 0).sum() / len(col_data)

                # extreme outliers penalty
                q1 = col_data.quantile(0.25)
                q3 = col_data.quantile(0.75)
                iqr = q3 - q1

                if iqr == 0:
                    outlier_ratio = 0
                else:
                    outliers = ((col_data < (q1 - 1.5 * iqr)) |
                                (col_data > (q3 + 1.5 * iqr))).sum()
                    outlier_ratio = outliers / len(col_data)

                col_score = 1 - (0.5 * negative_ratio + 0.5 * outlier_ratio)
                score += max(col_score, 0)

            # =========================
            # STRING CHECKS
            # =========================
            elif col_data.dtype == "object":
                checks += 1

                lengths = col_data.dropna().astype(str).str.len()

                if len(lengths) == 0:
                    continue

                std = lengths.std()
                unique_ratio = col_data.nunique() / len(col_data)

                # penalize too much variation OR too unique (IDs)
                if pd.isna(std):
                    col_score = 1
                else:
                    length_score = 1 if std < 40 else 0.6
                    uniqueness_penalty = 0.7 if unique_ratio > 0.9 else 1

                    col_score = length_score * uniqueness_penalty

                score += col_score

        except Exception:
            continue

    if checks == 0:
        return 50  # fallback instead of 0

    return round((score / checks) * 100, 2)


def compute_trust_score(raw_df, clean_df):
    completeness = calculate_completeness(raw_df)
    uniqueness = calculate_uniqueness(raw_df)
    consistency = calculate_consistency(clean_df)

    trust_score = (
        0.4 * completeness +
        0.3 * uniqueness +
        0.3 * consistency
    )

    return {
        "completeness": completeness,
        "uniqueness": uniqueness,
        "consistency": consistency,
        "trust_score": round(trust_score, 2)
    }