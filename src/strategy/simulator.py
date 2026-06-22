from src.strategy.tyre_model import get_degradation_rate
from src.strategy.track_model import get_pit_loss
from src.strategy.driver_model import get_driver_factor


def simulate_strategy(
    track: str,
    driver: str,
    tyre_compound: str,
    predicted_lap_time: float,
    laps_remaining: int
):

    pit_loss = get_pit_loss(track)
    degradation = get_degradation_rate(tyre_compound)
    driver_factor = get_driver_factor(driver)

    # ---------------------------
    # STAY OUT STRATEGY
    # ---------------------------
    stay_time = 0
    lap_time = predicted_lap_time * driver_factor

    for _ in range(int(laps_remaining)):
        stay_time += lap_time
        lap_time += degradation

    # ---------------------------
    # PIT NOW STRATEGY
    # ---------------------------
    pit_time = pit_loss

    fresh_lap = (predicted_lap_time - 1.2) * driver_factor

    for _ in range(int(laps_remaining)):
        pit_time += fresh_lap
        fresh_lap += degradation * 0.5  # fresher tyres degrade slower

    return {
        "stay_out_time": round(stay_time, 2),
        "pit_now_time": round(pit_time, 2),
        "delta": round(stay_time - pit_time, 2),
        "recommendation": "PIT NOW" if pit_time < stay_time else "STAY OUT"
    }