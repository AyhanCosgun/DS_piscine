import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


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

    train_data = train_data.drop(columns=["knight"])

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(train_data)

    pca = PCA()
    pca.fit(scaled_data)

    variance_percentages = pca.explained_variance_ratio_ * 100
    print("Variances (Percentage):")
    print(variance_percentages)

    cumulative_percentages = variance_percentages.cumsum()
    print("Cumulative Variances (Percentage):")
    print(cumulative_percentages)

    plt.figure(figsize=(10, 8))
    sns.lineplot(
        x=range(1, len(cumulative_percentages) + 1),
        y=cumulative_percentages
        )
    plt.title("Cumulative Explained Variance by PCA Components")
    plt.xlabel("Number of components")
    plt.ylabel("Explained Variance (%)")
    plt.savefig(output_dir / "cumulative_explained_variance.png",
                bbox_inches="tight",
                dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
