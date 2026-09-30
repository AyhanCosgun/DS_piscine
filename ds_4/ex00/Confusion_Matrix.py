from pathlib import Path
import sys
import numpy as np


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

    predictions_path = Path(__file__).resolve().parent.parent / sys.argv[1]
    truth_path = Path(__file__).resolve().parent.parent / sys.argv[2]
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

    class_to_index = {"Jedi": 1, "Sith": 0}

    TP, TN, FP, FN = 0, 0, 0, 0

    for pred, true in zip(predictions, truth):
        if class_to_index.get(true) == 1 and class_to_index.get(pred) == 1:
            TP += 1
        elif class_to_index.get(true) == 0 and class_to_index.get(pred) == 0:
            TN += 1
        elif class_to_index.get(true) == 1 and class_to_index.get(pred) == 0:
            FN += 1
        elif class_to_index.get(true) == 0 and class_to_index.get(pred) == 1:
            FP += 1

    precision_P = TP / (TP + FP) if (TP + FP) > 0 else 0
    precision_F = TN / (TN + FN) if (TN + FN) > 0 else 0
    recall_P = TP / (TP + FN) if (TP + FN) > 0 else 0
    recall_F = TN / (TN + FP) if (TN + FP) > 0 else 0
    f1_score_P = (2 * precision_P * recall_P) / (precision_P + recall_P) if (precision_P + recall_P) > 0 else 0
    f1_score_F = (2 * precision_F * recall_F) / (precision_F + recall_F) if (precision_F + recall_F) > 0 else 0
    print(f"Precision: {precision_P:.2f}, Recall: {recall_P:.2f}, F1-Score: {f1_score_P:.2f}")
    print(f"Precision: {precision_F:.2f}, Recall: {recall_F:.2f}, F1-Score: {f1_score_F:.2f}")
    confusion_matrix = np.array([[TP, FN], [FP, TN]])
    print(confusion_matrix)


if __name__ == "__main__":
    main()
