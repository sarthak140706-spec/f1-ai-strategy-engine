"""
overtake_model.py

Sprint 5 - Step 7

Evaluates undercut and overcut opportunities
based on current race gaps and tyre age.
"""

from typing import Dict


# ============================================================
# UNDERCUT / OVERCUT ANALYSIS
# ============================================================

def analyse_overtake_strategy(
    gap_data: Dict,
    race_state: Dict
) -> Dict:
    """
    Analyse whether an undercut or overcut
    opportunity exists.
    """

    gap_ahead = gap_data.get(
        "GapAhead"
    )

    tyre_age = race_state.get(
        "TyreAge",
        0
    )

    undercut = False

    overcut = False

    recommendation = (
        "Maintain current strategy."
    )

    # --------------------------------------------------------
    # UNDERCUT
    # --------------------------------------------------------

    if (

        gap_ahead is not None

        and gap_ahead <= 3

        and tyre_age >= 15

    ):

        undercut = True

        recommendation = (
            "Undercut opportunity detected."
        )

    # --------------------------------------------------------
    # OVERCUT
    # --------------------------------------------------------

    elif (

        gap_ahead is not None

        and gap_ahead > 5

        and tyre_age <= 10

    ):

        overcut = True

        recommendation = (
            "Overcut opportunity detected."
        )

    return {

        "UndercutAvailable":
            undercut,

        "OvercutAvailable":
            overcut,

        "Recommendation":
            recommendation

    }


# ============================================================
# DISPLAY
# ============================================================

def display_overtake_strategy(
    result: Dict
) -> None:

    print("\n" + "=" * 60)
    print("UNDERCUT / OVERCUT ANALYSIS")
    print("=" * 60)

    for key, value in result.items():

        print(f"{key}: {value}")

    print("=" * 60)


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

    from src.strategy.gap_model import (
        get_gap_information,
        evaluate_gap
    )

    session = load_session(

        2025,

        "British Grand Prix",

        "R"

    )

    race_state = build_race_state(

        session,

        "VER"

    )

    gap = get_gap_information(

        session,

        "VER"

    )

    gap = evaluate_gap(

        gap

    )

    result = analyse_overtake_strategy(

        gap,

        race_state

    )

    display_overtake_strategy(

        result

    )