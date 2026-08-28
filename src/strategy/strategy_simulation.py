"""
strategy_simulation.py

PHASE 3.5 — STRATEGY SIMULATION

Purpose
-------
Compare multiple possible race strategies and estimate their
projected remaining-race performance.

Candidate strategies:

    1. STAY OUT
    2. PIT -> SOFT
    3. PIT -> MEDIUM
    4. PIT -> HARD

This module does NOT:
    - make the final AI recommendation
    - calculate the unified strategy score
    - handle Flask/API integration

Those responsibilities belong to later Phase 3 steps.

Pipeline
--------

Race Situation
       ↓
Current Tyre / Tyre Age
       ↓
Remaining Laps
       ↓
Tyre Stint Analysis
       ↓
Pit Stop Cost
       ↓
Candidate Strategies
       ↓
Projected Race Time
       ↓
Strategy Ranking
"""

from typing import Dict, Any, List

from src.strategy.tyre_stint import (
    analyze_tyre_stint
)


# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_PIT_LOSS = 22.0

COMPOUNDS = [
    "SOFT",
    "MEDIUM",
    "HARD"
]


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_simulation_inputs(
    base_lap_time: float,
    current_tyre: str,
    tyre_age: int,
    remaining_laps: int,
    pit_loss: float
) -> None:
    """
    Validate inputs required by the strategy simulator.
    """

    if base_lap_time <= 0:

        raise ValueError(
            "base_lap_time must be greater than zero."
        )

    if not isinstance(
        current_tyre,
        str
    ) or not current_tyre.strip():

        raise ValueError(
            "current_tyre must be a valid compound."
        )

    if tyre_age < 0:

        raise ValueError(
            "tyre_age cannot be negative."
        )

    if remaining_laps <= 0:

        raise ValueError(
            "remaining_laps must be greater than zero."
        )

    if pit_loss < 0:

        raise ValueError(
            "pit_loss cannot be negative."
        )


# ============================================================
# SIMULATE STAY-OUT STRATEGY
# ============================================================

def simulate_stay_out(
    base_lap_time: float,
    current_tyre: str,
    tyre_age: int,
    remaining_laps: int
) -> Dict[str, Any]:
    """
    Simulate staying on the current tyre.

    No pit-stop loss is added.
    """

    stint = analyze_tyre_stint(

        base_lap_time=base_lap_time,

        compound=current_tyre,

        tyre_age=tyre_age,

        stint_length=remaining_laps

    )

    projected_time = (
        stint["TotalStintTime"]
    )

    return {

        "strategy":
            "STAY_OUT",

        "stops":
            0,

        "tyre_plan":
            current_tyre,

        "starting_tyre":
            current_tyre,

        "final_tyre":
            current_tyre,

        "stint_length":
            remaining_laps,

        "pit_loss":
            0.0,

        "projected_stint_time":
            round(
                projected_time,
                3
            ),

        "projected_total_time":
            round(
                projected_time,
                3
            ),

        "average_lap_time":
            round(
                stint["AverageLapTime"],
                3
            ),

        "degradation_impact":
            round(
                stint["DegradationImpact"],
                3
            ),

        "degradation_evaluation":
            stint.get(
                "DegradationEvaluation",
                "Unknown"
            )

    }


# ============================================================
# SIMULATE PIT STRATEGY
# ============================================================

def simulate_pit_strategy(
    base_lap_time: float,
    new_compound: str,
    remaining_laps: int,
    pit_loss: float
) -> Dict[str, Any]:
    """
    Simulate a pit-stop followed by a new tyre stint.

    The pit loss is added to the projected stint time.
    """

    stint = analyze_tyre_stint(

        base_lap_time=base_lap_time,

        compound=new_compound,

        tyre_age=0,

        stint_length=remaining_laps

    )

    projected_stint_time = (
        stint["TotalStintTime"]
    )

    projected_total_time = (
        projected_stint_time
        + pit_loss
    )

    return {

        "strategy":
            "PIT",

        "stops":
            1,

        "tyre_plan":
            f"PIT -> {new_compound}",

        "starting_tyre":
            new_compound,

        "final_tyre":
            new_compound,

        "stint_length":
            remaining_laps,

        "pit_loss":
            round(
                pit_loss,
                3
            ),

        "projected_stint_time":
            round(
                projected_stint_time,
                3
            ),

        "projected_total_time":
            round(
                projected_total_time,
                3
            ),

        "average_lap_time":
            round(
                stint["AverageLapTime"],
                3
            ),

        "degradation_impact":
            round(
                stint["DegradationImpact"],
                3
            ),

        "degradation_evaluation":
            stint.get(
                "DegradationEvaluation",
                "Unknown"
            )

    }


