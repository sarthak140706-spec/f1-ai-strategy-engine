import pandas as pd


# --------------------------------------------------
# CLEAN RAW FASTF1 DATA
# --------------------------------------------------

def clean_data(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    # Keep only accurate laps
    if "IsAccurate" in df.columns:

        df = df[
            df["IsAccurate"] == True
        ]

    # Remove deleted laps
    if "Deleted" in df.columns:

        df = df[
            df["Deleted"] != True
        ]

    # LapTime is required
    if "LapTime" in df.columns:

        df = df.dropna(
            subset=["LapTime"]
        )

    return df.reset_index(
        drop=True
    )


# --------------------------------------------------
# CONVERT LAP TIME
# --------------------------------------------------

def convert_time_features(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    if "LapTime" in df.columns:

        df["LapTimeSeconds"] = (
            pd.to_timedelta(
                df["LapTime"],
                errors="coerce"
            )
            .dt.total_seconds()
        )

    return df


# --------------------------------------------------
# REMOVE UNREALISTIC LAP TIMES
# --------------------------------------------------

def remove_outlier_laps(
    df: pd.DataFrame,
    min_lap_time: float = 50.0,
    max_lap_time: float = 200.0
) -> pd.DataFrame:

    """
    Remove extremely unrealistic lap times.

    This is a basic safety filter.
    V5 will later introduce track-specific
    outlier detection.
    """

    df = df.copy()

    if "LapTimeSeconds" not in df.columns:

        return df

    df = df[
        (
            df["LapTimeSeconds"]
            >= min_lap_time
        )
        &
        (
            df["LapTimeSeconds"]
            <= max_lap_time
        )
    ]

    return df.reset_index(
        drop=True
    )


# --------------------------------------------------
# FULL PREPROCESSING PIPELINE
# --------------------------------------------------

def preprocess_data(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Run the complete preprocessing pipeline.
    """

    df = clean_data(df)

    df = convert_time_features(df)

    df = remove_outlier_laps(df)

    return df