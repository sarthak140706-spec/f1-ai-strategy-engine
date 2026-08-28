"""
dynamic_race_state.py

PHASE 4.1 — DYNAMIC RACE STATE ENGINE

Purpose
-------
Reconstruct a driver's race state at any selected lap of a race.

Unlike the Phase 3 race-state engine, which mainly represents
the latest/current available race state, this module allows the
strategy system to examine historical race situations lap-by-lap.

Example
-------

2024 Bahrain Grand Prix
Driver: VER
Selected Lap: 35

The engine reconstructs:

    Position
    Tyre Compound
    Tyre Age
    Current Stint
    Stint Length
    Recent Pace
    Average Pace
    Degradation Rate
    Pit Stops Completed
    Remaining Laps
    Race Progress

This becomes the foundation for Phase 4 advanced strategy
intelligence.
"""

from typing import Dict, Any

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RECENT_PACE_WINDOW = 3

DEGRADATION_WINDOW = 8


# ============================================================
# HELPERS
# ============================================================

def _safe_int(value):
    """
    Safely convert a value to int.
    """

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

        return int(value)

    except (
        TypeError,
        ValueError
    ):

        return None


def _safe_float(value):
    """
    Safely convert a value to float.
    """

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return None


def _lap_time_to_seconds(value):
    """
    Convert FastF1 timedelta lap time to seconds.
    """

    if value is None:

        return None

    try:

        if pd.isna(value):

            return None

    except Exception:

        pass

    try:

        return float(
            value.total_seconds()
        )

    except Exception:

        try:

            return float(value)

        except (
            TypeError,
            ValueError
        ):

            return None


# ============================================================
# VALIDATION
# ============================================================

def validate_dynamic_state_inputs(
    session,
    driver: str,
    selected_lap: int
) -> None:
    """
    Validate inputs required by the dynamic race-state engine.
    """

    if session is None:

        raise ValueError(
            "session cannot be None."
        )

    if not isinstance(
        driver,
        str
    ) or not driver.strip():

        raise ValueError(
            "driver must be a valid "
            "driver abbreviation."
        )

    if not isinstance(
        selected_lap,
        int
    ):

        raise TypeError(
            "selected_lap must be an integer."
        )

    if selected_lap <= 0:

        raise ValueError(
            "selected_lap must be greater than zero."
        )

    if (
        session.laps is None
        or session.laps.empty
    ):

        raise ValueError(
            "Session does not contain lap data."
        )


# ============================================================
# DRIVER INFORMATION
# ============================================================

def get_driver_information(
    session,
    driver: str
) -> Dict[str, Any]:
    """
    Extract basic driver information from session results.
    """

    result = {

        "Driver":
            driver,

        "DriverNumber":
            None,

        "Team":
            None

    }

    if (
        session.results is None
        or session.results.empty
    ):

        return result

    results = session.results.copy()

    if "Abbreviation" not in results.columns:

        return result

    driver_results = results[

        results[
            "Abbreviation"
        ].astype(str).str.upper()
        ==
        driver.upper()

    ]

    if driver_results.empty:

        return result

    row = driver_results.iloc[0]

    result[
        "DriverNumber"
    ] = str(

        row.get(
            "DriverNumber",
            ""
        )

    )

    result[
        "Team"
    ] = str(

        row.get(
            "TeamName",
            ""
        )

    )

    return result


# ============================================================
# DRIVER LAP DATA
# ============================================================

