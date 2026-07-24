from data.strategy_params import (
    DEFAULT_PIT_LOSS,
    DEFAULT_TYRE_DEGRADATION,
    DEFAULT_FRESH_TYRE_BONUS
)


def simulate_strategy(
    current_lap,
    tyre_life,
    predicted_lap_time,
    laps_remaining,
    tyre_compound="MEDIUM",
    pit_loss=None
):

    """
    Simulate two basic strategies:

    1. Stay Out
    2. Pit Now

    This is still the V4 baseline simulator.

    V5 will replace the fixed degradation
    assumptions with data-driven models.
    """

    tyre_compound = (
        tyre_compound.upper()
    )

    if pit_loss is None:

        pit_loss = (
            DEFAULT_PIT_LOSS
        )

    degradation = (

        DEFAULT_TYRE_DEGRADATION.get(

            tyre_compound,

            0.06

        )

    )

    fresh_bonus = (

        DEFAULT_FRESH_TYRE_BONUS.get(

            tyre_compound,

            0.9

        )

    )

    # ------------------------------------------
    # STAY OUT
    # ------------------------------------------

    stay_out_time = 0.0

    lap_time = (
        predicted_lap_time
    )

    for lap_index in range(
        int(laps_remaining)
    ):

        tyre_age = (
            tyre_life
            + lap_index
        )

        degradation_penalty = (

            tyre_age
            * degradation

        )

        simulated_lap_time = (

            lap_time
            + degradation_penalty

        )

        stay_out_time += (
            simulated_lap_time
        )

    # ------------------------------------------
    # PIT NOW
    # ------------------------------------------

    pit_now_time = (
        pit_loss
    )

    for lap_index in range(
        int(laps_remaining)
    ):

        new_tyre_age = (
            lap_index
        )

        degradation_penalty = (

            new_tyre_age
            * degradation

        )

        simulated_lap_time = (

            predicted_lap_time
            - fresh_bonus
            + degradation_penalty

        )

        pit_now_time += (
            simulated_lap_time
        )

    # ------------------------------------------
    # DELTA
    # ------------------------------------------

    delta = (

        stay_out_time
        - pit_now_time

    )

    if delta > 0:

        recommendation = (
            "PIT"
        )

    else:

        recommendation = (
            "STAY"
        )

    return {

        "stay_out_time":
            round(
                stay_out_time,
                2
            ),

        "pit_now_time":
            round(
                pit_now_time,
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