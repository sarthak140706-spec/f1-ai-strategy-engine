def simulate_strategy(
    current_lap,
    tyre_life,
    predicted_lap_time,
    laps_remaining,
    pit_loss=22
):

    stay_out_time = 0

    lap_time = predicted_lap_time

    for _ in range(int(laps_remaining)):

        stay_out_time += lap_time

        lap_time += 0.08

    pit_now_time = pit_loss

    fresh_tyre_lap = predicted_lap_time - 1.2

    for _ in range(int(laps_remaining)):

        pit_now_time += fresh_tyre_lap

        fresh_tyre_lap += 0.04

    return {
        "stay_out": round(stay_out_time, 2),
        "pit_now": round(pit_now_time, 2)
    }