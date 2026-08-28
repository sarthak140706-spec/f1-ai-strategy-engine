"""
dynamic_strategy_simulation.py

PHASE 4.5 — DYNAMIC STRATEGY SIMULATION

Purpose
-------
Simulate and compare strategic options using the reconstructed
race state produced by Phase 4.1.

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
Candidate Strategy Simulation
        ↓
Projected Remaining-Race Time
        ↓
Dynamic Strategy Ranking


This module does NOT:
    - rebuild race state
    - analyze race situation
    - make the final AI recommendation
    - perform final strategy scoring

Those responsibilities belong to other Phase 4 modules.
"""

from typing import Dict, Any, List

from src.strategy.strategy_simulation import (
    run_strategy_simulation
)


# ============================================================
# DEFAULT CONFIGURATION
# ============================================================

DEFAULT_PIT_LOSS = 22.0


# ============================================================
# HELPERS
# ============================================================

def _safe_float(
    value,
    default=None
):
    """
    Safely convert a value to float.
    """

    if value is None:
        return default

    try:

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


def _safe_int(
    value,
    default=None
):
    """
    Safely convert a value to int.
    """

    if value is None:
        return default

    try:

        return int(value)

    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_dynamic_simulation_inputs(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any],
    tyre_strategy: Dict[str, Any],
    pit_decision: Dict[str, Any]
) -> None:
    """
    Validate Phase 4.5 inputs.
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


    current_lap = race_state.get(
        "CurrentLap"
    )

    remaining_laps = race_state.get(
        "LapsRemaining"
    )

    current_tyre = race_state.get(
        "TyreCompound"
    )

    tyre_life = race_state.get(
        "TyreLife"
    )

    recent_pace = race_state.get(
        "RecentPace"
    )


    if current_lap is None:

        raise ValueError(
            "CurrentLap is missing from race_state."
        )


    if remaining_laps is None:

        raise ValueError(
            "LapsRemaining is missing from race_state."
        )


    if int(
        remaining_laps
    ) <= 0:

        raise ValueError(
            "Dynamic simulation requires "
            "remaining laps greater than zero."
        )


    if current_tyre is None:

        raise ValueError(
            "TyreCompound is missing from race_state."
        )


    if tyre_life is None:

        raise ValueError(
            "TyreLife is missing from race_state."
        )


    if recent_pace is None:

        raise ValueError(
            "RecentPace is missing from race_state."
        )


# ============================================================
# DETERMINE PIT LOSS
# ============================================================

def determine_dynamic_pit_loss(
    pit_decision: Dict[str, Any]
) -> float:
    """
    Determine pit-stop loss from Phase 4.4.

    Falls back to the standard 22-second estimate.
    """

    pit_loss = _safe_float(

        pit_decision.get(
            "pit_loss"
        ),

        DEFAULT_PIT_LOSS

    )


    if pit_loss is None:

        pit_loss = DEFAULT_PIT_LOSS


    if pit_loss < 0:

        pit_loss = DEFAULT_PIT_LOSS


    return round(
        pit_loss,
        3
    )


# ============================================================
# DETERMINE BASE PACE
# ============================================================

def determine_dynamic_base_pace(
    race_state: Dict[str, Any]
) -> float:
    """
    Determine the base pace used by the simulator.

    Priority:

        RecentPace
            ↓
        AvgPaceLast3
            ↓
        AvgPaceLast5
            ↓
        AveragePace
    """

    candidates = [

        race_state.get(
            "RecentPace"
        ),

        race_state.get(
            "AvgPaceLast3"
        ),

        race_state.get(
            "AvgPaceLast5"
        ),

        race_state.get(
            "AveragePace"
        )

    ]


    for value in candidates:

        pace = _safe_float(
            value
        )

        if (
            pace is not None
            and pace > 0
        ):

            return pace


    raise ValueError(
        "No valid base pace is available "
        "for dynamic strategy simulation."
    )


# ============================================================
# NORMALIZE PHASE 3 SIMULATION STRATEGY
# ============================================================

def normalize_strategy(
    strategy: Dict[str, Any],
    race_state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add Phase 4 dynamic context to a simulated strategy.
    """

    result = strategy.copy()


    result[
        "simulation_lap"
    ] = race_state.get(
        "CurrentLap"
    )


    result[
        "position_at_simulation"
    ] = race_state.get(
        "Position"
    )


    result[
        "current_tyre_age"
    ] = race_state.get(
        "TyreLife"
    )


    result[
        "laps_remaining"
    ] = race_state.get(
        "LapsRemaining"
    )


    result[
        "dynamic_simulation"
    ] = True


    return result


