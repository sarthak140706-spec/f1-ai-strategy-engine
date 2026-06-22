import joblib
import pandas as pd


import os
import joblib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

pit_model = joblib.load(
    os.path.join(
        PROJECT_ROOT,
        "models",
        "pit_strategy_model.pkl"
    )
)

degradation_model = joblib.load(
    os.path.join(
        PROJECT_ROOT,
        "models",
        "degradation_model.pkl"
    )
)


def simulate_strategy(
    current_state,
    pit_loss=22,
    fresh_tyre_gain=1.2,
    degradation_per_lap=0.05
):
    """
    Compare two scenarios:
    1. Stay out
    2. Pit now
    """

    laps_remaining = int(current_state["LapsRemaining"])
    predicted_lap_time = current_state["AvgPaceLast5"]

    # Scenario 1: Stay out

    stay_out_total = 0
    current_lap_time = predicted_lap_time

    for _ in range(laps_remaining):
        stay_out_total += current_lap_time
        current_lap_time += degradation_per_lap

    # Scenario 2: Pit now

    pit_now_total = pit_loss

    fresh_lap_time = predicted_lap_time - fresh_tyre_gain

    for _ in range(laps_remaining):
        pit_now_total += fresh_lap_time
        fresh_lap_time += degradation_per_lap / 2

    recommendation = (
        "Pit Now"
        if pit_now_total < stay_out_total
        else "Stay Out"
    )

    return {
        "stay_out_time": round(stay_out_total, 2),
        "pit_now_time": round(pit_now_total, 2),
        "time_gain": round(
            abs(stay_out_total - pit_now_total),
            2
        ),
        "recommendation": recommendation
    }