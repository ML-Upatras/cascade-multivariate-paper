import pandas as pd


def load_home(data_path):
    # load data
    df = pd.read_csv(data_path / "HomeC.csv", low_memory=False)

    # remove  [kW]
    df.columns = [i.replace(" [kW]", "") for i in df.columns]

    # make all columns lowercase
    df.columns = [i.lower() for i in df.columns]

    # remove 1 nan
    df = df.dropna()

    # handle time
    df["time"] = pd.to_datetime(df["time"], unit="s")

    # simplify furniture and kitchen sensors
    df["furnace"] = df[["furnace 1", "furnace 2"]].sum(axis=1)
    df["kitchen"] = df[["kitchen 12", "kitchen 14", "kitchen 38"]].sum(axis=1)

    # drop old columns
    to_drop = [
        "furnace 1",
        "furnace 2",
        "kitchen 12",
        "kitchen 14",
        "kitchen 38",
        "icon",
        "summary",
    ]
    df = df.drop(to_drop, axis=1)

    # Drop the duplicate columns
    df = df.drop(["use", "gen"], axis=1)

    # for cloud cover replace these invalid values with the next valid value
    df["cloudcover"].replace(["cloudcover"], method="bfill", inplace=True)
    df["cloudcover"] = df["cloudcover"].astype("float")

    # group by hour
    df = df.groupby([pd.Grouper(key="time", freq="1h")]).mean()

    # add id
    df["id"] = 1

    return df
