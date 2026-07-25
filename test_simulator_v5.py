from src.data_loader import load_session
from src.race_state import build_race_state
from src.strategy.simulator import (
    simulate_from_race_state
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2025
GRAND_PRIX = "British Grand Prix"
SESSION_TYPE = "R"
DRIVER = "VER"


# ============================================================
# LOAD SESSION
# ============================================================

print("=" * 60)
print("V5 SPRINT 1 - STEP 5 SIMULATOR TEST")
print("=" * 60)

print("\nLoading FastF1 session...")

session = load_session(
    SEASON,
    GRAND_PRIX,
    SESSION_TYPE
)

print("Session loaded successfully.")


# ============================================================
# BUILD RACE STATE
# ============================================================

print("\nBuilding race state...")

race_state = build_race_state(
    session,
    DRIVER
)

print("Race state generated successfully.")


# ============================================================
# RUN SIMULATOR
# ============================================================

print("\nRunning strategy simulation...")

result = simulate_from_race_state(
    race_state
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 60)
print("STRATEGY SIMULATION RESULT")
print("=" * 60)

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
    f"\nStay Out Time: "
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

print(
    f"\nRecommendation: "
    f"{result['recommendation']}"
)

print("=" * 60)

print(
    "\nStep 5 simulator test completed successfully!"
)