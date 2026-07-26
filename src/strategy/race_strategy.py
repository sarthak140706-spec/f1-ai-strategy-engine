"""
race_strategy.py

V5 Sprint 2 - Step 3

Purpose:
--------
Analyze the strategy of all available drivers
in a selected F1 race.

Pipeline:

    Selected Race
          ↓
    Get Available Drivers
          ↓
    For Each Driver
          ↓
    strategy_engine.py
          ↓
    Race State
          ↓
    ML Prediction
          ↓
    Strategy Simulation
          ↓
    Decision Engine
          ↓
    Driver Strategy Result
          ↓
    Complete Race Strategy Overview

This module does NOT contain:
    - ML training logic
    - ML prediction logic
    - Simulator logic
    - Decision engine logic

It only coordinates multi-driver analysis.
"""

from typing import Dict, Any, List

import pandas as pd

from src.data_loader import (
    get_available_drivers
)

from src.strategy.strategy_engine import (
    run_strategy
)


# ============================================================
# ANALYZE SINGLE DRIVER
# ============================================================

def analyze_driver_strategy(
    season: int,
    grand_prix: str,
    driver: str,
    session_type: str = "R"
) -> Dict[str, Any]:
    """
    Analyze the complete strategy for one driver.

    Parameters
    ----------
    season : int
        F1 season year.

    grand_prix : str
        Grand Prix name.

    driver : str
        Driver abbreviation.

    session_type : str
        FastF1 session type.
        Default is "R".

    Returns
    -------
    dict
        Complete strategy result for the driver.
    """

    driver = str(
        driver
    ).upper()

    result = run_strategy(

        season=season,

        grand_prix=grand_prix,

        driver=driver,

        session_type=session_type

    )

    return result


# ============================================================
# ANALYZE COMPLETE RACE
# ============================================================

