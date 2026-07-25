from typing import Dict, Any

from src.strategy.tyre_model import (
    get_degradation_rate
)

from src.strategy.track_model import (
    get_pit_loss
)

from src.strategy.driver_model import (
    get_driver_factor
)


# ============================================================
# SIMULATE STRATEGY
# ============================================================

def simulate_strategy(
    track: str,
    driver: str,
    tyre_compound: str,
    predicted_lap_time: float,
    laps_remaining: int,
    degradation_rate: float = None
) -> Dict[str, Any]:
    """
    Simulate two basic strategy options:

        1. PIT NOW
        2. STAY OUT

    Parameters
    ----------
    track : str
        Circuit or track name.

    driver : str
        Driver abbreviation.

    tyre_compound : str
        Current tyre compound.

    predicted_lap_time : float
        Estimated current lap time in seconds.

    laps_remaining : int
        Number of laps remaining in the race.

    degradation_rate : float, optional
        Dynamic degradation rate estimated from race_state.py.

        If provided, the simulator uses this value.

        If not provided, the simulator falls back
        to the static tyre model.

    Returns
    -------
    dict
        Simulation results comparing PIT NOW
        and STAY OUT.
    """

    # ========================================================
    # VALIDATION
    # ========================================================

    if predicted_lap_time is None:

        raise ValueError(
            "predicted_lap_time cannot be None."
        )

    if laps_remaining is None:

        raise ValueError(
            "laps_remaining cannot be None."
        )

    if laps_remaining < 0:

        raise ValueError(
            "laps_remaining cannot be negative."
        )

    if predicted_lap_time <= 0:

        raise ValueError(
            "predicted_lap_time must be greater than zero."
        )

    # ========================================================
    # TRACK / TYRE / DRIVER PARAMETERS
    # ========================================================

    pit_loss = get_pit_loss(
        track
    )

    driver_factor = get_driver_factor(
        driver
    )

    # ========================================================
    # DEGRADATION
    # ========================================================

    # Use dynamic degradation from FastF1
    # if available.
    #
    # Otherwise fall back to the existing
    # static tyre model.

    if degradation_rate is not None:

        degradation = float(
            degradation_rate
        )

        # Degradation should not be negative.
        degradation = max(
            degradation,
            0.0
        )

    else:

        degradation = get_degradation_rate(
            tyre_compound
        )

    # ========================================================
    # STAY OUT STRATEGY
    # ========================================================

    stay_time = 0.0

    lap_time = (

        float(predicted_lap_time)
        * driver_factor

    )

    for _ in range(
        int(laps_remaining)
    ):

        stay_time += lap_time

        lap_time += degradation

    # ========================================================
    # PIT NOW STRATEGY
    # ========================================================

    pit_time = float(
        pit_loss
    )

    # Fresh tyres provide an initial pace advantage.
    #
    # This remains a baseline Sprint 1 assumption.
    # A future sprint can replace this with
    # compound-specific fresh tyre performance.

    fresh_lap = (

        float(predicted_lap_time)
        - 1.2

    ) * driver_factor

    # Prevent unrealistic negative lap times.

    fresh_lap = max(
        fresh_lap,
        1.0
    )

    for _ in range(
        int(laps_remaining)
    ):

        pit_time += fresh_lap

        # Fresh tyres degrade more slowly
        # in the baseline simulator.

        fresh_lap += (
            degradation * 0.5
        )

    # ========================================================
    # DELTA
    # ========================================================

    delta = (

        stay_time
        - pit_time

    )

    # Positive delta:
    #
    # PIT NOW is faster.
    #
    # Negative delta:
    #
    # STAY OUT is faster.

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    if pit_time < stay_time:

        recommendation = (
            "PIT NOW"
        )

    else:

        recommendation = (
            "STAY OUT"
        )

    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "track":
            track,

        "driver":
            driver,

        "tyre_compound":
            tyre_compound,

        "laps_remaining":
            int(laps_remaining),

        "predicted_lap_time":
            round(
                float(
                    predicted_lap_time
                ),
                3
            ),

        "pit_loss":
            round(
                float(
                    pit_loss
                ),
                3
            ),

        "degradation_rate":
            round(
                float(
                    degradation
                ),
                4
            ),

        "stay_out_time":
            round(
                stay_time,
                2
            ),

        "pit_now_time":
            round(
                pit_time,
                2
            ),

        "delta":
            round(
                delta,
                2
            ),

        "recommendation":
            recommendation

    }


# ============================================================
# SIMULATE FROM DYNAMIC RACE STATE
# ============================================================

