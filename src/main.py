from ingestion import load_datasets
from preprocessing import preprocess_datasets

if __name__ == "__main__":
    print("Loading datasets...\n")
    datasets = load_datasets("data/raw")

    print("\nCleaning datasets...\n")
    cleaned = preprocess_datasets(datasets)

    print(f"\nTotal cleaned datasets: {len(cleaned)}")

    # Print sample info
    for name, df in list(cleaned.items())[:2]:
        print(f"\nDataset: {name}")
        print(df.head())