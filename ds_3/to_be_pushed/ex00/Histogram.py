
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


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
    test_path = Path(__file__).resolve().parent.parent / "Test_knight.csv"
    train_path = Path(__file__).resolve().parent.parent / "Train_knight.csv"

    test_data = load_csv(test_path)
    if test_data is None:
        print(f"Failed to load {test_path.name}.")
        print("Aborting...")
        return

    train_data = load_csv(train_path)
    if train_data is None:
        print(f"Failed to load {train_path.name}.")
        print("Aborting...")
        return

    # Test table histogram
    fig, axes = plt.subplots(6, 5, figsize=(18, 20))

    for column, ax in zip(test_data.columns, axes.flatten()):
        ax.hist(test_data[column], bins=40,
                color='green', alpha=0.5, label="Knight")
        ax.set_title(column)
        ax.legend()

    fig.tight_layout()
    output_dir = Path(__file__).resolve().parent
    fig.savefig(
        output_dir / "Test_table_histogram.png",
        bbox_inches="tight",
        dpi=200)
    plt.show()

    # Train table histogram

    fig, axes = plt.subplots(6, 5, figsize=(18, 20))

    for column, ax in zip(train_data.columns, axes.flatten()):
        edges = np.histogram_bin_edges(train_data[column], bins=40)
        for label, group in train_data.groupby("knight"):
            ax.hist(group[column],
                    color='blue' if label == "Jedi" else 'red',
                    bins=edges,
                    density=True,
                    alpha=0.5 if label == "Jedi" else 0.3,
                    label=label)
        ax.set_title(column)
        ax.legend()

    fig.tight_layout()
    output_dir = Path(__file__).resolve().parent
    fig.savefig(
        output_dir / "Train_table_histogram.png",
        bbox_inches="tight",
        dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
