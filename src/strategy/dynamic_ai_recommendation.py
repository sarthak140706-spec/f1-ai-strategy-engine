"""
dynamic_ai_recommendation.py

PHASE 4.7 — DYNAMIC AI RECOMMENDATION

Purpose
-------
Convert the complete dynamic strategy pipeline into a final,
human-readable AI race strategy recommendation.

The recommendation uses:

    Phase 4.1 — Dynamic Race State
    Phase 4.2 — Dynamic Race Situation
    Phase 4.3 — Dynamic Tyre Strategy
    Phase 4.4 — Dynamic Pit Decision
    Phase 4.5 — Dynamic Strategy Simulation
    Phase 4.6 — Dynamic Strategy Scoring

Pipeline
--------

Dynamic Race State
        ↓
Dynamic Race Situation
        ↓
Dynamic Tyre Strategy
        ↓
Dynamic Pit Decision
        ↓
Dynamic Strategy Simulation
        ↓
Dynamic Strategy Scoring
        ↓
Final Dynamic AI Recommendation
"""

from typing import Dict, Any, List


# ============================================================
# HELPERS
# ============================================================

def _normalize_text(
    value
) -> str:
    """
    Normalize text for internal comparisons.
    """

    if value is None:

        return ""

    return (
        str(value)
        .strip()
        .upper()
        .replace("_", " ")
    )


def _safe_float(
    value,
    default: float = 0.0
) -> float:
    """
    Safely convert a value to float.
    """

    try:

        return float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_dynamic_recommendation_inputs(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any],
    tyre_strategy: Dict[str, Any],
    pit_decision: Dict[str, Any],
    simulation_result: Dict[str, Any],
    scoring_result: Dict[str, Any]
) -> None:
    """
    Validate Phase 4.7 inputs.
    """

    if not race_state:

        raise ValueError(
            "race_state cannot be empty."
        )


    if not race_situation:

        raise ValueError(
            "race_situation cannot be empty."
        )


    if not tyre_strategy:

        raise ValueError(
            "tyre_strategy cannot be empty."
        )


    if not pit_decision:

        raise ValueError(
            "pit_decision cannot be empty."
        )


    if not simulation_result:

        raise ValueError(
            "simulation_result cannot be empty."
        )


    if not scoring_result:

        raise ValueError(
            "scoring_result cannot be empty."
        )


    best_strategy = scoring_result.get(
        "best_strategy"
    )


    if not best_strategy:

        raise ValueError(
            "Dynamic scoring does not contain "
            "a best strategy."
        )


# ============================================================
# GET SECOND-BEST STRATEGY
# ============================================================

def get_second_best_strategy(
    strategies: List[Dict[str, Any]]
):
    """
    Return the second-ranked dynamic strategy.
    """

    if not strategies:

        return None


    ranked = sorted(

        strategies,

        key=lambda strategy:
            strategy.get(
                "dynamic_score_rank",
                999
            )

    )


    if len(ranked) < 2:

        return None


    return ranked[1]


# ============================================================
# EXPECTED ADVANTAGE
# ============================================================

def calculate_expected_advantage(
    best_strategy: Dict[str, Any],
    second_strategy: Dict[str, Any] | None
) -> float:
    """
    Calculate the projected time advantage of the
    selected strategy over the second-best strategy.

    This uses projected race time rather than score
    difference so that the result is understandable
    in seconds.
    """

    if second_strategy is None:

        return 0.0


    best_time = _safe_float(

        best_strategy.get(
            "projected_total_time"
        )

    )


    second_time = _safe_float(

        second_strategy.get(
            "projected_total_time"
        )

    )


    advantage = (
        second_time
        -
        best_time
    )


    return round(
        advantage,
        3
    )


# ============================================================
# CONFIDENCE
# ============================================================

def calculate_dynamic_confidence(
    best_strategy: Dict[str, Any],
    second_strategy: Dict[str, Any] | None,
    pit_decision: Dict[str, Any],
    tyre_strategy: Dict[str, Any]
) -> float:
    """
    Calculate final Phase 4.7 recommendation confidence.

    Confidence combines:

        Dynamic strategy score
        Pit-decision confidence
        Tyre-strategy confidence
        Separation from next-best dynamic score
    """

    best_score = _safe_float(

        best_strategy.get(
            "dynamic_overall_score"
        )

    )


    pit_confidence = _safe_float(

        pit_decision.get(
            "confidence"
        ),

        80.0

    )


    tyre_confidence = _safe_float(

        tyre_strategy.get(
            "Confidence"
        )

        or

        tyre_strategy.get(
            "confidence"
        ),

        80.0

    )


    score_gap = 0.0


    if second_strategy:

        second_score = _safe_float(

            second_strategy.get(
                "dynamic_overall_score"
            )

        )


        score_gap = max(

            0.0,

            best_score
            -
            second_score

        )


    # Convert score separation into a confidence contribution

    separation_confidence = min(

        100.0,

        70.0
        +
        (
            score_gap
            * 1.5
        )

    )


    confidence = (

        best_score
        * 0.40

        +

        pit_confidence
        * 0.25

        +

        tyre_confidence
        * 0.20

        +

        separation_confidence
        * 0.15

    )


    return round(

        max(
            0.0,
            min(
                99.0,
                confidence
            )
        ),

        1

    )


