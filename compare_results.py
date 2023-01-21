from collections import Counter
from pathlib import Path

import pandas as pd

from src.comparison.algorithm_comparison import algorithm_comparison
from src.comparison.best_models import calculate_best_models
from src.dataset.utils import get_dataset_names

RESULTS_BASE_DIR = Path("results")
FRIEDMAN_BASE_DIR = Path("friedman")
FRIEDMAN_TABLES = FRIEDMAN_BASE_DIR / "tables"
COMPARISON_TABLES = FRIEDMAN_BASE_DIR / "comparison_tables"
DATASET_TABLES = FRIEDMAN_BASE_DIR / "dataset_tables"
COMPARISON_TABLES.mkdir(parents=True, exist_ok=True)
DATASET_TABLES.mkdir(parents=True, exist_ok=True)

datasets = get_dataset_names()

if __name__ == "__main__":
    # calculate the best model for each dataset
    calculate_best_models(datasets, RESULTS_BASE_DIR, FRIEDMAN_BASE_DIR)

    # calculate comparison tables per algorithm combination
    algorithm_comparison(datasets, FRIEDMAN_TABLES, COMPARISON_TABLES)

    # iterate over friedman tables and create different tables per dataset
    counter = Counter()
    for dataset in datasets:
        print(f"Dataset: {dataset}")
        # create a dict to save the best model for each dataset
        df = pd.DataFrame(columns=["model", "2nd_model", "cascade", "voting"])
        for table in COMPARISON_TABLES.glob("*.csv"):
            ct = pd.read_csv(table)

            # get the row that corresponds to the dataset
            dataset_row = ct[ct["index"] == dataset]

            # isolate the columns that we want
            dataset_row = dataset_row[["model", "2nd_model", "cascade", "voting"]]

            # make them int
            dataset_row = dataset_row.astype(float)

            # add to df
            df = df.append(dataset_row, ignore_index=True)

        # create cascade_better column, 2nd_better column and 2nd_cascade_better column
        df["cascade_model"] = df["cascade"] < df["model"]
        df["cascade_2nd"] = df["cascade"] < df["2nd_model"]
        df["cascade_voting"] = df["cascade"] < df["voting"]

        # create a column if cascade is better than all
        df["cascade_better"] = (
            df["cascade_model"] & df["cascade_2nd"] & df["cascade_voting"]
        )

        # add the sum of the cascade_better column
        df.loc["sum"] = df.sum()

        # update counter
        counter["cascade_better"] = (
            counter["cascade_better"] + df["cascade_better"].loc["sum"]
        )
        counter["cascade_voting"] = (
            counter["cascade_voting"] + df["cascade_voting"].loc["sum"]
        )
        counter["total"] = counter["total"] + len(df) - 1

        # save the comparison table
        df.to_csv(DATASET_TABLES / f"{dataset}.csv")

    print(f"Counter: {counter}")
