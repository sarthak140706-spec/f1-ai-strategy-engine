"""
tyre_strategy.py

PHASE 3.3
TYRE STRATEGY DECISION ENGINE

Purpose:
--------
Evaluate available tyre compounds using the current race
situation and determine the best tyre strategy for the
remaining race.

This module builds on the existing tyre degradation engine.

Responsibilities:
-----------------
1. Evaluate individual compounds.
2. Evaluate SOFT / MEDIUM / HARD.
3. Estimate stint performance.
4. Account for tyre degradation.
5. Compare stay-out strategy.
6. Compare pit-to-compound strategies.
7. Rank candidate tyre strategies.
8. Select the best tyre strategy.
9. Generate a structured strategy recommendation.

This module DOES NOT decide whether a pit stop should
actually happen.

Pit-stop decision belongs to Phase 3.4.

Architecture:

    Race Situation
          |
          v
    Current Tyre / Age
          |
          v
    Remaining Laps
          |
          v
    Tyre Strategy Engine
          |
          +---- STAY OUT
          |
          +---- PIT -> SOFT
          |
          +---- PIT -> MEDIUM
          |
          +---- PIT -> HARD
          |
          v
    Strategy Ranking
          |
          v
    Best Tyre Strategy
"""


from typing import Dict, Any, List, Optional


from src.strategy.tyre_stint import (
    analyze_tyre_stint
)


# ============================================================
# CONSTANTS
# ============================================================

AVAILABLE_COMPOUNDS = [

    "SOFT",

    "MEDIUM",

    "HARD"

]


# ============================================================
# COMPOUND BASE PERFORMANCE
# ============================================================

COMPOUND_PACE_ADJUSTMENT = {

    "SOFT": -0.80,

    "MEDIUM": 0.00,

    "HARD": 0.60

}


# ============================================================
# COMPOUND DEGRADATION MULTIPLIERS
# ============================================================

COMPOUND_DEGRADATION_FACTOR = {

    "SOFT": 1.25,

    "MEDIUM": 1.00,

    "HARD": 0.85

}


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_compound(
    compound: str
) -> str:

    if not isinstance(
        compound,
        str
    ):

        raise TypeError(
            "compound must be a string."
        )

    compound = compound.upper().strip()

    if compound not in AVAILABLE_COMPOUNDS:

        raise ValueError(
            f"Unsupported tyre compound: {compound}. "
            f"Available compounds: "
            f"{AVAILABLE_COMPOUNDS}"
        )

    return compound


# ============================================================
# EVALUATE SINGLE COMPOUND
# ============================================================

def evaluate_compound_strategy(
    base_lap_time: float,
    compound: str,
    tyre_age: int,
    stint_length: int
) -> Dict[str, Any]:
    """
    Evaluate one tyre compound for a complete stint.

    This preserves the original tyre-stint analysis while
    adding Phase 3.3 strategy information.
    """

    if base_lap_time <= 0:

        raise ValueError(
            "base_lap_time must be greater than zero."
        )

    if tyre_age < 0:

        raise ValueError(
            "tyre_age cannot be negative."
        )

    if stint_length <= 0:

        raise ValueError(
            "stint_length must be greater than zero."
        )

    compound = validate_compound(
        compound
    )

    # --------------------------------------------------------
    # EXISTING TYRE STINT ENGINE
    # --------------------------------------------------------

    result = analyze_tyre_stint(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age,

        stint_length=stint_length

    )

    degradation = result[
        "DegradationImpact"
    ]

    total_time = result[
        "TotalStintTime"
    ]

    # --------------------------------------------------------
    # DEGRADATION EVALUATION
    # --------------------------------------------------------

    if degradation <= 1.0:

        degradation_evaluation = "Low"

    elif degradation <= 2.5:

        degradation_evaluation = "Moderate"

    else:

        degradation_evaluation = "High"

    # --------------------------------------------------------
    # STRATEGY QUALITY
    # --------------------------------------------------------

    strategy_quality = max(

        0.0,

        100.0 - (
            degradation * 10.0
        )

    )

    # --------------------------------------------------------
    # COMPOUND-SPECIFIC PACE
    # --------------------------------------------------------

    pace_adjustment = (
        COMPOUND_PACE_ADJUSTMENT[
            compound
        ]
    )

    estimated_compound_pace = (
        base_lap_time
        + pace_adjustment
    )

    result[
        "Compound"
    ] = compound

    result[
        "EstimatedCompoundPace"
    ] = round(

        estimated_compound_pace,

        3

    )

    result[
        "DegradationEvaluation"
    ] = degradation_evaluation

    result[
        "StrategyQuality"
    ] = round(

        strategy_quality,

        2

    )

    result[
        "TotalStintTime"
    ] = round(

        total_time,

        3

    )

    return result


