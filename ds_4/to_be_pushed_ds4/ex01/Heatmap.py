import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


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

    train_data["knight"] = train_data["knight"].map({"Jedi": 0, "Sith": 1})

    correlations = train_data.corr(method="pearson")

    plt.figure(figsize=(14, 12))
    sns.heatmap(correlations,
                center=0,
                cmap="rocket",
                square=True
                )
    plt.title("Correlation Heatmap")
    plt.savefig(output_dir / "correlation_heatmap.png",
                bbox_inches="tight",
                dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
