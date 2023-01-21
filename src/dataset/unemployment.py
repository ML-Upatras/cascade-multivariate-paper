import pandas as pd


def load_unemployment(data_path):
    # load data
    df = pd.read_csv(data_path / "USUnemployment.csv")

    # Create a list of tuples that contain the year, month, and value
    data_list = []
    for i in range(df.shape[0]):
        year = df.iloc[i, 0]
        for j in range(1, 13):
            month = df.columns[j]
            value = df.iloc[i, j]
            data_list.append((year, month, value))

    # Create a new dataframe from the list of tuples
    df_new = pd.DataFrame(data_list, columns=["time", "month", "ts"])

    # Combine the 'time' and 'month' columns
    df_new["time"] = df_new["time"].astype(str) + "-" + df_new["month"]

    # Convert the 'time' column to datetime format
    df_new["time"] = pd.to_datetime(df_new["time"], format="%Y-%b")

    # Drop the 'month' column
    df_new = df_new.drop("month", axis=1)

    return df_new
