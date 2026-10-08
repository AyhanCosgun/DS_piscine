import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier
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
		print("Usage: python Tree_random_forest_version.py Train_knight.csv Test_knight.csv")
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

	print("\n\nValidation sonuçları (Random Forest):")
	print("--------------------")


	# En iyi Random Forest hiperparametreleri
	best_RF_params_manuel = {
		'bootstrap': False,
		'n_estimators': 20,
		'max_depth': None,
		'min_samples_split': 2,
		'min_samples_leaf': 1,
		'max_features': 'sqrt',
		'criterion': 'gini',
		'class_weight': 'balanced',
		'max_leaf_nodes': 20,
		'random_state': 42
		}

	best_RF_params_GridSearch = {
		'bootstrap': True,
		'n_estimators': 100,
		'max_depth': 6,
		'min_samples_split': 5,
		'min_samples_leaf': 1,
		'max_features': 'sqrt',
		'criterion': 'entropy',
		'class_weight': None,
		'max_leaf_nodes': None,
		'random_state': 42
	}

	best_RF_params_RandomizedSearch = {
		'bootstrap': True,
		'n_estimators': 100,
		'max_depth': 6,
		'min_samples_split': 2,
		'min_samples_leaf': 2,
		'max_features': 'sqrt',
		'criterion': 'entropy',
		'class_weight': None,
		'max_leaf_nodes': None,
		'random_state': 42
	}


	model_manuel = RandomForestClassifier(**best_RF_params_manuel)
	model_GridSearch = RandomForestClassifier(**best_RF_params_GridSearch)
	model_RandomizedSearch = RandomForestClassifier(**best_RF_params_RandomizedSearch)
	model_manuel.fit(X_train, y_train)
	model_GridSearch.fit(X_train, y_train)
	model_RandomizedSearch.fit(X_train, y_train)

	validation_pred_1 = model_manuel.predict(X_validation)
	validation_pred_2 = model_GridSearch.predict(X_validation)
	validation_pred_3 = model_RandomizedSearch.predict(X_validation)

	tree_sample = model_manuel.estimators_[0]

	score_1 = f1_score(
		y_validation,
		validation_pred_1,
		pos_label="Jedi",
	)

	score_2 = f1_score(
		y_validation,
		validation_pred_2,
		pos_label="Jedi",
	)

	score_3 = f1_score(
		y_validation,
		validation_pred_3,
		pos_label="Jedi",
	)

	print("Best F1 (Model 1):", score_1)
	print("Best F1 (Model 2):", score_2)
	print("Best F1 (Model 3):", score_3)


	final_model = model_manuel  # En iyi modeli seçin (manuel ayarlanmış model)
	# final_model = model_GridSearch  # En iyi modeli seçin (GridSearch ile ayarlanmış model)
	# final_model = model_RandomizedSearch  # En iyi modeli seçin (RandomizedSearch ile ayarlanmış model)


	final_model.fit(X, y)


	test_predictions = final_model.predict(X_test)

	tree_sample = final_model.estimators_[0]  # Random Forest içindeki bir karar ağacını örnek olarak alıyoruz
	with open(f"{output_dir}/Tree.txt", "w", encoding="utf-8") as file:
		for prediction in test_predictions:
			file.write(f"{prediction}\n")

	print("\nTree.txt oluşturuldu.")


	plt.figure(figsize=(24, 12))

	plot_tree(
		tree_sample,
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
