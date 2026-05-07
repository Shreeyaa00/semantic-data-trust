import re
import numpy as np
from difflib import SequenceMatcher

# ==========================================
# GENERIC / LOW-INFORMATION COLUMNS
# ==========================================

GENERIC_COLUMNS = {
    "id",
    "name",
    "date",
    "time",
    "year",
    "month",
    "day",
    "created_at",
    "updated_at",
    "latitude",
    "longitude",
    "lat",
    "lon",
    "location",
    "address",
    "street",
    "city",
    "state",
    "zipcode",
    "zip",
    "borough",
    "boro",
    "category",
    "type",
    "description",
    "code",
    "status",
}


# ==========================================
# CLEAN COLUMN NAMES
# ==========================================

def clean_column(col):
    col = col.lower().strip()
    col = re.sub(r"[^a-z0-9_ ]", "", col)
    col = col.replace(" ", "_")
    return col


# ==========================================
# COLUMN NAME SIMILARITY
# ==========================================

def column_name_similarity(col1, col2):
    return SequenceMatcher(None, col1, col2).ratio()


# ==========================================
# IMPORTANT COLUMNS ONLY
# ==========================================

def get_important_columns(df):
    important = []

    for col in df.columns:
        c = clean_column(col)

        if c in GENERIC_COLUMNS:
            continue

        uniqueness = df[col].nunique(dropna=True)

        # remove near-constant columns
        if uniqueness <= 1:
            continue

        important.append(col)

    return important


# ==========================================
# SCHEMA SIMILARITY
# ==========================================

def column_similarity(df1, df2):

    cols1 = get_important_columns(df1)
    cols2 = get_important_columns(df2)

    if not cols1 or not cols2:
        return 0

    matched = 0

    for c1 in cols1:

        best = 0

        for c2 in cols2:

            sim = column_name_similarity(
                clean_column(c1),
                clean_column(c2)
            )

            best = max(best, sim)

        if best > 0.82:
            matched += 1

    return matched / max(len(cols1), len(cols2))


# ==========================================
# VALUE OVERLAP
# ==========================================

def value_overlap(df1, df2, sample_size=2000):

    cols1 = get_important_columns(df1)
    cols2 = get_important_columns(df2)

    if not cols1 or not cols2:
        return 0

    df1_sample = df1.sample(
        min(sample_size, len(df1)),
        random_state=42
    )

    df2_sample = df2.sample(
        min(sample_size, len(df2)),
        random_state=42
    )

    scores = []

    for col1 in cols1:

        best_overlap = 0

        for col2 in cols2:

            name_sim = column_name_similarity(
                clean_column(col1),
                clean_column(col2)
            )

            # only semantically similar columns
            if name_sim < 0.75:
                continue

            try:

                set1 = set(
                    df1_sample[col1]
                    .dropna()
                    .astype(str)
                    .str.lower()
                    .str.strip()
                )

                set2 = set(
                    df2_sample[col2]
                    .dropna()
                    .astype(str)
                    .str.lower()
                    .str.strip()
                )

                # ignore tiny sets
                if len(set1) < 20 or len(set2) < 20:
                    continue

                overlap = len(set1 & set2)
                ratio = overlap / min(len(set1), len(set2))

                best_overlap = max(best_overlap, ratio)

            except:
                continue

        scores.append(best_overlap)

    return np.mean(scores) if scores else 0


# ==========================================
# RELATIONSHIP SIMILARITY
# ==========================================

def relationship_score(rels1, rels2):

    if not rels1 or not rels2:
        return 0

    set1 = set(
        (
            clean_column(a),
            clean_column(b)
        )
        for a, b, _ in rels1
    )

    set2 = set(
        (
            clean_column(a),
            clean_column(b)
        )
        for a, b, _ in rels2
    )

    overlap = len(set1 & set2)
    total = len(set1 | set2)

    return overlap / total if total else 0


# ==========================================
# DATASET SIZE SIMILARITY
# ==========================================

def size_similarity(df1, df2):

    size1 = len(df1)
    size2 = len(df2)

    if size1 == 0 or size2 == 0:
        return 0

    return min(size1, size2) / max(size1, size2)


# ==========================================
# FINAL MATCH SCORE
# ==========================================

def dataset_match_score(df1, df2, rels1, rels2):

    schema = column_similarity(df1, df2)

    value = value_overlap(df1, df2)

    rel = relationship_score(rels1, rels2)

    size = size_similarity(df1, df2)

    final_score = (
        0.40 * schema +
        0.35 * value +
        0.15 * rel +
        0.10 * size
    )

    return round(final_score, 3)


# ==========================================
# RANK DATASETS
# ==========================================

def rank_datasets(query_name, datasets, relationships_dict):

    query_df = datasets[query_name]
    query_rels = relationships_dict.get(query_name, [])

    scores = []

    for name, df in datasets.items():

        if name == query_name:
            continue

        rels = relationships_dict.get(name, [])

        score = dataset_match_score(
            query_df,
            df,
            query_rels,
            rels
        )

        scores.append((name, score))

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores