from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
from sklearn.metrics import f1_score


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
	y = train_data["knight"].map({"Jedi": 1, "Sith": 0})

	X_train, X_validation, y_train, y_validation = train_test_split(
		X,
		y,
		test_size=0.20,
		random_state=42,
		stratify=y,
	)

	model = RandomForestClassifier(random_state=42)

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
	
	rand =RandomizedSearchCV(
		model,
		param_distributions=param_grid,
		n_iter=50,
		scoring="f1",
		cv=5,
		random_state=42,
		n_jobs=-1
	)

	rand.fit(X_train, y_train)

	print("Best parameters found in RandomizedSearchCV: ")
	print(rand.best_params_)

	print("Best score found in RandomizedSearchCV: ")
	print(rand.best_score_)

	# get the best model from the grid search
	best_model = rand.best_estimator_

	# make predictions on the test set using the best model
	# test_prediction = best_model.predict(X_test)
	validation_prediction = best_model.predict(X_validation)

	# calculate the f1 score of the predictions

	validation_f1_score = f1_score(
		y_validation,
		validation_prediction,
		pos_label=1
	)
	print(f"Validation F1 Score: {validation_f1_score}")

	# get the results of the randomized search as a pandas DataFrame
	results_df = pd.DataFrame(rand.cv_results_)

	print("\n\n")
	print(
	    results_df[
	        [
	            "params",
	            "mean_test_score",
	            "std_test_score",
	            "rank_test_score"
	        ]
	    ]
	    .sort_values("rank_test_score")
	)


if __name__ == "__main__":
	main()