def get_driver_laps(
    session,
    driver: str
) -> pd.DataFrame:
    """
    Return all lap records belonging to the requested driver.
    """

    laps = session.laps.copy()

    if "Driver" not in laps.columns:

        raise ValueError(
            "FastF1 lap data does not contain "
            "the Driver column."
        )

    driver_laps = laps[

        laps[
            "Driver"
        ].astype(str).str.upper()
        ==
        driver.upper()

    ].copy()

    if driver_laps.empty:

        raise ValueError(

            f"No lap data found for driver "
            f"{driver}."

        )

    if "LapNumber" not in driver_laps.columns:

        raise ValueError(
            "FastF1 lap data does not contain "
            "LapNumber."
        )

    driver_laps = driver_laps[

        driver_laps[
            "LapNumber"
        ].notna()

    ].copy()

    driver_laps[
        "LapNumber"
    ] = driver_laps[
        "LapNumber"
    ].astype(int)

    driver_laps = driver_laps.sort_values(
        "LapNumber"
    )

    return driver_laps


# ============================================================
# VALID LAP TIMES
# ============================================================

def prepare_lap_times(
    laps: pd.DataFrame
) -> pd.DataFrame:
    """
    Convert lap times to seconds and remove unusable records.
    """

    result = laps.copy()

    if "LapTime" not in result.columns:

        result[
            "LapTimeSeconds"
        ] = np.nan

        return result

    result[
        "LapTimeSeconds"
    ] = result[
        "LapTime"
    ].apply(
        _lap_time_to_seconds
    )

    # --------------------------------------------------------
    # REMOVE INVALID LAP TIMES
    # --------------------------------------------------------

    result = result[

        result[
            "LapTimeSeconds"
        ].notna()

    ].copy()

    # --------------------------------------------------------
    # USE ACCURATE LAPS WHERE AVAILABLE
    # --------------------------------------------------------

    if "IsAccurate" in result.columns:

        accurate = result[

            result[
                "IsAccurate"
            ] == True

        ]

        if not accurate.empty:

            result = accurate.copy()

    # --------------------------------------------------------
    # REMOVE DELETED LAPS WHERE AVAILABLE
    # --------------------------------------------------------

    if "Deleted" in result.columns:

        result = result[

            result[
                "Deleted"
            ] != True

        ].copy()

    return result


# ============================================================
# POSITION
# ============================================================

def determine_position(
    selected_lap_row
):
    """
    Return driver position at selected lap when available.
    """

    if "Position" not in selected_lap_row.index:

        return None

    return _safe_int(
        selected_lap_row.get(
            "Position"
        )
    )


# ============================================================
# CURRENT STINT
# ============================================================

def determine_current_stint(
    selected_lap_row
):
    """
    Determine the stint number at the selected lap.
    """

    if "Stint" not in selected_lap_row.index:

        return None

    return _safe_int(
        selected_lap_row.get(
            "Stint"
        )
    )


# ============================================================
# CURRENT STINT LENGTH
# ============================================================

def determine_stint_length(
    completed_laps: pd.DataFrame,
    current_stint
):
    """
    Calculate how many laps have been completed in the
    current stint by the selected lap.
    """

    if current_stint is None:

        return None

    if "Stint" not in completed_laps.columns:

        return None

    stint_laps = completed_laps[

        completed_laps[
            "Stint"
        ] == current_stint

    ]

    return int(
        len(stint_laps)
    )


# ============================================================
# TYRE COMPOUND
# ============================================================

def determine_tyre_compound(
    selected_lap_row
):
    """
    Determine tyre compound at selected lap.
    """

    if "Compound" not in selected_lap_row.index:

        return None

    compound = selected_lap_row.get(
        "Compound"
    )

    if pd.isna(
        compound
    ):

        return None

    compound = str(
        compound
    ).strip().upper()

    if not compound:

        return None

    return compound


# ============================================================
# TYRE LIFE
# ============================================================

def determine_tyre_life(
    selected_lap_row
):
    """
    Determine tyre age at the selected lap.
    """

    if "TyreLife" not in selected_lap_row.index:

        return None

    value = _safe_float(

        selected_lap_row.get(
            "TyreLife"
        )

    )

    if value is None:

        return None

    return round(
        value,
        2
    )


# ============================================================
# RECENT PACE
# ============================================================

