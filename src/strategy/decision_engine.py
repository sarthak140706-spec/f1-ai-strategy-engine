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

SMALL_SIMULATION_DELTA = 2.0


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

    ml_says_pit = (

        pit_probability
        >= HIGH_PIT_PROBABILITY

    )

    ml_says_stay = (

        pit_probability
        <= LOW_PIT_PROBABILITY

    )

    simulator_says_pit = (

        simulation_recommendation
        == "PIT NOW"

    )

    simulator_says_stay = (

        simulation_recommendation
        == "STAY OUT"

    )

    # ========================================================
    # STRONG AGREEMENT
    # ========================================================

    if (

        ml_says_pit
        and simulator_says_pit
        and simulation_delta
        >= STRONG_SIMULATION_DELTA

    ):

        return "HIGH"

    if (

        ml_says_stay
        and simulator_says_stay
        and simulation_delta
        <= -STRONG_SIMULATION_DELTA

    ):

        return "HIGH"

    # ========================================================
    # MODERATE AGREEMENT
    # ========================================================

    if (

        ml_says_pit
        and simulator_says_pit

    ):

        return "MEDIUM"

    if (

        ml_says_stay
        and simulator_says_stay

    ):

        return "MEDIUM"

    # ========================================================
    # CONFLICTING SIGNALS
    # ========================================================

    if (

        (
            ml_says_pit
            and simulator_says_stay
        )

        or

        (
            ml_says_stay
            and simulator_says_pit
        )

    ):

        return "LOW"

    # ========================================================
    # UNCERTAIN ML SIGNAL
    # ========================================================

    return "LOW"


# ============================================================
# GENERATE DECISION REASON
# ============================================================

def generate_reason(
    pit_probability: float,
    simulation_recommendation: str,
    simulation_delta: float,
    confidence: str
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
            "The ML model strongly favors a pit stop."
        )

    elif pit_probability <= LOW_PIT_PROBABILITY:

        ml_signal = (
            "The ML model strongly favors staying out."
        )

    else:

        ml_signal = (
            "The ML model has an uncertain pit-stop signal."
        )

    # ========================================================
    # SIMULATOR SIGNAL
    # ========================================================

    if simulation_recommendation == "PIT NOW":

        simulator_signal = (

            "The strategy simulator estimates that "
            f"pitting now saves approximately "
            f"{abs(simulation_delta):.2f} seconds."

        )

    else:

        simulator_signal = (

            "The strategy simulator estimates that "
            f"staying out is better by approximately "
            f"{abs(simulation_delta):.2f} seconds."

        )

    # ========================================================
    # FINAL REASON
    # ========================================================

    return (

        f"{ml_signal} "

        f"{simulator_signal} "

        f"Overall confidence is {confidence}."

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
    # STRONG AGREEMENT
    # --------------------------------------------------------

    if (

        pit_probability
        >= HIGH_PIT_PROBABILITY

        and

        simulation_recommendation
        == "PIT NOW"

    ):

        final_decision = (
            "PIT NOW"
        )

    elif (

        pit_probability
        <= LOW_PIT_PROBABILITY

        and

        simulation_recommendation
        == "STAY OUT"

    ):

        final_decision = (
            "STAY OUT"
        )

    # --------------------------------------------------------
    # CONFLICTING SIGNALS
    # --------------------------------------------------------

    elif (

        pit_probability
        >= HIGH_PIT_PROBABILITY

        and

        simulation_recommendation
        == "STAY OUT"

    ):

        # Simulator gets priority because
        # it directly evaluates future race time.

        final_decision = (
            "STAY OUT"
        )

    elif (

        pit_probability
        <= LOW_PIT_PROBABILITY

        and

        simulation_recommendation
        == "PIT NOW"

    ):

        final_decision = (
            "PIT NOW"
        )

    # --------------------------------------------------------
    # UNCERTAIN ML SIGNAL
    # --------------------------------------------------------

    else:

        # In uncertain situations,
        # follow the strategy simulator.

        final_decision = (

            simulation_recommendation

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

            confidence=confidence

        )

    )

    # ========================================================
    # RETURN FINAL RESULT
    # ========================================================

    return {

        # ML output
        "pit_probability":
            pit_probability,

        # Simulator output
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

        # Final AI decision
        "final_decision":
            final_decision,

        "confidence":
            confidence,

        "reason":
            reason

    }