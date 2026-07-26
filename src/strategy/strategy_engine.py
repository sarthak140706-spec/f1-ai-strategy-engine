"""
strategy_engine.py

V5 Sprint 2 - Step 2

Purpose:
--------
Orchestrate the complete F1 AI Strategy Engine pipeline.

Pipeline:

    FastF1 Session
          ↓
    Race State
          ↓
    ML Feature Engineering
          ↓
    XGBoost Pit Probability
          ↓
    Strategy Simulation
          ↓
    Decision Engine
          ↓
    Final AI Strategy Decision

This module acts as the main backend entry point
for the F1 AI Strategist.

It does NOT contain ML training logic.
It does NOT contain simulator logic.
It does NOT contain decision-making logic.

It only connects the existing modules together.
"""

from typing import Dict, Any

from src.data_loader import (
    load_session
)

from src.race_state import (
    build_race_state
)

from src.feature_engineering import (
    build_ml_features,
    validate_ml_features
)

from src.predict import (
    predict_pit_probability
)

from src.strategy.simulator import (
    simulate_strategy
)

from src.strategy.decision_engine import (
    get_strategy_decision
)


# ============================================================
# MAIN STRATEGY PIPELINE
# ============================================================

def run_strategy(
    season: int,
    grand_prix: str,
    driver: str,
    session_type: str = "R"
) -> Dict[str, Any]:
    """
    Run the complete F1 AI Strategy Engine pipeline.

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
        Default is "R" for Race.

    Returns
    -------
    dict
        Complete AI strategy result.

    Pipeline
    --------
    1. Load FastF1 session
    2. Build structured race state
    3. Build ML features
    4. Validate ML features
    5. Predict pit probability
    6. Run strategy simulation
    7. Run decision engine
    8. Return complete strategy result
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
        driver,
        str
    ) or not driver.strip():

        raise ValueError(
            "driver must be a valid "
            "non-empty driver abbreviation."
        )

    if not isinstance(
        session_type,
        str
    ) or not session_type.strip():

        raise ValueError(
            "session_type must be a valid "
            "non-empty string."
        )

    driver = driver.upper()

    # ========================================================
    # STEP 1
    # LOAD FASTF1 SESSION
    # ========================================================

    print(
        "\n" + "=" * 60
    )

    print(
        "F1 AI STRATEGY ENGINE"
    )

    print(
        "=" * 60
    )

    print(
        "\n[1/7] Loading FastF1 session..."
    )

    session = load_session(
        season=season,
        grand_prix=grand_prix,
        session_type=session_type
    )

    if session is None:

        raise RuntimeError(

            f"Unable to load FastF1 session: "

            f"{season} - "

            f"{grand_prix} - "

            f"{session_type}"

        )

    print(
        "FastF1 session loaded successfully."
    )

    # ========================================================
    # STEP 2
    # BUILD RACE STATE
    # ========================================================

    print(
        "\n[2/7] Building race state..."
    )

    race_state = build_race_state(
        session=session,
        driver=driver
    )

    if not race_state:

        raise RuntimeError(
            "Race state generation returned empty data."
        )

    print(
        "Race state generated successfully."
    )

    # ========================================================
    # STEP 3
    # BUILD ML FEATURES
    # ========================================================

    print(
        "\n[3/7] Building ML features..."
    )

    ml_features = build_ml_features(
        race_state
    )

    if ml_features.empty:

        raise RuntimeError(
            "ML feature generation returned empty data."
        )

    # ========================================================
    # STEP 4
    # VALIDATE ML FEATURES
    # ========================================================

    print(
        "\n[4/7] Validating ML features..."
    )

    validate_ml_features(
        ml_features
    )

    print(
        "ML features validated successfully."
    )

    # ========================================================
    # STEP 5
    # ML PIT PROBABILITY
    # ========================================================

    print(
        "\n[5/7] Running XGBoost prediction..."
    )

    pit_probability = (
        predict_pit_probability(
            ml_features
        )
    )

    print(
        f"Pit Probability: "
        f"{pit_probability}%"
    )

    # ========================================================
    # STEP 6
    # STRATEGY SIMULATION
    # ========================================================

    print(
        "\n[6/7] Running strategy simulation..."
    )

    tyre_compound = race_state.get(
        "TyreCompound"
    )

    laps_remaining = race_state.get(
        "LapsRemaining"
    )

    predicted_lap_time = race_state.get(
        "RecentPace"
    )

    track = race_state.get(
        "Circuit"
    )

    if track is None:

        track = race_state.get(
            "GrandPrix"
        )

    if tyre_compound is None:

        raise ValueError(
            "Tyre compound is unavailable "
            "in the current race state."
        )

    if laps_remaining is None:

        raise ValueError(
            "Laps remaining is unavailable "
            "in the current race state."
        )

    if predicted_lap_time is None:

        raise ValueError(
            "Recent lap time is unavailable "
            "in the current race state."
        )

    if track is None:

        raise ValueError(
            "Track information is unavailable "
            "in the current race state."
        )

    simulation_result = simulate_strategy(

        track=track,

        driver=driver,

        tyre_compound=tyre_compound,

        predicted_lap_time=predicted_lap_time,

        laps_remaining=laps_remaining

    )

    if not simulation_result:

        raise RuntimeError(
            "Strategy simulation returned empty data."
        )

    print(
        "Strategy simulation completed."
    )

    # ========================================================
    # STEP 7
    # FINAL DECISION ENGINE
    # ========================================================

    print(
        "\n[7/7] Generating final AI strategy decision..."
    )

    decision_result = get_strategy_decision(

        track=track,

        driver=driver,

        tyre_compound=tyre_compound,

        predicted_lap_time=predicted_lap_time,

        laps_remaining=laps_remaining,

        model_data=ml_features

    )

    if not decision_result:

        raise RuntimeError(
            "Decision engine returned empty data."
        )

    print(
        "Final strategy decision generated."
    )

    # ========================================================
    # COMBINE COMPLETE RESULT
    # ========================================================

    result = {

        # ----------------------------------------------------
        # SESSION INFORMATION
        # ----------------------------------------------------

        "season":
            race_state.get(
                "Season"
            ),

        "grand_prix":
            race_state.get(
                "GrandPrix"
            ),

        "circuit":
            race_state.get(
                "Circuit"
            ),

        "session_type":
            race_state.get(
                "SessionType"
            ),

        # ----------------------------------------------------
        # DRIVER INFORMATION
        # ----------------------------------------------------

        "driver":
            race_state.get(
                "Driver"
            ),

        "team":
            race_state.get(
                "Team"
            ),

        "driver_number":
            race_state.get(
                "DriverNumber"
            ),

        # ----------------------------------------------------
        # CURRENT RACE STATE
        # ----------------------------------------------------

        "current_lap":
            race_state.get(
                "CurrentLap"
            ),

        "total_laps":
            race_state.get(
                "TotalLaps"
            ),

        "laps_remaining":
            race_state.get(
                "LapsRemaining"
            ),

        "race_progress":
            race_state.get(
                "RaceProgress"
            ),

        "position":
            race_state.get(
                "Position"
            ),

        # ----------------------------------------------------
        # TYRE STATE
        # ----------------------------------------------------

        "tyre_compound":
            race_state.get(
                "TyreCompound"
            ),

        "tyre_life":
            race_state.get(
                "TyreLife"
            ),

        "current_stint_length":
            race_state.get(
                "CurrentStintLength"
            ),

        "pit_stops_completed":
            race_state.get(
                "PitStopsCompleted"
            ),

        # ----------------------------------------------------
        # PACE
        # ----------------------------------------------------

        "recent_pace":
            race_state.get(
                "RecentPace"
            ),

        "average_pace":
            race_state.get(
                "AveragePace"
            ),

        "avg_pace_last_3":
            race_state.get(
                "AvgPaceLast3"
            ),

        "avg_pace_last_5":
            race_state.get(
                "AvgPaceLast5"
            ),

        "avg_pace_last_10":
            race_state.get(
                "AvgPaceLast10"
            ),

        "degradation_rate":
            race_state.get(
                "DegradationRate"
            ),

        # ----------------------------------------------------
        # ML PREDICTION
        # ----------------------------------------------------

        "pit_probability":
            pit_probability,

        # ----------------------------------------------------
        # STRATEGY SIMULATION
        # ----------------------------------------------------

        "simulation":
            simulation_result,

        # ----------------------------------------------------
        # FINAL DECISION
        # ----------------------------------------------------

        "final_decision":
            decision_result.get(
                "final_decision"
            ),

        "confidence":
            decision_result.get(
                "confidence"
            ),

        "reason":
            decision_result.get(
                "reason"
            ),

        # ----------------------------------------------------
        # COMPLETE DECISION ENGINE OUTPUT
        # ----------------------------------------------------

        "decision_details":
            decision_result,

        # ----------------------------------------------------
        # ML FEATURES
        # ----------------------------------------------------

        "ml_features":
            ml_features

    }

    return result


# ============================================================
# DISPLAY STRATEGY RESULT
# ============================================================

def display_strategy_result(
    result: Dict[str, Any]
) -> None:
    """
    Display the final AI strategy result
    in a readable terminal format.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "F1 AI STRATEGY RECOMMENDATION"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # SESSION
    # --------------------------------------------------------

    print(
        "\nRACE INFORMATION"
    )

    print(
        "-" * 60
    )

    print(
        f"Season: "
        f"{result.get('season')}"
    )

    print(
        f"Grand Prix: "
        f"{result.get('grand_prix')}"
    )

    print(
        f"Circuit: "
        f"{result.get('circuit')}"
    )

    # --------------------------------------------------------
    # DRIVER
    # --------------------------------------------------------

    print(
        "\nDRIVER"
    )

    print(
        "-" * 60
    )

    print(
        f"Driver: "
        f"{result.get('driver')}"
    )

    print(
        f"Team: "
        f"{result.get('team')}"
    )

    print(
        f"Position: "
        f"{result.get('position')}"
    )

    # --------------------------------------------------------
    # RACE STATE
    # --------------------------------------------------------

    print(
        "\nCURRENT RACE STATE"
    )

    print(
        "-" * 60
    )

    print(
        f"Lap: "
        f"{result.get('current_lap')} / "
        f"{result.get('total_laps')}"
    )

    print(
        f"Laps Remaining: "
        f"{result.get('laps_remaining')}"
    )

    print(
        f"Tyre: "
        f"{result.get('tyre_compound')}"
    )

    print(
        f"Tyre Life: "
        f"{result.get('tyre_life')}"
    )

    print(
        f"Pit Stops Completed: "
        f"{result.get('pit_stops_completed')}"
    )

    # --------------------------------------------------------
    # ML
    # --------------------------------------------------------

    print(
        "\nMACHINE LEARNING"
    )

    print(
        "-" * 60
    )

    print(
        f"Pit Probability: "
        f"{result.get('pit_probability')}%"
    )

    # --------------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------------

    print(
        "\nFINAL AI DECISION"
    )

    print(
        "-" * 60
    )

    print(
        f"Decision: "
        f"{result.get('final_decision')}"
    )

    print(
        f"Confidence: "
        f"{result.get('confidence')}"
    )

    print(
        f"Reason: "
        f"{result.get('reason')}"
    )

    print(
        "\n" + "=" * 60
    )


# ============================================================
# END-TO-END TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # TEST CONFIGURATION
    # --------------------------------------------------------

    SEASON = 2025

    GRAND_PRIX = (
        "British Grand Prix"
    )

    DRIVER = "VER"

    SESSION_TYPE = "R"

    # --------------------------------------------------------
    # RUN COMPLETE PIPELINE
    # --------------------------------------------------------

    try:

        result = run_strategy(

            season=SEASON,

            grand_prix=GRAND_PRIX,

            driver=DRIVER,

            session_type=SESSION_TYPE

        )

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        display_strategy_result(
            result
        )

        print(
            "\n✅ END-TO-END STRATEGY PIPELINE TEST PASSED"
        )

    except Exception as e:

        print(
            "\n❌ END-TO-END STRATEGY PIPELINE TEST FAILED"
        )

        print(
            f"Error: {e}"
        )