import streamlit as st
import pandas as pd

from ingestion import load_datasets
from preprocessing import preprocess_datasets
from trust_score import compute_trust_score
from relationships import detect_relationships
from matcher import rank_datasets

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Semantic Data Trust Platform",
    layout="wide"
)

st.title("Semantic Data Trust & Discovery Platform")

st.markdown(
    """
    Analyze dataset quality, discover relationships,
    and semantically match datasets.
    """
)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_pipeline():

    datasets = load_datasets("data/raw")

    cleaned = preprocess_datasets(datasets)

    trust_scores = {}

    for name in datasets:

        trust_scores[name] = compute_trust_score(
            datasets[name],
            cleaned[name]
        )

    relationships_dict = {}

    for name, df in cleaned.items():

        relationships_dict[name] = detect_relationships(df)

    return datasets, cleaned, trust_scores, relationships_dict


datasets, cleaned, trust_scores, relationships_dict = load_pipeline()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Overview",
        "Trust Scores",
        "Relationships",
        "Dataset Matching",
        "Dataset Explorer"
    ]
)

# ==========================================
# OVERVIEW PAGE
# ==========================================

if page == "Overview":

    st.header("Dataset Overview")

    overview = []

    for name, df in cleaned.items():

        score = trust_scores[name]["trust_score"]

        overview.append({
            "Dataset": name,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Trust Score": round(score, 2)
        })

    overview_df = pd.DataFrame(overview)

    st.dataframe(
        overview_df,
        use_container_width=True
    )

# ==========================================
# TRUST SCORE PAGE
# ==========================================

elif page == "Trust Scores":

    st.header("Trust Score Analysis")

    dataset_name = st.selectbox(
        "Select Dataset",
        list(cleaned.keys())
    )

    scores = trust_scores[dataset_name]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Completeness",
        f"{scores['completeness']}%"
    )

    col2.metric(
        "Uniqueness",
        f"{scores['uniqueness']}%"
    )

    col3.metric(
        "Consistency",
        f"{scores['consistency']}%"
    )

    col4.metric(
        "Trust Score",
        f"{scores['trust_score']}%"
    )

# ==========================================
# RELATIONSHIPS PAGE
# ==========================================

elif page == "Relationships":

    st.header("Relationship Discovery")

    dataset_name = st.selectbox(
        "Select Dataset",
        list(cleaned.keys())
    )

    rels = relationships_dict[dataset_name]

    if rels:

        rel_df = pd.DataFrame(
            rels,
            columns=[
                "Source Column",
                "Target Column",
                "Confidence"
            ]
        )

        st.dataframe(
            rel_df,
            use_container_width=True
        )

    else:
        st.warning("No relationships detected.")

# ==========================================
# DATASET MATCHING PAGE
# ==========================================

elif page == "Dataset Matching":

    st.header("Semantic Dataset Matching")

    query_dataset = st.selectbox(
        "Select Query Dataset",
        list(cleaned.keys())
    )

    matches = rank_datasets(
        query_dataset,
        cleaned,
        relationships_dict
    )

    match_df = pd.DataFrame(
        matches,
        columns=[
            "Dataset",
            "Match Score"
        ]
    )

    st.dataframe(
        match_df,
        use_container_width=True
    )

# ==========================================
# DATASET EXPLORER
# ==========================================

elif page == "Dataset Explorer":

    st.header("Dataset Explorer")

    dataset_name = st.selectbox(
        "Select Dataset",
        list(cleaned.keys())
    )

    df = cleaned[dataset_name]

    st.write(f"Shape: {df.shape}")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )