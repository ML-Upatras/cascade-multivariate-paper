import pandas as pd


def load_kolkata(data_path):
    # load data
    df = pd.read_csv(data_path / "weather_data_kolkata_2015_2020.csv")

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # rename time
    df = df.rename(columns={"datetime": "time"})
    df["time"] = pd.to_datetime(df["time"])

    # rename temperature to ts
    df = df.rename(columns={"temperature": "ts"})

    # add id
    df["id"] = 1

    return df
