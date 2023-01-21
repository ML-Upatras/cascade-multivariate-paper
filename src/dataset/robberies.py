import pandas as pd


def load_robberies(data_path):
    # load dataset
    df = pd.read_csv(data_path / "Robberies.csv")

    # rename columns
    df.columns = ["time", "ts"]

    # convert time to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id
    df["id"] = 1

    return df
