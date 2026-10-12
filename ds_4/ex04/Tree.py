import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score
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

    if len(sys.argv) != 3:
        print("Usage: python Tree.py Train_knight.csv Test_knight.csv")
        return

    output_dir = Path(__file__).resolve().parent

    train_path = output_dir.parent / sys.argv[1]
    train_data = load_csv(train_path)
    if train_data is None:
        print(f"Failed to load {train_path.name}.")
        print("Aborting...")
        return

    test_path = output_dir.parent / sys.argv[2]
    test_data = load_csv(test_path)
    if test_data is None:
        print(f"Failed to load {test_path.name}.")
        print("Aborting...")
        return

    training_path = output_dir.parent / "Training_knight.csv"
    training_data = load_csv(training_path)
    if training_data is None:
        print(f"Failed to load {training_path.name}.")
        print("Aborting...")
        return

    validation_path = output_dir.parent / "Validation_knight.csv"
    validation_data = load_csv(validation_path)
    if validation_data is None:
        print(f"Failed to load {validation_path.name}.")
        print("Aborting...")
        return

    X = train_data.drop(columns=["knight"])
    y = train_data["knight"]

    X_test = test_data

    X_train = training_data.drop(columns=["knight"])
    y_train = training_data["knight"]

    X_validation = validation_data.drop(columns=["knight"])
    y_validation = validation_data["knight"]

    print("Train set dimensions:", X_train.shape)
    print("Validation set dimensions:", X_validation.shape)
    print("y_train dimensions:", y_train.shape)
    print("y_validation dimensions:", y_validation.shape)

    # Hyperparameter tuning
    candidate_depths = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, None]

    best_depth = None
    best_DT_f1 = -1.0

    print("\nValidation results:")
    print("--------------------")

    for depth in candidate_depths:
        model = DecisionTreeClassifier(
            criterion="gini",
            max_depth=depth,
            random_state=42,
        )

        model.fit(X_train, y_train)

        validation_pred = model.predict(X_validation)

        score = f1_score(
            y_validation,
            validation_pred,
            pos_label="Jedi",
        )

        print(f"max_depth={str(depth):>4} -> F1={score:.4f}")

        if score >= best_DT_f1:
            best_DT_f1 = score
            best_depth = depth

    print("\nBest hyperparameter:")
    print("max_depth =", best_depth)
    print("Validation F1 =", f"{best_DT_f1:.4f}")

    # Model selection based on the best hyperparameter
    final_model = DecisionTreeClassifier(
        criterion="gini",
        max_depth=best_depth,
        random_state=42,
    )

    final_model.fit(X, y)

    test_predictions = final_model.predict(X_test)

    with open(f"{output_dir}/Tree.txt", "w", encoding="utf-8") as file:
        for prediction in test_predictions:
            file.write(f"{prediction}\n")
    print(f"Predictions saved to {output_dir.name}/Tree.txt")

    plt.figure(figsize=(24, 12))

    plot_tree(
        final_model,
        feature_names=X.columns,
        class_names=final_model.classes_,
        filled=True,
        rounded=True
    )

    plt.title("Decision tree trained on all Knights features",
              fontsize=18)

    plt.tight_layout()
    plt.savefig(
        output_dir / "Tree.png",
        bbox_inches="tight",
        dpi=200
        )
    plt.show()


if __name__ == "__main__":
    main()