# ============================================================
# SIMULATE ALL STRATEGIES
# ============================================================

def simulate_all_strategies(
    base_lap_time: float,
    current_tyre: str,
    tyre_age: int,
    remaining_laps: int,
    pit_loss: float = DEFAULT_PIT_LOSS
) -> List[Dict[str, Any]]:
    """
    Simulate all currently available race strategies.

    Strategies:

        STAY OUT
        PIT -> SOFT
        PIT -> MEDIUM
        PIT -> HARD
    """

    validate_simulation_inputs(

        base_lap_time=base_lap_time,

        current_tyre=current_tyre,

        tyre_age=tyre_age,

        remaining_laps=remaining_laps,

        pit_loss=pit_loss

    )

    strategies = []

    # --------------------------------------------------------
    # STRATEGY 1 — STAY OUT
    # --------------------------------------------------------

    stay_out = simulate_stay_out(

        base_lap_time=base_lap_time,

        current_tyre=current_tyre,

        tyre_age=tyre_age,

        remaining_laps=remaining_laps

    )

    strategies.append(
        stay_out
    )

    # --------------------------------------------------------
    # STRATEGIES 2–4 — PIT
    # --------------------------------------------------------

    for compound in COMPOUNDS:

        pit_strategy = simulate_pit_strategy(

            base_lap_time=base_lap_time,

            new_compound=compound,

            remaining_laps=remaining_laps,

            pit_loss=pit_loss

        )

        strategies.append(
            pit_strategy
        )

    return strategies


# ============================================================
# RANK STRATEGIES
# ============================================================

