"""
ai_recommendation.py

PHASE 3.7 — AI RECOMMENDATION

Purpose
-------
Convert the outputs of the Phase 3 strategy pipeline into
a final human-readable AI strategy recommendation.

Pipeline:

    Race Situation
          +
    Tyre Strategy
          +
    Pit Decision
          +
    Strategy Simulation
          +
    Strategy Scoring
          ↓
    AI Recommendation

This module does NOT:
    - perform tyre simulation
    - calculate pit-stop probability
    - simulate strategies
    - calculate strategy scores
    - expose Flask routes
    - handle frontend rendering

It only combines the strategic information and produces
the final recommendation.
"""

from typing import Dict, Any, Optional


# ============================================================
# CONFIDENCE CONFIGURATION
# ============================================================

MIN_CONFIDENCE = 50.0

MAX_CONFIDENCE = 99.0


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_strategy_input(
    scoring_result: Dict[str, Any]
) -> None:
    """
    Validate the strategy-scoring result.
    """

    if not isinstance(
        scoring_result,
        dict
    ):

        raise TypeError(
            "scoring_result must be a dictionary."
        )

    strategies = scoring_result.get(
        "strategies"
    )

    if not strategies:

        raise ValueError(
            "No scored strategies were provided."
        )

    best_strategy = scoring_result.get(
        "best_strategy"
    )

    if not best_strategy:

        raise ValueError(
            "Best scored strategy is unavailable."
        )

    required_fields = [

        "strategy",

        "tyre_plan",

        "overall_score",

        "score_rank"

    ]

    for field in required_fields:

        if field not in best_strategy:

            raise ValueError(

                f"Best strategy is missing "
                f"required field: {field}"

            )


# ============================================================
# CONFIDENCE CALCULATION
# ============================================================

def calculate_recommendation_confidence(
    best_strategy: Dict[str, Any],
    strategies: list
) -> float:
    """
    Calculate recommendation confidence.

    Confidence considers:

        1. Overall strategy score
        2. Difference between first and second strategy
        3. Number of candidate strategies

    A larger score gap means stronger agreement.
    """

    best_score = float(
        best_strategy[
            "overall_score"
        ]
    )

    sorted_strategies = sorted(

        strategies,

        key=lambda strategy:
        strategy[
            "overall_score"
        ],

        reverse=True

    )

    if len(
        sorted_strategies
    ) > 1:

        second_score = float(

            sorted_strategies[1][
                "overall_score"
            ]

        )

        score_gap = (
            best_score
            - second_score
        )

    else:

        score_gap = 0.0

    # --------------------------------------------------------
    # Base confidence
    # --------------------------------------------------------

    confidence = best_score

    # --------------------------------------------------------
    # Strategy separation bonus
    # --------------------------------------------------------

    if score_gap >= 20:

        confidence += 5.0

    elif score_gap >= 10:

        confidence += 3.0

    elif score_gap >= 5:

        confidence += 1.5

    # --------------------------------------------------------
    # Clamp confidence
    # --------------------------------------------------------

    confidence = max(

        MIN_CONFIDENCE,

        min(

            MAX_CONFIDENCE,

            confidence

        )

    )

    return round(

        confidence,

        2

    )


# ============================================================
# EXTRACT ACTION
# ============================================================

def extract_action(
    best_strategy: Dict[str, Any]
) -> str:
    """
    Convert strategy type into a clean action.
    """

    strategy = str(

        best_strategy.get(
            "strategy",
            ""
        )

    ).upper()

    if strategy == "STAY_OUT":

        return "STAY OUT"

    if strategy == "PIT":

        return "PIT NOW"

    return strategy.replace(
        "_",
        " "
    )


# ============================================================
# EXTRACT TYRE
# ============================================================

def extract_recommended_tyre(
    best_strategy: Dict[str, Any]
) -> Optional[str]:
    """
    Extract the recommended tyre compound
    from the tyre plan.
    """

    tyre_plan = str(

        best_strategy.get(
            "tyre_plan",
            ""
        )

    ).upper()

    if not tyre_plan:

        return None

    if "SOFT" in tyre_plan:

        return "SOFT"

    if "MEDIUM" in tyre_plan:

        return "MEDIUM"

    if "HARD" in tyre_plan:

        return "HARD"

    return None


# ============================================================
# EXPECTED BENEFIT
# ============================================================

def calculate_expected_benefit(
    strategies: list,
    best_strategy: Dict[str, Any]
) -> float:
    """
    Calculate the projected advantage of the selected
    strategy against the second-best strategy.

    Positive value = selected strategy is better.
    """

    if len(
        strategies
    ) < 2:

        return 0.0

    sorted_strategies = sorted(

        strategies,

        key=lambda strategy:
        strategy[
            "projected_total_time"
        ]

    )

    best_time = float(

        best_strategy.get(
            "projected_total_time",
            0
        )

    )

    second_best = None

    for strategy in sorted_strategies:

        if strategy is not best_strategy:

            second_best = strategy

            break

    if second_best is None:

        return 0.0

    second_time = float(

        second_best.get(
            "projected_total_time",
            best_time
        )

    )

    return round(

        second_time
        - best_time,

        3

    )


