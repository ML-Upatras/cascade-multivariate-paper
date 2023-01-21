import logging

import pandas as pd


def load_sofia(data_path):
    # load data
    df = pd.read_csv(data_path / "Sofia_Temperature.csv")

    # rename columns
    df.columns = [
        "time",
        "ts",
        "dew_point",
        "humidity",
        "wind",
        "wind_speed",
        "wind_gust",
        "pressure",
        "condition",
    ]

    # label encoding condition and wind
    df["condition"] = df["condition"].astype("category").cat.codes
    df["wind"] = df["wind"].astype("category").cat.codes

    # convert times to datetime
    df["time"] = pd.to_datetime(df["time"])

    # aggregate by 1 hour and id
    df = df.groupby([pd.Grouper(key="time", freq="1h")]).mean()
    df = df.reset_index()

    # drop na
    df = df.dropna()

    # add id
    df["id"] = 1

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1h"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 hour: {df.shape}")

    return df
