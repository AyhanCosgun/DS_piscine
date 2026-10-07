import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path





from itertools import product

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

    X = train_data.drop(columns=["knight"])
    y = train_data["knight"]

    X_test = test_data

    X_train, X_validation, y_train, y_validation = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("Train set boyutu:", X_train.shape)
    print("Validation set boyutu:", X_validation.shape)
    print("y_train boyutu:", y_train.shape)
    print("y_validation boyutu:", y_validation.shape)

    candidate_depths = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, None]

    best_depth = None
    best_DT_f1 = -1.0

    print("\nValidation sonuçları (Decision Tree):")
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


    print("\nEn iyi hyperparameter:")
    print("max_depth =", best_depth)
    print("Validation F1 =", f"{best_DT_f1:.4f}")



    print("\n\nValidation sonuçları (Random Forest):")
    print("--------------------")



    # En iyi Random Forest hiperparametreleri
    best_RF_params = {'n_estimators': [20],
                      'max_depth': [None],
                      'min_samples_split': [2],
                      'min_samples_leaf': [1],
                      'max_features': ['sqrt'],
                      'criterion': ['gini'],
                      'class_weight': ['balanced'],
                      'bootstrap': [False],
                      'max_leaf_nodes': [20]}

    best_RF_score = -1
    keys = list(best_RF_params.keys())
    # best_RF_f1 = -1.0
    # best_n_estimators = 1
    # candidate_n_estimators = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for values in product(*(best_RF_params[key] for key in keys)):
        params = dict(zip(keys, values))
        model = RandomForestClassifier(**params, random_state=42)

        model.fit(X_train, y_train)

        validation_pred = model.predict(X_validation)

        score = f1_score(
            y_validation,
            validation_pred,
            pos_label="Jedi",
        )

        if score > best_RF_score:
            best_RF_score = score
            best_params = params.copy()

    print("Best F1:", best_RF_score)
    print("Best parameters:")
    print(best_params)

        # print(f"n_estimators={str(n_estimators):>4} -> F1={score:.4f}")

    #     if score > best_RF_f1:
    #         best_RF_f1 = score
    #         best_n_estimators = n_estimators


    # print("\nEn iyi hyperparameter:")
    # print("n_estimators =", best_n_estimators)
    # print("Validation F1 =", f"{best_RF_f1:.4f}")


    final_model = DecisionTreeClassifier(
        criterion="gini",
        max_depth=best_depth,
        random_state=42,
    )


    # ------------------------------------------------------------
    # 8. Final modeli tüm labeled training verisiyle eğit
    # ------------------------------------------------------------

    final_model.fit(X, y)


    # ------------------------------------------------------------
    # 9. Test verisi üzerinde prediction yap
    # ------------------------------------------------------------

    test_predictions = final_model.predict(X_test)


    with open(f"{output_dir}/Tree.txt", "w", encoding="utf-8") as file:
        for prediction in test_predictions:
            file.write(f"{prediction}\n")

    print("\nTree.txt oluşturuldu.")


    plt.figure(figsize=(24, 12))

    plot_tree(
        final_model,
        feature_names=X.columns,
        class_names=final_model.classes_,
        filled=True,
        rounded=True,
        fontsize=8,
    )

    plt.tight_layout()
    plt.savefig(
        output_dir / "Tree.png",
        bbox_inches="tight",
        dpi=200
        )
    plt.show()

if __name__ == "__main__":
    main()
