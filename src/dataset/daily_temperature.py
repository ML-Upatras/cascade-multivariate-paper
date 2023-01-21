import logging

import pandas as pd


def load_daily_temperature(data_path):
    # load data
    train = pd.read_csv(data_path / "DailyDelhiClimateTrain.csv")
    test = pd.read_csv(data_path / "DailyDelhiClimateTest.csv")

    # merge train and test
    df = pd.concat([train, test], axis=0)

    # rename columns
    df.columns = ["time", "ts", "humidity", "wind_speed", "pressure"]

    # convert date to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id column
    df["id"] = 1

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1d"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 day: {df.shape}")

    return df
