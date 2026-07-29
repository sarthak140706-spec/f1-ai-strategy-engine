"""
tyre_model.py

Sprint 4 - Step 3

Models tyre degradation and estimates the expected lap time
based on tyre compound, tyre age, and degradation rate.
"""

# ============================================================
# DEFAULT TYRE DEGRADATION RATES
# ============================================================

DEFAULT_DEGRADATION_RATES = {
    "SOFT": 0.085,
    "MEDIUM": 0.055,
    "HARD": 0.035
}


# ============================================================
# COMPOUND BASE PERFORMANCE
# ============================================================

COMPOUND_BASE_PACE = {
    "SOFT": -0.35,
    "MEDIUM": 0.00,
    "HARD": 0.25
}


# ============================================================
# GET DEGRADATION RATE
# ============================================================

def get_degradation_rate(
    compound: str,
    degradation_rates: dict | None = None
) -> float:
    """
    Return the degradation rate for a tyre compound.

    Parameters
    ----------
    compound : str
        Tyre compound: SOFT, MEDIUM, or HARD.

    degradation_rates : dict, optional
        Custom degradation rates.

    Returns
    -------
    float
        Degradation time added per tyre-age lap.
    """

    if compound is None:
        raise ValueError(
            "Tyre compound cannot be None."
        )

    compound = compound.upper()

    rates = (
        degradation_rates
        if degradation_rates is not None
        else DEFAULT_DEGRADATION_RATES
    )

    if compound not in rates:
        raise ValueError(
            f"Unknown tyre compound: {compound}"
        )

    return rates[compound]


# ============================================================
# GET COMPOUND PACE OFFSET
# ============================================================

def get_compound_pace_offset(
    compound: str
) -> float:
    """
    Return the base pace advantage or disadvantage
    of the selected tyre compound.

    Negative value = faster.
    Positive value = slower.
    """

    if compound is None:
        raise ValueError(
            "Tyre compound cannot be None."
        )

    compound = compound.upper()

    if compound not in COMPOUND_BASE_PACE:
        raise ValueError(
            f"Unknown tyre compound: {compound}"
        )

    return COMPOUND_BASE_PACE[compound]


# ============================================================
# CALCULATE TYRE DEGRADATION
# ============================================================

def calculate_tyre_degradation(
    compound: str,
    tyre_age: int,
    degradation_rates: dict | None = None
) -> float:
    """
    Calculate the additional lap time caused by tyre wear.

    A simple linear degradation model is used.

    Formula
    -------
    degradation = degradation_rate * tyre_age
    """

    if tyre_age < 0:
        raise ValueError(
            "Tyre age cannot be negative."
        )

    degradation_rate = get_degradation_rate(
        compound,
        degradation_rates
    )

    degradation = (
        degradation_rate * tyre_age
    )

    return round(
        degradation,
        4
    )


# ============================================================
# PREDICT LAP TIME
# ============================================================

def predict_degraded_lap_time(
    base_lap_time: float,
    compound: str,
    tyre_age: int,
    degradation_rates: dict | None = None
) -> float:
    """
    Predict lap time after accounting for:
    - Compound performance
    - Tyre degradation
    """

    if base_lap_time is None:
        raise ValueError(
            "Base lap time cannot be None."
        )

    if base_lap_time <= 0:
        raise ValueError(
            "Base lap time must be positive."
        )

    compound_offset = get_compound_pace_offset(
        compound
    )

    degradation = calculate_tyre_degradation(
        compound=compound,
        tyre_age=tyre_age,
        degradation_rates=degradation_rates
    )

    predicted_lap_time = (
        base_lap_time
        + compound_offset
        + degradation
    )

    return round(
        predicted_lap_time,
        3
    )


# ============================================================
# GENERATE TYRE DEGRADATION PROFILE
# ============================================================

def generate_degradation_profile(
    base_lap_time: float,
    compound: str,
    tyre_age: int,
    laps: int,
    degradation_rates: dict | None = None
) -> list:
    """
    Generate predicted lap times for future laps
    on the same tyre set.
    """

    if laps <= 0:
        raise ValueError(
            "Number of laps must be greater than zero."
        )

    if tyre_age < 0:
        raise ValueError(
            "Tyre age cannot be negative."
        )

    profile = []

    for lap_offset in range(laps):

        current_tyre_age = (
            tyre_age
            + lap_offset
        )

        predicted_lap_time = (
            predict_degraded_lap_time(

                base_lap_time=base_lap_time,

                compound=compound,

                tyre_age=current_tyre_age,

                degradation_rates=degradation_rates

            )
        )

        profile.append({

            "LapOffset": lap_offset,

            "TyreAge": current_tyre_age,

            "PredictedLapTime": predicted_lap_time

        })

    return profile


# ============================================================
# ESTIMATE STINT TIME
# ============================================================

def estimate_stint_time(
    base_lap_time: float,
    compound: str,
    tyre_age: int,
    stint_length: int,
    degradation_rates: dict | None = None
) -> float:
    """
    Estimate total time required to complete a tyre stint.
    """

    profile = generate_degradation_profile(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age,

        laps=stint_length,

        degradation_rates=degradation_rates

    )

    total_time = sum(

        lap["PredictedLapTime"]

        for lap in profile

    )

    return round(
        total_time,
        3
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SPRINT 4 - STEP 3 TEST")
    print("=" * 60)

    base_lap_time = 90.0

    compound = "MEDIUM"

    tyre_age = 5

    stint_length = 10

    # --------------------------------------------------------
    # Calculate Degradation
    # --------------------------------------------------------

    degradation = calculate_tyre_degradation(

        compound=compound,

        tyre_age=tyre_age

    )

    print("\nTYRE DEGRADATION")
    print("=" * 60)

    print(
        f"Compound: {compound}"
    )

    print(
        f"Tyre Age: {tyre_age} laps"
    )

    print(
        f"Degradation: {degradation:.4f} seconds"
    )

    # --------------------------------------------------------
    # Predict Lap Time
    # --------------------------------------------------------

    predicted_lap = predict_degraded_lap_time(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age

    )

    print("\nPREDICTED LAP TIME")
    print("=" * 60)

    print(
        f"Base Lap Time: {base_lap_time:.3f} seconds"
    )

    print(
        f"Predicted Lap Time: {predicted_lap:.3f} seconds"
    )

    # --------------------------------------------------------
    # Generate Degradation Profile
    # --------------------------------------------------------

    profile = generate_degradation_profile(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age,

        laps=stint_length

    )

    print("\nDEGRADATION PROFILE")
    print("=" * 60)

    for lap in profile:

        print(
            f"Lap +{lap['LapOffset']}: "
            f"Tyre Age = {lap['TyreAge']}, "
            f"Predicted Time = "
            f"{lap['PredictedLapTime']:.3f}s"
        )

    # --------------------------------------------------------
    # Estimate Stint Time
    # --------------------------------------------------------

    stint_time = estimate_stint_time(

        base_lap_time=base_lap_time,

        compound=compound,

        tyre_age=tyre_age,

        stint_length=stint_length

    )

    print("\nSTINT ESTIMATION")
    print("=" * 60)

    print(
        f"Stint Length: {stint_length} laps"
    )

    print(
        f"Estimated Stint Time: "
        f"{stint_time:.3f} seconds"
    )

    print("=" * 60)
    print("STEP 3 COMPLETED")
    print("=" * 60)