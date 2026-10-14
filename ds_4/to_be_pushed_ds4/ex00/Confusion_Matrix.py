from pathlib import Path
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def load_txt(path: Path) -> list:
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]

    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return []


def main():
    if len(sys.argv) != 3:
        print("Usage: python Confusion_Matrix.py <predictions_file_name> <truth_file_name>")
        return

    output_dir = Path(__file__).resolve().parent

    predictions_path = output_dir.parent / sys.argv[1]
    truth_path = output_dir.parent / sys.argv[2]
    predictions = load_txt(predictions_path)
    truth = load_txt(truth_path)

    if not predictions:
        print(f"Failed to load {predictions_path.name}.")
        print("Aborting...")
        return

    if not truth:
        print(f"Failed to load {truth_path.name}.")
        print("Aborting...")
        return

    assert len(predictions) == len(truth), "Predictions and truth lists must be of the same length."

    class_to_index = {"Jedi": 0, "Sith": 1}

    confusion_matrix = np.zeros((2, 2), dtype=int)

    for pred, true in zip(predictions, truth):
        confusion_matrix[class_to_index[true], class_to_index[pred]] += 1

    TN, FP, FN, TP = confusion_matrix.ravel()

    total_P = confusion_matrix[1, :].sum()
    total_N = confusion_matrix[0, :].sum()
    total = total_P + total_N

    accuracy = (TP + TN) / total if total > 0 else 0
    precision_P = TP / (TP + FP) if (TP + FP) > 0 else 0
    precision_F = TN / (TN + FN) if (TN + FN) > 0 else 0
    recall_P = TP / (TP + FN) if (TP + FN) > 0 else 0
    recall_F = TN / (TN + FP) if (TN + FP) > 0 else 0
    f1_score_P = (2 * precision_P * recall_P) / (precision_P + recall_P) \
        if (precision_P + recall_P) > 0 else 0
    f1_score_F = (2 * precision_F * recall_F) / (precision_F + recall_F) \
        if (precision_F + recall_F) > 0 else 0

    report = pd.DataFrame(
        {
            "precision": ["", precision_F, precision_P, "", ""],
            "recall": ["", recall_F, recall_P, "", ""],
            "f1-score": ["", f1_score_F, f1_score_P, "", accuracy],
            "total": ["", total_N, total_P, "", total]
        },
        index=["", "Jedi", "Sith", "", "accuracy"]
    )

    pd.options.display.float_format = "{:.2f}".format
    print(report)
    print()
    print(confusion_matrix)

    # Create a heatmap of the confusion matrix
    sns.heatmap(confusion_matrix,
                annot=True,
                fmt="d",
                cmap="viridis"
                )
    plt.xlabel("Prediction")
    plt.ylabel("Truth")
    plt.title("Confusion Matrix")
    plt.savefig(f"{output_dir}/confusion_matrix.png",
                dpi=200, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()
