import argparse
import logging
from pathlib import Path

import pandas as pd

from src.dataset.utils import get_dataset_names, load_dataset
from src.feature_extraction import temporal_feature_extraction

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
    "--p_steps",
    type=int,
    default=1,
    help="Number of previous timesteps to add on the dataset",
)
# create an argument for the forecasting horizon
parser.add_argument(
    "--fh",
    type=int,
    default=1,
    help="Forecasting horizon. Number of steps to forecast.",
)
args = parser.parse_args()

BASE_DIR = Path("data")
DATA_PATH = BASE_DIR / args.data.upper()
EXTRA_FEATURES = DATA_PATH / "extra_features.csv"
FINAL_DATASET = DATA_PATH / "final_dataset.csv"

LOGS_BASE_DIR = Path("logs")
LOGS_PATH = LOGS_BASE_DIR / args.data.upper()
LOGS_PATH.mkdir(parents=True, exist_ok=True)

# LOGGING SETUP
logging.basicConfig(
    filename=LOGS_PATH / "data_generation.log",
    filemode="w",
    level=args.logging.upper(),
    format="%(levelname)s - %(asctime)s - %(message)s",
)

if __name__ == "__main__":
    df = load_dataset(args.data, DATA_PATH)

    # drop nan
    df = df.dropna()
    logging.info(f"Shape after dropping nan: {df.shape}")

    # temporal feature extraction
    df = temporal_feature_extraction(df)
    logging.info(f"Shape after temporal feature extraction: {df.shape}")

    # feature extraction of previous steps
    if args.p_steps > 0:
        for step in range(1, args.p_steps + 1):
            df = pd.concat([df, df["ts"].shift(step).rename(f"ts_{step}")], axis=1)
    logging.info(f"Shape after adding previous steps: {df.shape}")

    # create label for target: group by id and create a ts_next column
    df = df.copy()
    df["ts_next"] = df.groupby("id")["ts"].shift(-args.fh)
    df = df.sort_values(by=["id", "time"])
    df = df.reset_index(drop=True)

    # drop rows with nan target (last row of each id) and print the number of rows dropped
    logging.info(
        f"Number of rows dropped: {df[df['ts_next'].isna()].shape[0]}",
    )
    df = df.dropna()

    # save the final dataframe
    df.to_csv(FINAL_DATASET, index=False)
    logging.info(f"Final dataset shape: {df.shape}")
    logging.info("Final dataset saved!")
