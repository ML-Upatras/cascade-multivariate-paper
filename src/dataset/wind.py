import pandas as pd


def load_wind(data_path):
    # load data
    df = pd.read_csv(data_path / "Wind Time Series Dataset(hourly).csv")

    # rename columns
    df.columns = ["time", "ts", "power"]

    # convert times to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id
    df["id"] = 1

    return df
