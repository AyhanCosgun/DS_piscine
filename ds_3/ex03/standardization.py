import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler

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

    scalar = StandardScaler()
    feature_columns = [c for c in train_data.columns if c != "knight"]
    train_data_scaled = scalar.fit_transform(train_data[feature_columns])
    train_data_scaled_df = pd.DataFrame(
        train_data_scaled,
        columns=feature_columns).join(train_data["knight"])
    test_data_scaled_df = pd.DataFrame(
        scalar.fit_transform(
        test_data),
        columns=feature_columns)

    pd.options.display.float_format = "{:.2f}".format
    print("Train data scaled:")
    print(train_data_scaled_df[feature_columns])
    print()
    print("Test data scaled:")
    print(test_data_scaled_df)


    # Standardized data scatter plots

    SEPERATING_PAIR = ("Empowered", "Prescience")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for label, group in train_data_scaled_df.groupby("knight"):
        axes[0].scatter(group[SEPERATING_PAIR[0]], group[SEPERATING_PAIR[1]],
                color='blue' if label == "Jedi" else 'red',
                alpha=0.5 if label == "Jedi" else 0.3,
                label=label,
                s=40)
    axes[0].set(title="Standardized Train Data Seperating Plot",
                xlabel=SEPERATING_PAIR[0],
                ylabel=SEPERATING_PAIR[1])
    axes[0].legend()

    axes[1].scatter(test_data_scaled_df[SEPERATING_PAIR[0]],
                    test_data_scaled_df[SEPERATING_PAIR[1]],
            color='green',
            alpha=0.5,
            label="Knight",
            s=40)
    axes[1].set(title="Standardized Test Data Seperating Plot",
                xlabel=SEPERATING_PAIR[0],
                ylabel=SEPERATING_PAIR[1])
    axes[1].legend()

    fig.tight_layout(w_pad=10.0)
    output_dir = Path(__file__).resolve().parent
    fig.savefig(
        output_dir / "Standardized_Data_plots.png",
        bbox_inches="tight",
        dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
