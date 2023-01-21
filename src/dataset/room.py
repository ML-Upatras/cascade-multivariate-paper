import logging

import pandas as pd


def load_room(data_path):
    # load data
    df = pd.read_csv(data_path / "MLTempDataset1.csv")

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # drop unnamed columns
    df = df.drop(columns=[col for col in df.columns if "unnamed" in col])

    # handle time
    df = df.rename(columns={"datetime": "time"})
    df["time"] = pd.to_datetime(df["time"])

    # add id
    df["id"] = 1

    # rename ts
    df = df.rename(columns={"hourly_temp": "ts"})

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1h"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 hour: {df.shape}")

    return df