# ============================================================
# FIND STRATEGY SELECTED BY PIT DECISION
# ============================================================

def identify_pit_decision_strategy(
    strategies: List[Dict[str, Any]],
    pit_decision: Dict[str, Any]
):
    """
    Find the strategy corresponding to the Phase 4.4 decision.
    """

    decision = (

        pit_decision.get(
            "decision"
        )

        or pit_decision.get(
            "action"
        )

        or ""

    )


    decision = (
        str(decision)
        .strip()
        .upper()
        .replace("_", " ")
    )


    recommended_tyre = (

        pit_decision.get(
            "recommended_tyre"
        )

        or ""

    )


    recommended_tyre = (
        str(recommended_tyre)
        .strip()
        .upper()
    )


    # --------------------------------------------------------
    # STAY OUT
    # --------------------------------------------------------

    if decision == "STAY OUT":

        for strategy in strategies:

            if (
                strategy.get(
                    "strategy"
                )
                ==
                "STAY_OUT"
            ):

                return strategy


    # --------------------------------------------------------
    # PIT
    # --------------------------------------------------------

    if decision in {

        "PIT",

        "PIT NOW"

    }:

        for strategy in strategies:

            if (
                strategy.get(
                    "strategy"
                )
                ==
                "PIT"
            ):

                final_tyre = str(

                    strategy.get(
                        "final_tyre",
                        ""
                    )

                ).upper()


                if (
                    final_tyre
                    ==
                    recommended_tyre
                ):

                    return strategy


    return None


# ============================================================
# DYNAMIC SIMULATION
# ============================================================

