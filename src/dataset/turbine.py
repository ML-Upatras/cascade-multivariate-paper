import pandas as pd


def load_turbine(data_path):
    # load data
    df = pd.read_csv(data_path / "TexasTurbine.csv")

    # make all columns lowercase
    df.columns = [col.lower() for col in df.columns]

    # rename columns
    df.columns = [
        "time",
        "ts",
        "wind_speed",
        "wind_direction",
        "pressure",
        "air_temperature",
    ]

    # handle time (it does not have year)
    df["time"] = pd.to_datetime(df["time"], format="%b %d, %I:%M %p")

    # add id
    df["id"] = 1

    return df
