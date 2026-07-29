"""
tyre_degradation.py

Sprint 4 - Step 2

Models tyre degradation and estimates lap-time loss
as tyre age increases.

The model uses:
- Tyre compound
- Tyre age
- Track
- Driver
- Base lap time

This module is designed to work with the existing
F1 AI Strategist V5 architecture.
"""

from typing import Optional


# ============================================================
# DEFAULT DEGRADATION RATES
# ============================================================

DEFAULT_DEGRADATION_RATES = {
    "SOFT": 0.080,
    "MEDIUM": 0.050,
    "HARD": 0.035,
}


# ============================================================
# COMPOUND PERFORMANCE FACTORS
# ============================================================

COMPOUND_FACTORS = {
    "SOFT": 0.97,
    "MEDIUM": 1.00,
    "HARD": 1.035,
}


# ============================================================
# TRACK DEGRADATION FACTORS
# ============================================================

TRACK_DEGRADATION_FACTORS = {
    "British Grand Prix": 1.00,
    "Bahrain Grand Prix": 1.20,
    "Monaco Grand Prix": 0.80,
    "Italian Grand Prix": 0.90,
    "Japanese Grand Prix": 1.05,
    "Australian Grand Prix": 0.95,
    "Spanish Grand Prix": 1.10,
    "Austrian Grand Prix": 0.95,
    "Belgian Grand Prix": 1.00,
    "Singapore Grand Prix": 1.15,
    "United States Grand Prix": 1.00,
    "Mexico City Grand Prix": 0.90,
    "São Paulo Grand Prix": 1.05,
    "Las Vegas Grand Prix": 0.85,
    "Qatar Grand Prix": 1.15,
    "Abu Dhabi Grand Prix": 1.00,
}


# ============================================================
# DRIVER FACTORS
# ============================================================

DEFAULT_DRIVER_FACTOR = 1.00


# ============================================================
# GET DEGRADATION RATE
# ============================================================

def get_degradation_rate(
    tyre_compound: str,
    track: Optional[str] = None
) -> float:
    """
    Return the estimated tyre degradation rate.

    Parameters
    ----------
    tyre_compound : str
        SOFT, MEDIUM, or HARD.

    track : str, optional
        Circuit name.

    Returns
    -------
    float
        Degradation in seconds per tyre-age lap.
    """

    compound = tyre_compound.upper()

    if compound not in DEFAULT_DEGRADATION_RATES:

        raise ValueError(
            f"Unsupported tyre compound: {tyre_compound}"
        )

    base_rate = DEFAULT_DEGRADATION_RATES[
        compound
    ]

    track_factor = TRACK_DEGRADATION_FACTORS.get(
        track,
        1.00
    )

    return base_rate * track_factor


# ============================================================
# CALCULATE TYRE DEGRADATION
# ============================================================

def calculate_tyre_degradation(
    tyre_compound: str,
    tyre_age: int,
    track: Optional[str] = None
) -> float:
    """
    Calculate the lap-time loss caused by tyre degradation.

    Parameters
    ----------
    tyre_compound : str
        Tyre compound.

    tyre_age : int
        Number of laps completed on the tyre.

    track : str, optional
        Circuit name.

    Returns
    -------
    float
        Estimated degradation penalty in seconds.
    """

    if tyre_age < 0:

        raise ValueError(
            "Tyre age cannot be negative."
        )

    degradation_rate = get_degradation_rate(

        tyre_compound,

        track

    )

    degradation = (

        degradation_rate

        *

        tyre_age

    )

    return round(
        degradation,
        4
    )


# ============================================================
# CALCULATE COMPOUND PERFORMANCE
# ============================================================

def calculate_compound_performance(
    tyre_compound: str,
    tyre_age: int
) -> float:
    """
    Calculate a simple performance multiplier
    based on compound and tyre age.

    Lower value indicates faster performance.

    Returns
    -------
    float
        Performance multiplier.
    """

    compound = tyre_compound.upper()

    if compound not in COMPOUND_FACTORS:

        raise ValueError(
            f"Unsupported tyre compound: {tyre_compound}"
        )

    base_factor = COMPOUND_FACTORS[
        compound
    ]

    degradation_penalty = (

        DEFAULT_DEGRADATION_RATES[compound]

        *

        tyre_age

    )

    return round(

        base_factor

        +

        degradation_penalty,

        4

    )


# ============================================================
# PREDICT LAP TIME WITH DEGRADATION
# ============================================================

