import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def load_csv(path: Path) -> pd.DataFrame | None:
    """
    Loads a CSV file into a pandas DataFrame.
    """
    
    try:
        df = pd.read_csv(path)
        print(f"Loading dataset of dimensions: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def main():
    """ Verifies the correct standardization and normalization methods for ex03 and ex04."""
    train_path = Path(__file__).resolve().parent.parent / "Train_knight.csv"
    
    train_data = load_csv(train_path)
    if train_data is None:
        print(f"Failed to load {train_path.name}.")
        print("Aborting...")
        return

    feature_columns = [c for c in train_data.columns if c != "knight"]
    raw = train_data.loc[360, feature_columns]

    standardizer = StandardScaler()
    standardized = pd.Series(
        standardizer.fit_transform(train_data[feature_columns])[360],
        index=feature_columns
    )

    normalizer = MinMaxScaler()
    normalized = pd.Series(
        normalizer.fit_transform(train_data[feature_columns])[360],
        index=feature_columns
    )

    comparison = pd.DataFrame({
        "raw": raw,
        "standardized": standardized,
        "normalized": normalized
    })

    print(comparison.to_string(
        float_format=lambda x: f"{x:.2f}"
    ))


if __name__ == "__main__":
    main()
