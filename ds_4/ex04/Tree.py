import pandas as pd
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor


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
    output_dir = Path(__file__).resolve().parent
    train_path = output_dir.parent / "Train_knight.csv"

    train_data = load_csv(train_path)
    if train_data is None:
        print(f"Failed to load {train_path.name}.")
        print("Aborting...")
        return
    Jedi_count = train_data["Knight"].sum()
    Sith_count = train_data['Sith'].sum()
    print(f"Jedi count: {Jedi_count}")
    print(f"Sith count: {Sith_count}")


if __name__ == "__main__":
    main()
