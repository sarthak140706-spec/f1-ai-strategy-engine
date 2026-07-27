"""
race_state.py

F1 AI Strategist
Sprint 3 - Step 2

Purpose:
--------
Convert raw FastF1 session data into a structured race state
that can later be consumed by:

    feature_engineering.py
    predict.py
    simulator.py
    decision_engine.py

This module does NOT train the ML model.
This module does NOT make the final PIT/STAY decision.

It answers:

"What is the current race state of a selected driver?"

Enhanced race-state information includes:

    - Session information
    - Driver information
    - Current lap
    - Current position
    - Position ahead
    - Position behind
    - Gap to car ahead
    - Gap to car behind
    - Current tyre compound
    - Tyre life
    - Current stint
    - Current stint length
    - Pit stops completed
    - Recent pace
    - Average pace
    - Rolling pace
    - Estimated degradation
    - Race progress
"""

from typing import Any, Dict, Optional

import pandas as pd


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _safe_float(value: Any) -> Optional[float]:
    """
    Safely convert a value to float.

    Returns:
        float if conversion succeeds
        None otherwise
    """

    try:

        if pd.isna(value):
            return None

        return float(value)

    except (TypeError, ValueError):

        return None


def _safe_int(value: Any) -> Optional[int]:
    """
    Safely convert a value to integer.

    Returns:
        int if conversion succeeds
        None otherwise
    """

    try:

        if pd.isna(value):
            return None

        return int(value)

    except (TypeError, ValueError):

        return None


# ============================================================
# SESSION INFORMATION
# ============================================================

def get_session_info(
    session
) -> Dict[str, Any]:
    """
    Extract basic information about the FastF1 session.

    Parameters
    ----------
    session :
        Loaded FastF1 session object.

    Returns
    -------
    dict
        Basic session metadata.
    """

    event = getattr(
        session,
        "event",
        None
    )

    session_info = {

        "Season":
            None,

        "GrandPrix":
            None,

        "Circuit":
            None,

        "SessionType":
            getattr(
                session,
                "name",
                None
            ),

    }

    if event is not None:

        try:

            session_info["Season"] = (
                event["EventDate"].year
            )

        except Exception:

            pass

        try:

            session_info["GrandPrix"] = (
                event["EventName"]
            )

        except Exception:

            pass

        try:

            session_info["Circuit"] = (
                event["Location"]
            )

        except Exception:

            pass

    return session_info


# ============================================================
# DRIVER INFORMATION
# ============================================================

def get_driver_info(
    session,
    driver: str
) -> Dict[str, Any]:
    """
    Extract driver and team information.

    Parameters
    ----------
    session :
        Loaded FastF1 session.

    driver :
        Driver abbreviation.

    Returns
    -------
    dict
        Driver information.
    """

    driver = str(
        driver
    ).upper()

    result = {

        "Driver":
            driver,

        "Team":
            None,

        "DriverNumber":
            None,

    }

    try:

        results = session.results

        if results is None or results.empty:

            return result

        # ----------------------------------------------------
        # Find driver row
        # ----------------------------------------------------

        driver_rows = pd.DataFrame()

        if "Abbreviation" in results.columns:

            driver_rows = results[

                results[
                    "Abbreviation"
                ]
                .astype(str)
                .str.upper()
                == driver

            ]

        # ----------------------------------------------------
        # Fallback to Driver column
        # ----------------------------------------------------

        elif "Driver" in results.columns:

            driver_rows = results[

                results[
                    "Driver"
                ]
                .astype(str)
                .str.upper()
                == driver

            ]

        if driver_rows.empty:

            return result

        row = driver_rows.iloc[0]

        if "TeamName" in row.index:

            result["Team"] = row[
                "TeamName"
            ]

        if "DriverNumber" in row.index:

            result["DriverNumber"] = row[
                "DriverNumber"
            ]

    except Exception:

        pass

    return result


# ============================================================
# DRIVER LAP DATA
# ============================================================

