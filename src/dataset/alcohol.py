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

    return df
