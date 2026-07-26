"""
run_strategy.py

V5 Sprint 2 - Step 3

Purpose:
--------
Run the complete F1 AI Strategy pipeline from a single entry point.

Pipeline:

    FastF1 Session
          ↓
    Race State
          ↓
    ML Features
          ↓
    XGBoost Prediction
          ↓
    Strategy Simulation
          ↓
    Decision Engine
          ↓
    Final AI Recommendation

This module acts as the main backend
orchestrator for the V5 strategy engine.
"""

from typing import Dict, Any


# ============================================================
# IMPORTS
# ============================================================

from src.data_loader import (
    load_session
)

from src.race_state import (
    build_race_state
)

from src.strategy.decision_engine import (
    get_decision_from_race_state
)


# ============================================================
# RUN COMPLETE STRATEGY PIPELINE
# ============================================================

def run_strategy(
    season: int,
    grand_prix: str,
    driver: str,
    session_type: str = "R"
) -> Dict[str, Any]:
    """
    Run the complete F1 AI Strategy pipeline.

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

        R   = Race
        Q   = Qualifying
        FP1 = Free Practice 1
        FP2 = Free Practice 2
        FP3 = Free Practice 3
        SQ  = Sprint Qualifying
        S   = Sprint

    Returns
    -------
    dict
        Complete AI strategy result.
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

    if not grand_prix:

        raise ValueError(
            "grand_prix cannot be empty."
        )

    if not driver:

        raise ValueError(
            "driver cannot be empty."
        )

    if not session_type:

        raise ValueError(
            "session_type cannot be empty."
        )


    driver = str(
        driver
    ).upper()

    session_type = str(
        session_type
    ).upper()


    # ========================================================
    # STEP 1 — LOAD FASTF1 SESSION
    # ========================================================

    print(
        "\n[1/4] Loading FastF1 session..."
    )

    session = load_session(

        season,

        grand_prix,

        session_type

    )


    if session is None:

        raise RuntimeError(

            "Failed to load FastF1 session.\n"

            f"Season: {season}\n"

            f"Grand Prix: {grand_prix}\n"

            f"Session: {session_type}"

        )


    print(
        "FastF1 session loaded successfully."
    )


    # ========================================================
    # STEP 2 — BUILD RACE STATE
    # ========================================================

    print(
        "\n[2/4] Building race state..."
    )

    race_state = build_race_state(

        session,

        driver

    )


    if not race_state:

        raise RuntimeError(

            "Race state generation returned empty data."

        )


    print(
        "Race state generated successfully."
    )


    # ========================================================
    # STEP 3 — RUN DECISION ENGINE
    # ========================================================

    print(
        "\n[3/4] Running AI strategy engine..."
    )

    decision = get_decision_from_race_state(

        race_state

    )


    if not decision:

        raise RuntimeError(

            "Decision engine returned empty result."

        )


    print(
        "AI strategy decision generated successfully."
    )


    # ========================================================
    # STEP 4 — BUILD FINAL RESULT
    # ========================================================

    print(
        "\n[4/4] Building final strategy result..."
    )


    result = {

        # ----------------------------------------------------
        # REQUEST INFORMATION
        # ----------------------------------------------------

        "request": {

            "season":
                season,

            "grand_prix":
                grand_prix,

            "session_type":
                session_type,

            "driver":
                driver

        },


        # ----------------------------------------------------
        # RACE STATE
        # ----------------------------------------------------

        "race_state":
            race_state,


        # ----------------------------------------------------
        # FINAL DECISION
        # ----------------------------------------------------

        "decision":
            decision

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
    in a readable format.
    """

    if not isinstance(
        result,
        dict
    ):

        raise TypeError(
            "result must be a dictionary."
        )


    decision = result.get(
        "decision",
        {}
    )


    race_state = result.get(
        "race_state",
        {}
    )


    # ========================================================
    # HEADER
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "🏎️ F1 AI STRATEGIST — FINAL RACE STRATEGY"
    )

    print(
        "=" * 70
    )


    # ========================================================
    # RACE INFORMATION
    # ========================================================

    print(
        "\nRACE INFORMATION"
    )

    print(
        "-" * 70
    )

    print(
        f"Season: "
        f"{race_state.get('Season')}"
    )

    print(
        f"Grand Prix: "
        f"{race_state.get('GrandPrix')}"
    )

    print(
        f"Circuit: "
        f"{race_state.get('Circuit')}"
    )

    print(
        f"Session: "
        f"{race_state.get('SessionType')}"
    )


    # ========================================================
    # DRIVER INFORMATION
    # ========================================================

    print(
        "\nDRIVER"
    )

    print(
        "-" * 70
    )

    print(
        f"Driver: "
        f"{race_state.get('Driver')}"
    )

    print(
        f"Team: "
        f"{race_state.get('Team')}"
    )

    print(
        f"Position: "
        f"{race_state.get('Position')}"
    )


    # ========================================================
    # CURRENT RACE STATE
    # ========================================================

    print(
        "\nCURRENT RACE STATE"
    )

    print(
        "-" * 70
    )

    print(
        f"Current Lap: "
        f"{race_state.get('CurrentLap')}"
    )

    print(
        f"Laps Remaining: "
        f"{race_state.get('LapsRemaining')}"
    )

    print(
        f"Race Progress: "
        f"{race_state.get('RaceProgress')}"
    )

    print(
        f"Tyre Compound: "
        f"{race_state.get('TyreCompound')}"
    )

    print(
        f"Tyre Life: "
        f"{race_state.get('TyreLife')}"
    )

    print(
        f"Current Stint Length: "
        f"{race_state.get('CurrentStintLength')}"
    )

    print(
        f"Pit Stops Completed: "
        f"{race_state.get('PitStopsCompleted')}"
    )


    # ========================================================
    # PERFORMANCE
    # ========================================================

    print(
        "\nPERFORMANCE"
    )

    print(
        "-" * 70
    )

    print(
        f"Recent Pace: "
        f"{race_state.get('RecentPace')}"
    )

    print(
        f"Average Pace: "
        f"{race_state.get('AveragePace')}"
    )

    print(
        f"Average Pace Last 3: "
        f"{race_state.get('AvgPaceLast3')}"
    )

    print(
        f"Average Pace Last 5: "
        f"{race_state.get('AvgPaceLast5')}"
    )

    print(
        f"Average Pace Last 10: "
        f"{race_state.get('AvgPaceLast10')}"
    )

    print(
        f"Degradation Rate: "
        f"{race_state.get('DegradationRate')}"
    )


    # ========================================================
    # AI STRATEGY
    # ========================================================

    print(
        "\nAI STRATEGY"
    )

    print(
        "-" * 70
    )

    print(
        f"Pit Probability: "
        f"{decision.get('pit_probability')}%"
    )

    print(
        f"Simulator Recommendation: "
        f"{decision.get('simulator_recommendation')}"
    )

    print(
        f"Final Decision: "
        f"{decision.get('final_decision')}"
    )

    print(
        f"Confidence: "
        f"{decision.get('confidence')}"
    )


    # ========================================================
    # STRATEGY TIMING
    # ========================================================

    print(
        "\nSTRATEGY SIMULATION"
    )

    print(
        "-" * 70
    )

    print(
        f"Stay Out Time: "
        f"{decision.get('stay_out_time')}"
    )

    print(
        f"Pit Now Time: "
        f"{decision.get('pit_now_time')}"
    )

    print(
        f"Delta: "
        f"{decision.get('delta')}"
    )


    # ========================================================
    # EXPLANATION
    # ========================================================

    print(
        "\nAI REASON"
    )

    print(
        "-" * 70
    )

    print(
        decision.get(
            "reason"
        )
    )


    # ========================================================
    # FOOTER
    # ========================================================

    print(
        "\n"
        + "=" * 70
    )

    print(
        "✅ COMPLETE STRATEGY PIPELINE EXECUTED SUCCESSFULLY"
    )

    print(
        "=" * 70
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

    DRIVER = "VER"


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    print(
        "=" * 70
    )

    print(
        "V5 SPRINT 2 - STEP 3"
    )

    print(
        "END-TO-END STRATEGY PIPELINE TEST"
    )

    print(
        "=" * 70
    )


    # --------------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------------

    result = run_strategy(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        driver=DRIVER,

        session_type=SESSION_TYPE

    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    display_strategy_result(

        result

    )


    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    print(
        "\n"
        "✅ STEP 3 TEST PASSED"
    )