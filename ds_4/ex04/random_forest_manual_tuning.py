from itertools import product
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path


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

    X = train_data.drop(columns=["knight"])
    y = train_data["knight"]

    X_train, X_validation, y_train, y_validation = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    param_grid = {
        "n_estimators": [20, 50, 100],
        "max_depth": [2, 4, 6, None],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2],
        "max_features": ["sqrt", "log2"],
        "criterion": ["gini", "entropy"],
        "class_weight": [None, "balanced"],
        "bootstrap": [True, False],
        "max_leaf_nodes": [None, 20, 50],
    }

    best_score = -1
    best_params = None

    keys = list(param_grid.keys())

    for values in product(*(param_grid[key] for key in keys)):

        params = dict(zip(keys, values))

        model = RandomForestClassifier(
            **params,
            random_state=42
        )

        model.fit(X_train, y_train)

        prediction = model.predict(X_validation)

        score = f1_score(
            y_validation,
            prediction,
            pos_label="Jedi"
        )

        if score > best_score:
            best_score = score
            best_params = params.copy()

    print("Best F1:", best_score)
    print("Best parameters:")
    print(best_params)

if __name__ == "__main__":
    main()