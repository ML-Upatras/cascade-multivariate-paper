import pandas as pd


def load_joho(data_path):
    # load data
    df = pd.read_csv(data_path / "malaysia_all_data_for_paper.csv", sep=";")

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # handle time
    df["time"] = pd.to_datetime(df["time"])

    # rename load to ts
    df = df.rename(columns={"load": "ts"})

    # add id
    df["id"] = 1

    return
