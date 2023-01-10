import pandas as pd


def load_power(data_path):
    id = 1
    csv_list = []
    for csv_path in data_path.iterdir():
        # check if path contains RealTimeConsumption
        if "RealTimeConsumption" in str(csv_path):
            # load data
            df = pd.read_csv(csv_path, encoding="cp1254")

            # make all columns lowercase
            df.columns = [col.lower() for col in df.columns]

            # handle time
            df["time"] = pd.to_datetime(df["date"] + " " + df["hour"])
            df = df.drop(columns=["date", "hour"])

            # add id
            df["id"] = id
            id += 1

            # rename target
            df = df.rename(columns={"consumption (mwh)": "ts"})

            # hande ts
            df["ts"] = df["ts"].str.replace(",", "")
            df["ts"] = df["ts"].astype(float)

            # add to list
            csv_list.append(df)

    # concat all csvs
    df = pd.concat(csv_list, axis=0)

    return df
