import pandas as pd


# --------------------------------------------------
# DETECT PIT STOPS
# --------------------------------------------------

def detect_pit_stops(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df = df.sort_values(
        by=[
            "Driver",
            "LapNumber"
        ]
    )

    if "Stint" in df.columns:

        df["PitLap"] = (

            df.groupby("Driver")["Stint"]
            .diff()
            .fillna(0)
            .gt(0)
            .astype(int)

        )

    else:

        df["PitLap"] = 0

    return df


# --------------------------------------------------
# CALCULATE PACE FEATURES
# --------------------------------------------------

def create_pace_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df = df.sort_values(
        by=[
            "Driver",
            "LapNumber"
        ]
    )

    grouped_laps = (
        df.groupby("Driver")
    )

    # Recent pace
    df["AvgPaceLast3"] = (

        grouped_laps[
            "LapTimeSeconds"
        ]

        .transform(
            lambda x:
            x.rolling(
                3,
                min_periods=1
            ).mean()
        )

    )

    df["AvgPaceLast5"] = (

        grouped_laps[
            "LapTimeSeconds"
        ]

        .transform(
            lambda x:
            x.rolling(
                5,
                min_periods=1
            ).mean()
        )

    )

    df["AvgPaceLast10"] = (

        grouped_laps[
            "LapTimeSeconds"
        ]

        .transform(
            lambda x:
            x.rolling(
                10,
                min_periods=1
            ).mean()
        )

    )

    return df


# --------------------------------------------------
# CREATE RACE FEATURES
# --------------------------------------------------

def create_race_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df = df.sort_values(
        by=[
            "Driver",
            "LapNumber"
        ]
    ).reset_index(
        drop=True
    )

    # ----------------------------------------------
    # TOTAL LAPS
    # ----------------------------------------------

    total_laps = (
        df["LapNumber"]
        .max()
    )

    if pd.isna(total_laps):

        total_laps = 1

    # ----------------------------------------------
    # RACE PROGRESS
    # ----------------------------------------------

    df["LapsRemaining"] = (

        total_laps
        - df["LapNumber"]

    )

    df["RaceProgress"] = (

        df["LapNumber"]
        / total_laps

    )

    # ----------------------------------------------
    # PACE
    # ----------------------------------------------

    df = create_pace_features(
        df
    )

    # ----------------------------------------------
    # DEGRADATION
    # ----------------------------------------------

    df["DegradationRate"] = (

        df["LapTimeSeconds"]
        - df["AvgPaceLast5"]

    )

    # ----------------------------------------------
    # STINT LENGTH
    # ----------------------------------------------

    if "Stint" in df.columns:

        df["CurrentStintLength"] = (

            df.groupby(
                [
                    "Driver",
                    "Stint"
                ]
            )

            .cumcount()

            + 1

        )

    else:

        df["CurrentStintLength"] = 1

    # ----------------------------------------------
    # PIT STOPS
    # ----------------------------------------------

    if "PitLap" in df.columns:

        df["PitStopsCompleted"] = (

            df.groupby(
                "Driver"
            )["PitLap"]

            .cumsum()

        )

    else:

        df["PitStopsCompleted"] = 0

    return df


# --------------------------------------------------
# CREATE TARGET
# --------------------------------------------------

def create_target(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    df["PitNextLap"] = (

        df.groupby(
            "Driver"
        )["PitLap"]

        .shift(-1)

        .fillna(0)

        .astype(int)

    )

    return df


# --------------------------------------------------
# PREPARE MODEL DATA
# --------------------------------------------------

def prepare_model_data(
    df: pd.DataFrame
):

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

    available_features = [

        feature

        for feature in features

        if feature in df.columns

    ]

    model_data = df[
        available_features
        + [target]
    ].dropna()

    return model_data