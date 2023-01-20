import argparse
import logging
from pathlib import Path

import pandas as pd

from src.dataset.air_quality import load_air_quality
from src.dataset.electricity import load_electricity
from src.dataset.energy import load_energy
from src.dataset.iot import load_iot
from src.dataset.joho import load_joho
from src.dataset.kolkata import load_kolkata
from src.dataset.parking import load_parking
from src.dataset.power import load_power
from src.dataset.room import load_room
from src.dataset.sofia import load_sofia
from src.dataset.solar import load_solar
from src.dataset.traffic import load_traffic
from src.dataset.turbine import load_turbine
from src.dataset.wind import load_wind
from src.feature_extraction import temporal_feature_extraction

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument(
    "--data",
    type=str,
    choices=[
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
        "wind",
        "sofia",
    ],
    help="Dataset to use. Choose between air_quality, traffic, energy, power, parking, room, solar, kolkata, turbine, joho, electricity, iot, home, wind, sofia.",
)
parser.add_argument(
    "--hours",
    type=int,
    default=1,
    help="Number of minutes to use for dataset aggregation. Default is 1",
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
CSV_PATH = DATA_PATH / f"{args.data}.csv"
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
    if args.data == "air_quality":
        df = load_air_quality(CSV_PATH)
    elif args.data == "traffic":
        df = load_traffic(CSV_PATH)
    elif args.data == "energy":
        df = load_energy(CSV_PATH)
    elif args.data == "power":
        df = load_power(DATA_PATH)
    elif args.data == "parking":
        df = load_parking(DATA_PATH)
    elif args.data == "room":
        df = load_room(DATA_PATH)
    elif args.data == "solar":
        df = load_solar(DATA_PATH)
    elif args.data == "kolkata":
        df = load_kolkata(DATA_PATH)
    elif args.data == "turbine":
        df = load_turbine(DATA_PATH)
    elif args.data == "joho":
        df = load_joho(DATA_PATH)
    elif args.data == "electricity":
        df = load_electricity(DATA_PATH)
    elif args.data == "iot":
        df = load_iot(DATA_PATH)
    elif args.data == "wind":
        df = load_wind(DATA_PATH)
    elif args.data == "sofia":
        df = load_sofia(DATA_PATH)

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq=f"{args.hours}h"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per {args.hours} hours: {df.shape}")

    # drop nan
    df = df.dropna()
    logging.info(f"Shape after dropping nan: {df.shape}")
    #
    # # feature extraction of previous steps for every column except time, id and ts
    # if args.p_steps > 0:
    #     for column in df.columns:
    #         if column not in ["time", "id", "ts"]:
    #             for step in range(1, args.p_steps + 1):
    #                 df[f"{column}_t_{step}"] = df[column].shift(step)

    # temporal feature extraction
    df = temporal_feature_extraction(df)
    logging.info(f"Shape after temporal feature extraction: {df.shape}")

    # feature extraction of previous steps
    if args.p_steps > 0:
        for step in range(1, args.p_steps + 1):
            df[f"ts_{step}"] = df["ts"].shift(step)
    logging.info(f"Shape after adding previous steps: {df.shape}")

    # create label for target: group by id and create a ts_next column
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
