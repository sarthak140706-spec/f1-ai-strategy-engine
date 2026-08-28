from src.data_loader import load_session

from src.strategy.dynamic_race_state import (
    build_dynamic_race_state,
    display_dynamic_race_state
)


# ============================================================
# PHASE 4.1 TEST
# ============================================================

print(
    "\n" + "=" * 70
)

print(
    "F1 AI STRATEGIST"
)

print(
    "PHASE 4.1 — DYNAMIC RACE STATE ENGINE TEST"
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
# LOAD SESSION
# ============================================================

print(
    "\n[1/3] Loading race session..."
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
# BUILD DYNAMIC STATE
# ============================================================

print(
    f"\n[2/3] Reconstructing race state "
    f"at lap {SELECTED_LAP}..."
)

state = build_dynamic_race_state(

    session=session,

    driver=DRIVER,

    selected_lap=SELECTED_LAP

)


display_dynamic_race_state(
    state
)


# ============================================================
# VALIDATION
# ============================================================

print(
    "\n[3/3] Validating reconstructed state..."
)


assert (
    state["CurrentLap"]
    ==
    SELECTED_LAP
), (
    "Selected lap mismatch."
)


assert (
    state["LapsRemaining"]
    >
    0
), (
    "Laps remaining should be positive "
    "for a mid-race snapshot."
)


assert (
    state["Driver"]
    ==
    DRIVER
), (
    "Driver mismatch."
)


assert (
    state["TyreCompound"]
    is not None
), (
    "Tyre compound missing."
)


assert (
    state["CurrentStint"]
    is not None
), (
    "Current stint missing."
)


assert (
    state["RecentPace"]
    is not None
), (
    "Recent pace missing."
)


assert (
    state["AveragePace"]
    is not None
), (
    "Average pace missing."
)


assert (
    state["RaceProgress"]
    >
    0
    and
    state["RaceProgress"]
    <
    1
), (
    "Race progress should represent "
    "a mid-race snapshot."
)


print(
    "\n" + "=" * 70
)

print(
    "✅ PHASE 4.1 DYNAMIC RACE STATE TEST PASSED"
)

print(
    "=" * 70
)