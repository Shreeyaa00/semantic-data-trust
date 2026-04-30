import pandas as pd


def completeness_score(df):
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isin(["UNKNOWN"]).sum().sum()
    
    score = 100 * (1 - missing_cells / total_cells)
    return round(score, 2)


def uniqueness_score(df):
    total_rows = df.shape[0]
    unique_rows = df.drop_duplicates().shape[0]
    
    score = 100 * (unique_rows / total_rows)
    return round(score, 2)


def consistency_score(df):
    consistent_columns = 0

    for col in df.columns:
        unique_types = df[col].apply(type).nunique()
        if unique_types == 1:
            consistent_columns += 1

    score = 100 * (consistent_columns / len(df.columns))
    return round(score, 2)


def compute_trust_score(df):
    c1 = completeness_score(df)
    c2 = uniqueness_score(df)
    c3 = consistency_score(df)

    final_score = round((c1 + c2 + c3) / 3, 2)

    return {
        "completeness": c1,
        "uniqueness": c2,
        "consistency": c3,
        "trust_score": final_score
    }