def analyze_race_strategy(
    season: int,
    grand_prix: str,
    session_type: str = "R"
) -> Dict[str, Any]:
    """
    Analyze the strategy of all available drivers
    in a selected race.

    Parameters
    ----------
    season : int
        F1 season year.

    grand_prix : str
        Grand Prix name.

    session_type : str
        FastF1 session type.
        Default is "R".

    Returns
    -------
    dict
        Complete race strategy analysis.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if not isinstance(
        season,
        int
    ):

        raise TypeError(
            "season must be an integer."
        )

    if not isinstance(
        grand_prix,
        str
    ) or not grand_prix.strip():

        raise ValueError(
            "grand_prix must be a valid "
            "non-empty string."
        )

    if not isinstance(
        session_type,
        str
    ) or not session_type.strip():

        raise ValueError(
            "session_type must be a valid "
            "non-empty string."
        )

    # ========================================================
    # LOAD AVAILABLE DRIVERS
    # ========================================================

    print(
        "\n" + "=" * 70
    )

    print(
        "F1 AI MULTI-DRIVER STRATEGY ANALYSIS"
    )

    print(
        "=" * 70
    )

    print(
        f"\nSeason: {season}"
    )

    print(
        f"Grand Prix: {grand_prix}"
    )

    print(
        f"Session: {session_type}"
    )

    print(
        "\n[1/3] Loading available drivers..."
    )

    drivers = get_available_drivers(

        season=season,

        grand_prix=grand_prix,

        session_type=session_type

    )

    if not drivers:

        raise RuntimeError(

            f"No drivers found for "

            f"{season} {grand_prix}."

        )

    print(
        f"Found {len(drivers)} drivers."
    )

    print(
        f"Drivers: {', '.join(drivers)}"
    )

    # ========================================================
    # ANALYZE EACH DRIVER
    # ========================================================

    print(
        "\n[2/3] Analyzing driver strategies..."
    )

    driver_results: List[
        Dict[str, Any]
    ] = []

    failed_drivers: List[
        Dict[str, Any]
    ] = []

    for index, driver in enumerate(
        drivers,
        start=1
    ):

        print(
            "\n" + "-" * 70
        )

        print(
            f"Analyzing driver "
            f"{index}/{len(drivers)}: "
            f"{driver}"
        )

        print(
            "-" * 70
        )

        try:

            result = analyze_driver_strategy(

                season=season,

                grand_prix=grand_prix,

                driver=driver,

                session_type=session_type

            )

            driver_results.append(
                result
            )

            print(
                f"✅ {driver} analysis completed."
            )

            print(
                f"Decision: "
                f"{result.get('final_decision')}"
            )

            print(
                f"Confidence: "
                f"{result.get('confidence')}"
            )

        except Exception as e:

            print(
                f"❌ Failed to analyze {driver}"
            )

            print(
                f"Error: {e}"
            )

            failed_drivers.append({

                "driver":
                    driver,

                "error":
                    str(e)

            })

    # ========================================================
    # VALIDATE RESULTS
    # ========================================================

    if not driver_results:

        raise RuntimeError(

            "Strategy analysis failed for "
            "all available drivers."

        )

    # ========================================================
    # CREATE STRATEGY TABLE
    # ========================================================

    print(
        "\n[3/3] Creating race strategy overview..."
    )

    strategy_rows = []

    for result in driver_results:

        strategy_rows.append({

            "Driver":
                result.get(
                    "driver"
                ),

            "Team":
                result.get(
                    "team"
                ),

            "Position":
                result.get(
                    "position"
                ),

            "CurrentLap":
                result.get(
                    "current_lap"
                ),

            "LapsRemaining":
                result.get(
                    "laps_remaining"
                ),

            "Tyre":
                result.get(
                    "tyre_compound"
                ),

            "TyreLife":
                result.get(
                    "tyre_life"
                ),

            "PitProbability":
                result.get(
                    "pit_probability"
                ),

            "SimulatorRecommendation":
                result.get(
                    "decision_details",
                ).get(
                    "simulator_recommendation"
                ),

            "SimulationDelta":
                result.get(
                    "decision_details"
                ).get(
                    "delta"
                ),

            "FinalDecision":
                result.get(
                    "final_decision"
                ),

            "Confidence":
                result.get(
                    "confidence"
                ),

            "Reason":
                result.get(
                    "reason"
                )

        })

    strategy_table = pd.DataFrame(
        strategy_rows
    )

    # ========================================================
    # SORT BY CURRENT POSITION
    # ========================================================

    if (
        "Position"
        in strategy_table.columns
    ):

        strategy_table = (
            strategy_table
            .sort_values(
                by="Position",
                na_position="last"
            )
            .reset_index(
                drop=True
            )
        )

    # ========================================================
    # RETURN COMPLETE ANALYSIS
    # ========================================================

    return {

        # ----------------------------------------------------
        # RACE INFORMATION
        # ----------------------------------------------------

        "season":
            season,

        "grand_prix":
            grand_prix,

        "session_type":
            session_type,

        # ----------------------------------------------------
        # DRIVER INFORMATION
        # ----------------------------------------------------

        "drivers_found":
            drivers,

        "drivers_analyzed":
            len(
                driver_results
            ),

        "drivers_failed":
            len(
                failed_drivers
            ),

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        "driver_results":
            driver_results,

        "failed_drivers":
            failed_drivers,

        # ----------------------------------------------------
        # STRATEGY TABLE
        # ----------------------------------------------------

        "strategy_table":
            strategy_table

    }


# ============================================================
# GET PIT RECOMMENDATIONS
# ============================================================

def get_pit_recommendations(
    race_analysis: Dict[str, Any]
) -> pd.DataFrame:
    """
    Extract drivers currently recommended
    to PIT NOW.

    Parameters
    ----------
    race_analysis : dict
        Result generated by analyze_race_strategy().

    Returns
    -------
    pandas.DataFrame
        Drivers recommended to pit.
    """

    if not isinstance(
        race_analysis,
        dict
    ):

        raise TypeError(
            "race_analysis must be a dictionary."
        )

    strategy_table = race_analysis.get(
        "strategy_table"
    )

    if not isinstance(
        strategy_table,
        pd.DataFrame
    ):

        raise ValueError(
            "strategy_table is missing "
            "or invalid."
        )

    if strategy_table.empty:

        return strategy_table.copy()

    return strategy_table[
        strategy_table[
            "FinalDecision"
        ] == "PIT NOW"
    ].copy()


# ============================================================
# GET STAY-OUT RECOMMENDATIONS
# ============================================================

def get_stay_out_recommendations(
    race_analysis: Dict[str, Any]
) -> pd.DataFrame:
    """
    Extract drivers currently recommended
    to STAY OUT.

    Parameters
    ----------
    race_analysis : dict
        Result generated by analyze_race_strategy().

    Returns
    -------
    pandas.DataFrame
        Drivers recommended to stay out.
    """

    if not isinstance(
        race_analysis,
        dict
    ):

        raise TypeError(
            "race_analysis must be a dictionary."
        )

    strategy_table = race_analysis.get(
        "strategy_table"
    )

    if not isinstance(
        strategy_table,
        pd.DataFrame
    ):

        raise ValueError(
            "strategy_table is missing "
            "or invalid."
        )

    if strategy_table.empty:

        return strategy_table.copy()

    return strategy_table[
        strategy_table[
            "FinalDecision"
        ] == "STAY OUT"
    ].copy()


# ============================================================
# DISPLAY RACE STRATEGY
# ============================================================

def display_race_strategy(
    race_analysis: Dict[str, Any]
) -> None:
    """
    Display the multi-driver race strategy
    in a readable terminal format.
    """

    if not isinstance(
        race_analysis,
        dict
    ):

        raise TypeError(
            "race_analysis must be a dictionary."
        )

    strategy_table = race_analysis.get(
        "strategy_table"
    )

    if not isinstance(
        strategy_table,
        pd.DataFrame
    ):

        raise ValueError(
            "strategy_table is missing "
            "or invalid."
        )

    print(
        "\n" + "=" * 100
    )

    print(
        "F1 AI RACE STRATEGY OVERVIEW"
    )

    print(
        "=" * 100
    )

    print(
        f"\nSeason: "
        f"{race_analysis.get('season')}"
    )

    print(
        f"Grand Prix: "
        f"{race_analysis.get('grand_prix')}"
    )

    print(
        f"Drivers Analyzed: "
        f"{race_analysis.get('drivers_analyzed')}"
    )

    print(
        f"Drivers Failed: "
        f"{race_analysis.get('drivers_failed')}"
    )

    # ========================================================
    # STRATEGY TABLE
    # ========================================================

    print(
        "\n" + "-" * 100
    )

    print(
        "DRIVER STRATEGY RECOMMENDATIONS"
    )

    print(
        "-" * 100
    )

    display_columns = [

        "Driver",

        "Team",

        "Position",

        "Tyre",

        "TyreLife",

        "PitProbability",

        "FinalDecision",

        "Confidence"

    ]

    available_columns = [

        column

        for column in display_columns

        if column
        in strategy_table.columns

    ]

    if available_columns:

        display_table = (
            strategy_table[
                available_columns
            ]
        ).copy()

        print(
            display_table.to_string(
                index=False
            )
        )

    else:

        print(
            strategy_table.to_string(
                index=False
            )
        )

    # ========================================================
    # PIT RECOMMENDATIONS
    # ========================================================

    pit_drivers = get_pit_recommendations(
        race_analysis
    )

    print(
        "\n" + "-" * 100
    )

    print(
        "PIT NOW RECOMMENDATIONS"
    )

    print(
        "-" * 100
    )

    if pit_drivers.empty:

        print(
            "No drivers are currently "
            "recommended to PIT NOW."
        )

    else:

        print(

            ", ".join(

                pit_drivers[
                    "Driver"
                ]
                .astype(str)
                .tolist()

            )

        )

    # ========================================================
    # STAY OUT RECOMMENDATIONS
    # ========================================================

    stay_out_drivers = (
        get_stay_out_recommendations(
            race_analysis
        )
    )

    print(
        "\n" + "-" * 100
    )

    print(
        "STAY OUT RECOMMENDATIONS"
    )

    print(
        "-" * 100
    )

    if stay_out_drivers.empty:

        print(
            "No drivers are currently "
            "recommended to STAY OUT."
        )

    else:

        print(

            ", ".join(

                stay_out_drivers[
                    "Driver"
                ]
                .astype(str)
                .tolist()

            )

        )

    # ========================================================
    # FAILED DRIVERS
    # ========================================================

    failed_drivers = race_analysis.get(
        "failed_drivers",
        []
    )

    if failed_drivers:

        print(
            "\n" + "-" * 100
        )

        print(
            "DRIVERS WITH FAILED ANALYSIS"
        )

        print(
            "-" * 100
        )

        for failed in failed_drivers:

            print(

                f"{failed.get('driver')}: "

                f"{failed.get('error')}"

            )

    print(
        "\n" + "=" * 100
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST CONFIGURATION
    # --------------------------------------------------------

    SEASON = 2025

    GRAND_PRIX = (
        "British Grand Prix"
    )

    SESSION_TYPE = "R"

    # --------------------------------------------------------
    # RUN MULTI-DRIVER ANALYSIS
    # --------------------------------------------------------

    try:

        race_analysis = analyze_race_strategy(

            season=SEASON,

            grand_prix=GRAND_PRIX,

            session_type=SESSION_TYPE

        )

        # ----------------------------------------------------
        # DISPLAY RESULTS
        # ----------------------------------------------------

        display_race_strategy(
            race_analysis
        )

        print(
            "\n✅ MULTI-DRIVER STRATEGY ANALYSIS "
            "TEST PASSED"
        )

    except Exception as e:

        print(
            "\n❌ MULTI-DRIVER STRATEGY ANALYSIS "
            "TEST FAILED"
        )

        print(
            f"Error: {e}"
        )