def calculate_recent_pace(
    completed_laps: pd.DataFrame,
    window: int = RECENT_PACE_WINDOW
):
    """
    Calculate average pace across the latest valid laps.
    """

    valid_laps = prepare_lap_times(
        completed_laps
    )

    if valid_laps.empty:

        return None

    recent = valid_laps.tail(
        window
    )

    if recent.empty:

        return None

    return round(

        float(

            recent[
                "LapTimeSeconds"
            ].mean()

        ),

        3

    )


# ============================================================
# AVERAGE PACE
# ============================================================

def calculate_average_pace(
    completed_laps: pd.DataFrame
):
    """
    Calculate driver's average race pace up to selected lap.
    """

    valid_laps = prepare_lap_times(
        completed_laps
    )

    if valid_laps.empty:

        return None

    return round(

        float(

            valid_laps[
                "LapTimeSeconds"
            ].mean()

        ),

        3

    )


# ============================================================
# PACE WINDOWS
# ============================================================

def calculate_pace_window(
    completed_laps: pd.DataFrame,
    window: int
):
    """
    Calculate average pace over a specified recent window.
    """

    valid_laps = prepare_lap_times(
        completed_laps
    )

    if valid_laps.empty:

        return None

    recent = valid_laps.tail(
        window
    )

    if recent.empty:

        return None

    return round(

        float(

            recent[
                "LapTimeSeconds"
            ].mean()

        ),

        3

    )


# ============================================================
# DEGRADATION
# ============================================================

def calculate_degradation_rate(
    completed_laps: pd.DataFrame,
    current_stint,
    window: int = DEGRADATION_WINDOW
):
    """
    Estimate tyre degradation using the slope of recent
    lap times inside the current stint.

    Positive value:
        lap times are increasing -> tyres getting slower.

    Negative value:
        lap times are improving.

    Units:
        seconds per lap.
    """

    if current_stint is None:

        return None

    if "Stint" not in completed_laps.columns:

        return None

    stint_laps = completed_laps[

        completed_laps[
            "Stint"
        ] == current_stint

    ].copy()

    stint_laps = prepare_lap_times(
        stint_laps
    )

    if len(
        stint_laps
    ) < 3:

        return None

    stint_laps = stint_laps.tail(
        window
    )

    x = np.arange(
        len(stint_laps)
    )

    y = stint_laps[
        "LapTimeSeconds"
    ].astype(float).to_numpy()

    if len(
        y
    ) < 3:

        return None

    try:

        slope = np.polyfit(
            x,
            y,
            1
        )[0]

    except Exception:

        return None

    return round(
        float(slope),
        4
    )


# ============================================================
# PIT STOPS COMPLETED
# ============================================================

def calculate_pit_stops_completed(
    completed_laps: pd.DataFrame
):
    """
    Count completed pit stops before or at the selected lap.
    """

    if "PitInTime" in completed_laps.columns:

        return int(

            completed_laps[
                "PitInTime"
            ].notna().sum()

        )

    # --------------------------------------------------------
    # FALLBACK USING STINT NUMBER
    # --------------------------------------------------------

    if "Stint" in completed_laps.columns:

        stints = completed_laps[
            "Stint"
        ].dropna()

        if not stints.empty:

            maximum_stint = int(
                stints.max()
            )

            return max(
                0,
                maximum_stint - 1
            )

    return 0


# ============================================================
# TOTAL LAPS
# ============================================================

def determine_total_laps(
    session,
    driver_laps: pd.DataFrame
):
    """
    Determine total race laps.
    """

    try:

        total_laps = session.total_laps

        if (
            total_laps is not None
            and not pd.isna(
                total_laps
            )
        ):

            return int(
                total_laps
            )

    except Exception:

        pass

    if driver_laps.empty:

        return None

    return int(

        driver_laps[
            "LapNumber"
        ].max()

    )


# ============================================================
# BUILD DYNAMIC RACE STATE
# ============================================================