# ============================================================
# EVALUATE ALL COMPOUNDS
# ============================================================

def evaluate_all_compounds(
    base_lap_time: float,
    tyre_age: int,
    stint_length: int
) -> List[Dict[str, Any]]:
    """
    Evaluate SOFT, MEDIUM and HARD compounds.
    """

    results = []

    for compound in AVAILABLE_COMPOUNDS:

        result = evaluate_compound_strategy(

            base_lap_time=base_lap_time,

            compound=compound,

            tyre_age=tyre_age,

            stint_length=stint_length

        )

        results.append(
            result
        )

    # --------------------------------------------------------
    # RANK BY TOTAL STINT TIME
    # --------------------------------------------------------

    results.sort(

        key=lambda x:
        x["TotalStintTime"]

    )

    for rank, result in enumerate(

        results,

        start=1

    ):

        result[
            "StrategyRank"
        ] = rank

    return results


# ============================================================
# SELECT OPTIMAL TYRE STRATEGY
# ============================================================

def select_optimal_tyre_strategy(
    strategies: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Select the compound with the lowest projected stint time.
    """

    if not strategies:

        return None

    best_strategy = min(

        strategies,

        key=lambda x:
        x["TotalStintTime"]

    )

    selected = best_strategy.copy()

    selected[
        "SelectedCompound"
    ] = True

    return selected


# ============================================================
# BUILD STAY-OUT STRATEGY
# ============================================================

def build_stay_out_strategy(
    base_lap_time: float,
    current_compound: str,
    tyre_age: int,
    remaining_laps: int
) -> Dict[str, Any]:
    """
    Build a strategy representing staying on the current tyre.

    This is a Phase 3.3 strategy comparison only.

    Phase 3.4 will make the actual PIT / STAY OUT decision.
    """

    if remaining_laps <= 0:

        raise ValueError(
            "remaining_laps must be greater than zero."
        )

    current_compound = validate_compound(
        current_compound
    )

    result = evaluate_compound_strategy(

        base_lap_time=base_lap_time,

        compound=current_compound,

        tyre_age=tyre_age,

        stint_length=remaining_laps

    )

    strategy = {

        "StrategyType":
            "STAY_OUT",

        "Action":
            "STAY OUT",

        "Compound":
            current_compound,

        "StartingTyreAge":
            tyre_age,

        "StintLength":
            remaining_laps,

        "ProjectedStintTime":
            result[
                "TotalStintTime"
            ],

        "AverageLapTime":
            result[
                "AverageLapTime"
            ],

        "DegradationImpact":
            result[
                "DegradationImpact"
            ],

        "DegradationEvaluation":
            result[
                "DegradationEvaluation"
            ],

        "StrategyQuality":
            result[
                "StrategyQuality"
            ],

        "PitRequired":
            False

    }

    return strategy


# ============================================================
# BUILD PIT-TO-COMPOUND STRATEGY
# ============================================================

def build_pit_compound_strategy(
    base_lap_time: float,
    current_compound: str,
    current_tyre_age: int,
    target_compound: str,
    remaining_laps: int,
    pit_loss_seconds: float = 22.0
) -> Dict[str, Any]:
    """
    Build a PIT -> COMPOUND strategy.

    The pit loss is included only for strategy comparison.

    The actual pit-stop decision belongs to Phase 3.4.
    """

    if remaining_laps <= 0:

        raise ValueError(
            "remaining_laps must be greater than zero."
        )

    if pit_loss_seconds < 0:

        raise ValueError(
            "pit_loss_seconds cannot be negative."
        )

    current_compound = validate_compound(
        current_compound
    )

    target_compound = validate_compound(
        target_compound
    )

    # --------------------------------------------------------
    # NEW TYRE STINT
    # --------------------------------------------------------

    stint_result = evaluate_compound_strategy(

        base_lap_time=base_lap_time,

        compound=target_compound,

        tyre_age=0,

        stint_length=remaining_laps

    )

    projected_stint_time = (
        stint_result[
            "TotalStintTime"
        ]
    )

    # --------------------------------------------------------
    # TOTAL STRATEGY TIME
    # --------------------------------------------------------

    projected_total_time = (
        projected_stint_time
        + pit_loss_seconds
    )

    # --------------------------------------------------------
    # STRATEGY QUALITY
    # --------------------------------------------------------

    strategy_quality = max(

        0.0,

        stint_result[
            "StrategyQuality"
        ]
        - (
            pit_loss_seconds * 0.5
        )

    )

    strategy = {

        "StrategyType":
            "PIT",

        "Action":
            "PIT",

        "CurrentCompound":
            current_compound,

        "Compound":
            target_compound,

        "StartingTyreAge":
            current_tyre_age,

        "NewTyreAge":
            0,

        "StintLength":
            remaining_laps,

        "PitLossSeconds":
            round(
                pit_loss_seconds,
                3
            ),

        "ProjectedStintTime":
            round(
                projected_stint_time,
                3
            ),

        "ProjectedTotalTime":
            round(
                projected_total_time,
                3
            ),

        "AverageLapTime":
            stint_result[
                "AverageLapTime"
            ],

        "DegradationImpact":
            stint_result[
                "DegradationImpact"
            ],

        "DegradationEvaluation":
            stint_result[
                "DegradationEvaluation"
            ],

        "StrategyQuality":
            round(
                strategy_quality,
                2
            ),

        "PitRequired":
            True

    }

    return strategy


# ============================================================
# BUILD COMPLETE RACE TYRE STRATEGIES
# ============================================================

def evaluate_race_tyre_strategies(
    base_lap_time: float,
    current_compound: str,
    tyre_age: int,
    remaining_laps: int,
    pit_loss_seconds: float = 22.0
) -> List[Dict[str, Any]]:
    """
    Evaluate all realistic tyre strategies for the remaining race.

    Candidate strategies:

        1. STAY OUT
        2. PIT -> SOFT
        3. PIT -> MEDIUM
        4. PIT -> HARD
    """

    if base_lap_time <= 0:

        raise ValueError(
            "base_lap_time must be greater than zero."
        )

    if tyre_age < 0:

        raise ValueError(
            "tyre_age cannot be negative."
        )

    if remaining_laps <= 0:

        raise ValueError(
            "remaining_laps must be greater than zero."
        )

    current_compound = validate_compound(
        current_compound
    )

    strategies = []

    # --------------------------------------------------------
    # STRATEGY 1 — STAY OUT
    # --------------------------------------------------------

    stay_out = build_stay_out_strategy(

        base_lap_time=base_lap_time,

        current_compound=current_compound,

        tyre_age=tyre_age,

        remaining_laps=remaining_laps

    )

    strategies.append(
        stay_out
    )

    # --------------------------------------------------------
    # STRATEGIES 2–4 — PIT TO NEW COMPOUND
    # --------------------------------------------------------

    for compound in AVAILABLE_COMPOUNDS:

        pit_strategy = build_pit_compound_strategy(

            base_lap_time=base_lap_time,

            current_compound=current_compound,

            current_tyre_age=tyre_age,

            target_compound=compound,

            remaining_laps=remaining_laps,

            pit_loss_seconds=pit_loss_seconds

        )

        strategies.append(
            pit_strategy
        )

    # --------------------------------------------------------
    # RANK STRATEGIES
    # --------------------------------------------------------

    strategies.sort(

        key=lambda strategy:
        strategy[
            "ProjectedTotalTime"
        ]
        if strategy[
            "StrategyType"
        ] == "PIT"
        else strategy[
            "ProjectedStintTime"
        ]

    )

    # --------------------------------------------------------
    # ASSIGN RANK
    # --------------------------------------------------------

    for rank, strategy in enumerate(

        strategies,

        start=1

    ):

        strategy[
            "StrategyRank"
        ] = rank

    return strategies


# ============================================================
# SELECT BEST RACE TYRE STRATEGY
# ============================================================

def select_best_race_tyre_strategy(
    strategies: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Select the best overall tyre strategy.

    This function DOES NOT make the final pit-stop decision.
    """

    if not strategies:

        return None

    def strategy_time(
        strategy
    ):

        if strategy[
            "StrategyType"
        ] == "PIT":

            return strategy[
                "ProjectedTotalTime"
            ]

        return strategy[
            "ProjectedStintTime"
        ]

    best = min(

        strategies,

        key=strategy_time

    )

    selected = best.copy()

    selected[
        "SelectedStrategy"
    ] = True

    return selected


# ============================================================
# GENERATE STRATEGY RECOMMENDATION
# ============================================================

def generate_tyre_strategy_recommendation(
    strategies: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate a structured tyre strategy recommendation.

    This is the final output of Phase 3.3.

    Phase 3.4 will later determine whether the pit action
    should actually be executed.
    """

    if not strategies:

        return {

            "recommendation":
                "NO STRATEGY",

            "compound":
                None,

            "strategy_type":
                None,

            "confidence":
                0.0,

            "reason":
                "No valid tyre strategies available."

        }

    best_strategy = (
        select_best_race_tyre_strategy(
            strategies
        )
    )

    if best_strategy is None:

        return {

            "recommendation":
                "NO STRATEGY",

            "compound":
                None,

            "strategy_type":
                None,

            "confidence":
                0.0,

            "reason":
                "Unable to select a tyre strategy."

        }

    # --------------------------------------------------------
    # FIND SECOND-BEST STRATEGY
    # --------------------------------------------------------

    ranked = sorted(

        strategies,

        key=lambda strategy:

        strategy[
            "ProjectedTotalTime"
        ]
        if strategy[
            "StrategyType"
        ] == "PIT"

        else strategy[
            "ProjectedStintTime"
        ]

    )

    best_time = (

        ranked[0][
            "ProjectedTotalTime"
        ]

        if ranked[0][
            "StrategyType"
        ] == "PIT"

        else ranked[0][
            "ProjectedStintTime"
        ]

    )

    second_time = (

        ranked[1][
            "ProjectedTotalTime"
        ]

        if ranked[1][
            "StrategyType"
        ] == "PIT"

        else ranked[1][
            "ProjectedStintTime"
        ]

    ) if len(ranked) > 1 else best_time

    time_gap = max(

        0.0,

        second_time - best_time

    )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = min(

        99.0,

        60.0
        + (
            time_gap * 5.0
        )
        + (
            best_strategy[
                "StrategyQuality"
            ] * 0.25
        )

    )

    confidence = round(

        confidence,

        2

    )

    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    if best_strategy[
        "StrategyType"
    ] == "STAY_OUT":

        recommendation = (
            "STAY OUT"
        )

        reason = (

            "Staying on the current "
            f"{best_strategy['Compound']} "
            "compound provides the lowest "
            "projected remaining-race time "
            "among the evaluated tyre strategies."

        )

    else:

        recommendation = (
            "PIT"
        )

        reason = (

            "A switch to the "
            f"{best_strategy['Compound']} "
            "compound provides the lowest "
            "projected remaining-race time "
            "after accounting for the estimated "
            "pit-stop loss."

        )

    return {

        "recommendation":
            recommendation,

        "compound":
            best_strategy[
                "Compound"
            ],

        "strategy_type":
            best_strategy[
                "StrategyType"
            ],

        "strategy_rank":
            best_strategy[
                "StrategyRank"
            ],

        "projected_time":
            best_time,

        "time_advantage":
            round(
                time_gap,
                3
            ),

        "confidence":
            confidence,

        "reason":
            reason,

        "selected_strategy":
            best_strategy

    }


# ============================================================
# DISPLAY COMPOUND STRATEGIES
# ============================================================

def display_tyre_strategies(
    strategies: List[Dict[str, Any]]
) -> None:
    """
    Display ranked compound strategies.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "TYRE STRATEGY ANALYSIS"
    )

    print(
        "=" * 60
    )

    if not strategies:

        print(
            "No tyre strategies available."
        )

        return

    for strategy in strategies:

        print(
            f"\nRank: "
            f"{strategy['StrategyRank']}"
        )

        print(
            f"Strategy: "
            f"{strategy.get('StrategyType')}"
        )

        print(
            f"Compound: "
            f"{strategy['Compound']}"
        )

        print(
            f"Stint Length: "
            f"{strategy['StintLength']} laps"
        )

        if strategy[
            "StrategyType"
        ] == "PIT":

            print(
                f"Pit Loss: "
                f"{strategy['PitLossSeconds']:.3f}s"
            )

            print(
                f"Projected Total Time: "
                f"{strategy['ProjectedTotalTime']:.3f}s"
            )

        else:

            print(
                f"Projected Stint Time: "
                f"{strategy['ProjectedStintTime']:.3f}s"
            )

        print(
            f"Average Lap Time: "
            f"{strategy['AverageLapTime']:.3f}s"
        )

        print(
            f"Degradation Impact: "
            f"{strategy['DegradationImpact']:.3f}s"
        )

        print(
            f"Degradation: "
            f"{strategy['DegradationEvaluation']}"
        )

        print(
            f"Strategy Quality: "
            f"{strategy['StrategyQuality']:.2f}"
        )

    print(
        "\n" + "=" * 60
    )


# ============================================================
# DISPLAY OPTIMAL STRATEGY
# ============================================================

def display_optimal_tyre_strategy(
    strategy: Optional[Dict[str, Any]]
) -> None:
    """
    Display the selected optimal tyre strategy.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "OPTIMAL TYRE STRATEGY"
    )

    print(
        "=" * 60
    )

    if strategy is None:

        print(
            "No valid tyre strategy found."
        )

        print(
            "=" * 60
        )

        return

    print(
        f"Action: "
        f"{strategy.get('Action')}"
    )

    print(
        f"Compound: "
        f"{strategy.get('Compound')}"
    )

    print(
        f"Strategy Rank: "
        f"{strategy.get('StrategyRank')}"
    )

    if strategy.get(
        "StrategyType"
    ) == "PIT":

        print(
            f"Pit Loss: "
            f"{strategy.get('PitLossSeconds', 0):.3f}s"
        )

        print(
            f"Projected Total Time: "
            f"{strategy.get('ProjectedTotalTime', 0):.3f}s"
        )

    else:

        print(
            f"Projected Stint Time: "
            f"{strategy.get('ProjectedStintTime', 0):.3f}s"
        )

    print(
        f"Average Lap Time: "
        f"{strategy.get('AverageLapTime', 0):.3f}s"
    )

    print(
        f"Degradation Impact: "
        f"{strategy.get('DegradationImpact', 0):.3f}s"
    )

    print(
        f"Strategy Quality: "
        f"{strategy.get('StrategyQuality', 0):.2f}"
    )

    print(
        "=" * 60
    )


# ============================================================
# DISPLAY FINAL RECOMMENDATION
# ============================================================

def display_tyre_strategy_recommendation(
    recommendation: Dict[str, Any]
) -> None:
    """
    Display the Phase 3.3 recommendation.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "PHASE 3.3 TYRE STRATEGY RECOMMENDATION"
    )

    print(
        "=" * 60
    )

    print(
        f"Recommendation: "
        f"{recommendation.get('recommendation')}"
    )

    print(
        f"Compound: "
        f"{recommendation.get('compound')}"
    )

    print(
        f"Strategy Type: "
        f"{recommendation.get('strategy_type')}"
    )

    print(
        f"Confidence: "
        f"{recommendation.get('confidence')}%"
    )

    print(
        f"Reason: "
        f"{recommendation.get('reason')}"
    )

    print(
        "=" * 60
    )

# ============================================================
# PHASE 3.8 API ADAPTER
# ============================================================

def generate_tyre_strategy(
    base_lap_time: float,
    current_tyre: str,
    tyre_age: int,
    remaining_laps: int,
    pit_loss: float = 22.0
) -> Dict[str, Any]:
    """
    Generate the Phase 3.3 tyre strategy decision
    in a format compatible with the Phase 3.8 API.

    This function acts as an adapter around the existing
    Phase 3.3 tyre-strategy engine.

    Parameters
    ----------
    base_lap_time : float
        Current/recent lap pace in seconds.

    current_tyre : str
        Current tyre compound.

    tyre_age : int
        Current tyre age in laps.

    remaining_laps : int
        Remaining race laps.

    pit_loss : float
        Estimated pit-stop time loss.

    Returns
    -------
    dict
        Structured tyre strategy decision.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if base_lap_time <= 0:
        raise ValueError(
            "base_lap_time must be greater than zero."
        )

    if tyre_age < 0:
        raise ValueError(
            "tyre_age cannot be negative."
        )

    if remaining_laps < 0:
        raise ValueError(
            "remaining_laps cannot be negative."
        )

    if pit_loss < 0:
        raise ValueError(
            "pit_loss cannot be negative."
        )

    if not isinstance(current_tyre, str):
        raise TypeError(
            "current_tyre must be a string."
        )

    current_tyre = current_tyre.upper().strip()

    if current_tyre not in {
        "SOFT",
        "MEDIUM",
        "HARD"
    }:
        raise ValueError(
            "current_tyre must be SOFT, MEDIUM or HARD."
        )

    # ========================================================
    # HANDLE COMPLETED RACE
    # ========================================================

    if remaining_laps == 0:

        return {
            "Recommendation": "STAY_OUT",
            "Compound": current_tyre,
            "StrategyType": "STAY_OUT",
            "Confidence": 100.0,
            "Reason": (
                "The race has reached the final lap, "
                "so no additional pit stop is required."
            ),
            "Strategies": []
        }

    # ========================================================
    # EVALUATE CURRENT TYRE
    # ========================================================

    current_strategy = evaluate_compound_strategy(

        base_lap_time=base_lap_time,

        compound=current_tyre,

        tyre_age=tyre_age,

        stint_length=remaining_laps

    )

    # ========================================================
    # EVALUATE ALL NEW-COMPOUND OPTIONS
    # ========================================================

    compound_strategies = []

    for compound in [
        "SOFT",
        "MEDIUM",
        "HARD"
    ]:

        # A pit strategy starts the new tyre from age 0.
        strategy = evaluate_compound_strategy(

            base_lap_time=base_lap_time,

            compound=compound,

            tyre_age=0,

            stint_length=remaining_laps

        )

        projected_total_time = (
            strategy["TotalStintTime"]
            + pit_loss
        )

        strategy["Action"] = "PIT"

        strategy["PitLoss"] = round(
            pit_loss,
            3
        )

        strategy["ProjectedTotalTime"] = round(
            projected_total_time,
            3
        )

        compound_strategies.append(
            strategy
        )

    # ========================================================
    # CURRENT TYRE / STAY OUT
    # ========================================================

    stay_out = current_strategy.copy()

    stay_out["Action"] = "STAY_OUT"

    stay_out["PitLoss"] = 0.0

    stay_out["ProjectedTotalTime"] = round(
        stay_out["TotalStintTime"],
        3
    )

    # ========================================================
    # COMBINE CANDIDATES
    # ========================================================

    candidates = [
        stay_out
    ] + compound_strategies

    # ========================================================
    # RANK CANDIDATES
    # ========================================================

    candidates.sort(
        key=lambda strategy:
        strategy["ProjectedTotalTime"]
    )

    for rank, strategy in enumerate(
        candidates,
        start=1
    ):

        strategy["StrategyRank"] = rank

    # ========================================================
    # SELECT BEST
    # ========================================================

    best = candidates[0]

    # ========================================================
    # CALCULATE CONFIDENCE
    # ========================================================

    if len(candidates) > 1:

        second_best = candidates[1]

        advantage = (
            second_best["ProjectedTotalTime"]
            - best["ProjectedTotalTime"]
        )

    else:

        advantage = 0.0

    confidence = min(
        99.0,
        max(
            50.0,
            70.0 + (
                advantage * 10.0
            )
        )
    )

    confidence = round(
        confidence,
        1
    )

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    if best["Action"] == "STAY_OUT":

        recommendation = "STAY OUT"

        reason = (
            f"Staying on the current "
            f"{current_tyre} compound provides "
            f"the lowest projected remaining-race "
            f"time among the evaluated tyre strategies."
        )

    else:

        recommendation = "PIT"

        recommended_compound = (
            best["Compound"]
        )

        reason = (
            f"Pitting to {recommended_compound} "
            f"is projected to provide the lowest "
            f"remaining-race time after accounting "
            f"for the estimated {pit_loss:.1f}s "
            f"pit-stop loss."
        )

    # ========================================================
    # API-COMPATIBLE RESULT
    # ========================================================

    return {

        "Recommendation":
            recommendation,

        "Compound":
            best["Compound"],

        "StrategyType":
            best["Action"],

        "Confidence":
            confidence,

        "CurrentTyre":
            current_tyre,

        "TyreAge":
            tyre_age,

        "RemainingLaps":
            remaining_laps,

        "PitLoss":
            round(
                pit_loss,
                3
            ),

        "ProjectedTotalTime":
            round(
                best["ProjectedTotalTime"],
                3
            ),

        "AverageLapTime":
            round(
                best["AverageLapTime"],
                3
            ),

        "DegradationImpact":
            round(
                best["DegradationImpact"],
                3
            ),

        "StrategyQuality":
            round(
                best["StrategyQuality"],
                2
            ),

        "EstimatedBenefit":
            round(
                advantage,
                3
            ),

        "Reason":
            reason,

        "SelectedStrategy":
            best,

        "Strategies":
            candidates
    }


# ============================================================
# PHASE 3.3 TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n" + "=" * 60
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 3.3 — TYRE STRATEGY DECISION ENGINE"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # TEST CONFIGURATION
    # --------------------------------------------------------

    BASE_LAP_TIME = 96.2

    CURRENT_COMPOUND = "HARD"

    TYRE_AGE = 22

    REMAINING_LAPS = 22

    PIT_LOSS_SECONDS = 22.0

    # --------------------------------------------------------
    # STEP 1
    # EVALUATE BASIC COMPOUNDS
    # --------------------------------------------------------

    print(
        "\n[1/4] Evaluating tyre compounds..."
    )

    compound_results = evaluate_all_compounds(

        base_lap_time=BASE_LAP_TIME,

        tyre_age=0,

        stint_length=REMAINING_LAPS

    )

    print(
        "Compound evaluation completed."
    )

    # --------------------------------------------------------
    # STEP 2
    # EVALUATE RACE STRATEGIES
    # --------------------------------------------------------

    print(
        "\n[2/4] Evaluating race tyre strategies..."
    )

    race_strategies = (
        evaluate_race_tyre_strategies(

            base_lap_time=BASE_LAP_TIME,

            current_compound=CURRENT_COMPOUND,

            tyre_age=TYRE_AGE,

            remaining_laps=REMAINING_LAPS,

            pit_loss_seconds=PIT_LOSS_SECONDS

        )
    )

    print(
        "Race strategy evaluation completed."
    )

    # --------------------------------------------------------
    # STEP 3
    # DISPLAY STRATEGIES
    # --------------------------------------------------------

    print(
        "\n[3/4] Ranking tyre strategies..."
    )

    display_tyre_strategies(

        race_strategies

    )

    optimal_strategy = (
        select_best_race_tyre_strategy(
            race_strategies
        )
    )

    display_optimal_tyre_strategy(

        optimal_strategy

    )

    # --------------------------------------------------------
    # STEP 4
    # GENERATE RECOMMENDATION
    # --------------------------------------------------------

    print(
        "\n[4/4] Generating tyre recommendation..."
    )

    recommendation = (
        generate_tyre_strategy_recommendation(

            race_strategies

        )
    )

    display_tyre_strategy_recommendation(

        recommendation

    )

    # --------------------------------------------------------
    # VERIFICATION
    # --------------------------------------------------------

    assert len(
        compound_results
    ) == 3

    assert len(
        race_strategies
    ) == 4

    assert optimal_strategy is not None

    assert recommendation[
        "recommendation"
    ] in [

        "PIT",

        "STAY OUT"

    ]

    assert recommendation[
        "compound"
    ] in AVAILABLE_COMPOUNDS

    print(
        "\n" + "=" * 60
    )

    print(
        "PHASE 3.3 TYRE STRATEGY TEST PASSED"
    )

    print(
        "=" * 60
    )