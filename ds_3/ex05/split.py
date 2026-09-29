#! /home/ayhan/python-projects/venv/bin/python3.10
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import sys


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
    if len(sys.argv) != 2:
        print("Usage: python split.py Train_knight.csv")
        return
    train_path = Path(__file__).resolve().parent / sys.argv[1]

    train_data = load_csv(train_path)
    if train_data is None:
        print(f"Failed to load {train_path.name}.")
        print("Aborting...")
        return

    training, validation = train_test_split(
        train_data, test_size=0.2,
        random_state=42,
        shuffle=True,
        stratify=train_data["knight"]
    )

    assert len(training) + len(validation) == len(train_data)
    assert training.index.intersection(validation.index).empty
    assert list(training.columns) == list(validation.columns) == list(train_data.columns)

    print(f"len(training): {len(training)},len(validation): {len(validation)}")

    print("\n Value percentage of train_data:")
    print(train_data["knight"].value_counts(normalize=True).map("{:.2%}".format))

    print("\n Value percentage of training data:")
    print(training["knight"].value_counts(normalize=True).map("{:.2%}".format))

    print("\n Value percentage of validation data:")
    print(validation["knight"].value_counts(normalize=True).map("{:.2%}".format))

    output_dir = Path(__file__).resolve().parent
    training.to_csv(output_dir / "Training_knight.csv", index=False)
    validation.to_csv(output_dir / "Validation_knight.csv", index=False)


if __name__ == "__main__":
    main()
