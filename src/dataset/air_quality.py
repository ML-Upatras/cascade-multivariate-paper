import logging

import numpy as np
import pandas as pd


def load_air_quality(data_path):
    df = pd.read_csv(data_path / "air_quality.csv", sep=";")
    logging.info(f"Shape of dataset: {df.shape}")

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # drop unnamed columns
    df = df.drop(columns=[col for col in df.columns if "unnamed" in col])

    # convert date to datetime
    df["time"] = pd.to_datetime(df["time"], format="%H.%M.%S").dt.strftime("%H:%M:%S")
    df["time"] = df["date"] + " " + df["time"]
    df["time"] = pd.to_datetime(df["time"])
    df.drop(["date"], axis=1, inplace=True)

    # replace , with . and convert to float on all columns except time
    for col in df.columns:
        if col != "time":
            df[col] = df[col].replace(",", ".", regex=True).astype(float)

    # replacing null data from -200 to NaN for posterior treatment
    df = df.replace(-200, np.nan)

    # drop columns with a lot of null values
    to_drop = ["nox(gt)", "no2(gt)", "nmhc(gt)"]
    df = df.drop(columns=to_drop)

    # fill with the previous value
    df = df.fillna(method="ffill")

    # rename vehicle to target
    df = df.rename(columns={"co(gt)": "ts"})

    # add id column
    df["id"] = 1

    return df
