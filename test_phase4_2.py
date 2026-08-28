from src.data_loader import load_session

from src.strategy.dynamic_race_state import (
    build_dynamic_race_state
)

from src.strategy.dynamic_race_situation import (
    analyze_dynamic_race_situation,
    display_dynamic_race_situation
)


# ============================================================
# PHASE 4.2 TEST
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "F1 AI STRATEGIST"
)

print(
    "PHASE 4.2 — DYNAMIC RACE SITUATION TEST"
)

print(
    "=" * 70
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain"

DRIVER = "VER"

SELECTED_LAP = 35


# ============================================================
# STEP 1
# LOAD SESSION
# ============================================================

print(
    "\n[1/4] Loading race session..."
)

session = load_session(

    season=SEASON,

    grand_prix=GRAND_PRIX,

    session_type="R"

)

assert session is not None

print(
    "✅ Race session loaded."
)


# ============================================================
# STEP 2
# BUILD PHASE 4.1 STATE
# ============================================================

print(
    "\n[2/4] Building dynamic race state..."
)

race_state = build_dynamic_race_state(

    session=session,

    driver=DRIVER,

    selected_lap=SELECTED_LAP

)

assert race_state

print(
    "✅ Dynamic race state generated."
)


# ============================================================
# STEP 3
# ANALYZE PHASE 4.2 SITUATION
# ============================================================

print(
    "\n[3/4] Analyzing strategic race situation..."
)

situation = analyze_dynamic_race_situation(
    race_state
)

display_dynamic_race_situation(
    situation
)


# ============================================================
# STEP 4
# VALIDATION
# ============================================================

print(
    "\n[4/4] Validating race situation..."
)


assert (
    situation["driver"]
    ==
    DRIVER
), (
    "Driver mismatch."
)


assert (
    situation["current_lap"]
    ==
    SELECTED_LAP
), (
    "Selected lap mismatch."
)


assert (
    situation["race_stage"]
    in [
        "EARLY",
        "MID",
        "LATE",
        "FINAL"
    ]
), (
    "Invalid race stage."
)


assert (
    situation["position_status"]
    !=
    "UNKNOWN"
), (
    "Position status missing."
)


assert (
    situation["tyre_status"]
    !=
    "UNKNOWN"
), (
    "Tyre status missing."
)


assert (
    situation["pace_status"]
    !=
    "UNKNOWN"
), (
    "Pace status missing."
)


assert (
    situation["pit_urgency"]
    !=
    "UNKNOWN"
), (
    "Pit urgency missing."
)


assert (
    situation["race_situation"]
    is not None
), (
    "Race situation missing."
)


assert (
    situation["strategic_summary"]
), (
    "Strategic summary missing."
)


print(
    "\n" + "=" * 70
)

print(
    "✅ PHASE 4.2 DYNAMIC RACE SITUATION TEST PASSED"
)

print(
    "=" * 70
)