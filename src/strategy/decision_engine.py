from typing import Dict, Any

from src.predict import (
    predict_pit_probability
)

from src.strategy.simulator import (
    simulate_strategy
)


# ============================================================
# CONFIGURATION
# ============================================================

HIGH_PIT_PROBABILITY = 70.0

LOW_PIT_PROBABILITY = 30.0

STRONG_SIMULATION_DELTA = 5.0


# ============================================================
# CALCULATE ML RECOMMENDATION
# ============================================================

def get_ml_recommendation(
    pit_probability: float
) -> str:
    """
    Convert ML pit probability into a raw ML recommendation.

    Returns
    -------
    str
        PIT NOW, STAY OUT, or UNCERTAIN
    """

    if pit_probability >= HIGH_PIT_PROBABILITY:

        return "PIT NOW"

    if pit_probability <= LOW_PIT_PROBABILITY:

        return "STAY OUT"

    return "UNCERTAIN"


# ============================================================
# CALCULATE CONFIDENCE
# ============================================================

def calculate_confidence(
    pit_probability: float,
    simulation_recommendation: str,
    simulation_delta: float
) -> str:
    """
    Calculate confidence by combining:

    1. ML pit probability
    2. Strategy simulator recommendation
    3. Simulation time advantage

    Returns
    -------
    str
        HIGH, MEDIUM, or LOW
    """

    ml_recommendation = get_ml_recommendation(
        pit_probability
    )

    # ========================================================
    # STRONG AGREEMENT
    # ========================================================

    if (

        ml_recommendation == "PIT NOW"

        and

        simulation_recommendation == "PIT NOW"

        and

        simulation_delta >= STRONG_SIMULATION_DELTA

    ):

        return "HIGH"


    if (

        ml_recommendation == "STAY OUT"

        and

        simulation_recommendation == "STAY OUT"

        and

        simulation_delta <= -STRONG_SIMULATION_DELTA

    ):

        return "HIGH"


    # ========================================================
    # MODERATE AGREEMENT
    # ========================================================

    if (

        ml_recommendation == "PIT NOW"

        and

        simulation_recommendation == "PIT NOW"

    ):

        return "MEDIUM"


    if (

        ml_recommendation == "STAY OUT"

        and

        simulation_recommendation == "STAY OUT"

    ):

        return "MEDIUM"


    # ========================================================
    # UNCERTAIN OR CONFLICTING SIGNALS
    # ========================================================

    return "LOW"


# ============================================================
# GENERATE DECISION REASON
# ============================================================

def generate_reason(
    pit_probability: float,
    simulation_recommendation: str,
    simulation_delta: float,
    final_decision: str,
    confidence: str,
    decision_source: str
) -> str:
    """
    Generate a human-readable explanation
    for the final strategy decision.
    """

    # ========================================================
    # ML SIGNAL
    # ========================================================

    if pit_probability >= HIGH_PIT_PROBABILITY:

        ml_signal = (
            f"The ML model strongly favors pitting now "
            f"with a {pit_probability:.2f}% pit probability."
        )

    elif pit_probability <= LOW_PIT_PROBABILITY:

        ml_signal = (
            f"The ML model strongly favors staying out "
            f"with a {pit_probability:.2f}% pit probability."
        )

    else:

        ml_signal = (
            f"The ML model gives a {pit_probability:.2f}% "
            f"pit probability, indicating an uncertain signal."
        )


    # ========================================================
    # SIMULATOR SIGNAL
    # ========================================================

    if simulation_recommendation == "PIT NOW":

        simulator_signal = (

            "The strategy simulator estimates that "
            f"pitting now provides a {abs(simulation_delta):.2f} "
            "second advantage over staying out."

        )

    else:

        simulator_signal = (

            "The strategy simulator estimates that "
            f"staying out provides a {abs(simulation_delta):.2f} "
            "second advantage over pitting now."

        )


    # ========================================================
    # FINAL DECISION SIGNAL
    # ========================================================

    decision_signal = (

        f"The final recommendation is {final_decision}. "

        f"The decision was primarily based on the "
        f"{decision_source}. "

        f"Overall confidence is {confidence}."

    )


    # ========================================================
    # COMBINE REASON
    # ========================================================

    return (

        f"{ml_signal} "

        f"{simulator_signal} "

        f"{decision_signal}"

    )


# ============================================================
# GET STRATEGY DECISION
# ============================================================

