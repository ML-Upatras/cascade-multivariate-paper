import pandas as pd


def load_meat(data_path):
    # load data
    df = pd.read_csv(data_path / "meat_prices_20180103_20211027.csv")

    # rename columns
    df.columns = ["id", "time", "ts"]

    # convert date to datetime
    df["time"] = pd.to_datetime(df["time"])

    # label encode id
    df["id"] = df["id"].astype("category").cat.codes

    return df
