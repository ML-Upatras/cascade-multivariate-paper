import logging

import numpy as np
import pandas as pd


def load_electricity(data_path):
    # load .txt file
    with open(data_path / "household_power_consumption.txt", "r") as f:
        lines = f.readlines()

    # split the first line and get the column names
    columns = lines[0].split(";")
    columns = [c.strip() for c in columns]
    lines = lines[1:]

    # each line split it on ";" and add them in a df
    df = pd.DataFrame([line.strip().split(";") for line in lines], columns=columns)

    # make all columns lowercase
    df.columns = [c.lower() for c in df.columns]

    # convert to datetime
    df["time"] = pd.to_datetime(df["date"] + " " + df["time"])
    df = df.drop(columns=["date"])

    # replace ? with nan to every column except time
    df = df.replace("?", np.nan)
    df = df.replace("", np.nan)

    # convert to float except time
    df = df.astype({c: float for c in df.columns if c != "time"})

    # group by time hourly
    df = df.groupby([pd.Grouper(key="time", freq="1h")]).mean()
    df = df.reset_index()

    # forward fill nan
    df = df.fillna(method="ffill")

    # rename global_active_power to ts
    df = df.rename(columns={"global_active_power": "ts"})

    # add id
    df["id"] = 1

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1h"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 hour: {df.shape}")

    return df
