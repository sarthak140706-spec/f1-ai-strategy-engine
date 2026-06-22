import pandas as pd


def detect_pit_stops(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["PitLap"] = (
        df.groupby("Driver")["Stint"]
        .diff()
        .fillna(0)
        .gt(0)
        .astype(int)
    )

    return df


def create_race_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df = df.sort_values(
        by=["Driver", "LapNumber"]
    ).reset_index(drop=True)

    total_laps = df["LapNumber"].max()

    df["LapsRemaining"] = total_laps - df["LapNumber"]

    df["RaceProgress"] = df["LapNumber"] / total_laps

    df["AvgPaceLast3"] = (
        df.groupby("Driver")["LapTimeSeconds"]
        .transform(
            lambda x: x.rolling(3, min_periods=1).mean()
        )
    )

    df["AvgPaceLast5"] = (
        df.groupby("Driver")["LapTimeSeconds"]
        .transform(
            lambda x: x.rolling(5, min_periods=1).mean()
        )
    )

    df["AvgPaceLast10"] = (
        df.groupby("Driver")["LapTimeSeconds"]
        .transform(
            lambda x: x.rolling(10, min_periods=1).mean()
        )
    )

    df["DegradationRate"] = (
        df["LapTimeSeconds"] - df["AvgPaceLast5"]
    )

    df["CurrentStintLength"] = (
        df.groupby(["Driver", "Stint"])
        .cumcount() + 1
    )

    df["PitStopsCompleted"] = (
        df.groupby("Driver")["PitLap"]
        .cumsum()
    )

    return df


def create_target(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["PitNextLap"] = (
        df.groupby("Driver")["PitLap"]
        .shift(-1)
        .fillna(0)
        .astype(int)
    )

    return df


def prepare_model_data(df: pd.DataFrame):

    features = [
        "LapNumber",
        "TyreLife",
        "Position",
        "LapsRemaining",
        "RaceProgress",
        "AvgPaceLast3",
        "AvgPaceLast5",
        "AvgPaceLast10",
        "DegradationRate",
        "CurrentStintLength",
        "PitStopsCompleted"
    ]

    target = "PitNextLap"

    model_data = df[
        features + [target]
    ].dropna()

    return model_data