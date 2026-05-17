import streamlit as st
import pandas as pd
import plotly.express as px

from ingestion import load_datasets
from preprocessing import preprocess_datasets
from trust_score import compute_trust_score
from relationships import detect_relationships
from matcher import rank_datasets

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Semantic Data Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.metric-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #333;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("Semantic Data Intelligence Platform")

st.markdown("""
AI-powered platform for:

- Dataset Trust Scoring
- Relationship Discovery
- Semantic Dataset Matching
- Urban Data Intelligence
""")

# =========================================================
# LOAD DATA
# =========================================================

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

# =========================================================
# SIDEBAR
# =========================================================

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

# =========================================================
# OVERVIEW PAGE
# =========================================================

if page == "Overview":

    st.header("Platform Overview")

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

    # =====================================================
    # KPI METRICS
    # =====================================================

    total_datasets = len(cleaned)
    avg_trust = round(overview_df["Trust Score"].mean(), 2)
    highest_trust = round(overview_df["Trust Score"].max(), 2)
    total_rows = overview_df["Rows"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Datasets", total_datasets)
    col2.metric("Average Trust", avg_trust)
    col3.metric("Highest Trust", highest_trust)
    col4.metric("Total Records", f"{total_rows:,}")

    st.divider()

    # =====================================================
    # TRUST SCORE BAR CHART
    # =====================================================

    st.subheader("Dataset Trust Rankings")

    chart_df = overview_df.sort_values(
        by="Trust Score",
        ascending=False
    )

    fig = px.bar(
        chart_df,
        x="Trust Score",
        y="Dataset",
        orientation="h",
        color="Trust Score",
        height=600,
        title="Trust Score Comparison Across Datasets"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # DATAFRAME
    # =====================================================

    st.subheader("Dataset Summary")

    st.dataframe(
        overview_df,
        use_container_width=True
    )

# =========================================================
# TRUST SCORE PAGE
# =========================================================

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

    st.divider()

    # =====================================================
    # RADAR / BAR VISUALIZATION
    # =====================================================

    score_df = pd.DataFrame({
        "Metric": [
            "Completeness",
            "Uniqueness",
            "Consistency",
            "Trust Score"
        ],
        "Value": [
            scores['completeness'],
            scores['uniqueness'],
            scores['consistency'],
            scores['trust_score']
        ]
    })

    fig = px.bar(
        score_df,
        x="Metric",
        y="Value",
        color="Metric",
        title="Trust Score Components"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =====================================================
    # AI-STYLE INSIGHTS
    # =====================================================

    st.subheader("Automated Insights")

    if scores["trust_score"] >= 95:
        st.success(
            "Excellent dataset quality detected with strong reliability."
        )

    elif scores["trust_score"] >= 85:
        st.warning(
            "Moderately high-quality dataset with minor inconsistencies."
        )

    else:
        st.error(
            "Low trust dataset detected. Additional cleaning recommended."
        )

# =========================================================
# RELATIONSHIPS PAGE
# =========================================================

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

        st.subheader("Detected Relationships")

        st.dataframe(
            rel_df,
            use_container_width=True
        )

        # =================================================
        # CONFIDENCE DISTRIBUTION
        # =================================================

        fig = px.histogram(
            rel_df,
            x="Confidence",
            nbins=20,
            title="Relationship Confidence Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning("No relationships detected.")

# =========================================================
# DATASET MATCHING PAGE
# =========================================================

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

    st.subheader("Matching Results")

    st.dataframe(
        match_df,
        use_container_width=True
    )

    # =====================================================
    # MATCH SCORE VISUALIZATION
    # =====================================================

    fig = px.bar(
        match_df,
        x="Match Score",
        y="Dataset",
        orientation="h",
        color="Match Score",
        title="Semantic Similarity Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# DATASET EXPLORER
# =========================================================

elif page == "Dataset Explorer":

    st.header("Dataset Explorer")

    dataset_name = st.selectbox(
        "Select Dataset",
        list(cleaned.keys())
    )

    df = cleaned[dataset_name]

    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))
    col3.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

    st.divider()

    st.subheader("Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

    st.subheader("Column Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )