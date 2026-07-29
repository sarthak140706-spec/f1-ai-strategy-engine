"""
tyre_data.py

Sprint 4 - Step 1

Extracts tyre stint data from a FastF1 session.

The extracted data contains:
- Driver
- Lap number
- Tyre compound
- Tyre age
- Lap time
- Stint number

This data will be used in later Sprint 4 steps
to build the tyre degradation model.
"""

import pandas as pd


# ============================================================
# EXTRACT TYRE STINT DATA
# ============================================================

def extract_tyre_stint_data(
    session
) -> pd.DataFrame:
    """
    Extract tyre stint and lap data from a loaded
    FastF1 session.

    Parameters
    ----------
    session : fastf1.core.Session
        Loaded FastF1 session.

    Returns
    -------
    pandas.DataFrame
        Clean tyre stint dataset.
    """

    if session is None:

        raise ValueError(
            "Session cannot be None."
        )

    laps = session.laps.copy()

    if laps.empty:

        raise ValueError(
            "No lap data available in the session."
        )

    # --------------------------------------------------------
    # Required Columns
    # --------------------------------------------------------

    required_columns = [

        "Driver",

        "LapNumber",

        "Compound",

        "TyreLife",

        "LapTime",

        "Stint"

    ]

    missing_columns = [

        column

        for column in required_columns

        if column not in laps.columns

    ]

    if missing_columns:

        raise ValueError(

            "Missing required columns: "

            + str(missing_columns)

        )

    # --------------------------------------------------------
    # Select Required Data
    # --------------------------------------------------------

    tyre_data = laps[

        required_columns

    ].copy()

    # --------------------------------------------------------
    # Convert Lap Time to Seconds
    # --------------------------------------------------------

    tyre_data["LapTimeSeconds"] = (

        tyre_data["LapTime"]

        .dt.total_seconds()

    )

    # --------------------------------------------------------
    # Remove Invalid Rows
    # --------------------------------------------------------

    tyre_data = tyre_data.dropna(

        subset=[

            "Driver",

            "LapNumber",

            "Compound",

            "TyreLife",

            "LapTimeSeconds"

        ]

    )

    # --------------------------------------------------------
    # Remove Zero / Negative Lap Times
    # --------------------------------------------------------

    tyre_data = tyre_data[

        tyre_data["LapTimeSeconds"] > 0

    ]

    # --------------------------------------------------------
    # Clean Compound Names
    # --------------------------------------------------------

    tyre_data["Compound"] = (

        tyre_data["Compound"]

        .astype(str)

        .str.upper()

        .str.strip()

    )

    # --------------------------------------------------------
    # Sort Data
    # --------------------------------------------------------

    tyre_data = tyre_data.sort_values(

        by=[

            "Driver",

            "Stint",

            "LapNumber"

        ]

    ).reset_index(

        drop=True

    )

    return tyre_data


# ============================================================
# GET DRIVER TYRE STINTS
# ============================================================

def get_driver_tyre_stints(
    tyre_data: pd.DataFrame,
    driver: str
) -> pd.DataFrame:
    """
    Return tyre stint data for a specific driver.
    """

    if tyre_data.empty:

        return tyre_data.copy()

    driver_data = tyre_data[

        tyre_data["Driver"].astype(str).str.upper()

        ==

        driver.upper()

    ].copy()

    return driver_data.reset_index(

        drop=True

    )


# ============================================================
# GET VALID TYRE COMPOUNDS
# ============================================================

def get_valid_tyre_data(
    tyre_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Keep only recognised F1 dry tyre compounds.
    """

    valid_compounds = [

        "SOFT",

        "MEDIUM",

        "HARD"

    ]

    valid_data = tyre_data[

        tyre_data["Compound"].isin(

            valid_compounds

        )

    ].copy()

    return valid_data.reset_index(

        drop=True

    )


# ============================================================
# GET STINT SUMMARY
# ============================================================

def get_stint_summary(
    tyre_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate a summary for every driver tyre stint.
    """

    if tyre_data.empty:

        return pd.DataFrame()

    summary = (

        tyre_data

        .groupby(

            [

                "Driver",

                "Stint",

                "Compound"

            ],

            as_index=False

        )

        .agg(

            StartLap=(

                "LapNumber",

                "min"

            ),

            EndLap=(

                "LapNumber",

                "max"

            ),

            StintLaps=(

                "LapNumber",

                "count"

            ),

            AverageLapTime=(

                "LapTimeSeconds",

                "mean"

            ),

            BestLapTime=(

                "LapTimeSeconds",

                "min"

            ),

            AverageTyreLife=(

                "TyreLife",

                "mean"

            )

        )

    )

    return summary


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from src.data_loader import (

        load_session

    )

    print("=" * 60)

    print(

        "SPRINT 4 - STEP 1 TEST"

    )

    print("=" * 60)

    # --------------------------------------------------------
    # Load Session
    # --------------------------------------------------------

    session = load_session(

        2025,

        "British Grand Prix",

        "R"

    )

    # --------------------------------------------------------
    # Extract Tyre Data
    # --------------------------------------------------------

    tyre_data = extract_tyre_stint_data(

        session

    )

    print(

        "\nTOTAL TYRE LAP RECORDS:",

        len(tyre_data)

    )

    # --------------------------------------------------------
    # Filter Valid Compounds
    # --------------------------------------------------------

    valid_tyre_data = get_valid_tyre_data(

        tyre_data

    )

    print(

        "VALID DRY TYRE RECORDS:",

        len(valid_tyre_data)

    )

    # --------------------------------------------------------
    # Driver Example
    # --------------------------------------------------------

    driver_data = get_driver_tyre_stints(

        valid_tyre_data,

        "VER"

    )

    print(

        "\nVERSTAPPEN TYRE RECORDS:",

        len(driver_data)

    )

    # --------------------------------------------------------
    # Stint Summary
    # --------------------------------------------------------

    stint_summary = get_stint_summary(

        valid_tyre_data

    )

    print(

        "\nTOTAL TYRE STINTS:",

        len(stint_summary)

    )

    # --------------------------------------------------------
    # Display Sample Data
    # --------------------------------------------------------

    print(

        "\nTYRE DATA SAMPLE"

    )

    print("=" * 60)

    print(

        valid_tyre_data.head(10).to_string(

            index=False

        )

    )

    # --------------------------------------------------------
    # Display Stint Summary
    # --------------------------------------------------------

    print(

        "\nSTINT SUMMARY"

    )

    print("=" * 60)

    print(

        stint_summary.head(10).to_string(

            index=False

        )

    )

    print("=" * 60)

    print(

        "STEP 1 COMPLETED"

    )

    print("=" * 60)