import pandas as pd


def load_traffic(data_path):
    df = pd.read_csv(data_path / "traffic.csv")

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # handle time
    df = df.rename(columns={"datetime": "time"})
    df["time"] = pd.to_datetime(df["time"])

    # drop id
    df = df.drop(columns=["id"])

    # rename junction to id & vehicle to target
    df = df.rename(columns={"junction": "id", "vehicles": "ts"})

    return df
