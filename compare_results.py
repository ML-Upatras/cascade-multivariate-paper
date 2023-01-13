from pathlib import Path

import pandas as pd

RESULTS_BASE_DIR = Path("results")
FRIEDMAN_BASE_DIR = Path("friedman")

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
    "home",
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