# ============================================================
# DETERMINE FINAL ACTION
# ============================================================

def determine_recommendation_action(
    best_strategy: Dict[str, Any]
) -> str:
    """
    Convert the best strategy into a human-readable
    recommendation.
    """

    strategy = _normalize_text(

        best_strategy.get(
            "strategy"
        )

    )


    if strategy == "STAY OUT":

        return "STAY OUT"


    if strategy == "PIT":

        return "PIT NOW"


    return strategy or "UNKNOWN"


# ============================================================
# RECOMMENDED TYRE
# ============================================================

def determine_recommended_tyre(
    best_strategy: Dict[str, Any],
    race_state: Dict[str, Any]
) -> str:
    """
    Determine final recommended tyre.
    """

    tyre = (

        best_strategy.get(
            "final_tyre"
        )

        or

        best_strategy.get(
            "starting_tyre"
        )

    )


    if tyre:

        return str(
            tyre
        ).upper()


    return str(

        race_state.get(
            "TyreCompound",
            "UNKNOWN"
        )

    ).upper()


# ============================================================
# REASON GENERATION
# ============================================================

def generate_dynamic_reason(
    action: str,
    recommended_tyre: str,
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any],
    pit_decision: Dict[str, Any],
    best_strategy: Dict[str, Any],
    expected_advantage: float
) -> str:
    """
    Generate the final human-readable strategic explanation.
    """

    current_lap = race_state.get(
        "CurrentLap"
    )


    total_laps = race_state.get(
        "TotalLaps"
    )


    remaining_laps = race_state.get(
        "LapsRemaining"
    )


    position = race_state.get(
        "Position"
    )


    current_tyre = race_state.get(
        "TyreCompound"
    )


    tyre_age = race_state.get(
        "TyreLife"
    )


    race_state_name = (

        race_situation.get(
            "race_situation"
        )

        or

        race_situation.get(
            "RaceSituation"
        )

        or

        "UNKNOWN"

    )


    tyre_status = (

        race_situation.get(
            "tyre_status"
        )

        or

        "UNKNOWN"

    )


    pit_urgency = (

        race_situation.get(
            "pit_urgency"
        )

        or

        "UNKNOWN"

    )


    dynamic_score = _safe_float(

        best_strategy.get(
            "dynamic_overall_score"
        )

    )


    # ========================================================
    # STAY OUT
    # ========================================================

    if action == "STAY OUT":

        return (

            f"Stay out on the current {current_tyre} tyres. "
            f"At lap {current_lap}/{total_laps}, the driver is running "
            f"P{position} with {remaining_laps} laps remaining and the "
            f"current tyre age is {tyre_age} laps. "
            f"The race situation is classified as {race_state_name} "
            f"with tyre condition {tyre_status} and pit urgency "
            f"{pit_urgency}. "
            f"The current strategy achieved the highest dynamic score "
            f"of {dynamic_score:.2f}. "
            f"It is projected to hold an advantage of "
            f"{expected_advantage:.3f} seconds over the next-best "
            f"available strategy."
        )


    # ========================================================
    # PIT
    # ========================================================

    pit_loss = _safe_float(

        pit_decision.get(
            "pit_loss"
        )

    )


    return (

        f"Pit now and switch to {recommended_tyre}. "
        f"At lap {current_lap}/{total_laps}, the driver is running "
        f"P{position} with {remaining_laps} laps remaining. "
        f"The current {current_tyre} tyres are {tyre_age} laps old. "
        f"The race situation is classified as {race_state_name}, "
        f"with tyre condition {tyre_status} and pit urgency "
        f"{pit_urgency}. "
        f"Despite an estimated pit-stop loss of {pit_loss:.2f} seconds, "
        f"the {recommended_tyre} strategy achieved the highest dynamic "
        f"score of {dynamic_score:.2f}. "
        f"It is projected to provide an advantage of "
        f"{expected_advantage:.3f} seconds over the next-best strategy."
    )


# ============================================================
# COMPLETE DYNAMIC AI RECOMMENDATION
# ============================================================

