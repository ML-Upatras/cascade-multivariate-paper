import pandas as pd


def load_parking(data_path):
    df = pd.DataFrame(columns=["ts", "time"])
    # open .txt file and add it to csv
    with open(data_path / "parking-klcc-2016-2017.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line.split(";") for line in lines]

        # add to dataframe
        for line in lines:
            df = df.append(
                {
                    "ts": line[1],
                    "time": line[2],
                },
                ignore_index=True,
            )

        # convert time to datetime
        df["time"] = pd.to_datetime(df["time"])

        # add id
        df["id"] = 1

        # replace "FULL" with 5500
        df["ts"] = df["ts"].replace("FULL", 5500)

        # remove rows with OPEN
        df = df[df["ts"] != "OPEN"]

        # convert ts to float
        df["ts"] = df["ts"].astype(float)

    return df
