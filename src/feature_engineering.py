import pandas as pd


# ============================================================
# ML FEATURE DEFINITIONS
# ============================================================

ML_FEATURES = [

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


# ============================================================
# DETECT PIT STOPS
# ============================================================

def detect_pit_stops(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Detect pit stops from changes in stint number.

    Used primarily for the historical training pipeline.
    """

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


# ============================================================
# CALCULATE PACE FEATURES
# ============================================================

def create_pace_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create rolling pace features for historical
    race data.

    Features:
        AvgPaceLast3
        AvgPaceLast5
        AvgPaceLast10
    """

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

    # --------------------------------------------------------
    # Average pace over last 3 laps
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Average pace over last 5 laps
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Average pace over last 10 laps
    # --------------------------------------------------------

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


# ============================================================
# CREATE RACE FEATURES
# ============================================================

def create_race_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create race-related features for the historical
    training dataset.

    This function is retained for model training.
    """

    df = df.copy()

    df = df.sort_values(
        by=[
            "Driver",
            "LapNumber"
        ]
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # TOTAL LAPS
    # --------------------------------------------------------

    total_laps = (

        df["LapNumber"]
        .max()

    )

    if pd.isna(total_laps):

        total_laps = 1

    # --------------------------------------------------------
    # RACE PROGRESS
    # --------------------------------------------------------

    df["LapsRemaining"] = (

        total_laps
        - df["LapNumber"]

    )

    df["RaceProgress"] = (

        df["LapNumber"]
        / total_laps

    )

    # --------------------------------------------------------
    # PACE
    # --------------------------------------------------------

    df = create_pace_features(
        df
    )

    # --------------------------------------------------------
    # DEGRADATION
    # --------------------------------------------------------

    df["DegradationRate"] = (

        df["LapTimeSeconds"]
        - df["AvgPaceLast5"]

    )

    # --------------------------------------------------------
    # STINT LENGTH
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # PIT STOPS
    # --------------------------------------------------------

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


# ============================================================
# CREATE TARGET
# ============================================================

def create_target(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create the supervised learning target.

    Target:
        PitNextLap

    1 = Driver pits on next lap
    0 = Driver does not pit on next lap
    """

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


# ============================================================
# PREPARE MODEL DATA
# ============================================================

def prepare_model_data(
    df: pd.DataFrame
):
    """
    Prepare historical data for model training.

    Returns:
        DataFrame containing the 11 ML features
        and the target.
    """

    target = "PitNextLap"

    available_features = [

        feature

        for feature in ML_FEATURES

        if feature in df.columns

    ]

    model_data = df[

        available_features
        + [target]

    ].dropna()

    return model_data


# ============================================================
# V5 DYNAMIC INFERENCE FEATURES
# ============================================================

def build_ml_features(
    race_state: dict
) -> pd.DataFrame:
    """
    Convert the structured race state generated by
    race_state.py into the exact feature format
    expected by the trained ML model.

    This function is used during V5 dynamic prediction.

    Parameters
    ----------
    race_state : dict
        Structured race state generated by race_state.py.

    Returns
    -------
    pandas.DataFrame
        Single-row DataFrame containing the 11 ML features.
    """

    if not isinstance(
        race_state,
        dict
    ):

        raise TypeError(
            "race_state must be a dictionary."
        )

    # --------------------------------------------------------
    # Map race_state fields to ML model fields
    # --------------------------------------------------------

    feature_mapping = {

        "LapNumber":
            race_state.get(
                "CurrentLap"
            ),

        "TyreLife":
            race_state.get(
                "TyreLife"
            ),

        "Position":
            race_state.get(
                "Position"
            ),

        "LapsRemaining":
            race_state.get(
                "LapsRemaining"
            ),

        "RaceProgress":
            race_state.get(
                "RaceProgress"
            ),

        "AvgPaceLast3":
            race_state.get(
                "AvgPaceLast3"
            ),

        "AvgPaceLast5":
            race_state.get(
                "AvgPaceLast5"
            ),

        "AvgPaceLast10":
            race_state.get(
                "AvgPaceLast10"
            ),

        "DegradationRate":
            race_state.get(
                "DegradationRate"
            ),

        "CurrentStintLength":
            race_state.get(
                "CurrentStintLength"
            ),

        "PitStopsCompleted":
            race_state.get(
                "PitStopsCompleted"
            )

    }

    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    features_df = pd.DataFrame(
        [feature_mapping]
    )

    # --------------------------------------------------------
    # Ensure exact feature order
    # --------------------------------------------------------

    features_df = features_df[
        ML_FEATURES
    ]

    return features_df


# ============================================================
# VALIDATE ML FEATURES
# ============================================================

def validate_ml_features(
    features_df: pd.DataFrame
) -> bool:
    """
    Validate that the generated DataFrame contains
    the exact 11 features required by the ML model.

    Returns:
        True if validation succeeds.

    Raises:
        ValueError if features are missing or ordered incorrectly.
    """

    # --------------------------------------------------------
    # Check columns
    # --------------------------------------------------------

    actual_columns = list(
        features_df.columns
    )

    expected_columns = ML_FEATURES

    if actual_columns != expected_columns:

        raise ValueError(

            "ML feature mismatch.\n"

            f"Expected: {expected_columns}\n"

            f"Received: {actual_columns}"

        )

    # --------------------------------------------------------
    # Check number of rows
    # --------------------------------------------------------

    if len(features_df) != 1:

        raise ValueError(

            "Dynamic prediction expects "
            "exactly one race-state row."

        )

    # --------------------------------------------------------
    # Check missing values
    # --------------------------------------------------------

    missing_features = (

        features_df.columns[
            features_df.isna().any()
        ]

        .tolist()

    )

    if missing_features:

        raise ValueError(

            "Missing values detected in ML features: "

            f"{missing_features}"

        )

    return True