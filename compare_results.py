from collections import Counter
from pathlib import Path

import pandas as pd

RESULTS_BASE_DIR = Path("results")
FRIEDMAN_BASE_DIR = Path("friedman")
FRIEDMAN_TABLES = FRIEDMAN_BASE_DIR / "tables"
COMPARISON_TABLES = FRIEDMAN_BASE_DIR / "comparison_tables"
COMPARISON_TABLES.mkdir(parents=True, exist_ok=True)

datasets = [
    "air_quality",
    "traffic",
    "energy",
    "power",
    "parking",
    "room",
    "solar",
    "kolkata",
    "turbine",
    "joho",
    "electricity",
    "iot",
    # "home",
]

if __name__ == "__main__":
    # create a dict to save the best model for each dataset
    best_models = pd.DataFrame(
        columns=["dataset", "model", "2nd_model", "type", "mse", "rmse"]
    )
    for dataset in datasets:
        print(f"Dataset: {dataset}")
        try:
            RESULTS_PATH = RESULTS_BASE_DIR / dataset.upper()
            METRICS_CSV = RESULTS_PATH / "metrics.csv"
            metrics = pd.read_csv(METRICS_CSV)
        except FileNotFoundError:
            print(f"File not found for {dataset}")
            continue

        # sort by mse
        metrics = metrics.sort_values(by="mse")

        # get the best model
        best_model = metrics.iloc[0]
        best_models = best_models.append(best_model, ignore_index=True)

        # add dataset name
        best_models.loc[best_models.index[-1], "dataset"] = dataset

        # save the best model for each dataset
        best_models.to_csv(RESULTS_BASE_DIR / "best_models.csv", index=False)

    # print percentages of each best model type
    print(best_models["type"].value_counts(normalize=True))

    # load the friedman tables
    counter = Counter()
    for table in FRIEDMAN_TABLES.glob("*.csv"):
        ft = pd.read_csv(table)
        ft = ft.reset_index(drop=True)
        ft = ft.drop(columns=["Unnamed: 0"])

        # create a column that indicates if the cascade is better than voting
        ft["cascade_better"] = ft["cascade"] < ft["voting"]

        # create a column to indicate if the 2nd_model is better than the 1st
        ft["2nd_better"] = ft["2nd_model"] < ft["model"]

        # create a column to indicate if the 2nd and the cascade are better simultaneously
        ft["2nd_cascade_better"] = ft["2nd_better"] & ft["cascade_better"]

        # create a row that has the sum of the cascade_better column
        ft.loc["sum"] = ft.sum()

        # count a how many times the cascade is better than voting
        counter["cascade_better"] = (
            counter["cascade_better"] + ft["cascade_better"].loc["sum"]
        )
        counter["2nd_better"] = counter["2nd_better"] + ft["2nd_better"].loc["sum"]
        counter["2nd_cascade_better"] = (
            counter["2nd_cascade_better"] + ft["2nd_cascade_better"].loc["sum"]
        )
        counter["total"] = counter["total"] + len(ft) - 1

        # reset index and replace each value except the last one with the dataset names
        ft = ft.reset_index()
        for i, dataset in enumerate(datasets):
            ft.loc[i, "index"] = dataset

        # save the comparison table
        ft.to_csv(COMPARISON_TABLES / table.name)

    print(f"Counter: {counter}")
