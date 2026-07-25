from src.data_loader import load_session
from src.race_state import build_race_state
from src.predict import predict_from_race_state


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
print("V5 SPRINT 1 - STEP 4 PREDICTION TEST")
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
# RUN PREDICTION
# ============================================================

print("\nRunning ML prediction...")

result = predict_from_race_state(
    race_state
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n" + "=" * 60)
print("AI PIT STRATEGY PREDICTION")
print("=" * 60)

print(
    f"Driver: "
    f"{result['driver']}"
)

print(
    f"Team: "
    f"{result['team']}"
)

print(
    f"Current Lap: "
    f"{result['current_lap']}"
)

print(
    f"Position: "
    f"{result['position']}"
)

print(
    f"Tyre: "
    f"{result['tyre_compound']}"
)

print(
    f"Tyre Life: "
    f"{result['tyre_life']}"
)

print(
    f"Pit Probability: "
    f"{result['pit_probability']}%"
)

print(
    f"Raw ML Decision: "
    f"{result['decision']}"
)

print("=" * 60)

print(
    "\nStep 4 prediction test completed successfully!"
)