def get_driver_laps(
    session,
    driver: str
) -> pd.DataFrame:
    """
    Retrieve valid lap data for a specific driver.

    Parameters
    ----------
    session :
        Loaded FastF1 session.

    driver :
        Driver abbreviation.

    Returns
    -------
    pandas.DataFrame
        Cleaned driver lap data.
    """

    driver = str(
        driver
    ).upper()

    try:

        laps = (

            session.laps
            .pick_drivers(
                driver
            )
            .copy()

        )

    except Exception:

        return pd.DataFrame()

    if laps.empty:

        return laps

    # --------------------------------------------------------
    # Sort by lap number
    # --------------------------------------------------------

    if "LapNumber" in laps.columns:

        laps = laps.sort_values(
            by="LapNumber"
        ).reset_index(
            drop=True
        )

    # --------------------------------------------------------
    # Convert lap time to seconds
    # --------------------------------------------------------

    if "LapTime" in laps.columns:

        laps["LapTimeSeconds"] = (

            laps[
                "LapTime"
            ]
            .dt
            .total_seconds()

        )

    # --------------------------------------------------------
    # Convert sector times to seconds
    # --------------------------------------------------------

    for column in [

        "Sector1Time",
        "Sector2Time",
        "Sector3Time",

    ]:

        if column in laps.columns:

            laps[
                f"{column}Seconds"
            ] = (

                laps[
                    column
                ]
                .dt
                .total_seconds()

            )

    # --------------------------------------------------------
    # Remove laps without valid lap time
    # --------------------------------------------------------

    if "LapTimeSeconds" in laps.columns:

        laps = laps[

            laps[
                "LapTimeSeconds"
            ]
            .notna()

        ].copy()

    return laps


# ============================================================
# CURRENT LAP
# ============================================================

def get_current_lap(
    laps: pd.DataFrame
) -> Optional[int]:
    """
    Determine the latest completed lap for the driver.
    """

    if laps.empty:

        return None

    if "LapNumber" not in laps.columns:

        return None

    valid_laps = (

        laps[
            "LapNumber"
        ]
        .dropna()

    )

    if valid_laps.empty:

        return None

    return _safe_int(
        valid_laps.max()
    )


# ============================================================
# POSITION
# ============================================================

def get_current_position(
    session,
    driver: str,
    laps: Optional[pd.DataFrame] = None
) -> Optional[int]:
    """
    Get the driver's latest known race position.

    Priority:

    1. Latest valid Position value in driver lap data.
    2. Session results Position value.

    Parameters
    ----------
    session :
        Loaded FastF1 session.

    driver :
        Driver abbreviation.

    laps :
        Driver-specific lap data.

    Returns
    -------
    int or None
        Current/latest known position.
    """

    driver = str(
        driver
    ).upper()

    # --------------------------------------------------------
    # First try lap-level position
    # --------------------------------------------------------

    if laps is not None and not laps.empty:

        if "Position" in laps.columns:

            valid_positions = (

                laps[
                    "Position"
                ]
                .dropna()

            )

            if not valid_positions.empty:

                return _safe_int(

                    valid_positions.iloc[-1]

                )

    # --------------------------------------------------------
    # Fallback to session results
    # --------------------------------------------------------

    try:

        results = session.results

        if results is None or results.empty:

            return None

        if "Abbreviation" not in results.columns:

            return None

        driver_rows = results[

            results[
                "Abbreviation"
            ]
            .astype(str)
            .str.upper()
            == driver

        ]

        if driver_rows.empty:

            return None

        row = driver_rows.iloc[0]

        if "Position" in row.index:

            return _safe_int(
                row[
                    "Position"
                ]
            )

    except Exception:

        pass

    return None


# ============================================================
# POSITION AHEAD / BEHIND
# ============================================================