def build_dynamic_race_state(
    session,
    driver: str,
    selected_lap: int
) -> Dict[str, Any]:
    """
    Reconstruct the driver's race state at a selected lap.

    Example:

        build_dynamic_race_state(
            session=session,
            driver="VER",
            selected_lap=35
        )
    """

    driver = driver.strip().upper()

    validate_dynamic_state_inputs(

        session=session,

        driver=driver,

        selected_lap=selected_lap

    )

    # --------------------------------------------------------
    # DRIVER DATA
    # --------------------------------------------------------

    driver_information = (
        get_driver_information(
            session,
            driver
        )
    )

    driver_laps = get_driver_laps(

        session=session,

        driver=driver

    )

    # --------------------------------------------------------
    # CHECK LAP EXISTS
    # --------------------------------------------------------

    maximum_driver_lap = int(

        driver_laps[
            "LapNumber"
        ].max()

    )

    if selected_lap > maximum_driver_lap:

        raise ValueError(

            f"Selected lap {selected_lap} "
            f"is unavailable for {driver}. "

            f"Maximum completed lap is "
            f"{maximum_driver_lap}."

        )

    # --------------------------------------------------------
    # ALL LAPS UP TO SELECTED LAP
    # --------------------------------------------------------

    completed_laps = driver_laps[

        driver_laps[
            "LapNumber"
        ] <= selected_lap

    ].copy()

    selected_rows = driver_laps[

        driver_laps[
            "LapNumber"
        ] == selected_lap

    ]

    if selected_rows.empty:

        raise ValueError(

            f"No lap record exists for "
            f"{driver} on lap {selected_lap}."

        )

    selected_lap_row = (
        selected_rows.iloc[-1]
    )

    # --------------------------------------------------------
    # TOTAL / REMAINING LAPS
    # --------------------------------------------------------

    total_laps = determine_total_laps(

        session=session,

        driver_laps=driver_laps

    )

    if total_laps is None:

        laps_remaining = None

        race_progress = None

    else:

        laps_remaining = max(

            0,

            total_laps
            -
            selected_lap

        )

        race_progress = round(

            selected_lap
            /
            total_laps,

            4

        )

    # --------------------------------------------------------
    # STINT
    # --------------------------------------------------------

    current_stint = (
        determine_current_stint(
            selected_lap_row
        )
    )

    current_stint_length = (
        determine_stint_length(

            completed_laps,

            current_stint

        )
    )

    # --------------------------------------------------------
    # TYRE
    # --------------------------------------------------------

    tyre_compound = (
        determine_tyre_compound(
            selected_lap_row
        )
    )

    tyre_life = (
        determine_tyre_life(
            selected_lap_row
        )
    )

    # --------------------------------------------------------
    # POSITION
    # --------------------------------------------------------

    position = determine_position(
        selected_lap_row
    )

    # --------------------------------------------------------
    # PACE
    # --------------------------------------------------------

    recent_pace = (
        calculate_recent_pace(
            completed_laps
        )
    )

    average_pace = (
        calculate_average_pace(
            completed_laps
        )
    )

    avg_pace_last_3 = (
        calculate_pace_window(
            completed_laps,
            3
        )
    )

    avg_pace_last_5 = (
        calculate_pace_window(
            completed_laps,
            5
        )
    )

    avg_pace_last_10 = (
        calculate_pace_window(
            completed_laps,
            10
        )
    )

    # --------------------------------------------------------
    # DEGRADATION
    # --------------------------------------------------------

    degradation_rate = (
        calculate_degradation_rate(

            completed_laps,

            current_stint

        )
    )

    # --------------------------------------------------------
    # PIT STOPS
    # --------------------------------------------------------

    pit_stops_completed = (
        calculate_pit_stops_completed(
            completed_laps
        )
    )

    # --------------------------------------------------------
    # EVENT INFORMATION
    # --------------------------------------------------------

    grand_prix = None

    circuit = None

    season = None

    try:

        grand_prix = str(

            session.event[
                "EventName"
            ]

        )

    except Exception:

        pass

    try:

        circuit = str(

            session.event[
                "Location"
            ]

        )

    except Exception:

        pass

    try:

        season = int(

            session.event[
                "EventDate"
            ].year

        )

    except Exception:

        pass

    # ========================================================
    # FINAL DYNAMIC STATE
    # ========================================================

    return {

        "Season":
            season,

        "GrandPrix":
            grand_prix,

        "Circuit":
            circuit,

        "SessionType":
            "Race",

        "Driver":
            driver,

        "DriverNumber":
            driver_information.get(
                "DriverNumber"
            ),

        "Team":
            driver_information.get(
                "Team"
            ),

        "CurrentLap":
            selected_lap,

        "TotalLaps":
            total_laps,

        "LapsRemaining":
            laps_remaining,

        "RaceProgress":
            race_progress,

        "Position":
            position,

        "TyreCompound":
            tyre_compound,

        "TyreLife":
            tyre_life,

        "CurrentStint":
            current_stint,

        "CurrentStintLength":
            current_stint_length,

        "PitStopsCompleted":
            pit_stops_completed,

        "RecentPace":
            recent_pace,

        "AveragePace":
            average_pace,

        "AvgPaceLast3":
            avg_pace_last_3,

        "AvgPaceLast5":
            avg_pace_last_5,

        "AvgPaceLast10":
            avg_pace_last_10,

        "DegradationRate":
            degradation_rate,

        "DynamicState":
            True

    }


