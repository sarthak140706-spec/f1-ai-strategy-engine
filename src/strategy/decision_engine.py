from src.strategy.simulator import simulate_strategy


def get_strategy_decision(
    track,
    driver,
    tyre_compound,
    predicted_lap_time,
    laps_remaining
):

    result = simulate_strategy(
        track,
        driver,
        tyre_compound,
        predicted_lap_time,
        laps_remaining
    )

    if result["delta"] > 5:
        confidence = "HIGH"
    elif result["delta"] > 2:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return {
        **result,
        "confidence": confidence
    }