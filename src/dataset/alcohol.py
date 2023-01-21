import logging

import pandas as pd


def load_alcohol(data_path):
    # load data
    df = pd.read_csv(data_path / "S4248SM144NCEN.csv")

    # rename columns
    df.columns = ["time", "ts"]

    # convert time to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id column
    df["id"] = 1

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1d"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 day: {df.shape}")

    return df
