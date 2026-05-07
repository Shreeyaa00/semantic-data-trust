def detect_relationships(df, threshold=0.95, uniqueness_threshold=0.9, dominance_threshold=0.85):
    relationships = []

    for col1 in df.columns:

        # Skip high-cardinality columns (ID-like)
        uniqueness_ratio = df[col1].nunique() / len(df)
        # Strong ID detection
        if uniqueness_ratio > 0.8:
            continue

# Also drop columns with too many unique values (almost IDs)
        if df[col1].nunique() > 0.5 * len(df):
            continue

        # Skip columns with dominant single value (low information)
        top_freq = df[col1].value_counts(normalize=True, dropna=True)
        if len(top_freq) > 0 and top_freq.iloc[0] > dominance_threshold:
            continue

        for col2 in df.columns:
            if col1 == col2:
                continue

            try:
                grouped = df.groupby(col1)[col2].nunique()
                valid_ratio = (grouped == 1).sum() / len(grouped)

                if valid_ratio >= threshold:
                    relationships.append((col1, col2, round(valid_ratio, 2)))

            except Exception:
                continue

    return relationships