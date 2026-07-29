"""
tyre_strategy.py

Sprint 4 - Step 7

Integrates tyre degradation intelligence with
multi-compound strategy evaluation.

The module:
- Evaluates candidate tyre compounds
- Estimates stint performance
- Considers tyre degradation
- Selects the best compound for a given stint
"""

from typing import Dict, Any, List

from src.strategy.tyre_stint import (
    analyze_tyre_stint
)


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

    result = analyze_tyre_stint(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age,

        stint_length=stint_length

    )

    # --------------------------------------------------------
    # STRATEGY QUALITY
    # --------------------------------------------------------

    degradation = result[
        "DegradationImpact"
    ]

    total_time = result[
        "TotalStintTime"
    ]

    # Lower degradation and lower total time
    # indicate better tyre performance.

    if degradation <= 1.0:

        degradation_evaluation = "Low"

    elif degradation <= 2.5:

        degradation_evaluation = "Moderate"

    else:

        degradation_evaluation = "High"

    result[
        "DegradationEvaluation"
    ] = degradation_evaluation

    result[
        "StrategyQuality"
    ] = round(

        100
        - (
            degradation * 10
        ),

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

    compounds = [

        "SOFT",

        "MEDIUM",

        "HARD"

    ]

    results = []

    for compound in compounds:

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
) -> Dict[str, Any] | None:
    """
    Select the best tyre compound strategy.
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
# DISPLAY TYRE STRATEGIES
# ============================================================

def display_tyre_strategies(
    strategies: List[Dict[str, Any]]
) -> None:
    """
    Display ranked tyre strategies.
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
            f"Compound: "
            f"{strategy['Compound']}"
        )

        print(
            f"Stint Length: "
            f"{strategy['StintLength']} laps"
        )

        print(
            f"Average Lap Time: "
            f"{strategy['AverageLapTime']:.3f}s"
        )

        print(
            f"Total Stint Time: "
            f"{strategy['TotalStintTime']:.3f}s"
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
        "=" * 60
    )


# ============================================================
# DISPLAY OPTIMAL STRATEGY
# ============================================================

def display_optimal_tyre_strategy(
    strategy: Dict[str, Any] | None
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

    else:

        print(
            f"Selected Compound: "
            f"{strategy['Compound']}"
        )

        print(
            f"Total Stint Time: "
            f"{strategy['TotalStintTime']:.3f}s"
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
            f"Strategy Quality: "
            f"{strategy['StrategyQuality']:.2f}"
        )

    print(
        "=" * 60
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 60
    )

    print(
        "SPRINT 4 - STEP 7 TEST"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # TEST CONFIGURATION
    # --------------------------------------------------------

    BASE_LAP_TIME = 90.0

    TYRE_AGE = 0

    STINT_LENGTH = 20

    # --------------------------------------------------------
    # EVALUATE ALL COMPOUNDS
    # --------------------------------------------------------

    strategies = evaluate_all_compounds(

        base_lap_time=BASE_LAP_TIME,

        tyre_age=TYRE_AGE,

        stint_length=STINT_LENGTH

    )

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    display_tyre_strategies(

        strategies

    )

    # --------------------------------------------------------
    # SELECT OPTIMAL STRATEGY
    # --------------------------------------------------------

    optimal_strategy = (
        select_optimal_tyre_strategy(
            strategies
        )
    )

    # --------------------------------------------------------
    # DISPLAY OPTIMAL STRATEGY
    # --------------------------------------------------------

    display_optimal_tyre_strategy(

        optimal_strategy

    )

    print(
        "=" * 60
    )

    print(
        "STEP 7 COMPLETED"
    )

    print(
        "=" * 60
    )