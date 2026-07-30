"""
V5 STEP 10D - EDGE CASE & ROBUSTNESS VALIDATION

Purpose:
--------
Validate that the F1 AI Strategy Engine handles
invalid inputs and unusual race conditions safely.
"""

from src.data_loader import load_session
from src.race_state import build_race_state
from src.strategy.decision_engine import get_decision_from_race_state


# ============================================================
# CONFIGURATION
# ============================================================

SEASON = 2025
GRAND_PRIX = "British Grand Prix"
SESSION_TYPE = "R"
DRIVER = "VER"


# ============================================================
# HEADER
# ============================================================

print("=" * 80)

print(
    "V5 STEP 10D - EDGE CASE & ROBUSTNESS VALIDATION"
)

print("=" * 80)


# ============================================================
# TEST 1 - INVALID DRIVER
# ============================================================

print("\n[TEST 1] Invalid Driver")

try:

    session = load_session(
        SEASON,
        GRAND_PRIX,
        SESSION_TYPE
    )

    build_race_state(
        session,
        "XYZ"
    )

    print(
        "❌ FAIL - Invalid driver was accepted."
    )

except Exception as e:

    print(
        "✅ PASS - Invalid driver handled safely."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 2 - INVALID GRAND PRIX
# ============================================================

print("\n[TEST 2] Invalid Grand Prix")

try:

    load_session(
        SEASON,
        "Invalid Grand Prix",
        SESSION_TYPE
    )

    print(
        "❌ FAIL - Invalid Grand Prix was accepted."
    )

except Exception as e:

    print(
        "✅ PASS - Invalid Grand Prix handled safely."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 3 - INVALID SEASON
# ============================================================

print("\n[TEST 3] Invalid Season")

try:

    load_session(
        1800,
        GRAND_PRIX,
        SESSION_TYPE
    )

    print(
        "❌ FAIL - Invalid season was accepted."
    )

except Exception as e:

    print(
        "✅ PASS - Invalid season handled safely."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 4 - EMPTY DRIVER
# ============================================================

print("\n[TEST 4] Empty Driver")

try:

    build_race_state(
        {},
        ""
    )

    print(
        "❌ FAIL - Empty driver was accepted."
    )

except Exception as e:

    print(
        "✅ PASS - Empty driver handled safely."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 5 - EMPTY GRAND PRIX
# ============================================================

print("\n[TEST 5] Empty Grand Prix")

try:

    load_session(
        SEASON,
        "",
        SESSION_TYPE
    )

    print(
        "❌ FAIL - Empty Grand Prix was accepted."
    )

except Exception as e:

    print(
        "✅ PASS - Empty Grand Prix handled safely."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 6 - MISSING RACE STATE FIELDS
# ============================================================

print("\n[TEST 6] Missing Race-State Fields")

try:

    incomplete_race_state = {

        "Driver": "VER"

    }

    get_decision_from_race_state(
        incomplete_race_state
    )

    print(
        "❌ FAIL - Incomplete race state was accepted."
    )

except Exception as e:

    print(
        "✅ PASS - Missing fields handled safely."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# LOAD VALID RACE STATE
# ============================================================

print(
    "\n[INFO] Loading valid race state for "
    "edge-case simulation tests..."
)

session = load_session(
    SEASON,
    GRAND_PRIX,
    SESSION_TYPE
)

race_state = build_race_state(
    session,
    DRIVER
)

print(
    "Valid race state loaded successfully."
)


# ============================================================
# TEST 7 - UNSUPPORTED TYRE COMPOUND
# ============================================================

print("\n[TEST 7] Unsupported Tyre Compound")

try:

    invalid_tyre_state = race_state.copy()

    invalid_tyre_state[
        "TyreCompound"
    ] = "UNKNOWN_TYRE"

    result = get_decision_from_race_state(
        invalid_tyre_state
    )

    print(
        "⚠️ WARNING - Unsupported tyre was accepted."
    )

    print(
        f"   Final Decision: "
        f"{result.get('final_decision')}"
    )

except Exception as e:

    print(
        "✅ PASS - Unsupported tyre handled safely."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 8 - ZERO LAPS REMAINING
# ============================================================

print("\n[TEST 8] Zero Laps Remaining")

try:

    zero_laps_state = race_state.copy()

    zero_laps_state[
        "LapsRemaining"
    ] = 0

    result = get_decision_from_race_state(
        zero_laps_state
    )

    print(
        "✅ PASS - Zero laps remaining processed."
    )

    print(
        f"   Final Decision: "
        f"{result.get('final_decision')}"
    )

except Exception as e:

    print(
        "❌ FAIL - Zero laps remaining caused error."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 9 - VERY HIGH DEGRADATION
# ============================================================

print("\n[TEST 9] Very High Tyre Degradation")

try:

    high_deg_state = race_state.copy()

    high_deg_state[
        "DegradationRate"
    ] = 10.0

    high_deg_state[
        "LapsRemaining"
    ] = 20

    result = get_decision_from_race_state(
        high_deg_state
    )

    print(
        "✅ PASS - High degradation scenario processed."
    )

    print(
        f"   Final Decision: "
        f"{result.get('final_decision')}"
    )

    print(
        f"   Confidence: "
        f"{result.get('confidence')}"
    )

except Exception as e:

    print(
        "❌ FAIL - High degradation caused error."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# TEST 10 - VERY LOW DEGRADATION
# ============================================================

print("\n[TEST 10] Very Low Tyre Degradation")

try:

    low_deg_state = race_state.copy()

    low_deg_state[
        "DegradationRate"
    ] = -10.0

    low_deg_state[
        "LapsRemaining"
    ] = 20

    result = get_decision_from_race_state(
        low_deg_state
    )

    print(
        "✅ PASS - Low degradation scenario processed."
    )

    print(
        f"   Final Decision: "
        f"{result.get('final_decision')}"
    )

    print(
        f"   Confidence: "
        f"{result.get('confidence')}"
    )

except Exception as e:

    print(
        "❌ FAIL - Low degradation caused error."
    )

    print(
        f"   Error: {type(e).__name__}: {e}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print(
    "\n"
    + "=" * 80
)

print(
    "✅ STEP 10D - EDGE-CASE & ROBUSTNESS TESTS EXECUTED"
)

print(
    "=" * 80
)