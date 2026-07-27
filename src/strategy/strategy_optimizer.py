"""
strategy_optimizer.py

Sprint 3 - Step 3

Simulates every generated strategy and evaluates the
selected tyre compound before ranking.
"""

from src.strategy.strategy_generator import (
    generate_strategies
)

from src.strategy.simulator import (
    simulate_strategy
)


# ============================================================
# SIMULATE A SINGLE STRATEGY
# ============================================================

def simulate_strategy_plan(
    strategy: dict,
    race_state: dict,
    track: str
) -> dict:
    """
    Simulate one complete strategy and estimate the
    total race time.
    """

    laps_remaining = race_state.get("LapsRemaining")

    if laps_remaining is None or laps_remaining <= 0:
        raise ValueError(
            "Invalid number of laps remaining."
        )

    current_compound = race_state.get(
        "TyreCompound"
    )

    current_lap_time = race_state.get(
        "AveragePace"
    )

    current_driver = race_state.get(
        "Driver"
    )

    current_lap = race_state.get(
        "CurrentLap"
    )

    if current_lap_time is None:
        raise ValueError(
            "AveragePace is missing."
        )

    pit_lap = strategy.get("pit_lap")

    new_compound = strategy.get("compound_after_pit")

    if pit_lap is None or new_compound is None:
        raise ValueError(
        "Strategy is missing pit_lap or compound_after_pit."
    )

    total_time = 0.0

    current_tyre = current_compound

    for lap_offset in range(laps_remaining):

        simulated_lap = current_lap + lap_offset

        remaining = laps_remaining - lap_offset

        if simulated_lap == pit_lap:

            simulation = simulate_strategy(

                track=track,

                driver=current_driver,

                tyre_compound=new_compound,

                predicted_lap_time=current_lap_time,

                laps_remaining=remaining

            )

            total_time += simulation[
                "pit_now_time"
            ]

            current_tyre = new_compound

        else:

            simulation = simulate_strategy(

                track=track,

                driver=current_driver,

                tyre_compound=current_tyre,

                predicted_lap_time=current_lap_time,

                laps_remaining=remaining

            )

            total_time += simulation[
                "stay_out_time"
            ]

    result = strategy.copy()

    result["PredictedRaceTime"] = round(
        total_time,
        2
    )

    return result


# ============================================================
# SIMULATE ALL STRATEGIES
# ============================================================

def simulate_candidate_strategies(
    race_state: dict,
    track: str
) -> list:
    """
    Simulate every generated strategy.
    """

    candidates = generate_strategies(
    current_lap=race_state["CurrentLap"],
    laps_remaining=race_state["LapsRemaining"],
    current_compound=race_state["TyreCompound"]
)

    results = []

    for strategy in candidates:

        simulated = simulate_strategy_plan(

            strategy=strategy,

            race_state=race_state,

            track=track

        )

        results.append(
            simulated
        )

    return results


# ============================================================
# EVALUATE TYRE COMPOUND
# ============================================================

def evaluate_strategy_compound(
    strategy: dict,
    race_state: dict
) -> dict:
    """
    Evaluate whether the selected tyre compound
    is suitable for the remaining race distance.
    """

    laps_after_pit = (

        race_state["LapsRemaining"]

        -

        (

            strategy["pit_lap"]

            -

            race_state["CurrentLap"]

        )

    )

    compound = strategy["compound_after_pit"]

    score = 50

    evaluation = "Average"

    # --------------------------------------------------------
    # SOFT
    # --------------------------------------------------------

    if compound == "SOFT":

        if laps_after_pit <= 12:

            score = 95
            evaluation = "Excellent"

        elif laps_after_pit <= 18:

            score = 80
            evaluation = "Good"

        else:

            score = 45
            evaluation = "Poor"

    # --------------------------------------------------------
    # MEDIUM
    # --------------------------------------------------------

    elif compound == "MEDIUM":

        if laps_after_pit <= 22:

            score = 90
            evaluation = "Excellent"

        elif laps_after_pit <= 30:

            score = 82
            evaluation = "Good"

        else:

            score = 65
            evaluation = "Average"

    # --------------------------------------------------------
    # HARD
    # --------------------------------------------------------

    elif compound == "HARD":

        if laps_after_pit >= 20:

            score = 94
            evaluation = "Excellent"

        elif laps_after_pit >= 12:

            score = 84
            evaluation = "Good"

        else:

            score = 60
            evaluation = "Average"

    strategy["CompoundScore"] = score
    strategy["CompoundEvaluation"] = evaluation
    strategy["LapsAfterPit"] = laps_after_pit

    return strategy

# ============================================================
# EVALUATE ALL STRATEGIES
# ============================================================

def evaluate_all_strategies(
    strategies: list,
    race_state: dict
) -> list:
    """
    Evaluate every simulated strategy.
    """

    evaluated = []

    for strategy in strategies:

        evaluated.append(

            evaluate_strategy_compound(

                strategy,

                race_state

            )

        )

    return evaluated

# ============================================================
# PIT WINDOW OPTIMISATION
# ============================================================

