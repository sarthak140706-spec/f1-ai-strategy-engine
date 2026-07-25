import pandas as pd

from src.strategy.decision_engine import (
    get_strategy_decision
)


# ============================================================
# CREATE SAMPLE MODEL DATA
# ============================================================

model_data = pd.DataFrame([{

    "LapNumber": 42,

    "TyreLife": 18,

    "Position": 3,

    "LapsRemaining": 16,

    "RaceProgress": 0.72,

    "AvgPaceLast3": 92.421,

    "AvgPaceLast5": 92.512,

    "AvgPaceLast10": 92.603,

    "DegradationRate": 0.21,

    "CurrentStintLength": 18,

    "PitStopsCompleted": 1

}])


# ============================================================
# RUN DECISION ENGINE
# ============================================================

result = get_strategy_decision(

    track="Silverstone",

    driver="VER",

    tyre_compound="MEDIUM",

    predicted_lap_time=92.512,

    laps_remaining=16,

    model_data=model_data

)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("=" * 60)

print(
    "V5 SPRINT 1 - STEP 6 DECISION ENGINE TEST"
)

print("=" * 60)

print()

print(
    f"Pit Probability: "
    f"{result['pit_probability']}%"
)

print(
    f"Simulator Recommendation: "
    f"{result['simulator_recommendation']}"
)

print(
    f"Stay Out Time: "
    f"{result['stay_out_time']} sec"
)

print(
    f"Pit Now Time: "
    f"{result['pit_now_time']} sec"
)

print(
    f"Delta: "
    f"{result['delta']} sec"
)

print()

print(
    f"FINAL DECISION: "
    f"{result['final_decision']}"
)

print(
    f"CONFIDENCE: "
    f"{result['confidence']}"
)

print()

print(
    "REASON:"
)

print(
    result["reason"]
)

print("=" * 60)