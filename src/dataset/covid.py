import pandas as pd


def load_covid(data_path):
    # load data
    df = pd.read_csv(data_path / "owid-covid-data.csv")

    # isolate only worldwide data
    df = df[df["location"] == "World"]

    # drop columns with more that 20% missing values
    cols_to_drop = []
    for col in df.columns:
        if df[col].isna().sum() / len(df) > 0.2:
            cols_to_drop.append(col)
    df = df.drop(cols_to_drop, axis=1)

    # fill missing values
    df = df.fillna(method="ffill")

    # rename total_cases to ts and date to time
    df = df.rename(columns={"total_cases": "ts", "date": "time"})

    # convert time to datetime
    df["time"] = pd.to_datetime(df["time"])

    # add id
    df["id"] = 1

    return df