def get_strategy_decision(
    track: str,
    driver: str,
    tyre_compound: str,
    predicted_lap_time: float,
    laps_remaining: int,
    model_data
) -> Dict[str, Any]:
    """
    Combine the XGBoost ML prediction and
    strategy simulation into one final decision.

    Pipeline:

        Model Features
              ↓
        XGBoost Prediction
              ↓
        Pit Probability

        +

        Race Parameters
              ↓
        Strategy Simulator
              ↓
        PIT NOW / STAY OUT

              ↓
        Decision Engine
              ↓
        Final Recommendation
    """

    # ========================================================
    # ML PREDICTION
    # ========================================================

    pit_probability = (

        predict_pit_probability(
            model_data
        )

    )


    # ========================================================
    # ML RECOMMENDATION
    # ========================================================

    ml_recommendation = (

        get_ml_recommendation(
            pit_probability
        )

    )


    # ========================================================
    # SIMULATE STRATEGY
    # ========================================================

    simulation_result = (

        simulate_strategy(

            track=track,

            driver=driver,

            tyre_compound=tyre_compound,

            predicted_lap_time=predicted_lap_time,

            laps_remaining=laps_remaining

        )

    )


    # ========================================================
    # EXTRACT SIMULATION RESULTS
    # ========================================================

    simulation_delta = (

        simulation_result[
            "delta"
        ]

    )

    simulation_recommendation = (

        simulation_result[
            "recommendation"
        ]

    )


    # ========================================================
    # DETERMINE FINAL DECISION
    # ========================================================

    # --------------------------------------------------------
    # CASE 1: ML AND SIMULATOR AGREE
    # --------------------------------------------------------

    if (

        ml_recommendation != "UNCERTAIN"

        and

        ml_recommendation
        == simulation_recommendation

    ):

        final_decision = (

            ml_recommendation

        )

        decision_source = (

            "ML model and strategy simulator agreement"

        )


    # --------------------------------------------------------
    # CASE 2: ML IS UNCERTAIN
    # --------------------------------------------------------

    elif ml_recommendation == "UNCERTAIN":

        final_decision = (

            simulation_recommendation

        )

        decision_source = (

            "strategy simulator because the ML signal "
            "is uncertain"

        )


    # --------------------------------------------------------
    # CASE 3: ML AND SIMULATOR CONFLICT
    # --------------------------------------------------------

    else:

        # The simulator evaluates the expected total
        # race time for the remaining laps.
        #
        # Therefore, when ML and simulator disagree,
        # the simulator gets priority.

        final_decision = (

            simulation_recommendation

        )

        decision_source = (

            "strategy simulator because the ML model "
            "and simulator produced conflicting signals"

        )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = (

        calculate_confidence(

            pit_probability=pit_probability,

            simulation_recommendation=(

                simulation_recommendation

            ),

            simulation_delta=(

                simulation_delta

            )

        )

    )


    # ========================================================
    # REASON
    # ========================================================

    reason = (

        generate_reason(

            pit_probability=pit_probability,

            simulation_recommendation=(

                simulation_recommendation

            ),

            simulation_delta=(

                simulation_delta

            ),

            final_decision=(

                final_decision

            ),

            confidence=(

                confidence

            ),

            decision_source=(

                decision_source

            )

        )

    )


    # ========================================================
    # RETURN FINAL RESULT
    # ========================================================

    return {

        # ----------------------------------------------------
        # ML OUTPUT
        # ----------------------------------------------------

        "pit_probability":

            pit_probability,


        "ml_recommendation":

            ml_recommendation,


        # ----------------------------------------------------
        # SIMULATOR OUTPUT
        # ----------------------------------------------------

        "stay_out_time":

            simulation_result[
                "stay_out_time"
            ],


        "pit_now_time":

            simulation_result[
                "pit_now_time"
            ],


        "delta":

            simulation_delta,


        "simulator_recommendation":

            simulation_recommendation,


        # ----------------------------------------------------
        # FINAL AI DECISION
        # ----------------------------------------------------

        "final_decision":

            final_decision,


        "decision_source":

            decision_source,


        "confidence":

            confidence,


        "reason":

            reason

    }

# ============================================================
# V5 DYNAMIC RACE STATE DECISION
# ============================================================

