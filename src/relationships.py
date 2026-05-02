def detect_relationships(df, threshold=0.95, uniqueness_threshold=0.9):
    relationships = []

    columns = df.columns

    for col1 in columns:
        uniqueness_ratio = df[col1].nunique() / len(df)
        if uniqueness_ratio > uniqueness_threshold:
            continue

        for col2 in columns:
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