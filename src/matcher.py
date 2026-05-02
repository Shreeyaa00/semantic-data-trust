from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def column_similarity(df1, df2):
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)

    overlap = len(cols1.intersection(cols2))
    total = len(cols1.union(cols2))

    return overlap / total if total != 0 else 0

def semantic_similarity(cols1, cols2):
    emb1 = model.encode(list(cols1))
    emb2 = model.encode(list(cols2))

    sim_matrix = cosine_similarity(emb1, emb2)
    return sim_matrix.max()


def value_overlap(df1, df2):
    score = 0

    # sample for speed
    df1 = df1.sample(min(5000, len(df1)))
    df2 = df2.sample(min(5000, len(df2)))

    for col1 in df1.columns:
        for col2 in df2.columns:
            try:
                set1 = set(df1[col1].dropna().astype(str).unique())
                set2 = set(df2[col2].dropna().astype(str).unique())

                overlap = len(set1.intersection(set2))

                if overlap > 50:
                    score += 1
            except:
                continue

    return score

def dataset_match_score(df1, df2):
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)

    s_schema = column_similarity(df1, df2)
    s_semantic = semantic_similarity(cols1, cols2)
    s_value = value_overlap(df1, df2)

    final_score = (
        0.5 * s_schema +
        0.3 * s_semantic +
        0.2 * (s_value / 10)
    )

    return round(final_score, 3)


def rank_datasets(query_name, datasets):
    query_df = datasets[query_name]
    scores = []

    for name, df in datasets.items():
        if name == query_name:
            continue

        score = dataset_match_score(query_df, df)
        scores.append((name, round(score, 3)))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores