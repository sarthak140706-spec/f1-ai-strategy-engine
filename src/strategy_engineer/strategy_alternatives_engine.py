"""
F1 AI STRATEGIST
PHASE 7.3 — STRATEGY ALTERNATIVES ENGINE

Purpose
-------
Convert the simulation and scoring outputs produced by the
existing strategy engine into a clean, ranked comparison of
available race strategies.

Pipeline
--------

Manual User Input
        ↓
7.1 Manual Race-State Builder
        ↓
7.2 AI Strategy Engineer Service
        ↓
4.5 Dynamic Strategy Simulation
        ↓
4.6 Dynamic Strategy Scoring
        ↓
7.3 Strategy Alternatives Engine
        ↓
Ranked Strategy Comparison

Typical alternatives
--------------------

    STAY OUT

    PIT -> SOFT

    PIT -> MEDIUM

    PIT -> HARD


IMPORTANT
---------
Phase 7.3 does NOT:

- rebuild strategy simulation
- rebuild strategy scoring
- override the Phase 4 AI recommendation
- optimize pit windows
- generate final frontend explanations

It only converts existing verified strategy outputs into a
clean alternatives-comparison layer.
"""


from __future__ import annotations

from typing import Any, Dict, List, Optional


# ============================================================
# PHASE 7.2
# ============================================================

from src.strategy_engineer.strategy_engineer_service import (
    run_strategy_engineer_service
)


# ============================================================
# CONSTANTS
# ============================================================

PHASE = "7.3"

COMPONENT = "strategy_alternatives_engine"


# ============================================================
# GENERIC HELPERS
# ============================================================

def _first_value(
    data: Dict[str, Any],
    *keys: str,
    default: Any = None
) -> Any:
    """
    Return the first available non-None dictionary value.
    """

    if not isinstance(
        data,
        dict
    ):

        return default


    for key in keys:

        value = data.get(
            key
        )


        if value is not None:

            return value


    return default


# ============================================================
# SAFE FLOAT
# ============================================================

def _safe_float(
    value: Any,
    default: Optional[float] = None
) -> Optional[float]:
    """
    Safely convert a value to float.
    """

    try:

        if value is None:

            return default


        return float(
            value
        )


    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# SAFE INTEGER
# ============================================================

def _safe_int(
    value: Any,
    default: Optional[int] = None
) -> Optional[int]:
    """
    Safely convert a value to integer.
    """

    try:

        if value is None:

            return default


        return int(
            value
        )


    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# NORMALISE TEXT
# ============================================================

def _normalise_text(
    value: Any
) -> str:
    """
    Convert strategy text into a standard uppercase form.
    """

    if value is None:

        return ""


    return (

        str(value)
        .strip()
        .upper()

    )


# ============================================================
# STRATEGY DISPLAY NAME
# ============================================================

def build_strategy_display_name(
    strategy: str,
    final_tyre: Optional[str],
    tyre_plan: Optional[str]
) -> str:
    """
    Build a frontend-friendly strategy name.
    """

    strategy = _normalise_text(
        strategy
    )


    final_tyre = _normalise_text(
        final_tyre
    )


    tyre_plan = (
        str(tyre_plan).strip()
        if tyre_plan is not None
        else ""
    )


    # ========================================================
    # STAY OUT
    # ========================================================

    if strategy in {

        "STAY_OUT",
        "STAY OUT"

    }:

        return "STAY OUT"


    # ========================================================
    # PIT STRATEGY
    # ========================================================

    if strategy == "PIT":

        if final_tyre:

            return (
                f"PIT → {final_tyre}"
            )


        if tyre_plan:

            return (
                tyre_plan
                .replace(
                    "->",
                    "→"
                )
            )


        return "PIT"


    # ========================================================
    # FALLBACK
    # ========================================================

    if tyre_plan:

        return (
            tyre_plan
            .replace(
                "->",
                "→"
            )
        )


    return (
        strategy
        .replace(
            "_",
            " "
        )
        or
        "UNKNOWN"
    )


# ============================================================
# EXTRACT STRATEGY LIST
# ============================================================

def extract_strategy_candidates(
    strategy_result: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Extract the most complete strategy list available.

    Preference order:

        Phase 4.6 scoring strategies
        ↓
        Phase 4.5 simulation strategies
        ↓
        Phase 4.7 strategy comparison
    """

    if not isinstance(
        strategy_result,
        dict
    ):

        return []


    # ========================================================
    # SCORING RESULT
    # ========================================================

    scoring = strategy_result.get(
        "strategy_scoring"
    )


    if isinstance(
        scoring,
        dict
    ):

        strategies = scoring.get(
            "strategies"
        )


        if (
            isinstance(
                strategies,
                list
            )
            and
            strategies
        ):

            return strategies


    # ========================================================
    # PIPELINE SCORING
    # ========================================================

    pipeline = strategy_result.get(
        "pipeline"
    )


    if isinstance(
        pipeline,
        dict
    ):

        phase_4_6 = pipeline.get(
            "phase_4_6"
        )


        if isinstance(
            phase_4_6,
            dict
        ):

            strategies = phase_4_6.get(
                "strategies"
            )


            if (
                isinstance(
                    strategies,
                    list
                )
                and
                strategies
            ):

                return strategies


    # ========================================================
    # SIMULATION RESULT
    # ========================================================

    simulation = strategy_result.get(
        "strategy_simulation"
    )


    if isinstance(
        simulation,
        dict
    ):

        strategies = simulation.get(
            "strategies"
        )


        if (
            isinstance(
                strategies,
                list
            )
            and
            strategies
        ):

            return strategies


    # ========================================================
    # AI RECOMMENDATION
    # ========================================================

    ai_result = strategy_result.get(
        "ai_recommendation"
    )


    if isinstance(
        ai_result,
        dict
    ):

        comparison = ai_result.get(
            "strategy_comparison"
        )


        if (
            isinstance(
                comparison,
                list
            )
            and
            comparison
        ):

            return comparison


    return []


# ============================================================
# NORMALISE ONE ALTERNATIVE
# ============================================================

def normalise_strategy_alternative(
    strategy: Dict[str, Any],
    index: int
) -> Dict[str, Any]:
    """
    Convert one Phase 4 strategy result into the Phase 7.3
    alternatives contract.
    """

    if not isinstance(
        strategy,
        dict
    ):

        raise TypeError(
            "Each strategy alternative must be a dictionary."
        )


    # ========================================================
    # STRATEGY IDENTITY
    # ========================================================

    strategy_type = _first_value(

        strategy,

        "strategy",
        "Strategy",

        default="UNKNOWN"

    )


    strategy_type = _normalise_text(
        strategy_type
    )


    final_tyre = _first_value(

        strategy,

        "final_tyre",
        "FinalTyre"

    )


    if final_tyre is not None:

        final_tyre = _normalise_text(
            final_tyre
        )


    starting_tyre = _first_value(

        strategy,

        "starting_tyre",
        "StartingTyre"

    )


    if starting_tyre is not None:

        starting_tyre = _normalise_text(
            starting_tyre
        )


    tyre_plan = _first_value(

        strategy,

        "tyre_plan",
        "TyrePlan"

    )


    # ========================================================
    # SCORE
    # ========================================================

    dynamic_score = _safe_float(

        _first_value(

            strategy,

            "dynamic_overall_score",
            "dynamic_score",
            "DynamicScore"

        )

    )


    overall_score = _safe_float(

        _first_value(

            strategy,

            "overall_score",
            "base_overall_score",
            "OverallScore"

        )

    )


    # ========================================================
    # RANK
    # ========================================================

    rank = _safe_int(

        _first_value(

            strategy,

            "dynamic_score_rank",
            "score_rank",
            "strategy_rank"

        ),

        default=(
            index + 1
        )

    )


    # ========================================================
    # TIMING
    # ========================================================

    projected_total_time = _safe_float(

        _first_value(

            strategy,

            "projected_total_time",
            "ProjectedTotalTime"

        )

    )


    projected_stint_time = _safe_float(

        _first_value(

            strategy,

            "projected_stint_time",
            "ProjectedStintTime"

        )

    )


    average_lap_time = _safe_float(

        _first_value(

            strategy,

            "average_lap_time",
            "AverageLapTime"

        )

    )


    time_difference = _safe_float(

        _first_value(

            strategy,

            "time_difference",
            "TimeDifference"

        ),

        default=0.0

    )


    # ========================================================
    # PIT INFORMATION
    # ========================================================

    stops = _safe_int(

        _first_value(

            strategy,

            "stops",
            "Stops"

        ),

        default=0

    )


    pit_loss = _safe_float(

        _first_value(

            strategy,

            "pit_loss",
            "PitLoss"

        ),

        default=0.0

    )


    # ========================================================
    # STINT
    # ========================================================

    stint_length = _safe_int(

        _first_value(

            strategy,

            "stint_length",
            "StintLength"

        )

    )


    laps_remaining = _safe_int(

        _first_value(

            strategy,

            "laps_remaining",
            "LapsRemaining"

        )

    )


    current_tyre_age = _safe_float(

        _first_value(

            strategy,

            "current_tyre_age",
            "CurrentTyreAge"

        )

    )


    # ========================================================
    # COMPONENT SCORES
    # ========================================================

    component_scores = {

        "pace":
            _safe_float(
                strategy.get(
                    "pace_score"
                )
            ),

        "tyre":
            _safe_float(
                strategy.get(
                    "tyre_score"
                )
            ),

        "degradation":
            _safe_float(
                strategy.get(
                    "degradation_score"
                )
            ),

        "pit":
            _safe_float(
                strategy.get(
                    "pit_score"
                )
            ),

        "position":
            _safe_float(
                strategy.get(
                    "position_score"
                )
            ),

        "risk":
            _safe_float(
                strategy.get(
                    "risk_score"
                )
            ),

        "traffic":
            _safe_float(
                strategy.get(
                    "traffic_score"
                )
            ),

        "decision_alignment":
            _safe_float(
                strategy.get(
                    "decision_alignment_score"
                )
            ),

        "tyre_alignment":
            _safe_float(
                strategy.get(
                    "tyre_alignment_score"
                )
            ),

        "race_situation":
            _safe_float(
                strategy.get(
                    "race_situation_score"
                )
            ),

        "dynamic_context":
            _safe_float(
                strategy.get(
                    "dynamic_context_score"
                )
            ),

    }


    # ========================================================
    # DISPLAY NAME
    # ========================================================

    display_name = build_strategy_display_name(

        strategy=
            strategy_type,

        final_tyre=
            final_tyre,

        tyre_plan=
            tyre_plan

    )


    # ========================================================
    # RETURN CONTRACT
    # ========================================================

    return {

        "id":
            f"strategy_{index + 1}",

        "rank":
            rank,

        "strategy":
            strategy_type,

        "display_name":
            display_name,

        "starting_tyre":
            starting_tyre,

        "final_tyre":
            final_tyre,

        "tyre_plan":
            tyre_plan,

        "stops":
            stops,

        "pit_loss":
            pit_loss,

        "stint_length":
            stint_length,

        "laps_remaining":
            laps_remaining,

        "current_tyre_age":
            current_tyre_age,

        "average_lap_time":
            average_lap_time,

        "projected_stint_time":
            projected_stint_time,

        "projected_total_time":
            projected_total_time,

        "time_difference":
            time_difference,

        "overall_score":
            overall_score,

        "dynamic_score":
            dynamic_score,

        "component_scores":
            component_scores,

        "raw":
            strategy,

    }


# ============================================================
# SORT ALTERNATIVES
# ============================================================

def sort_strategy_alternatives(
    alternatives: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Rank alternatives using the dynamic score.

    Highest score is preferred.

    Projected total time acts as the secondary comparison
    when scores are equal.
    """

    def sort_key(
        strategy: Dict[str, Any]
    ):

        dynamic_score = strategy.get(
            "dynamic_score"
        )


        projected_time = strategy.get(
            "projected_total_time"
        )


        if dynamic_score is None:

            dynamic_score = -1_000_000.0


        if projected_time is None:

            projected_time = 1_000_000_000.0


        return (

            -dynamic_score,

            projected_time

        )


    ordered = sorted(

        alternatives,

        key=sort_key

    )


    # ========================================================
    # ASSIGN PHASE 7.3 RANK
    # ========================================================

    for index, alternative in enumerate(
        ordered,
        start=1
    ):

        alternative[
            "comparison_rank"
        ] = index


    return ordered


# ============================================================
# FIND BEST ALTERNATIVE
# ============================================================

def get_best_strategy_alternative(
    alternatives: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Return the highest-ranked strategy.
    """

    if not alternatives:

        return None


    return alternatives[
        0
    ]


# ============================================================
# FIND SECOND-BEST ALTERNATIVE
# ============================================================

def get_second_best_strategy_alternative(
    alternatives: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Return the second-ranked strategy when available.
    """

    if len(
        alternatives
    ) < 2:

        return None


    return alternatives[
        1
    ]


# ============================================================
# CALCULATE SCORE ADVANTAGE
# ============================================================

def calculate_score_advantage(
    best_strategy: Optional[Dict[str, Any]],
    second_strategy: Optional[Dict[str, Any]]
) -> Optional[float]:
    """
    Calculate the dynamic-score gap between the best and
    second-best alternatives.
    """

    if (
        not best_strategy
        or
        not second_strategy
    ):

        return None


    best_score = best_strategy.get(
        "dynamic_score"
    )


    second_score = second_strategy.get(
        "dynamic_score"
    )


    if (
        best_score is None
        or
        second_score is None
    ):

        return None


    return round(

        best_score
        -
        second_score,

        2

    )


# ============================================================
# CALCULATE TIME ADVANTAGE
# ============================================================

def calculate_time_advantage(
    best_strategy: Optional[Dict[str, Any]],
    second_strategy: Optional[Dict[str, Any]]
) -> Optional[float]:
    """
    Calculate projected time advantage of the best strategy.

    Positive means the best strategy is projected to finish
    that many seconds sooner.
    """

    if (
        not best_strategy
        or
        not second_strategy
    ):

        return None


    best_time = best_strategy.get(
        "projected_total_time"
    )


    second_time = second_strategy.get(
        "projected_total_time"
    )


    if (
        best_time is None
        or
        second_time is None
    ):

        return None


    return round(

        second_time
        -
        best_time,

        3

    )


# ============================================================
# AI RECOMMENDATION ALIGNMENT
# ============================================================

def determine_ai_alignment(
    strategy_result: Dict[str, Any],
    best_strategy: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Compare the final Phase 4.7 recommendation with the
    highest-ranked strategy alternative.

    This does NOT modify either decision.
    """

    ai_recommendation = _normalise_text(

        strategy_result.get(
            "recommendation"
        )

    )


    ai_tyre = _normalise_text(

        strategy_result.get(
            "recommended_tyre"
        )

    )


    if not best_strategy:

        return {

            "aligned":
                False,

            "ai_recommendation":
                ai_recommendation,

            "ai_recommended_tyre":
                ai_tyre,

            "best_strategy":
                None,

        }


    best_type = _normalise_text(

        best_strategy.get(
            "strategy"
        )

    )


    best_tyre = _normalise_text(

        best_strategy.get(
            "final_tyre"
        )

    )


    # ========================================================
    # ACTION NORMALISATION
    # ========================================================

    ai_is_stay_out = (
        ai_recommendation
        in {
            "STAY OUT",
            "STAY_OUT",
        }
    )


    best_is_stay_out = (
        best_type
        in {
            "STAY OUT",
            "STAY_OUT",
        }
    )


    ai_is_pit = (

        "PIT"
        in ai_recommendation

    )


    best_is_pit = (
        best_type == "PIT"
    )


    action_aligned = (

        (
            ai_is_stay_out
            and
            best_is_stay_out
        )

        or

        (
            ai_is_pit
            and
            best_is_pit
        )

    )


    tyre_aligned = (

        not ai_tyre

        or

        not best_tyre

        or

        ai_tyre
        ==
        best_tyre

    )


    return {

        "aligned":
            bool(
                action_aligned
                and
                tyre_aligned
            ),

        "action_aligned":
            action_aligned,

        "tyre_aligned":
            tyre_aligned,

        "ai_recommendation":
            ai_recommendation,

        "ai_recommended_tyre":
            ai_tyre,

        "best_strategy":
            best_strategy.get(
                "display_name"
            ),

    }


# ============================================================
# BUILD ALTERNATIVES FROM 7.2 RESULT
# ============================================================

def build_strategy_alternatives(
    strategy_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build the Phase 7.3 alternatives result from an already
    executed Phase 7.2 strategy result.
    """

    if not isinstance(
        strategy_result,
        dict
    ):

        raise TypeError(
            "strategy_result must be a dictionary."
        )


    if not strategy_result:

        raise ValueError(
            "strategy_result cannot be empty."
        )


    if strategy_result.get(
        "phase"
    ) != "7.2":

        raise ValueError(
            "Phase 7.3 requires a Phase 7.2 strategy result."
        )


    # ========================================================
    # EXTRACT CANDIDATES
    # ========================================================

    candidates = extract_strategy_candidates(
        strategy_result
    )


    if not candidates:

        raise RuntimeError(
            "No strategy alternatives were found in the "
            "Phase 7.2 simulation/scoring output."
        )


    # ========================================================
    # NORMALISE
    # ========================================================

    alternatives = [

        normalise_strategy_alternative(

            strategy=
                strategy,

            index=
                index

        )

        for index, strategy
        in enumerate(
            candidates
        )

    ]


    # ========================================================
    # SORT
    # ========================================================

    alternatives = sort_strategy_alternatives(
        alternatives
    )


    # ========================================================
    # BEST / SECOND
    # ========================================================

    best_strategy = (
        get_best_strategy_alternative(
            alternatives
        )
    )


    second_strategy = (
        get_second_best_strategy_alternative(
            alternatives
        )
    )


    # ========================================================
    # ADVANTAGES
    # ========================================================

    score_advantage = calculate_score_advantage(

        best_strategy=
            best_strategy,

        second_strategy=
            second_strategy

    )


    time_advantage = calculate_time_advantage(

        best_strategy=
            best_strategy,

        second_strategy=
            second_strategy

    )


    # ========================================================
    # AI ALIGNMENT
    # ========================================================

    ai_alignment = determine_ai_alignment(

        strategy_result=
            strategy_result,

        best_strategy=
            best_strategy

    )


    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "engine":
            COMPONENT,

        "phase":
            PHASE,

        "status":
            "SUCCESS",

        "driver":
            strategy_result.get(
                "driver"
            ),

        "circuit":
            strategy_result.get(
                "circuit"
            ),

        "current_lap":
            strategy_result.get(
                "current_lap"
            ),

        "total_laps":
            strategy_result.get(
                "total_laps"
            ),

        "position":
            strategy_result.get(
                "position"
            ),

        "current_tyre":
            strategy_result.get(
                "current_tyre"
            ),

        "race_situation":
            strategy_result.get(
                "race_situation"
            ),

        "pit_decision":
            strategy_result.get(
                "pit_decision"
            ),

        "ai_recommendation":
            strategy_result.get(
                "recommendation"
            ),

        "ai_recommended_tyre":
            strategy_result.get(
                "recommended_tyre"
            ),

        "strategy_count":
            len(
                alternatives
            ),

        "alternatives":
            alternatives,

        "best_strategy":
            best_strategy,

        "second_best_strategy":
            second_strategy,

        "score_advantage":
            score_advantage,

        "time_advantage_seconds":
            time_advantage,

        "ai_alignment":
            ai_alignment,

        "phase_7_2_result":
            strategy_result,

    }


# ============================================================
# MAIN PHASE 7.3 SERVICE
# ============================================================

def run_strategy_alternatives_engine(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute Phase 7.2 and construct the ranked Phase 7.3
    strategy comparison.
    """

    # ========================================================
    # PHASE 7.2
    # ========================================================

    strategy_result = (
        run_strategy_engineer_service(
            race_input
        )
    )


    # ========================================================
    # PHASE 7.3
    # ========================================================

    return build_strategy_alternatives(
        strategy_result
    )


# ============================================================
# DISPLAY
# ============================================================

def display_strategy_alternatives(
    result: Dict[str, Any]
) -> None:
    """
    Display the Phase 7.3 strategy comparison.
    """

    if not result:

        print(
            "No Phase 7.3 strategy alternatives available."
        )

        return


    print(
        "\n" + "=" * 86
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.3 — STRATEGY ALTERNATIVES ENGINE"
    )

    print(
        "=" * 86
    )


    print(
        f"Driver:           "
        f"{result.get('driver', '--')}"
    )


    print(
        f"Circuit:          "
        f"{result.get('circuit', '--')}"
    )


    print(
        f"Lap:              "
        f"{result.get('current_lap', '--')}"
        f"/"
        f"{result.get('total_laps', '--')}"
    )


    position = result.get(
        "position"
    )


    if position is not None:

        print(
            f"Position:         "
            f"P{position}"
        )


    print(
        f"Current Tyre:     "
        f"{result.get('current_tyre', '--')}"
    )


    print(
        f"Race Situation:   "
        f"{result.get('race_situation', '--')}"
    )


    print(
        f"Pit Decision:     "
        f"{result.get('pit_decision', '--')}"
    )


    print(
        f"AI Recommendation:"
        f" {result.get('ai_recommendation', '--')}"
    )


    print(
        "-" * 86
    )


    print(
        f"{'RANK':<7}"
        f"{'STRATEGY':<24}"
        f"{'SCORE':<12}"
        f"{'TIME':<16}"
        f"{'Δ TIME':<12}"
        f"{'STOPS':<8}"
    )


    print(
        "-" * 86
    )


    for alternative in result.get(
        "alternatives",
        []
    ):

        rank = alternative.get(
            "comparison_rank"
        )


        name = alternative.get(
            "display_name"
        )


        score = alternative.get(
            "dynamic_score"
        )


        projected_time = alternative.get(
            "projected_total_time"
        )


        time_difference = alternative.get(
            "time_difference"
        )


        stops = alternative.get(
            "stops"
        )


        score_text = (

            f"{score:.2f}"

            if score is not None

            else "--"

        )


        time_text = (

            f"{projected_time:.3f}s"

            if projected_time is not None

            else "--"

        )


        difference_text = (

            f"{time_difference:.3f}s"

            if time_difference is not None

            else "--"

        )


        print(

            f"{rank:<7}"
            f"{name:<24}"
            f"{score_text:<12}"
            f"{time_text:<16}"
            f"{difference_text:<12}"
            f"{stops:<8}"

        )


    print(
        "-" * 86
    )


    best = result.get(
        "best_strategy"
    )


    if best:

        print(
            f"Best Strategy:        "
            f"{best.get('display_name')}"
        )


        print(
            f"Best Dynamic Score:   "
            f"{best.get('dynamic_score')}"
        )


    print(
        f"Score Advantage:      "
        f"{result.get('score_advantage')}"
    )


    print(
        f"Time Advantage:       "
        f"{result.get('time_advantage_seconds')} s"
    )


    alignment = result.get(
        "ai_alignment",
        {}
    )


    print(
        f"AI/Ranking Aligned:   "
        f"{alignment.get('aligned')}"
    )


    print(
        "=" * 86
    )