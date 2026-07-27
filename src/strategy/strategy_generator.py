"""
strategy_generator.py

Sprint 3 - Step 1

Purpose:
--------
Generate possible future pit strategies.

This module does NOT:
    - simulate strategies
    - rank strategies
    - select the optimal strategy

It only creates candidate strategies.

Pipeline:

Race State
     |
     ▼
Strategy Generator
     |
     ▼
Candidate Strategies
     |
     ▼
Multi Lap Simulator (Sprint 3 Step 2)
"""


from typing import Dict, List, Any


# ============================================================
# DEFAULT CONFIGURATION
# ============================================================


AVAILABLE_COMPOUNDS = [

    "SOFT",

    "MEDIUM",

    "HARD"

]


# Minimum and maximum laps to consider
# around the current lap.

DEFAULT_PIT_WINDOW = 10



# ============================================================
# GENERATE PIT WINDOWS
# ============================================================


def generate_pit_windows(
    current_lap: int,
    laps_remaining: int,
    window: int = DEFAULT_PIT_WINDOW
) -> List[int]:
    """
    Generate possible pit stop laps.

    Example:

    Current lap = 20

    Generates:

    [22,24,26,28,30]

    """

    if current_lap is None:

        return []


    if laps_remaining <= 0:

        return []


    start = current_lap + 2


    end = min(

        current_lap + window,

        current_lap + laps_remaining

    )


    pit_windows = list(

        range(

            start,

            end + 1,

            2

        )

    )


    return pit_windows



# ============================================================
# GENERATE COMPOUND OPTIONS
# ============================================================


def generate_compound_options(
    current_compound: str
) -> List[str]:
    """
    Generate possible tyre choices after pit stop.

    Current tyre is removed because
    switching to another compound is
    usually strategically preferred.

    """

    compounds = AVAILABLE_COMPOUNDS.copy()


    current_compound = (

        str(current_compound)
        .upper()

        if current_compound

        else None

    )


    if current_compound in compounds:

        compounds.remove(
            current_compound
        )


    return compounds



# ============================================================
# CREATE STRATEGY
# ============================================================


def create_strategy(
    pit_lap: int,
    tyre: str
) -> Dict[str, Any]:
    """
    Create one strategy object.
    """

    return {


        "pit_lap":
            pit_lap,


        "compound_after_pit":
            tyre,


        "strategy_type":
            "ONE_STOP"


    }



# ============================================================
# GENERATE STRATEGIES
# ============================================================


def generate_strategies(
    current_lap: int,
    laps_remaining: int,
    current_compound: str
) -> List[Dict[str, Any]]:
    """
    Generate all possible candidate strategies.

    Parameters
    ----------

    current_lap:
        Current race lap.


    laps_remaining:
        Remaining race distance.


    current_compound:
        Current tyre compound.



    Returns
    -------

    List of possible strategies.


    Example output:

    [
        {
            "pit_lap":25,
            "compound_after_pit":"HARD",
            "strategy_type":"ONE_STOP"
        },

        {
            "pit_lap":27,
            "compound_after_pit":"MEDIUM",
            "strategy_type":"ONE_STOP"
        }
    ]

    """


    strategies = []


    pit_windows = generate_pit_windows(

        current_lap,

        laps_remaining

    )


    compounds = generate_compound_options(

        current_compound

    )



    for pit_lap in pit_windows:


        for compound in compounds:


            strategy = create_strategy(

                pit_lap,

                compound

            )


            strategies.append(

                strategy

            )


    return strategies



# ============================================================
# DISPLAY STRATEGIES
# ============================================================


def print_strategies(
    strategies: List[Dict[str, Any]]
):
    """
    Display generated strategies.
    """


    print()

    print("=" * 60)

    print(
        "GENERATED STRATEGIES"
    )

    print("=" * 60)



    for index, strategy in enumerate(

        strategies,

        start=1

    ):

        print(

            f"{index}. "
            f"Pit Lap: {strategy['pit_lap']} | "
            f"After Pit: {strategy['compound_after_pit']} | "
            f"Type: {strategy['strategy_type']}"

        )


    print("=" * 60)


# ============================================================
# GENERATE CANDIDATE STRATEGIES
# ============================================================

def generate_candidate_strategies(
    race_state: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Wrapper used by the strategy optimizer.

    Converts the race_state dictionary into the
    inputs required by generate_strategies().
    """

    return generate_strategies(

        current_lap=race_state["CurrentLap"],

        laps_remaining=race_state["LapsRemaining"],

        current_compound=race_state["TyreCompound"]

    )
# ============================================================
# TESTING
# ============================================================


if __name__ == "__main__":


    print(
        "=" * 60
    )


    print(
        "SPRINT 3 - STEP 1"
    )


    print(
        "STRATEGY GENERATOR TEST"
    )


    print(
        "=" * 60
    )



    # Example race state

    CURRENT_LAP = 25

    LAPS_REMAINING = 30

    CURRENT_TYRE = "MEDIUM"



    strategies = generate_strategies(

        current_lap=CURRENT_LAP,

        laps_remaining=LAPS_REMAINING,

        current_compound=CURRENT_TYRE

    )


    print_strategies(

        strategies

    )


    print()

    print(
        f"Total Strategies Generated: {len(strategies)}"
    )


    print()

    print(
        "STEP 1 TEST COMPLETED"
    )


    print(
        "=" * 60
    )