def run_dynamic_strategy_simulation(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any],
    tyre_strategy: Dict[str, Any],
    pit_decision: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Run Phase 4.5 dynamic strategy simulation.
    """

    validate_dynamic_simulation_inputs(

        race_state=race_state,

        race_situation=race_situation,

        tyre_strategy=tyre_strategy,

        pit_decision=pit_decision

    )


    # ========================================================
    # EXTRACT DYNAMIC INPUTS
    # ========================================================

    current_lap = _safe_int(

        race_state.get(
            "CurrentLap"
        )

    )


    remaining_laps = _safe_int(

        race_state.get(
            "LapsRemaining"
        )

    )


    current_tyre = str(

        race_state.get(
            "TyreCompound"
        )

    ).strip().upper()


    tyre_age = _safe_int(

        race_state.get(
            "TyreLife"
        ),

        0

    )


    base_lap_time = (
        determine_dynamic_base_pace(
            race_state
        )
    )


    pit_loss = (
        determine_dynamic_pit_loss(
            pit_decision
        )
    )


    # ========================================================
    # RUN EXISTING PHASE 3.5 SIMULATOR
    # ========================================================

    simulation = run_strategy_simulation(

        base_lap_time=float(
            base_lap_time
        ),

        current_tyre=current_tyre,

        tyre_age=int(
            tyre_age
        ),

        remaining_laps=int(
            remaining_laps
        ),

        pit_loss=float(
            pit_loss
        )

    )


    strategies = simulation.get(
        "strategies",
        []
    )


    if not strategies:

        raise RuntimeError(
            "No dynamic strategy simulations "
            "were generated."
        )


    # ========================================================
    # ADD DYNAMIC CONTEXT
    # ========================================================

    dynamic_strategies = [

        normalize_strategy(

            strategy=strategy,

            race_state=race_state

        )

        for strategy in strategies

    ]


    # ========================================================
    # BEST PROJECTED STRATEGY
    # ========================================================

    best_strategy = min(

        dynamic_strategies,

        key=lambda item:
            item[
                "projected_total_time"
            ]

    )


    # ========================================================
    # PHASE 4.4 SELECTED STRATEGY
    # ========================================================

    decision_strategy = (
        identify_pit_decision_strategy(

            strategies=dynamic_strategies,

            pit_decision=pit_decision

        )
    )


    # ========================================================
    # STRATEGY AGREEMENT
    # ========================================================

    decision_matches_simulation = False


    if decision_strategy is not None:

        decision_matches_simulation = (

            decision_strategy.get(
                "strategy_rank"
            )
            ==
            1

        )


    # ========================================================
    # TYRE ENGINE RECOMMENDATION
    # ========================================================

    tyre_recommendation = (

        tyre_strategy.get(
            "Recommendation"
        )

        or

        tyre_strategy.get(
            "recommendation"
        )

    )


    tyre_compound = (

        tyre_strategy.get(
            "Compound"
        )

        or

        tyre_strategy.get(
            "recommended_compound"
        )

        or

        tyre_strategy.get(
            "recommended_tyre"
        )

    )


    # ========================================================
    # RACE SITUATION
    # ========================================================

    situation = (

        race_situation.get(
            "race_situation"
        )

        or

        race_situation.get(
            "RaceSituation"
        )

        or

        race_situation.get(
            "situation"
        )

    )


    # ========================================================
    # RESULT
    # ========================================================

    return {

        "dynamic_simulation":
            True,

        "current_lap":
            current_lap,

        "remaining_laps":
            remaining_laps,

        "position":
            race_state.get(
                "Position"
            ),

        "current_tyre":
            current_tyre,

        "current_tyre_age":
            race_state.get(
                "TyreLife"
            ),

        "base_lap_time":
            round(
                float(
                    base_lap_time
                ),
                3
            ),

        "pit_loss":
            pit_loss,

        "race_situation":
            situation,

        "tyre_recommendation":
            tyre_recommendation,

        "tyre_recommended_compound":
            tyre_compound,

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

        "strategy_count":
            len(
                dynamic_strategies
            ),

        "strategies":
            dynamic_strategies,

        "best_strategy":
            best_strategy,

        "best_strategy_rank":
            best_strategy.get(
                "strategy_rank"
            ),

        "pit_decision_strategy":
            decision_strategy,

        "decision_matches_simulation":
            decision_matches_simulation

    }


# ============================================================
# DISPLAY DYNAMIC SIMULATION
# ============================================================

def display_dynamic_strategy_simulation(
    result: Dict[str, Any]
) -> None:
    """
    Display Phase 4.5 strategy simulation.
    """

    print(
        "\n" + "=" * 72
    )

    print(
        "PHASE 4.5 — DYNAMIC STRATEGY SIMULATION"
    )

    print(
        "=" * 72
    )


    print(
        f"Current Lap: "
        f"{result.get('current_lap')}"
    )


    print(
        f"Remaining Laps: "
        f"{result.get('remaining_laps')}"
    )


    print(
        f"Position: P"
        f"{result.get('position')}"
    )


    print(
        f"Current Tyre: "
        f"{result.get('current_tyre')}"
    )


    print(
        f"Tyre Age: "
        f"{result.get('current_tyre_age')}"
    )


    print(
        f"Base Lap Time: "
        f"{result.get('base_lap_time')}s"
    )


    print(
        f"Pit Loss: "
        f"{result.get('pit_loss')}s"
    )


    print(
        f"Race Situation: "
        f"{result.get('race_situation')}"
    )


    print(
        f"Phase 4.4 Decision: "
        f"{result.get('pit_decision')}"
    )


    print(
        "-" * 72
    )

    print(
        "DYNAMIC STRATEGY COMPARISON"
    )

    print(
        "-" * 72
    )


    strategies = result.get(
        "strategies",
        []
    )


    for strategy in strategies:

        print(

            f"Rank "
            f"{strategy.get('strategy_rank')}"

            f" | "

            f"{strategy.get('tyre_plan')}"

            f" | Stops: "
            f"{strategy.get('stops')}"

            f" | Time: "
            f"{strategy.get('projected_total_time'):.3f}s"

            f" | Avg Lap: "
            f"{strategy.get('average_lap_time'):.3f}s"

            f" | Diff: +"
            f"{strategy.get('time_difference'):.3f}s"

        )


    print(
        "-" * 72
    )


    best = result.get(
        "best_strategy"
    )


    if best:

        print(
            f"Best Strategy: "
            f"{best.get('tyre_plan')}"
        )

        print(
            f"Projected Time: "
            f"{best.get('projected_total_time')}s"
        )

        print(
            f"Strategy Rank: "
            f"{best.get('strategy_rank')}"
        )


    print(
        f"Pit Decision Matches Simulation: "
        f"{result.get('decision_matches_simulation')}"
    )


    print(
        "=" * 72
    )