def get_decision_from_race_state(
    race_state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate the complete final AI strategy decision
    directly from a dynamically generated race state.

    Pipeline:

        FastF1 Session
              ↓
        Race State
              ↓
        ML Features
              ↓
        XGBoost Pit Probability
              ↓
        Strategy Simulation
              ↓
        Decision Engine
              ↓
        Final AI Recommendation

    Parameters
    ----------
    race_state : dict
        Structured race state generated by race_state.py.

    Returns
    -------
    dict
        Complete final AI strategy decision.
    """

    # ========================================================
    # VALIDATE INPUT
    # ========================================================

    if not isinstance(
        race_state,
        dict
    ):

        raise TypeError(
            "race_state must be a dictionary."
        )

    # ========================================================
    # REQUIRED RACE STATE VALUES
    # ========================================================

    required_fields = [

        "Driver",

        "Circuit",

        "TyreCompound",

        "RecentPace",

        "LapsRemaining"

    ]

    missing_fields = [

        field

        for field in required_fields

        if race_state.get(field) is None

    ]

    if missing_fields:

        raise ValueError(

            "Missing required race-state fields: "

            + ", ".join(
                missing_fields
            )

        )

    # ========================================================
    # BUILD ML FEATURES
    # ========================================================

    from src.feature_engineering import (

        build_ml_features,

        validate_ml_features

    )

    model_data = build_ml_features(
        race_state
    )

    # ========================================================
    # VALIDATE ML FEATURES
    # ========================================================

    validate_ml_features(
        model_data
    )

    # ========================================================
    # EXTRACT RACE PARAMETERS
    # ========================================================

    track = race_state[
        "Circuit"
    ]

    driver = race_state[
        "Driver"
    ]

    tyre_compound = race_state[
        "TyreCompound"
    ]

    predicted_lap_time = race_state[
        "RecentPace"
    ]

    laps_remaining = race_state[
        "LapsRemaining"
    ]

    # ========================================================
    # RUN FINAL DECISION ENGINE
    # ========================================================

    decision = get_strategy_decision(

        track=track,

        driver=driver,

        tyre_compound=tyre_compound,

        predicted_lap_time=predicted_lap_time,

        laps_remaining=laps_remaining,

        model_data=model_data

    )

    # ========================================================
    # ADD RACE STATE INFORMATION
    # ========================================================

    result = {

        # ----------------------------------------------------
        # Session
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
        # Driver
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
        # Current Race State
        # ----------------------------------------------------

        "current_lap":
            race_state.get(
                "CurrentLap"
            ),

        "position":
            race_state.get(
                "Position"
            ),

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

        "laps_remaining":
            race_state.get(
                "LapsRemaining"
            ),

        "race_progress":
            race_state.get(
                "RaceProgress"
            ),

        # ----------------------------------------------------
        # Pace
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

        # ----------------------------------------------------
        # Degradation
        # ----------------------------------------------------

        "degradation_rate":
            race_state.get(
                "DegradationRate"
            ),

        # ----------------------------------------------------
        # ML + Simulation + Final Decision
        # ----------------------------------------------------

        "pit_probability":
            decision.get(
                "pit_probability"
            ),

        "stay_out_time":
            decision.get(
                "stay_out_time"
            ),

        "pit_now_time":
            decision.get(
                "pit_now_time"
            ),

        "delta":
            decision.get(
                "delta"
            ),

        "simulator_recommendation":
            decision.get(
                "simulator_recommendation"
            ),

        "final_decision":
            decision.get(
                "final_decision"
            ),

        "confidence":
            decision.get(
                "confidence"
            ),

        "reason":
            decision.get(
                "reason"
            ),

        # ----------------------------------------------------
        # ML Features
        # ----------------------------------------------------

        "model_features":
            model_data

    }

    return result

# ============================================================
# V5 DYNAMIC DECISION ENGINE TEST
# ============================================================

if __name__ == "__main__":

    from src.data_loader import (
        load_session
    )

    from src.race_state import (
        build_race_state
    )


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
        "V5 SPRINT 2 - DYNAMIC DECISION ENGINE TEST"
    )

    print(
        "=" * 70
    )


    # --------------------------------------------------------
    # LOAD SESSION
    # --------------------------------------------------------

    print(
        "\n[1/4] Loading FastF1 session..."
    )

    session = load_session(

        SEASON,

        GRAND_PRIX,

        SESSION_TYPE

    )

    if session is None:

        raise RuntimeError(

            "Failed to load FastF1 session."

        )

    print(
        "Session loaded successfully."
    )


    # --------------------------------------------------------
    # BUILD RACE STATE
    # --------------------------------------------------------

    print(
        "\n[2/4] Building race state..."
    )

    race_state = build_race_state(

        session,

        DRIVER

    )

    print(
        "Race state generated successfully."
    )


    # --------------------------------------------------------
    # RUN DECISION ENGINE
    # --------------------------------------------------------

    print(
        "\n[3/4] Running final AI decision engine..."
    )

    result = get_decision_from_race_state(

        race_state

    )

    print(
        "Decision engine executed successfully."
    )


    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    print(
        "\n[4/4] FINAL AI STRATEGY RESULT"
    )

    print(
        "=" * 70
    )

    print(
        f"Grand Prix: "
        f"{result['grand_prix']}"
    )

    print(
        f"Driver: "
        f"{result['driver']}"
    )

    print(
        f"Team: "
        f"{result['team']}"
    )

    print(
        f"Current Lap: "
        f"{result['current_lap']}"
    )

    print(
        f"Position: "
        f"{result['position']}"
    )

    print(
        f"Tyre: "
        f"{result['tyre_compound']}"
    )

    print(
        f"Tyre Life: "
        f"{result['tyre_life']}"
    )

    print(
        f"Laps Remaining: "
        f"{result['laps_remaining']}"
    )

    print(
        f"Pit Probability: "
        f"{result['pit_probability']}%"
    )

    print(
        f"Simulator Recommendation: "
        f"{result['simulator_recommendation']}"
    )

    print(
        f"Final Decision: "
        f"{result['final_decision']}"
    )

    print(
        f"Confidence: "
        f"{result['confidence']}"
    )

    print(
        f"\nReason:"
    )

    print(
        result["reason"]
    )

    print(
        "=" * 70
    )

    print(
        "\n✅ V5 DYNAMIC DECISION ENGINE TEST PASSED"
    )