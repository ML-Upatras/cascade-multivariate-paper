import pandas as pd


def load_riders(data_path):
    # load data
    df = pd.read_csv(data_path / "portland-oregon-average-monthly-.csv")

    # rename columns
    df.columns = ["time", "ts"]

    df = df[:-1]

    # convert date to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id column
    df["id"] = 1

    return df