# ============================================================
# GENERATE REASON
# ============================================================

def generate_reason(
    best_strategy: Dict[str, Any],
    confidence: float,
    expected_benefit: float,
    race_situation: Optional[Dict[str, Any]] = None,
    tyre_decision: Optional[Dict[str, Any]] = None,
    pit_decision: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate a human-readable strategic explanation.

    The reasoning is built from the strongest available
    strategic evidence.
    """

    action = extract_action(
        best_strategy
    )

    tyre = extract_recommended_tyre(
        best_strategy
    )

    score = float(

        best_strategy.get(
            "overall_score",
            0
        )

    )

    degradation = best_strategy.get(
        "degradation_impact"
    )

    projected_time = best_strategy.get(
        "projected_total_time"
    )

    # --------------------------------------------------------
    # STAY OUT
    # --------------------------------------------------------

    if action == "STAY OUT":

        reason = (

            f"The current {tyre or 'tyre'} strategy "
            f"has the highest overall strategy score "
            f"of {score:.2f}."

        )

        if projected_time is not None:

            reason += (

                f" Its projected remaining-race "
                f"time is {float(projected_time):.3f} "
                f"seconds."

            )

        if degradation is not None:

            reason += (

                f" The estimated degradation impact "
                f"is {float(degradation):.3f} seconds."

            )

        if expected_benefit > 0:

            reason += (

                f" It is projected to provide a "
                f"{expected_benefit:.3f}-second advantage "
                f"over the next-best projected strategy."

            )

        reason += (

            f" The strategic model currently gives "
            f"this recommendation {confidence:.2f}% "
            f"confidence."

        )

        return reason

    # --------------------------------------------------------
    # PIT
    # --------------------------------------------------------

    if action == "PIT NOW":

        reason = (

            f"Pitting now and switching to "
            f"{tyre or 'the recommended compound'} "
            f"provides the highest overall strategy "
            f"score of {score:.2f}."

        )

        if projected_time is not None:

            reason += (

                f" The projected remaining-race "
                f"time is {float(projected_time):.3f} "
                f"seconds."

            )

        pit_loss = best_strategy.get(
            "pit_loss"
        )

        if pit_loss is not None:

            reason += (

                f" The estimated pit-stop loss is "
                f"{float(pit_loss):.3f} seconds."

            )

        if expected_benefit > 0:

            reason += (

                f" The strategy is projected to "
                f"gain approximately "
                f"{expected_benefit:.3f} seconds "
                f"against the next-best option."

            )

        reason += (

            f" Overall recommendation confidence "
            f"is {confidence:.2f}%."

        )

        return reason

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return (

        f"The strategy engine selected "
        f"{action} with an overall strategy "
        f"score of {score:.2f} and "
        f"{confidence:.2f}% confidence."

    )


# ============================================================
# GENERATE AI RECOMMENDATION
# ============================================================

def generate_ai_recommendation(
    scoring_result: Dict[str, Any],
    race_situation: Optional[Dict[str, Any]] = None,
    tyre_decision: Optional[Dict[str, Any]] = None,
    pit_decision: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate the final Phase 3.7 AI recommendation.
    """

    validate_strategy_input(
        scoring_result
    )

    strategies = scoring_result[
        "strategies"
    ]

    best_strategy = scoring_result[
        "best_strategy"
    ]

    # --------------------------------------------------------
    # ACTION
    # --------------------------------------------------------

    action = extract_action(
        best_strategy
    )

    # --------------------------------------------------------
    # TYRE
    # --------------------------------------------------------

    recommended_tyre = (
        extract_recommended_tyre(
            best_strategy
        )
    )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = (
        calculate_recommendation_confidence(

            best_strategy=best_strategy,

            strategies=strategies

        )
    )

    # --------------------------------------------------------
    # EXPECTED BENEFIT
    # --------------------------------------------------------

    expected_benefit = (
        calculate_expected_benefit(

            strategies=strategies,

            best_strategy=best_strategy

        )
    )

    # --------------------------------------------------------
    # REASONING
    # --------------------------------------------------------

    reason = generate_reason(

        best_strategy=best_strategy,

        confidence=confidence,

        expected_benefit=expected_benefit,

        race_situation=race_situation,

        tyre_decision=tyre_decision,

        pit_decision=pit_decision

    )

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    recommendation = {

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

        "confidence":
            confidence,

        "overall_score":
            best_strategy.get(
                "overall_score"
            ),

        "strategy_rank":
            best_strategy.get(
                "score_rank"
            ),

        "expected_benefit_seconds":
            expected_benefit,

        "projected_total_time":
            best_strategy.get(
                "projected_total_time"
            ),

        "pit_loss":
            best_strategy.get(
                "pit_loss"
            ),

        "degradation_impact":
            best_strategy.get(
                "degradation_impact"
            ),

        "reason":
            reason,

        "selected_strategy":
            best_strategy,

        "strategy_comparison":
            strategies

    }

    return recommendation


# ============================================================
# DISPLAY RECOMMENDATION
# ============================================================

def display_ai_recommendation(
    recommendation: Dict[str, Any]
) -> None:
    """
    Display the final AI recommendation.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "PHASE 3.7 — AI RECOMMENDATION"
    )

    print(
        "=" * 60
    )

    print(
        f"\nRecommendation: "
        f"{recommendation.get('recommendation')}"
    )

    print(
        f"Recommended Tyre: "
        f"{recommendation.get('recommended_tyre')}"
    )

    print(
        f"Strategy Type: "
        f"{recommendation.get('strategy_type')}"
    )

    print(
        f"Tyre Plan: "
        f"{recommendation.get('tyre_plan')}"
    )

    print(
        f"Confidence: "
        f"{recommendation.get('confidence'):.2f}%"
    )

    print(
        f"Overall Score: "
        f"{recommendation.get('overall_score'):.2f}"
    )

    print(
        f"Strategy Rank: "
        f"{recommendation.get('strategy_rank')}"
    )

    print(
        f"Expected Benefit: "
        f"{recommendation.get('expected_benefit_seconds'):.3f}s"
    )

    print(
        f"Projected Total Time: "
        f"{recommendation.get('projected_total_time'):.3f}s"
    )

    print(
        "\nReason:"
    )

    print(
        recommendation.get(
            "reason"
        )
    )

    print(
        "\n" + "=" * 60
    )


# ============================================================
# PHASE 3.7 TEST
# ============================================================

if __name__ == "__main__":

    from src.strategy.strategy_simulation import (
        run_strategy_simulation
    )

    from src.strategy.strategy_scoring import (
        run_strategy_scoring
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 3.7 — AI RECOMMENDATION"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # TEST CONFIGURATION
    # --------------------------------------------------------

    BASE_LAP_TIME = 96.8

    CURRENT_TYRE = "HARD"

    TYRE_AGE = 22

    REMAINING_LAPS = 22

    PIT_LOSS = 22.0

    # --------------------------------------------------------
    # STEP 1 — STRATEGY SIMULATION
    # --------------------------------------------------------

    print(
        "\n[1/3] Loading strategy simulation..."
    )

    simulation_result = (
        run_strategy_simulation(

            base_lap_time=BASE_LAP_TIME,

            current_tyre=CURRENT_TYRE,

            tyre_age=TYRE_AGE,

            remaining_laps=REMAINING_LAPS,

            pit_loss=PIT_LOSS

        )
    )

    strategies = simulation_result[
        "strategies"
    ]

    print(
        f"Loaded "
        f"{len(strategies)} "
        f"candidate strategies."
    )

    # --------------------------------------------------------
    # STEP 2 — STRATEGY SCORING
    # --------------------------------------------------------

    print(
        "\n[2/3] Loading strategy scores..."
    )

    scoring_result = run_strategy_scoring(
        strategies
    )

    print(
        "Strategy scoring loaded."
    )

    # --------------------------------------------------------
    # STEP 3 — AI RECOMMENDATION
    # --------------------------------------------------------

    print(
        "\n[3/3] Generating AI recommendation..."
    )

    recommendation = (
        generate_ai_recommendation(
            scoring_result=scoring_result
        )
    )

    display_ai_recommendation(
        recommendation
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    assert recommendation.get(
        "recommendation"
    ), (
        "Recommendation was not generated."
    )

    assert recommendation.get(
        "recommended_tyre"
    ), (
        "Recommended tyre was not generated."
    )

    assert recommendation.get(
        "strategy_type"
    ), (
        "Strategy type was not generated."
    )

    assert recommendation.get(
        "confidence"
    ) is not None, (
        "Confidence was not generated."
    )

    assert 0 <= recommendation[
        "confidence"
    ] <= 100, (
        "Confidence must be between 0 and 100."
    )

    assert recommendation.get(
        "overall_score"
    ) is not None, (
        "Overall strategy score is missing."
    )

    assert recommendation.get(
        "reason"
    ), (
        "AI reasoning was not generated."
    )

    assert recommendation.get(
        "selected_strategy"
    ), (
        "Selected strategy is missing."
    )

    assert recommendation.get(
        "strategy_comparison"
    ), (
        "Strategy comparison is missing."
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "✅ PHASE 3.7 AI RECOMMENDATION TEST PASSED"
    )

    print(
        "=" * 60
    )