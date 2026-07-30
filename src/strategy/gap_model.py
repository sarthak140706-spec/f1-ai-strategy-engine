"""
gap_model.py

Sprint 5 - Step 6

Estimates the gap to the car ahead and behind
using FastF1 timing information.
"""

from typing import Dict


# ============================================================
# GAP ANALYSIS
# ============================================================

def get_gap_information(
    session,
    driver: str
) -> Dict:
    """
    Estimate race gaps around the selected driver.
    """

    try:

        laps = session.laps.pick_drivers(
            driver
        )

        if laps.empty:

            raise ValueError

        latest = laps.iloc[-1]

        position = int(
            latest["Position"]
        )

        total_drivers = int(
            session.laps["Driver"].nunique()
        )

        # ----------------------------------------------------
        # Placeholder gap estimation.
        #
        # Future Sprint:
        # Replace with true timing interval
        # calculations using FastF1 timing data.
        # ----------------------------------------------------

        if position == 1:

            gap_ahead = None

        else:

            gap_ahead = round(
                position * 1.5,
                2
            )

        if position == total_drivers:

            gap_behind = None

        else:

            gap_behind = round(
                (total_drivers - position) * 1.3,
                2
            )

        return {

            "Position":
                position,

            "GapAhead":
                gap_ahead,

            "GapBehind":
                gap_behind

        }

    except Exception:

        return {

            "Position": None,

            "GapAhead": None,

            "GapBehind": None

        }


# ============================================================
# GAP EVALUATION
# ============================================================

def evaluate_gap(
    gap_data: Dict
) -> Dict:
    """
    Evaluate whether the current race gaps
    provide strategic flexibility.
    """

    gap_ahead = gap_data.get(
        "GapAhead"
    )

    gap_behind = gap_data.get(
        "GapBehind"
    )

    status = "UNKNOWN"

    if gap_ahead is None:

        status = "LEADING"

    elif gap_ahead >= 5:

        status = "SAFE"

    elif gap_ahead >= 2:

        status = "MODERATE"

    else:

        status = "CLOSE"

    gap_data["GapStatus"] = status

    if gap_behind is None:

        gap_data["RearRisk"] = "NONE"

    elif gap_behind < 2:

        gap_data["RearRisk"] = "HIGH"

    elif gap_behind < 5:

        gap_data["RearRisk"] = "MEDIUM"

    else:

        gap_data["RearRisk"] = "LOW"

    return gap_data


# ============================================================
# DISPLAY
# ============================================================

def display_gap_information(
    gap_data: Dict
) -> None:

    print("\n" + "=" * 60)
    print("GAP ANALYSIS")
    print("=" * 60)

    for key, value in gap_data.items():

        print(f"{key}: {value}")

    print("=" * 60)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from src.data_loader import (
        load_session
    )

    session = load_session(

        2025,

        "British Grand Prix",

        "R"

    )

    gap = get_gap_information(

        session,

        "VER"

    )

    gap = evaluate_gap(

        gap

    )

    display_gap_information(

        gap
    )