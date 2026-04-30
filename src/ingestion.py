import pandas as pd
import os

def load_datasets(folder_path):
    datasets = {}
    
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            path = os.path.join(folder_path, file)
            try:
                df = pd.read_csv(path, low_memory=False, nrows=200000)
                datasets[file] = df
                print(f"Loaded {file} | Shape: {df.shape}")
            except Exception as e:
                print(f"Error loading {file}: {e}")
    
    return datasets


if __name__ == "__main__":
    data = load_datasets("data/raw")
    print(f"\nTotal datasets loaded: {len(data)}")