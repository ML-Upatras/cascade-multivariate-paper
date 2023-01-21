import pandas as pd


def load_air(data_path):
    # load data
    df = pd.read_csv(data_path / "AirPassengers.csv")

    # rename columns
    df.columns = ["time", "ts"]

    # convert date to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id column
    df["id"] = 1

    return df