def predict_degraded_lap_time(
    base_lap_time: float,
    tyre_compound: str,
    tyre_age: int,
    track: Optional[str] = None,
    driver_factor: float = DEFAULT_DRIVER_FACTOR
) -> float:
    """
    Predict lap time after considering tyre degradation.

    Parameters
    ----------
    base_lap_time : float
        Current estimated lap time in seconds.

    tyre_compound : str
        SOFT, MEDIUM, or HARD.

    tyre_age : int
        Number of laps completed on current tyres.

    track : str, optional
        Circuit name.

    driver_factor : float
        Driver performance adjustment.

    Returns
    -------
    float
        Predicted degraded lap time.
    """

    if base_lap_time <= 0:

        raise ValueError(
            "Base lap time must be greater than zero."
        )

    if driver_factor <= 0:

        raise ValueError(
            "Driver factor must be greater than zero."
        )

    degradation = calculate_tyre_degradation(

        tyre_compound=tyre_compound,

        tyre_age=tyre_age,

        track=track

    )

    predicted_lap_time = (

        base_lap_time

        +

        degradation

    ) * driver_factor

    return round(

        predicted_lap_time,

        3

    )


# ============================================================
# PROJECT TYRE LIFE
# ============================================================

def project_tyre_life(
    base_lap_time: float,
    tyre_compound: str,
    current_tyre_age: int,
    laps_to_project: int,
    track: Optional[str] = None,
    driver_factor: float = DEFAULT_DRIVER_FACTOR
) -> list:
    """
    Project future lap times for a tyre stint.

    Returns a list containing projected lap information.
    """

    if current_tyre_age < 0:

        raise ValueError(
            "Current tyre age cannot be negative."
        )

    if laps_to_project <= 0:

        raise ValueError(
            "Laps to project must be greater than zero."
        )

    projection = []

    for lap_number in range(

        laps_to_project

    ):

        tyre_age = (

            current_tyre_age

            +

            lap_number

        )

        degradation = calculate_tyre_degradation(

            tyre_compound,

            tyre_age,

            track

        )

        predicted_lap_time = predict_degraded_lap_time(

            base_lap_time,

            tyre_compound,

            tyre_age,

            track,

            driver_factor

        )

        projection.append({

            "Lap": lap_number + 1,

            "TyreAge": tyre_age,

            "Compound": tyre_compound,

            "Degradation": degradation,

            "PredictedLapTime": predicted_lap_time

        })

    return projection


# ============================================================
# COMPARE COMPOUNDS
# ============================================================

def compare_compounds(
    base_lap_time: float,
    tyre_age: int = 0,
    track: Optional[str] = None
) -> list:
    """
    Compare predicted performance of all tyre compounds.
    """

    compounds = [

        "SOFT",

        "MEDIUM",

        "HARD"

    ]

    comparison = []

    for compound in compounds:

        degradation = calculate_tyre_degradation(

            compound,

            tyre_age,

            track

        )

        predicted_lap_time = predict_degraded_lap_time(

            base_lap_time,

            compound,

            tyre_age,

            track

        )

        comparison.append({

            "Compound": compound,

            "TyreAge": tyre_age,

            "Degradation": degradation,

            "PredictedLapTime": predicted_lap_time

        })

    comparison.sort(

        key=lambda x: x["PredictedLapTime"]

    )

    return comparison


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "SPRINT 4 - STEP 2 TEST"
    )

    print("=" * 60)

    base_lap_time = 90.0

    track = "British Grand Prix"

    # --------------------------------------------------------
    # TEST DEGRADATION
    # --------------------------------------------------------

    print("\nTYRE DEGRADATION")

    print("=" * 60)

    for compound in [

        "SOFT",

        "MEDIUM",

        "HARD"

    ]:

        degradation = calculate_tyre_degradation(

            tyre_compound=compound,

            tyre_age=10,

            track=track

        )

        print(

            f"{compound}: "

            f"{degradation:.4f} seconds"

        )

    # --------------------------------------------------------
    # TEST LAP TIME PREDICTION
    # --------------------------------------------------------

    print("\nDEGRADED LAP TIME")

    print("=" * 60)

    for compound in [

        "SOFT",

        "MEDIUM",

        "HARD"

    ]:

        lap_time = predict_degraded_lap_time(

            base_lap_time=base_lap_time,

            tyre_compound=compound,

            tyre_age=10,

            track=track

        )

        print(

            f"{compound}: "

            f"{lap_time:.3f} seconds"

        )

    # --------------------------------------------------------
    # TEST COMPOUND COMPARISON
    # --------------------------------------------------------

    print("\nCOMPOUND COMPARISON")

    print("=" * 60)

    comparison = compare_compounds(

        base_lap_time=base_lap_time,

        tyre_age=10,

        track=track

    )

    for result in comparison:

        print(result)

    # --------------------------------------------------------
    # TEST TYRE LIFE PROJECTION
    # --------------------------------------------------------

    print("\nTYRE LIFE PROJECTION")

    print("=" * 60)

    projection = project_tyre_life(

        base_lap_time=base_lap_time,

        tyre_compound="MEDIUM",

        current_tyre_age=5,

        laps_to_project=5,

        track=track

    )

    for result in projection:

        print(result)

    print("=" * 60)

    print(
        "STEP 2 COMPLETED"
    )

    print("=" * 60)