def rank_strategies(
    strategies: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Rank strategies according to projected total time.

    Lower projected time = better projected strategy.
    """

    if not strategies:

        return []

    ranked = sorted(

        strategies,

        key=lambda strategy:
        strategy["projected_total_time"]

    )

    for rank, strategy in enumerate(

        ranked,

        start=1

    ):

        strategy[
            "strategy_rank"
        ] = rank

    return ranked


# ============================================================
# FIND BEST STRATEGY
# ============================================================

def get_best_strategy(
    strategies: List[Dict[str, Any]]
) -> Dict[str, Any] | None:
    """
    Return the strategy with the lowest projected time.
    """

    if not strategies:

        return None

    return min(

        strategies,

        key=lambda strategy:
        strategy["projected_total_time"]

    )


# ============================================================
# CALCULATE TIME DIFFERENCE
# ============================================================

def calculate_strategy_advantage(
    strategies: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Calculate the projected time advantage of each strategy
    relative to the best available strategy.
    """

    if not strategies:

        return []

    best_time = min(

        strategy["projected_total_time"]

        for strategy in strategies

    )

    for strategy in strategies:

        strategy[
            "time_difference"
        ] = round(

            strategy[
                "projected_total_time"
            ] - best_time,

            3

        )

    return strategies


# ============================================================
# COMPLETE STRATEGY SIMULATION
# ============================================================

def run_strategy_simulation(
    base_lap_time: float,
    current_tyre: str,
    tyre_age: int,
    remaining_laps: int,
    pit_loss: float = DEFAULT_PIT_LOSS
) -> Dict[str, Any]:
    """
    Run the complete Phase 3.5 strategy simulation.

    Returns:
        Complete simulation result containing:

        - candidate strategies
        - ranking
        - best strategy
        - projected advantage
    """

    strategies = simulate_all_strategies(

        base_lap_time=base_lap_time,

        current_tyre=current_tyre,

        tyre_age=tyre_age,

        remaining_laps=remaining_laps,

        pit_loss=pit_loss

    )

    ranked_strategies = rank_strategies(
        strategies
    )

    ranked_strategies = (
        calculate_strategy_advantage(
            ranked_strategies
        )
    )

    best_strategy = get_best_strategy(
        ranked_strategies
    )

    return {

        "strategy_count":
            len(ranked_strategies),

        "strategies":
            ranked_strategies,

        "best_strategy":
            best_strategy,

        "best_strategy_rank":
            (
                best_strategy[
                    "strategy_rank"
                ]
                if best_strategy
                else None
            )

    }


# ============================================================
# DISPLAY STRATEGY SIMULATION
# ============================================================

def display_strategy_simulation(
    result: Dict[str, Any]
) -> None:
    """
    Display strategy simulation results.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "STRATEGY SIMULATION"
    )

    print(
        "=" * 60
    )

    strategies = result.get(
        "strategies",
        []
    )

    if not strategies:

        print(
            "No strategies available."
        )

        return

    for strategy in strategies:

        print(
            f"\nRank: "
            f"{strategy['strategy_rank']}"
        )

        print(
            f"Strategy: "
            f"{strategy['strategy']}"
        )

        print(
            f"Tyre Plan: "
            f"{strategy['tyre_plan']}"
        )

        print(
            f"Stops: "
            f"{strategy['stops']}"
        )

        print(
            f"Stint Length: "
            f"{strategy['stint_length']} laps"
        )

        print(
            f"Pit Loss: "
            f"{strategy['pit_loss']:.3f}s"
        )

        print(
            f"Projected Stint Time: "
            f"{strategy['projected_stint_time']:.3f}s"
        )

        print(
            f"Projected Total Time: "
            f"{strategy['projected_total_time']:.3f}s"
        )

        print(
            f"Average Lap Time: "
            f"{strategy['average_lap_time']:.3f}s"
        )

        print(
            f"Degradation Impact: "
            f"{strategy['degradation_impact']:.3f}s"
        )

        print(
            f"Time Difference: "
            f"{strategy['time_difference']:.3f}s"
        )

    # --------------------------------------------------------
    # BEST STRATEGY
    # --------------------------------------------------------

    best = result.get(
        "best_strategy"
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "BEST PROJECTED STRATEGY"
    )

    print(
        "=" * 60
    )

    if best:

        print(
            f"Strategy: "
            f"{best['strategy']}"
        )

        print(
            f"Tyre Plan: "
            f"{best['tyre_plan']}"
        )

        print(
            f"Projected Total Time: "
            f"{best['projected_total_time']:.3f}s"
        )

        print(
            f"Strategy Rank: "
            f"{best['strategy_rank']}"
        )

    print(
        "=" * 60
    )


# ============================================================
# PHASE 3.5 TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n" + "=" * 60
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 3.5 — STRATEGY SIMULATION"
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
    # RUN SIMULATION
    # --------------------------------------------------------

    print(
        "\n[1/2] Simulating candidate strategies..."
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

    print(
        "Strategy simulation completed."
    )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    print(
        "\n[2/2] Ranking projected strategies..."
    )

    display_strategy_simulation(
        simulation_result
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    strategies = simulation_result[
        "strategies"
    ]

    assert len(strategies) == 4, (
        "Expected four candidate strategies."
    )

    assert (
        simulation_result[
            "best_strategy"
        ]
        is not None
    ), (
        "Best strategy was not generated."
    )

    assert all(

        "strategy_rank" in strategy

        for strategy in strategies

    ), (
        "Strategy ranking was not generated."
    )

    assert all(

        "projected_total_time"
        in strategy

        for strategy in strategies

    ), (
        "Projected strategy time missing."
    )

    assert (
        strategies[0]["strategy_rank"]
        == 1
    ), (
        "Best strategy is not ranked first."
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "✅ PHASE 3.5 STRATEGY SIMULATION TEST PASSED"
    )

    print(
        "=" * 60
    )