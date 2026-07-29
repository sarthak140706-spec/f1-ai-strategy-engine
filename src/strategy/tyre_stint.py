"""
tyre_stint.py

Sprint 4 - Step 4

Analyzes tyre stint performance using the tyre degradation model.

The module:
- Predicts lap times across a stint
- Calculates total stint time
- Calculates average lap time
- Calculates degradation impact
- Compares different tyre compounds
"""

from src.strategy.tyre_model import (
    predict_degraded_lap_time,
    generate_degradation_profile,
    estimate_stint_time
)


# ============================================================
# ANALYZE SINGLE TYRE STINT
# ============================================================

def analyze_tyre_stint(
    base_lap_time: float,
    compound: str,
    tyre_age: int,
    stint_length: int
) -> dict:
    """
    Analyze the performance of one tyre stint.

    Parameters
    ----------
    base_lap_time : float
        Base lap time in seconds.

    compound : str
        Tyre compound.

    tyre_age : int
        Current age of the tyre set.

    stint_length : int
        Number of laps in the stint.

    Returns
    -------
    dict
        Complete stint performance analysis.
    """

    if base_lap_time <= 0:
        raise ValueError(
            "Base lap time must be positive."
        )

    if tyre_age < 0:
        raise ValueError(
            "Tyre age cannot be negative."
        )

    if stint_length <= 0:
        raise ValueError(
            "Stint length must be greater than zero."
        )

    profile = generate_degradation_profile(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age,

        laps=stint_length

    )

    total_stint_time = estimate_stint_time(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age,

        stint_length=stint_length

    )

    first_lap_time = profile[0][
        "PredictedLapTime"
    ]

    last_lap_time = profile[-1][
        "PredictedLapTime"
    ]

    average_lap_time = (
        total_stint_time
        / stint_length
    )

    degradation_impact = (
        last_lap_time
        - first_lap_time
    )

    result = {

        "Compound": compound.upper(),

        "StartingTyreAge": tyre_age,

        "StintLength": stint_length,

        "FirstLapTime": round(
            first_lap_time,
            3
        ),

        "LastLapTime": round(
            last_lap_time,
            3
        ),

        "AverageLapTime": round(
            average_lap_time,
            3
        ),

        "TotalStintTime": round(
            total_stint_time,
            3
        ),

        "DegradationImpact": round(
            degradation_impact,
            3
        ),

        "Profile": profile

    }

    return result


# ============================================================
# COMPARE TYRE COMPOUNDS
# ============================================================

def compare_tyre_compounds(
    base_lap_time: float,
    tyre_age: int,
    stint_length: int
) -> list:
    """
    Compare all available tyre compounds
    for the same stint length.
    """

    compounds = [

        "SOFT",

        "MEDIUM",

        "HARD"

    ]

    comparisons = []

    for compound in compounds:

        analysis = analyze_tyre_stint(

            base_lap_time=base_lap_time,

            compound=compound,

            tyre_age=tyre_age,

            stint_length=stint_length

        )

        comparisons.append(

            analysis

        )

    comparisons.sort(

        key=lambda x: x[
            "TotalStintTime"
        ]

    )

    for index, result in enumerate(

        comparisons,

        start=1

    ):

        result["PerformanceRank"] = index

    return comparisons


# ============================================================
# SELECT BEST COMPOUND
# ============================================================

def select_best_compound(
    compound_comparisons: list
) -> dict | None:
    """
    Select the compound with the lowest predicted
    total stint time.
    """

    if not compound_comparisons:

        return None

    best = min(

        compound_comparisons,

        key=lambda x: x[
            "TotalStintTime"
        ]

    )

    return best.copy()


# ============================================================
# DISPLAY COMPOUND COMPARISON
# ============================================================

def display_compound_comparison(
    comparisons: list
) -> None:
    """
    Display tyre compound performance results.
    """

    print("\n" + "=" * 60)

    print(
        "TYRE COMPOUND PERFORMANCE COMPARISON"
    )

    print("=" * 60)

    if not comparisons:

        print(
            "No tyre comparison available."
        )

        return

    for result in comparisons:

        print(

            f"\nRank: "
            f"{result['PerformanceRank']}"

        )

        print(

            f"Compound: "
            f"{result['Compound']}"

        )

        print(

            f"Stint Length: "
            f"{result['StintLength']} laps"

        )

        print(

            f"Average Lap Time: "
            f"{result['AverageLapTime']:.3f}s"

        )

        print(

            f"Total Stint Time: "
            f"{result['TotalStintTime']:.3f}s"

        )

        print(

            f"Degradation Impact: "
            f"{result['DegradationImpact']:.3f}s"

        )

    print("=" * 60)


# ============================================================
# DISPLAY BEST COMPOUND
# ============================================================

def display_best_compound(
    best_compound: dict | None
) -> None:
    """
    Display the best-performing tyre compound.
    """

    print("\n" + "=" * 60)

    print(
        "BEST TYRE COMPOUND"
    )

    print("=" * 60)

    if best_compound is None:

        print(
            "No valid compound found."
        )

    else:

        print(

            f"Compound: "
            f"{best_compound['Compound']}"

        )

        print(

            f"Performance Rank: "
            f"{best_compound['PerformanceRank']}"

        )

        print(

            f"Average Lap Time: "
            f"{best_compound['AverageLapTime']:.3f}s"

        )

        print(

            f"Total Stint Time: "
            f"{best_compound['TotalStintTime']:.3f}s"

        )

        print(

            f"Degradation Impact: "
            f"{best_compound['DegradationImpact']:.3f}s"

        )

    print("=" * 60)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "SPRINT 4 - STEP 4 TEST"
    )

    print("=" * 60)

    base_lap_time = 90.0

    tyre_age = 0

    stint_length = 15

    # --------------------------------------------------------
    # Compare All Compounds
    # --------------------------------------------------------

    comparisons = compare_tyre_compounds(

        base_lap_time=base_lap_time,

        tyre_age=tyre_age,

        stint_length=stint_length

    )

    # --------------------------------------------------------
    # Display Comparison
    # --------------------------------------------------------

    display_compound_comparison(

        comparisons

    )

    # --------------------------------------------------------
    # Select Best Compound
    # --------------------------------------------------------

    best_compound = select_best_compound(

        comparisons

    )

    # --------------------------------------------------------
    # Display Best Compound
    # --------------------------------------------------------

    display_best_compound(

        best_compound

    )

    print("=" * 60)

    print(
        "STEP 4 COMPLETED"
    )

    print("=" * 60)