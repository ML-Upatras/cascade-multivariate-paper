import logging

import pandas as pd


def load_iot(data_path):
    df = pd.read_csv(data_path / "IOT-temp.csv")

    # drop id and room room_id/id
    df = df.drop(columns=["id", "room_id/id"])

    # rename columns
    df.columns = ["time", "ts", "out/in"]

    # convert time to datetime
    df["time"] = pd.to_datetime(df["time"])

    # separate time series into in and out
    df_in = df[df["out/in"] == "in"].drop(columns=["out/in"])
    df_out = df[df["out/in"] == "out"].drop(columns=["out/in"])

    # group by time hourly
    df_in = df.groupby([pd.Grouper(key="time", freq="1h")]).mean()
    df_out = df.groupby([pd.Grouper(key="time", freq="1h")]).mean()
    df_in = df_in.reset_index()
    df_out = df_out.reset_index()

    # combine the two time series with an id column to identify them
    df_in["id"] = 1
    df_out["id"] = 2
    df = pd.concat([df_in, df_out], axis=0)

    # drop rows with missing values
    df = df.dropna()

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1h"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 hour: {df.shape}")

    return df
