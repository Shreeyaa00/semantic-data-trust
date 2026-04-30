from ingestion import load_datasets
from preprocessing import preprocess_datasets
from trust_score import compute_trust_score
from relationships import detect_relationships

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
    print("\n=== TRUST SCORES ===\n")

    for name, df in cleaned.items():
        scores = compute_trust_score(df)
    
        print(f"\nDataset: {name}")
        print(scores)
    
    print("\n=== RELATIONSHIPS ===\n")

    for name, df in list(cleaned.items())[:3]:  # test on 3 datasets first
        print(f"\nDataset: {name}")
    
        rels = detect_relationships(df)

        for r in rels[:5]:  # show top 5
            print(f"{r[0]} → {r[1]} (confidence: {r[2]})")