# initialize friedman dataset
import logging
from pathlib import Path

import pandas as pd

from stac import bonferroni_dunn_test, friedman_test, holm_test

# PATHING
BASE_DIR = Path("data")
RESULTS_BASE_DIR = Path("results")
LOGS_BASE_DIR = Path("logs")
FRIEDMAN_BASE_DIR = Path("friedman")
FRIEDMAN_TABLES_DIR = FRIEDMAN_BASE_DIR / "tables"
FRIEDMAN_RANKING_DIR = FRIEDMAN_BASE_DIR / "ranking"
BONFERRONI_DUNN_DIR = FRIEDMAN_BASE_DIR / "bonferroni_dunn"
HOLM_DIR = FRIEDMAN_BASE_DIR / "holm"
FRIEDMAN_TABLES_DIR.mkdir(parents=True, exist_ok=True)
FRIEDMAN_RANKING_DIR.mkdir(parents=True, exist_ok=True)
BONFERRONI_DUNN_DIR.mkdir(parents=True, exist_ok=True)
HOLM_DIR.mkdir(parents=True, exist_ok=True)

# LOGGING SETUP
logging.basicConfig(
    filename=LOGS_BASE_DIR / "friedman.log",
    filemode="w",
    level="INFO",
    format="%(levelname)s - %(asctime)s - %(message)s",
)

models = [
    "DecisionTreeRegressor",
    "RandomForestRegressor",
    "GradientBoostingRegressor",
    "XGBoostRegressor",
    "SVR",
]
datasets = ["air_quality", "traffic", "energy", "power", "parking", "room", "solar"]


if __name__ == "__main__":
    # iterate over models
    for model in models:
        # iterate over the other models
        for model_2 in models:
            logging.info(f"Friedman {model} & {model_2}...")
            # initialize dataframe for each combination (25 df)
            friedman_df = pd.DataFrame(
                columns=["model", "2nd_model", "cascade", "voting"]
            )

            # iterate over datasets
            for dataset in datasets:
                RESULTS_PATH = RESULTS_BASE_DIR / dataset.upper()
                METRICS_CSV = RESULTS_PATH / "metrics.csv"
                metrics = pd.read_csv(METRICS_CSV)

                # isolate plane model run for the first model
                first_model = metrics[
                    (metrics["model"] == model) & (metrics["type"] == "plain")
                ]
                first_model_mse = first_model["mse"].tolist()[0]

                # isolate plane model run for the second model
                second_model = metrics[
                    (metrics["model"] == model_2) & (metrics["type"] == "plain")
                ]
                second_model_mse = second_model["mse"].tolist()[0]

                # isolate cascade model run with base model the first model
                cascade = metrics[
                    (metrics["model"] == model)
                    & (metrics["2nd_model"] == model_2)
                    & (metrics["type"] == "cascade")
                ]
                cascade_mse = cascade["mse"].tolist()[0]

                # isolate voting with base model the first model
                voting = metrics[
                    (metrics["model"] == model)
                    & (metrics["2nd_model"] == model_2)
                    & (metrics["type"] == "voting")
                ]
                voting_mse = voting["mse"].tolist()[0]

                # create a row for the dataframe
                row = {
                    "model": first_model_mse,
                    "2nd_model": second_model_mse,
                    "cascade": cascade_mse,
                    "voting": voting_mse,
                }

                # append the row to the dataframe with index the dataset name
                friedman_df.loc[dataset] = row

            # save the dataframe
            friedman_df = friedman_df.reset_index(drop=True)
            friedman_df.to_csv(FRIEDMAN_TABLES_DIR / f"{model}_{model_2}.csv")
            logging.info(f"Friedman tables for {model} & {model_2} saved.")

            # compute the friedman test
            friedman_df = friedman_df.reset_index(drop=True)
            statistic, p_value, ranking, rank_cmp = friedman_test(
                *friedman_df.to_dict().values()
            )
            friedman = pd.DataFrame(index=friedman_df.columns.tolist())
            friedman["ranking"] = ranking
            friedman = friedman.sort_values(by="ranking")
            friedman.to_csv(FRIEDMAN_RANKING_DIR / f"{model}_{model_2}.csv")
            logging.info(f"Friedman for {model} & {model_2} finished.")

            # post-hock: create a dictionary with format 'groupname':'pivotal quantity'
            ranking_dict = dict(zip(friedman_df.columns, ranking))

            # post-hock: compute the bonferroni-dunn test
            comparisons, z_values, p_values, adj_p_values = bonferroni_dunn_test(
                ranking_dict, control="cascade"
            )
            bonferroni_dunn = pd.DataFrame(index=comparisons)
            bonferroni_dunn["z_values"] = z_values
            bonferroni_dunn["p_values"] = p_values
            bonferroni_dunn["adj_p_values"] = adj_p_values
            bonferroni_dunn.to_csv(BONFERRONI_DUNN_DIR / f"{model}_{model_2}.csv")
            logging.info(f"Bonferroni-Dunn for {model} & {model_2} finished.")

            # post-hoc: holms test
            comparisons, z_values, p_values, adj_p_values = holm_test(
                ranking_dict, control="cascade"
            )
            holm = pd.DataFrame(index=comparisons)
            holm["z_values"] = z_values
            holm["p_values"] = p_values
            holm["adj_p_values"] = adj_p_values
            holm.to_csv(HOLM_DIR / f"{model}_{model_2}.csv")
            logging.info(f"Holm for {model} & {model_2} finished.")
