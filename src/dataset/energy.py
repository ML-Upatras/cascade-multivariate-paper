import logging

import pandas as pd


def load_energy(data_path):
    # load data
    df = pd.read_csv(data_path / "energy.csv")

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # handle time
    df = df.rename(columns={"datetime": "time"})
    df["time"] = pd.to_datetime(df["time"])

    # add id
    df["id"] = 1

    # rename target
    df = df.rename(columns={"pjm_load_mw": "ts"})

    # aggregate by x hours and id
    df = df.groupby([pd.Grouper(key="time", freq="1h"), "id"]).mean()
    df = df.reset_index()
    logging.info(f"Shape after grouping per 1 hour: {df.shape}")

    return df
