import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score, precision_score
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
		print("Usage: python KNN.py Train_knight.csv Test_knight.csv")
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
	results = []

	best_KNN_f1 = -1.0
	best_f1_k = -1
	for k in range(1, 30):
		model = Pipeline([
			('scaler', StandardScaler()),
			('knn', KNeighborsClassifier(n_neighbors=k))
		])

		model.fit(X_train, y_train)
		validation_pred = model.predict(X_validation)

		precision = precision_score(y_validation, validation_pred, average='weighted')
		f1 = f1_score(y_validation, validation_pred, average='weighted')

		if f1 > best_KNN_f1:
			best_KNN_f1 = f1
			best_f1_k = k

		results.append({
			"k": k,
			"precision": precision,
			"f1": f1,
		})

	results_df = pd.DataFrame(results)

	print("\nValidation results:")
	print("--------------------")
	print(results_df.to_string(index=False, header=["k", "Precision", "F1 Score"]))

	print(f"\nBest KNN model: k={best_f1_k}, F1 Score={best_KNN_f1:.4f}")

	# Model selection based on the best k-value
	final_model = Pipeline([
		('scaler', StandardScaler()),
		('knn', KNeighborsClassifier(n_neighbors=best_f1_k))
	])
	final_model.fit(X_train, y_train)

	test_predictions = final_model.predict(X_test)

	with open(output_dir / "KNN.txt", "w", encoding="utf-8") as file:
		for prediction in test_predictions:
			file.write(f"{prediction}\n")

	print(f"Predictions saved to {output_dir.name}/KNN.txt")

	# k-values vs precision plot
	plt.figure(figsize=(10, 8))
	sns.lineplot(
		data=results_df,
		x="k",
		y="precision"
		)
	plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
	plt.title("KNN: k-values vs Precision")
	plt.xlabel("k values")
	plt.ylabel("accuracy")
	plt.savefig(output_dir / "knn_precision_plot.png", bbox_inches="tight", dpi=200)
	plt.show()


if __name__ == "__main__":
	main()