def get_position_context(
    session,
    driver: str,
    current_position: Optional[int],
    laps: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Determine the driver's position context.

    Calculates:

        PositionAhead
        PositionBehind

    The values represent the positions immediately
    ahead of and behind the selected driver.

    Example:

        Current position = 5

        PositionAhead = 4
        PositionBehind = 6

    If the current position is unavailable,
    both values return None.
    """

    result = {

        "PositionAhead":
            None,

        "PositionBehind":
            None,

    }

    if current_position is None:

        return result

    # --------------------------------------------------------
    # Basic positional context
    # --------------------------------------------------------

    if current_position > 1:

        result[
            "PositionAhead"
        ] = current_position - 1

    # --------------------------------------------------------
    # Position behind
    # --------------------------------------------------------

    result[
        "PositionBehind"
    ] = current_position + 1

    # --------------------------------------------------------
    # If lap data contains a positional classification,
    # use the actual observed positions where possible.
    # --------------------------------------------------------

    if laps is not None and not laps.empty:

        if "Position" in laps.columns:

            valid_positions = (

                laps[
                    "Position"
                ]
                .dropna()

            )

            if not valid_positions.empty:

                latest_position = _safe_int(

                    valid_positions.iloc[-1]

                )

                if latest_position is not None:

                    if latest_position > 1:

                        result[
                            "PositionAhead"
                        ] = (

                            latest_position
                            - 1

                        )

                    result[
                        "PositionBehind"
                    ] = (

                        latest_position
                        + 1

                    )

    return result


# ============================================================
# GAP INFORMATION
# ============================================================

def get_gap_information(
    laps: pd.DataFrame
) -> Dict[str, Any]:
    """
    Extract gap information when available.

    FastF1 versions and session types may expose
    different gap-related columns.

    Possible fields include:

        GapToLeader
        Time
        IntervalToPositionAhead

    The function safely checks for available data.

    Returns
    -------
    dict
        Gap to car ahead and behind.
    """

    result = {

        "GapToAhead":
            None,

        "GapToBehind":
            None,

    }

    if laps.empty:

        return result

    # --------------------------------------------------------
    # Gap to car ahead
    # --------------------------------------------------------

    ahead_columns = [

        "IntervalToPositionAhead",

        "GapToAhead",

        "Time",

    ]

    for column in ahead_columns:

        if column in laps.columns:

            values = (

                laps[
                    column
                ]
                .dropna()

            )

            if not values.empty:

                result[
                    "GapToAhead"
                ] = _safe_float(

                    values.iloc[-1]

                )

                break

    # --------------------------------------------------------
    # Gap to car behind
    # --------------------------------------------------------
    #
    # Some FastF1 datasets do not expose a direct
    # gap-to-behind value.
    #
    # Therefore we only populate this field if a
    # suitable column is available.
    # --------------------------------------------------------

    behind_columns = [

        "GapToBehind",

        "IntervalToPositionBehind",

    ]

    for column in behind_columns:

        if column in laps.columns:

            values = (

                laps[
                    column
                ]
                .dropna()

            )

            if not values.empty:

                result[
                    "GapToBehind"
                ] = _safe_float(

                    values.iloc[-1]

                )

                break

    return result


# ============================================================
# TYRE INFORMATION
# ============================================================

def get_tyre_information(
    laps: pd.DataFrame
) -> Dict[str, Any]:
    """
    Extract current tyre compound,
    tyre life,
    current stint,
    and current stint length.
    """

    result = {

        "TyreCompound":
            None,

        "TyreLife":
            None,

        "CurrentStint":
            None,

        "CurrentStintLength":
            None,

    }

    if laps.empty:

        return result

    # --------------------------------------------------------
    # Latest valid lap
    # --------------------------------------------------------

    latest_lap = laps.iloc[-1]

    # --------------------------------------------------------
    # Tyre compound
    # --------------------------------------------------------

    if "Compound" in latest_lap.index:

        compound = latest_lap[
            "Compound"
        ]

        if pd.notna(compound):

            result[
                "TyreCompound"
            ] = str(
                compound
            ).upper()

    # --------------------------------------------------------
    # Tyre life
    # --------------------------------------------------------

    if "TyreLife" in latest_lap.index:

        result[
            "TyreLife"
        ] = _safe_int(

            latest_lap[
                "TyreLife"
            ]

        )

    # --------------------------------------------------------
    # Current stint
    # --------------------------------------------------------

    if "Stint" in latest_lap.index:

        result[
            "CurrentStint"
        ] = _safe_int(

            latest_lap[
                "Stint"
            ]

        )

    # --------------------------------------------------------
    # Current stint length
    # --------------------------------------------------------

    if "Stint" in laps.columns:

        valid_stints = (

            laps[
                "Stint"
            ]
            .dropna()

        )

        if not valid_stints.empty:

            current_stint = (

                valid_stints.iloc[-1]

            )

            current_stint_laps = laps[

                laps[
                    "Stint"
                ]
                == current_stint

            ]

            result[
                "CurrentStintLength"
            ] = len(

                current_stint_laps

            )

    return result


# ============================================================
# PIT STOPS
# ============================================================

def get_pit_stops(
    laps: pd.DataFrame
) -> int:
    """
    Estimate the number of completed pit stops.

    FastF1 lap data does not always expose a direct
    pit-stop count, so changes in stint number are
    used as an approximation.

    Example:

        Stint 1 → Stint 2
        = 1 pit stop

        Stint 1 → Stint 2 → Stint 3
        = 2 pit stops
    """

    if laps.empty:

        return 0

    if "Stint" not in laps.columns:

        return 0

    valid_stints = (

        laps[
            "Stint"
        ]
        .dropna()
        .unique()

    )

    return max(

        len(
            valid_stints
        )
        - 1,

        0

    )


# ============================================================
# PACE CALCULATIONS
# ============================================================

def get_pace_information(
    laps: pd.DataFrame
) -> Dict[str, Any]:
    """
    Calculate recent and average race pace.
    """

    result = {

        "RecentPace":
            None,

        "AveragePace":
            None,

        "AvgPaceLast3":
            None,

        "AvgPaceLast5":
            None,

        "AvgPaceLast10":
            None,

    }

    if laps.empty:

        return result

    if "LapTimeSeconds" not in laps.columns:

        return result

    valid_times = (

        laps[
            "LapTimeSeconds"
        ]
        .dropna()

    )

    if valid_times.empty:

        return result

    # --------------------------------------------------------
    # Average pace
    # --------------------------------------------------------

    result[
        "AveragePace"
    ] = _safe_float(

        valid_times.mean()

    )

    # --------------------------------------------------------
    # Most recent lap pace
    # --------------------------------------------------------

    result[
        "RecentPace"
    ] = _safe_float(

        valid_times.iloc[-1]

    )

    # --------------------------------------------------------
    # Rolling pace windows
    # --------------------------------------------------------

    if len(valid_times) >= 3:

        result[
            "AvgPaceLast3"
        ] = _safe_float(

            valid_times
            .tail(3)
            .mean()

        )

    if len(valid_times) >= 5:

        result[
            "AvgPaceLast5"
        ] = _safe_float(

            valid_times
            .tail(5)
            .mean()

        )

    if len(valid_times) >= 10:

        result[
            "AvgPaceLast10"
        ] = _safe_float(

            valid_times
            .tail(10)
            .mean()

        )

    return result


# ============================================================
# DEGRADATION ESTIMATION
# ============================================================

def estimate_degradation(
    laps: pd.DataFrame
) -> Optional[float]:
    """
    Estimate tyre degradation from lap-time trends.

    This is an initial approximation.

    Returns
    -------
    float or None
        Estimated seconds per lap degradation.
    """

    if laps.empty:

        return None

    if "LapTimeSeconds" not in laps.columns:

        return None

    if len(laps) < 5:

        return None

    valid_laps = laps[

        laps[
            "LapTimeSeconds"
        ]
        .notna()

    ].copy()

    if len(valid_laps) < 5:

        return None

    # --------------------------------------------------------
    # Use recent 10 valid laps
    # --------------------------------------------------------

    recent = (

        valid_laps
        .tail(10)
        .copy()

    )

    if len(recent) < 5:

        return None

    # --------------------------------------------------------
    # Create sequential lap index
    # --------------------------------------------------------

    recent = (

        recent
        .reset_index(
            drop=True
        )

    )

    recent[
        "LapIndex"
    ] = range(

        len(recent)

    )

    try:

        # ----------------------------------------------------
        # Linear regression approximation
        #
        # Lap Time =
        #     slope * Lap Index + intercept
        #
        # Slope approximates degradation.
        # ----------------------------------------------------

        slope = (

            recent[
                "LapTimeSeconds"
            ]
            .cov(
                recent[
                    "LapIndex"
                ]
            )

            /

            recent[
                "LapIndex"
            ]
            .var()

        )

        return _safe_float(
            slope
        )

    except Exception:

        return None


# ============================================================
# RACE PROGRESS
# ============================================================

def get_race_progress(
    current_lap: Optional[int],
    total_laps: Optional[int]
) -> Dict[str, Any]:
    """
    Calculate laps remaining and race progress.
    """

    result = {

        "TotalLaps":
            total_laps,

        "LapsRemaining":
            None,

        "RaceProgress":
            None,

    }

    if current_lap is None:

        return result

    if total_laps is None:

        return result

    if total_laps <= 0:

        return result

    result[
        "LapsRemaining"
    ] = max(

        total_laps
        - current_lap,

        0

    )

    result[
        "RaceProgress"
    ] = _safe_float(

        current_lap
        /
        total_laps

    )

    return result


# ============================================================
# MAIN RACE STATE BUILDER
# ============================================================

def build_race_state(
    session,
    driver: str
) -> Dict[str, Any]:
    """
    Build a complete structured race state
    for a selected driver.

    Parameters
    ----------
    session :
        Loaded FastF1 session.

    driver :
        Driver abbreviation.

    Returns
    -------
    dict
        Structured race state.
    """

    driver = str(
        driver
    ).upper()

    # --------------------------------------------------------
    # Load driver laps
    # --------------------------------------------------------

    laps = get_driver_laps(

        session,

        driver

    )

    if laps.empty:

        raise ValueError(

            f"No valid lap data found "
            f"for driver: {driver}"

        )

    # --------------------------------------------------------
    # Session information
    # --------------------------------------------------------

    session_info = get_session_info(
        session
    )

    # --------------------------------------------------------
    # Driver information
    # --------------------------------------------------------

    driver_info = get_driver_info(

        session,

        driver

    )

    # --------------------------------------------------------
    # Current lap
    # --------------------------------------------------------

    current_lap = get_current_lap(
        laps
    )

    # --------------------------------------------------------
    # Current position
    # --------------------------------------------------------

    current_position = get_current_position(

        session,

        driver,

        laps

    )

    # --------------------------------------------------------
    # Position context
    # --------------------------------------------------------

    position_context = get_position_context(

        session,

        driver,

        current_position,

        laps

    )

    # --------------------------------------------------------
    # Gap information
    # --------------------------------------------------------

    gap_information = get_gap_information(
        laps
    )

    # --------------------------------------------------------
    # Tyre information
    # --------------------------------------------------------

    tyre_info = get_tyre_information(
        laps
    )

    # --------------------------------------------------------
    # Pit stops
    # --------------------------------------------------------

    pit_stops = get_pit_stops(
        laps
    )

    # --------------------------------------------------------
    # Pace
    # --------------------------------------------------------

    pace_info = get_pace_information(
        laps
    )

    # --------------------------------------------------------
    # Degradation
    # --------------------------------------------------------

    degradation = estimate_degradation(
        laps
    )

    # --------------------------------------------------------
    # Total race laps
    # --------------------------------------------------------

    total_laps = None

    try:

        total_laps = _safe_int(

            session.total_laps

        )

    except Exception:

        pass

    # --------------------------------------------------------
    # Race progress
    # --------------------------------------------------------

    race_progress = get_race_progress(

        current_lap,

        total_laps

    )

    # --------------------------------------------------------
    # Combine everything
    # --------------------------------------------------------

    race_state = {

        # ----------------------------------------------------
        # Session
        # ----------------------------------------------------

        **session_info,

        # ----------------------------------------------------
        # Driver
        # ----------------------------------------------------

        **driver_info,

        # ----------------------------------------------------
        # Race state
        # ----------------------------------------------------

        "CurrentLap":
            current_lap,

        "Position":
            current_position,

        # ----------------------------------------------------
        # Position context
        # ----------------------------------------------------

        **position_context,

        # ----------------------------------------------------
        # Gap information
        # ----------------------------------------------------

        **gap_information,

        # ----------------------------------------------------
        # Tyres
        # ----------------------------------------------------

        **tyre_info,

        # ----------------------------------------------------
        # Pit stops
        # ----------------------------------------------------

        "PitStopsCompleted":
            pit_stops,

        # ----------------------------------------------------
        # Pace
        # ----------------------------------------------------

        **pace_info,

        # ----------------------------------------------------
        # Degradation
        # ----------------------------------------------------

        "DegradationRate":
            degradation,

        # ----------------------------------------------------
        # Race progress
        # ----------------------------------------------------

        **race_progress,

    }

    return race_state


# ============================================================
# CONVERT RACE STATE TO DATAFRAME
# ============================================================

def race_state_to_dataframe(
    race_state: Dict[str, Any]
) -> pd.DataFrame:
    """
    Convert a race-state dictionary into a
    single-row DataFrame.

    This will be useful later when passing
    features to the ML model.
    """

    return pd.DataFrame(

        [
            race_state
        ]

    )


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    from src.data_loader import (
        load_session
        )

    print(
        "=" * 60
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "SPRINT 3 - RACE STATE ENHANCEMENT TEST"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # Test configuration
    # --------------------------------------------------------

    season = 2025

    grand_prix = (
        "British Grand Prix"
    )

    session_type = "R"

    driver = "VER"

    # --------------------------------------------------------
    # Load session
    # --------------------------------------------------------

    print(
        "\nLoading FastF1 session..."
    )

    session = load_session(

        season,

        grand_prix,

        session_type

    )

    if session is None:

        raise RuntimeError(

            "Failed to load FastF1 session."

        )

    print(
        "Session loaded successfully."
    )

    # --------------------------------------------------------
    # Build race state
    # --------------------------------------------------------

    print(
        "\nBuilding enhanced race state..."
    )

    state = build_race_state(

        session,

        driver

    )

    print(
        "\nRace state generated successfully."
    )

    # --------------------------------------------------------
    # Display race state
    # --------------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "ENHANCED RACE STATE"
    )

    print(
        "=" * 60
    )

    for key, value in state.items():

        print(

            f"{key}: {value}"

        )

    # --------------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "RACE STATE DATAFRAME"
    )

    print(
        "=" * 60
    )

    state_df = race_state_to_dataframe(
        state
    )

    print(
        state_df.to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Test completed
    # --------------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "SPRINT 3 - RACE STATE ENHANCEMENT TEST COMPLETED"
    )

    print(
        "=" * 60
    )