def simulate_from_race_state(
    race_state: dict
) -> Dict[str, Any]:
    """
    Run the strategy simulator using the dynamic
    race state generated by race_state.py.

    Pipeline:

        FastF1
            ↓
        race_state.py
            ↓
        Dynamic Race State
            ↓
        Strategy Simulator
            ↓
        PIT NOW vs STAY OUT

    Parameters
    ----------
    race_state : dict
        Structured race state generated by race_state.py.

    Returns
    -------
    dict
        Strategy simulation result.
    """

    if not isinstance(
        race_state,
        dict
    ):

        raise TypeError(
            "race_state must be a dictionary."
        )

    # ========================================================
    # EXTRACT RACE STATE
    # ========================================================

    track = race_state.get(
        "Circuit"
    )

    driver = race_state.get(
        "Driver"
    )

    tyre_compound = race_state.get(
        "TyreCompound"
    )

    predicted_lap_time = race_state.get(
        "AvgPaceLast5"
    )

    laps_remaining = race_state.get(
        "LapsRemaining"
    )

    degradation_rate = race_state.get(
        "DegradationRate"
    )

    # ========================================================
    # VALIDATE REQUIRED DATA
    # ========================================================

    missing_fields = []

    if track is None:

        missing_fields.append(
            "Circuit"
        )

    if driver is None:

        missing_fields.append(
            "Driver"
        )

    if tyre_compound is None:

        missing_fields.append(
            "TyreCompound"
        )

    if predicted_lap_time is None:

        missing_fields.append(
            "AvgPaceLast5"
        )

    if laps_remaining is None:

        missing_fields.append(
            "LapsRemaining"
        )

    if missing_fields:

        raise ValueError(

            "Missing required race state fields: "

            f"{missing_fields}"

        )

    # ========================================================
    # RUN SIMULATION
    # ========================================================

    return simulate_strategy(

        track=track,

        driver=driver,

        tyre_compound=tyre_compound,

        predicted_lap_time=predicted_lap_time,

        laps_remaining=int(
            laps_remaining
        ),

        degradation_rate=degradation_rate

    )


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    from src.data_loader import (
        load_session
    )

    from src.race_state import (
        build_race_state
    )


    # --------------------------------------------------------
    # TEST CONFIGURATION
    # --------------------------------------------------------

    SEASON = 2025

    GRAND_PRIX = (
        "British Grand Prix"
    )

    SESSION_TYPE = "R"

    DRIVER = "VER"


    # --------------------------------------------------------
    # LOAD SESSION
    # --------------------------------------------------------

    print(
        "=" * 60
    )

    print(
        "V5 SPRINT 1 - STEP 5 SIMULATOR TEST"
    )

    print(
        "=" * 60
    )

    print(
        "\nLoading FastF1 session..."
    )

    session = load_session(

        SEASON,

        GRAND_PRIX,

        SESSION_TYPE

    )

    print(
        "Session loaded successfully."
    )


    # --------------------------------------------------------
    # BUILD RACE STATE
    # --------------------------------------------------------

    print(
        "\nBuilding race state..."
    )

    race_state = build_race_state(

        session,

        DRIVER

    )

    print(
        "Race state generated successfully."
    )


    # --------------------------------------------------------
    # RUN SIMULATION
    # --------------------------------------------------------

    print(
        "\nRunning strategy simulation..."
    )

    result = simulate_from_race_state(

        race_state

    )


    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "V5 STRATEGY SIMULATION"
    )

    print(
        "=" * 60
    )

    print(
        f"Track: "
        f"{result['track']}"
    )

    print(
        f"Driver: "
        f"{result['driver']}"
    )

    print(
        f"Tyre: "
        f"{result['tyre_compound']}"
    )

    print(
        f"Laps Remaining: "
        f"{result['laps_remaining']}"
    )

    print(
        f"Predicted Lap Time: "
        f"{result['predicted_lap_time']} sec"
    )

    print(
        f"Pit Loss: "
        f"{result['pit_loss']} sec"
    )

    print(
        f"Degradation Rate: "
        f"{result['degradation_rate']} sec/lap"
    )

    print(
        "\nSTAY OUT"
    )

    print(
        f"Estimated Time: "
        f"{result['stay_out_time']} sec"
    )

    print(
        "\nPIT NOW"
    )

    print(
        f"Estimated Time: "
        f"{result['pit_now_time']} sec"
    )

    print(
        "\nDelta: "
        f"{result['delta']} sec"
    )

    print(
        "\nRecommendation: "
        f"{result['recommendation']}"
    )

    print(
        "=" * 60
    )

    print(
        "\nStep 5 simulator test completed."
    )