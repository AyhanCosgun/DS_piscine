
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


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

    # Train seperating / mixing scatter plots

    SEPERATING_PAIR = ("Empowered", "Prescience")
    MIXING_PAIR = ("Midi-chlorien", "Push")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for label, group in train_data.groupby("knight"):
        axes[0].scatter(group[SEPERATING_PAIR[0]], group[SEPERATING_PAIR[1]],
                        color='blue' if label == "Jedi" else 'red',
                        alpha=0.5 if label == "Jedi" else 0.3,
                        label=label,
                        s=40)
    axes[0].set(title="Train Data Seperating Plot",
                xlabel=SEPERATING_PAIR[0],
                ylabel=SEPERATING_PAIR[1])
    axes[0].legend()

    for label, group in train_data.groupby("knight"):
        axes[1].scatter(group[MIXING_PAIR[0]], group[MIXING_PAIR[1]],
                        color='blue' if label == "Jedi" else 'red',
                        alpha=0.5 if label == "Jedi" else 0.3,
                        label=label,
                        s=40)
    axes[1].set(title="Train Data Mixing Plot",
                xlabel=MIXING_PAIR[0],
                ylabel=MIXING_PAIR[1])
    axes[1].legend()

    fig.tight_layout(w_pad=10.0)
    output_dir = Path(__file__).resolve().parent
    fig.savefig(
        output_dir / "Train_seperating-mixing.png",
        bbox_inches="tight",
        dpi=200)
    plt.show()


# Test seperating / mixing scatter plots

    SEPERATING_PAIR = ("Empowered", "Prescience")
    MIXING_PAIR = ("Midi-chlorien", "Push")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    axes[0].scatter(test_data[SEPERATING_PAIR[0]], test_data[SEPERATING_PAIR[1]],
                    color='green',
                    alpha=0.5,
                    label="Knight",
                    s=40)
    axes[0].set(title="Test Data Seperating Plot",
                xlabel=SEPERATING_PAIR[0],
                ylabel=SEPERATING_PAIR[1])
    axes[0].legend()

    axes[1].scatter(test_data[MIXING_PAIR[0]], test_data[MIXING_PAIR[1]],
                    color='green',
                    alpha=0.5,
                    label="Knight",
                    s=40)
    axes[1].set(title="Test Data Mixing Plot",
                xlabel=MIXING_PAIR[0],
                ylabel=MIXING_PAIR[1])
    axes[1].legend()

    fig.tight_layout(w_pad=10.0)
    output_dir = Path(__file__).resolve().parent
    fig.savefig(
        output_dir / "Test_seperating-mixing.png",
        bbox_inches="tight",
        dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