# ============================================================
# DISPLAY DYNAMIC STATE
# ============================================================

def display_dynamic_race_state(
    state: Dict[str, Any]
) -> None:
    """
    Display reconstructed race state.
    """

    print(
        "\n" + "=" * 65
    )

    print(
        "PHASE 4.1 — DYNAMIC RACE STATE"
    )

    print(
        "=" * 65
    )

    print(
        f"Race: "
        f"{state.get('GrandPrix')}"
    )

    print(
        f"Circuit: "
        f"{state.get('Circuit')}"
    )

    print(
        f"Driver: "
        f"{state.get('Driver')}"
    )

    print(
        f"Team: "
        f"{state.get('Team')}"
    )

    print(
        "-" * 65
    )

    print(
        f"Lap: "
        f"{state.get('CurrentLap')}"
        f"/"
        f"{state.get('TotalLaps')}"
    )

    print(
        f"Laps Remaining: "
        f"{state.get('LapsRemaining')}"
    )

    print(
        f"Race Progress: "
        f"{state.get('RaceProgress')}"
    )

    print(
        f"Position: "
        f"{state.get('Position')}"
    )

    print(
        "-" * 65
    )

    print(
        f"Tyre: "
        f"{state.get('TyreCompound')}"
    )

    print(
        f"Tyre Life: "
        f"{state.get('TyreLife')}"
    )

    print(
        f"Current Stint: "
        f"{state.get('CurrentStint')}"
    )

    print(
        f"Stint Length: "
        f"{state.get('CurrentStintLength')}"
    )

    print(
        f"Pit Stops Completed: "
        f"{state.get('PitStopsCompleted')}"
    )

    print(
        "-" * 65
    )

    print(
        f"Recent Pace: "
        f"{state.get('RecentPace')}"
    )

    print(
        f"Average Pace: "
        f"{state.get('AveragePace')}"
    )

    print(
        f"Last 3 Pace: "
        f"{state.get('AvgPaceLast3')}"
    )

    print(
        f"Last 5 Pace: "
        f"{state.get('AvgPaceLast5')}"
    )

    print(
        f"Last 10 Pace: "
        f"{state.get('AvgPaceLast10')}"
    )

    print(
        f"Degradation Rate: "
        f"{state.get('DegradationRate')}"
    )

    print(
        "=" * 65
    )