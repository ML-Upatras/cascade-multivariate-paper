import pandas as pd


def load_solar(data_path):
    # load 2015 & 2016 data
    df_2015 = pd.read_csv(data_path / "TimeSeries_TotalSolarGen_and_Load_IT_2015.csv")
    df_2016 = pd.read_csv(data_path / "TimeSeries_TotalSolarGen_and_Load_IT_2016.csv")

    # concatenate 2015 & 2016
    df = pd.concat([df_2015, df_2016], axis=0)

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # rename columns
    df.columns = ["time", "load", "ts"]

    # The time comes expressed in Coordinated Universal Time (UTC), and the format of Date and Time is "%Y-%m-%dT%H%M%SZ".
    df["time"] = pd.to_datetime(df["time"])

    # drop nan
    df = df.dropna()

    # add id
    df["id"] = 1

    return df
