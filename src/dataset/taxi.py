import logging

import pandas as pd


def load_taxi(data_path):
    # load data
    df = pd.read_csv(data_path / "dataset.csv")

    # rename columns
    df.columns = ["unnamed", "time", "ts"]

    # drop unnamed column
    df = df.drop(columns=["unnamed"])

    # convert time to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id column
    df["id"] = 1

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1h"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 hour: {df.shape}")

    return df
