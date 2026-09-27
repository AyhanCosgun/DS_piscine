import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def load_csv(path: Path) -> pd.DataFrame | None:
    """
    Loads a CSV file into a pandas DataFrame.
    """
    
    try:
        df = pd.read_csv(path)
        print(f"Loadind dataset of dimensions: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def main():
    train_path = Path(__file__).resolve().parent.parent / "Train_knight.csv"
   
    train_data = load_csv(train_path)
    if train_data is None:
        print(f"Failed to load {train_path.name}.")
        print("Aborting...")
        return

    y = train_data["knight"].map({"Jedi": 1, "Sith": 0})
    X = train_data.drop(columns="knight")

    correlations = X.corrwith(y, method="pearson").sort_values(ascending=False)
    result = pd.concat([pd.Series({"knight": 1.0}), correlations])
    print(result.to_string(float_format=lambda value: f"{value:.6f}"))

if __name__ == "__main__":
    main()
