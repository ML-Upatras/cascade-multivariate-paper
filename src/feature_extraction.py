# create a function that create temporal features for a df
import pandas as pd


def temporal_feature_extraction(df):
    # create a copy of the df
    df = df.copy()

    # hour based features
    df["hour"] = df["time"].dt.hour
    df["next_hour"] = df["time"] + pd.Timedelta(hours=1)
    df["next_hour"] = df["next_hour"].dt.hour
    df["prev_hour"] = df["time"] - pd.Timedelta(hours=1)
    df["prev_hour"] = df["prev_hour"].dt.hour

    # day based features
    df["day"] = df["time"].dt.day
    df["day_of_week"] = df["time"].dt.isocalendar().week
    df["day_of_year"] = df["time"].dt.dayofyear
    df["next_day"] = df["time"] + pd.Timedelta(days=1)
    df["prev_day"] = df["time"] - pd.Timedelta(days=1)
    df["next_day"] = df["next_day"].dt.day
    df["prev_day"] = df["prev_day"].dt.day

    # week based features
    df["week_of_year"] = df["time"].dt.isocalendar().week
    df["next_week"] = df["time"] + pd.Timedelta(weeks=1)
    df["prev_week"] = df["time"] - pd.Timedelta(weeks=1)
    df["next_week"] = df["next_week"].dt.isocalendar().week
    df["prev_week"] = df["prev_week"].dt.isocalendar().week

    # month based features
    df["month"] = df["time"].dt.month

    # year based features
    df["year"] = df["time"].dt.year

    return df
