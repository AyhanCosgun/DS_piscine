import pandas as pd
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor


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


def calculate_vif(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i in range(df.shape[1]):
        vif = variance_inflation_factor(df.values, i)
        rows.append({
            "feature": df.columns[i],
            "VIF": vif,
            "Tolerance": 1 / vif if vif != 0 else float('inf')})
    return pd.DataFrame(rows)


def main():
    output_dir = Path(__file__).resolve().parent
    train_path = output_dir.parent / "Train_knight.csv"

    train_data = load_csv(train_path)
    if train_data is None:
        print(f"Failed to load {train_path.name}.")
        print("Aborting...")
        return

    train_data = train_data.drop(columns=["knight"])
    copy_data = train_data.copy()

    print("\nCalculating VIF and Tolerance for raw data ...")
    print(calculate_vif(copy_data))

    print("\nStarting feature selection process...")
    while True:
        vif_values = []
        for i in range(copy_data.shape[1]):
            vif = variance_inflation_factor(copy_data.values, i)
            vif_values.append(vif)

        vif = pd.Series(vif_values, index=copy_data.columns)
        max_vif = vif.max()
        max_vif_feature = vif.idxmax()

        if max_vif < 5:
            break
        print(f"Removing '{max_vif_feature}' with VIF: {max_vif}")
        copy_data = copy_data.drop(columns=[max_vif_feature])

    print("\nFinal data after feature selection:")
    print(calculate_vif(copy_data))


if __name__ == "__main__":
    main()