def generate_dynamic_ai_recommendation(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any],
    tyre_strategy: Dict[str, Any],
    pit_decision: Dict[str, Any],
    simulation_result: Dict[str, Any],
    scoring_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run Phase 4.7 dynamic AI recommendation generation.
    """

    validate_dynamic_recommendation_inputs(

        race_state=race_state,

        race_situation=race_situation,

        tyre_strategy=tyre_strategy,

        pit_decision=pit_decision,

        simulation_result=simulation_result,

        scoring_result=scoring_result

    )


    strategies = scoring_result.get(
        "strategies",
        []
    )


    best_strategy = scoring_result.get(
        "best_strategy"
    )


    second_strategy = get_second_best_strategy(
        strategies
    )


    action = determine_recommendation_action(
        best_strategy
    )


    recommended_tyre = determine_recommended_tyre(

        best_strategy=best_strategy,

        race_state=race_state

    )


    expected_advantage = (
        calculate_expected_advantage(

            best_strategy=best_strategy,

            second_strategy=second_strategy

        )
    )


    confidence = calculate_dynamic_confidence(

        best_strategy=best_strategy,

        second_strategy=second_strategy,

        pit_decision=pit_decision,

        tyre_strategy=tyre_strategy

    )


    reason = generate_dynamic_reason(

        action=action,

        recommended_tyre=recommended_tyre,

        race_state=race_state,

        race_situation=race_situation,

        pit_decision=pit_decision,

        best_strategy=best_strategy,

        expected_advantage=expected_advantage

    )


    return {

        # ----------------------------------------------------
        # PHASE INFORMATION
        # ----------------------------------------------------

        "dynamic_recommendation":
            True,


        # ----------------------------------------------------
        # RACE CONTEXT
        # ----------------------------------------------------

        "driver":
            race_state.get(
                "Driver"
            ),

        "current_lap":
            race_state.get(
                "CurrentLap"
            ),

        "total_laps":
            race_state.get(
                "TotalLaps"
            ),

        "remaining_laps":
            race_state.get(
                "LapsRemaining"
            ),

        "position":
            race_state.get(
                "Position"
            ),

        "current_tyre":
            race_state.get(
                "TyreCompound"
            ),

        "tyre_age":
            race_state.get(
                "TyreLife"
            ),


        # ----------------------------------------------------
        # FINAL RECOMMENDATION
        # ----------------------------------------------------

        "recommendation":
            action,

        "recommended_tyre":
            recommended_tyre,

        "strategy_type":
            best_strategy.get(
                "strategy"
            ),

        "tyre_plan":
            best_strategy.get(
                "tyre_plan"
            ),


        # ----------------------------------------------------
        # STRATEGY PERFORMANCE
        # ----------------------------------------------------

        "dynamic_score":
            best_strategy.get(
                "dynamic_overall_score"
            ),

        "base_score":
            best_strategy.get(
                "base_overall_score"
            ),

        "strategy_rank":
            best_strategy.get(
                "dynamic_score_rank"
            ),

        "projected_total_time":
            best_strategy.get(
                "projected_total_time"
            ),

        "expected_advantage_seconds":
            expected_advantage,

        "confidence":
            confidence,


        # ----------------------------------------------------
        # STRATEGIC CONTEXT
        # ----------------------------------------------------

        "race_situation":
            (

                race_situation.get(
                    "race_situation"
                )

                or

                race_situation.get(
                    "RaceSituation"
                )

            ),

        "pit_decision":
            (

                pit_decision.get(
                    "decision"
                )

                or

                pit_decision.get(
                    "action"
                )

            ),


        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        "reason":
            reason,


        # ----------------------------------------------------
        # SELECTED STRATEGY
        # ----------------------------------------------------

        "selected_strategy":
            best_strategy,


        # ----------------------------------------------------
        # STRATEGY COMPARISON
        # ----------------------------------------------------

        "strategy_comparison":
            strategies

    }


# ============================================================
# DISPLAY
# ============================================================

def display_dynamic_ai_recommendation(
    recommendation: Dict[str, Any]
) -> None:
    """
    Display final Phase 4.7 AI recommendation.
    """

    print(
        "\n" + "=" * 72
    )

    print(
        "PHASE 4.7 — DYNAMIC AI RECOMMENDATION"
    )

    print(
        "=" * 72
    )


    print(
        f"Driver: "
        f"{recommendation.get('driver')}"
    )


    print(
        f"Current Lap: "
        f"{recommendation.get('current_lap')}"
        f"/"
        f"{recommendation.get('total_laps')}"
    )


    print(
        f"Position: P"
        f"{recommendation.get('position')}"
    )


    print(
        f"Current Tyre: "
        f"{recommendation.get('current_tyre')}"
    )


    print(
        "-" * 72
    )


    print(
        f"AI Recommendation: "
        f"{recommendation.get('recommendation')}"
    )


    print(
        f"Recommended Tyre: "
        f"{recommendation.get('recommended_tyre')}"
    )


    print(
        f"Tyre Plan: "
        f"{recommendation.get('tyre_plan')}"
    )


    print(
        f"Dynamic Score: "
        f"{recommendation.get('dynamic_score')}"
    )


    print(
        f"Strategy Rank: "
        f"{recommendation.get('strategy_rank')}"
    )


    print(
        f"Projected Time: "
        f"{recommendation.get('projected_total_time')}s"
    )


    print(
        f"Expected Advantage: "
        f"{recommendation.get('expected_advantage_seconds')}s"
    )


    print(
        f"Confidence: "
        f"{recommendation.get('confidence')}%"
    )


    print(
        f"Race Situation: "
        f"{recommendation.get('race_situation')}"
    )


    print(
        "-" * 72
    )


    print(
        "AI REASONING"
    )


    print(
        "-" * 72
    )


    print(
        recommendation.get(
            "reason",
            "--"
        )
    )


    print(
        "=" * 72
    )