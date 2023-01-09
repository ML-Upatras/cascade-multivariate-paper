import argparse
import logging
from pathlib import Path

import pandas as pd
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
    VotingRegressor,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.evaluation import calculate_metrics

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument(
    "--data",
    type=str,
    choices=["air_quality", "traffic", "energy", "power", "parking"],
    help="Dataset to use. Choose between air_quality, traffic, energy, power, parking",
)
parser.add_argument(
    "--logging",
    type=str,
    default="info",
    choices=["info", "debug", "warning", "error"],
    help="Logging level. Choose between info, debug, warning, error",
)
args = parser.parse_args()

# PATHING
BASE_DIR = Path("data")
DATA_PATH = BASE_DIR / args.data.upper()
FINAL_DATASET = DATA_PATH / "final_dataset.csv"

RESULTS_BASE_DIR = Path("results")
RESULTS_PATH = RESULTS_BASE_DIR / args.data.upper()
METRICS_CSV = RESULTS_PATH / "metrics.csv"
RESULTS_PATH.mkdir(parents=True, exist_ok=True)

LOGS_BASE_DIR = Path("logs")
LOGS_PATH = LOGS_BASE_DIR / args.data.upper()
LOGS_PATH.mkdir(parents=True, exist_ok=True)

# LOGGING SETUP
logging.basicConfig(
    filename=LOGS_PATH / "training.log",
    filemode="w",
    level=args.logging.upper(),
    format="%(levelname)s - %(asctime)s - %(message)s",
)

# DEFINE REGRESSION MODELS
models = {
    "DecisionTreeRegressor": DecisionTreeRegressor(),
    "RandomForestRegressor": RandomForestRegressor(),
    "XGBoostRegressor": XGBRegressor(),
    "SVR": SVR(),
    "GradientBoostingRegressor": GradientBoostingRegressor(),
}

if __name__ == "__main__":
    # load data
    df = pd.read_csv(FINAL_DATASET)

    # TODO: Add a flag to be uni-variate or multivariate

    # log the metadata
    logging.info(f"Shape of dataset: {df.shape}")
    logging.debug(f"Columns of dataset: {df.columns.tolist()}")

    # split to features and target
    features = df.drop(columns=["ts_next", "time", "id"])
    label = df["ts_next"]

    # split to train and test
    features_train, features_test, label_train, label_test = train_test_split(
        features, label, test_size=0.2, random_state=42
    )

    # normalize data with standard scaler
    scaler = StandardScaler()
    features_train = pd.DataFrame(
        scaler.fit_transform(features_train), columns=features_train.columns
    )
    features_test = pd.DataFrame(
        scaler.transform(features_test), columns=features_test.columns
    )

    # I must do 5 x 5 = 25 combinations
    results = pd.DataFrame(columns=["model", "2nd_model", "type", "mse", "rmse"])
    for model_name, model in models.items():
        # isolate features
        pfeatures_train = features_train.copy()
        pfeatures_test = features_test.copy()

        # fit model
        logging.info(
            f"plain training: {model_name}, with {pfeatures_train.shape[1]} features..."
        )
        model.fit(pfeatures_train, label_train)

        # make predictions for train and test (will be used for cascade)
        preds_train = model.predict(pfeatures_train)
        preds_test = model.predict(pfeatures_test)

        # evaluate model's mse and rmse
        results = calculate_metrics(
            results, model_name, "", label_test, preds_test, "plain"
        )

        # TODO: calculate importance's

        # voting and cascade
        for cmodel_name, cmodel in models.items():
            # calculate voting
            voting = VotingRegressor(
                [(f"{model_name}_1", model), (f"{cmodel_name}_2", cmodel)]
            )

            # fit voting
            logging.info(
                f"voting {model_name} with {cmodel_name} for {pfeatures_train.shape[1]} features..."
            )
            voting.fit(pfeatures_train, label_train)

            # predict
            vpreds = voting.predict(pfeatures_test)

            # evaluate voting mse and rmse
            results = calculate_metrics(
                results, model_name, cmodel_name, label_test, vpreds, "voting"
            )

            # TODO: calculate importance's

            # create feature set for cascade
            cfeatures_train = features_train.copy()
            cfeatures_test = features_test.copy()
            cfeatures_train["preds"] = preds_train
            cfeatures_test["preds"] = preds_test

            # fit cascade model
            logging.info(
                f"cascade {model_name} with {cmodel_name} for {pfeatures_train.shape[1]} features..."
            )
            cmodel.fit(cfeatures_train, label_train)

            # make predictions
            cpreds = cmodel.predict(cfeatures_test)

            # evaluate cascade's mse and rmse
            results = calculate_metrics(
                results, model_name, cmodel_name, label_test, cpreds, "cascade"
            )

            # TODO: calculate importance's

    # export results
    results = results.sort_values(by=["model", "mse"])
    results.to_csv(METRICS_CSV, index=False)
    logging.info("Results have been exported!")
