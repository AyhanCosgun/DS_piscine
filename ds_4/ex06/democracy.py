import sys
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import f1_score, precision_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


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
        print("Usage: python democracy.py Train_knight.csv Test_knight.csv")
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

    tree = DecisionTreeClassifier(
        criterion="gini",
        max_depth=4,
        random_state=42,
    )

    knn = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', KNeighborsClassifier(n_neighbors=11))
    ])

    logistic = Pipeline([
        ('scaler', StandardScaler()),
        ('logistic', LogisticRegression())
    ])

    voting = VotingClassifier(
        estimators=[
            ('decision_tree', tree),
            ('knn', knn),
            ('logistic', logistic)
        ],
        voting='hard'
    )
    voting.fit(X_train, y_train)

    predictions = voting.predict(X_validation)
    f1 = f1_score(y_validation, predictions, average='weighted')
    precision = precision_score(y_validation, predictions, average='weighted')
    accuracy = accuracy_score(y_validation, predictions)

    print(f"\nvoting model:\
           F1 Score = {f1:.2f},\
           Precision = {precision:.2f},\
           Accuracy = {accuracy:.2f}")

    voting.fit(X, y)
    test_predictions = voting.predict(X_test)

    with open(output_dir / "Voting.txt", "w", encoding="utf-8") as file:
        for prediction in test_predictions:
            file.write(f"{prediction}\n")

    print(f"Predictions saved to {output_dir.name}/Voting.txt")


if __name__ == "__main__":
    main()
