import pandas as pd

def clean_dataframe(df):
    # Drop columns with too many missing values
    threshold = 0.4
    df = df.dropna(axis=1, thresh=int(len(df) * threshold))

    # Fill remaining missing values
    df = df.fillna("UNKNOWN")

    # Standardize column names
    df.columns = [
        col.strip().lower().replace(" ", "_")
        for col in df.columns
    ]

    # Remove duplicate rows
    df = df.drop_duplicates()

    return df


def preprocess_datasets(datasets):
    cleaned = {}

    for name, df in datasets.items():
        try:
            cleaned_df = clean_dataframe(df)
            cleaned[name] = cleaned_df
            print(f"Cleaned {name} | Shape: {cleaned_df.shape}")
        except Exception as e:
            print(f"Error cleaning {name}: {e}")

    return cleaned