def evaluate_pit_window(
    strategy: dict,
    race_state: dict
) -> dict:
    """
    Evaluate how suitable the selected pit lap is.

    A simple scoring model is used based on:
    - Current lap
    - Remaining laps
    - Distance after the pit stop
    """

    current_lap = race_state["CurrentLap"]

    laps_remaining = race_state["LapsRemaining"]

    pit_lap = strategy["pit_lap"]

    laps_after_pit = laps_remaining - (
        pit_lap - current_lap
    )

    score = 50

    evaluation = "Average"

    recommended = False

    # ---------------------------------------------
    # Excellent Window
    # ---------------------------------------------

    if 15 <= laps_after_pit <= 25:

        score = 95

        evaluation = "Excellent"

        recommended = True

    # ---------------------------------------------
    # Good Window
    # ---------------------------------------------

    elif 10 <= laps_after_pit < 15:

        score = 85

        evaluation = "Good"

    elif 25 < laps_after_pit <= 30:

        score = 82

        evaluation = "Good"

    # ---------------------------------------------
    # Average Window
    # ---------------------------------------------

    elif 5 <= laps_after_pit < 10:

        score = 70

        evaluation = "Average"

    elif laps_after_pit > 30:

        score = 65

        evaluation = "Average"

    # ---------------------------------------------
    # Poor Window
    # ---------------------------------------------

    else:

        score = 40

        evaluation = "Poor"

    strategy["PitWindowScore"] = score

    strategy["PitWindowEvaluation"] = evaluation

    strategy["RecommendedWindow"] = recommended

    return strategy


# ============================================================
# OPTIMISE PIT WINDOWS
# ============================================================

def optimise_pit_windows(
    strategies: list,
    race_state: dict
) -> list:
    """
    Evaluate every strategy's pit window.
    """

    optimised = []

    for strategy in strategies:

        optimised.append(

            evaluate_pit_window(

                strategy,

                race_state

            )

        )

    return optimised

# ============================================================
# STRATEGY RANKING ENGINE
# ============================================================

def calculate_strategy_score(
    strategy: dict
) -> float:
    """
    Calculate an overall strategy score.

    Higher score = Better strategy.
    """

    race_time = strategy.get(
        "PredictedRaceTime",
        999999.0
    )

    compound_score = strategy.get(
        "CompoundScore",
        0
    )

    pit_score = strategy.get(
        "PitWindowScore",
        0
    )

    total_score = (

        compound_score * 0.40

        +

        pit_score * 0.30

        +

        max(
            0,
            100 - (race_time / 100)
        ) * 0.30

    )

    strategy["StrategyScore"] = round(
        total_score,
        2
    )

    return strategy


# ============================================================
# RANK STRATEGIES
# ============================================================

def rank_strategies(
    strategies: list
) -> list:
    """
    Rank every candidate strategy from best
    to worst.
    """

    ranked = []

    for strategy in strategies:

        ranked.append(

            calculate_strategy_score(
                strategy
            )

        )

    ranked.sort(

        key=lambda x: x["StrategyScore"],

        reverse=True

    )

    for index, strategy in enumerate(

        ranked,

        start=1

    ):

        strategy["Rank"] = index

    return ranked

# ============================================================
# OPTIMAL STRATEGY SELECTION
# ============================================================

def select_optimal_strategy(
    ranked_strategies: list
) -> dict | None:
    """
    Select the highest-ranked strategy.

    Parameters
    ----------
    ranked_strategies : list

    Returns
    -------
    dict | None
        Best strategy if available.
    """

    if not ranked_strategies:

        return None

    best_strategy = ranked_strategies[0].copy()

    best_strategy["SelectedStrategy"] = True

    return best_strategy


# ============================================================
# DISPLAY BEST STRATEGY
# ============================================================

def display_best_strategy(
    strategy: dict | None
) -> None:
    """
    Print the selected optimal strategy.
    """

    print("\n" + "=" * 60)
    print("OPTIMAL STRATEGY")
    print("=" * 60)

    if strategy is None:

        print("No valid strategy found.")

    else:

        for key, value in strategy.items():

            print(f"{key}: {value}")

    print("=" * 60)
# ============================================================
# COMPLETE STRATEGY PIPELINE
# ============================================================

def run_strategy_pipeline(
    race_state: dict,
    track: str
) -> dict:
    """
    Execute the complete strategy optimisation pipeline.
    """

    simulated = simulate_candidate_strategies(
        race_state,
        track
    )

    evaluated = evaluate_all_strategies(
        simulated,
        race_state
    )

    optimised = optimise_pit_windows(
        evaluated,
        race_state
    )

    ranked = rank_strategies(
        optimised
    )

    best = select_optimal_strategy(
        ranked
    )

    return {
        "best_strategy": best,
        "ranked_strategies": ranked
    }

# ============================================================
# STRATEGY RECOMMENDATION ENGINE
# ============================================================

def generate_strategy_recommendation(
    strategy: dict | None
) -> str:
    """
    Generate a human-readable recommendation for the
    selected strategy.
    """

    if strategy is None:

        return (
            "No valid strategy recommendation "
            "could be generated."
        )

    pit_lap = strategy["pit_lap"]

    compound = strategy["compound_after_pit"]

    score = strategy["StrategyScore"]

    recommendation = (
        f"Pit on Lap {pit_lap} and switch to "
        f"{compound} tyres.\n"
        f"Overall Strategy Score: {score}"
    )

    return recommendation


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from src.data_loader import (
        load_session
    )

    from src.race_state import (
        build_race_state
    )

    print("=" * 60)
    print("SPRINT 3 - STEP 8 TEST")
    print("=" * 60)

    session = load_session(

        2025,

        "British Grand Prix",

        "R"

    )

    race_state = build_race_state(

        session,

        "VER"

    )

    pipeline = run_strategy_pipeline(

        race_state,

        race_state["Circuit"]

    )

    ranked = pipeline["ranked_strategies"]

    best = pipeline["best_strategy"]

    print("\nRANKED STRATEGIES")
    print("=" * 60)

    for strategy in ranked:

        print(strategy)

    display_best_strategy(

        best

    )

    print("\nSTRATEGY RECOMMENDATION")
    print("=" * 60)

    recommendation = generate_strategy_recommendation(

        best

    )

    print(recommendation)

    print("=" * 60)
    print("STEP 8 COMPLETED")
    print("=" * 60)