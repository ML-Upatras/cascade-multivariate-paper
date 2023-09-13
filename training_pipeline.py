import argparse
import logging
from pathlib import Path

import pandas as pd
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
    VotingRegressor,
)
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.linear_model import SGDRegressor, Lasso
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from xgboost import XGBRegressor

from src.dataset.utils import get_dataset_names
from src.evaluation import calculate_importance, calculate_metrics

# GET DATASET NAMES
datasets = get_dataset_names()

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument(
    "--data",
    type=str,
    choices=datasets,
    help=f"Dataset to use. Choose between {', '.join(datasets)}.",
)
parser.add_argument(
    "--logging",
    type=str,
    default="info",
    choices=["info", "debug", "warning", "error"],
    help="Logging level. Choose between info, debug, warning, error",
)
parser.add_argument(
    "--ii",
    type=int,
    default=0,
    help="Number of iterations for importance calculation. If it's 0 then the importance it is not calculated.",
)
parser.add_argument(
    "--perc",
    type=int,
    default=30,
    help="Percentage of features to select. Default is 30",
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

IMPORTANCE_BASE_DIR = Path("results")
IMPORTANCE_PATH = IMPORTANCE_BASE_DIR / args.data.upper()
IMPORTANCE_CSV = IMPORTANCE_PATH / "importance.csv"

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
    "Lasso": Lasso(),
    "SGDRegressor": SGDRegressor(),
    "MLPRegressor": MLPRegressor(max_iter=500),
    # "RandomForestRegressor": RandomForestRegressor(),
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

    # select features
    if 0 < args.perc <= 100:
        # define feature selection & fit to train data
        select = SelectPercentile(f_classif, percentile=args.perc)
        selected_features = select.fit_transform(features_train, label_train)
        selected_features_names = features_train.columns[select.get_support()]

        # isolate selected features on features_train and features_test
        features_train = features_train[selected_features_names]
        features_test = features_test[selected_features_names]
        logging.debug(f"Selected features: {features_train.columns.tolist()}")

    # I must do 5 x 5 = 25 combinations
    results = pd.DataFrame(columns=["model", "2nd_model", "type", "mse", "rmse"])
    importance = pd.DataFrame(
        columns=["model", "2nd_model", "type", "feature", "importance", "std"]
    )
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

        # calculate feature importance
        if model_name in ["RandomForestRegressor", "XGBoostRegressor"]:
            if args.ii > 0:
                importance = calculate_importance(
                    importance,
                    model_name,
                    "",
                    "plain",
                    model,
                    pfeatures_test,
                    label_test,
                    "neg_mean_squared_error",
                    args.ii,
                )

        # voting and cascade
        for cmodel_name, cmodel in models.items():
            # do everything if the model is not the same
            if model_name != cmodel_name:
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

                # calculate importance
                if model_name in ["RandomForestRegressor", "XGBoostRegressor"]:
                    if args.ii > 0:
                        importance = calculate_importance(
                            importance,
                            model_name,
                            cmodel_name,
                            "voting",
                            voting,
                            pfeatures_test,
                            label_test,
                            "neg_mean_squared_error",
                            args.ii,
                        )

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

                # calculate importance
                if model_name in ["RandomForestRegressor", "XGBoostRegressor"]:
                    if args.ii > 0:
                        importance = calculate_importance(
                            importance,
                            model_name,
                            cmodel_name,
                            "cascade",
                            cmodel,
                            cfeatures_test,
                            label_test,
                            "neg_mean_squared_error",
                            args.ii,
                        )

    # export results
    results = results.sort_values(by=["model", "mse"])
    results.to_csv(METRICS_CSV, index=False)
    logging.info("Results have been exported!")

    # export importance
    if args.ii > 0:
        importance.to_csv(IMPORTANCE_CSV, index=False)
        logging.info("Importance have been exported!")
