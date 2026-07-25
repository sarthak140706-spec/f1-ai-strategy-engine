from src.data_loader import load_session
from src.race_state import build_race_state
from src.feature_engineering import (
    build_ml_features,
    validate_ml_features
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
print("V5 SPRINT 1 - STEP 3 FEATURE ENGINEERING TEST")
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
# BUILD ML FEATURES
# ============================================================

print("\nGenerating ML features...")

features = build_ml_features(
    race_state
)


# ============================================================
# VALIDATE FEATURES
# ============================================================

print("\nValidating ML features...")

validate_ml_features(
    features
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("GENERATED ML FEATURES")
print("=" * 60)

print(features.to_string(index=False))


print("\n" + "=" * 60)
print("FEATURE COLUMNS")
print("=" * 60)

for column in features.columns:
    print(column)


print("\n" + "=" * 60)
print("STEP 3 FEATURE VALIDATION SUCCESSFUL!")
print("=" * 60)