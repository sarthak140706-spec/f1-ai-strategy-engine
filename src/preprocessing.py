import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df = df[df["IsAccurate"] == True]

    df = df[df["Deleted"] != True]

    df = df.dropna(subset=["LapTime"])

    return df


def convert_time_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["LapTimeSeconds"] = (
        pd.to_timedelta(df["LapTime"])
        .dt.total_seconds()
    )

    return df