from src.data_loader import load_session

from src.strategy.dynamic_race_state import (
    build_dynamic_race_state
)

from src.strategy.dynamic_race_situation import (
    analyze_dynamic_race_situation
)

from src.strategy.dynamic_tyre_strategy import (
    generate_dynamic_tyre_strategy,
    display_dynamic_tyre_strategy
)


# ============================================================
# PHASE 4.3 TEST
# ============================================================

print(
    "\n" + "=" * 72
)

print(
    "F1 AI STRATEGIST"
)

print(
    "PHASE 4.3 — DYNAMIC TYRE STRATEGY ENGINE TEST"
)

print(
    "=" * 72
)


# ============================================================
# CONFIGURATION
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
    "\n[1/5] Loading race session..."
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
# BUILD DYNAMIC RACE STATE
# ============================================================

print(
    "\n[2/5] Building dynamic race state..."
)

race_state = build_dynamic_race_state(

    session=session,

    driver=DRIVER,

    selected_lap=SELECTED_LAP

)

assert race_state

print(
    "✅ Phase 4.1 race state generated."
)


# ============================================================
# STEP 3
# ANALYZE RACE SITUATION
# ============================================================

print(
    "\n[3/5] Analyzing dynamic race situation..."
)

race_situation = (
    analyze_dynamic_race_situation(
        race_state
    )
)

assert race_situation

print(
    "✅ Phase 4.2 race situation generated."
)


# ============================================================
# STEP 4
# GENERATE DYNAMIC TYRE STRATEGY
# ============================================================

print(
    "\n[4/5] Evaluating dynamic tyre strategies..."
)

result = generate_dynamic_tyre_strategy(

    race_state=race_state,

    race_situation=race_situation

)

display_dynamic_tyre_strategy(
    result
)


# ============================================================
# STEP 5
# VALIDATION
# ============================================================

print(
    "\n[5/5] Validating tyre strategy engine..."
)


# ------------------------------------------------------------
# CORRECT LAP
# ------------------------------------------------------------

assert (
    result["current_lap"]
    ==
    SELECTED_LAP
), (
    "Incorrect current lap."
)


# ------------------------------------------------------------
# STRATEGIES GENERATED
# ------------------------------------------------------------

assert (
    result["strategy_count"]
    ==
    4
), (
    "Expected four tyre strategies."
)


# ------------------------------------------------------------
# BEST STRATEGY EXISTS
# ------------------------------------------------------------

assert (
    result["best_strategy"]
    is not None
), (
    "Best tyre strategy missing."
)


# ------------------------------------------------------------
# VALID RECOMMENDATION
# ------------------------------------------------------------

assert (
    result["recommendation"]
    in [
        "STAY OUT",
        "PIT"
    ]
), (
    "Invalid tyre recommendation."
)


# ------------------------------------------------------------
# VALID COMPOUND
# ------------------------------------------------------------

assert (
    result["recommended_compound"]
    in [
        "SOFT",
        "MEDIUM",
        "HARD"
    ]
), (
    "Invalid recommended compound."
)


# ------------------------------------------------------------
# ALL OPTIONS CONTAIN REQUIRED DATA
# ------------------------------------------------------------

for strategy in result[
    "strategies"
]:

    assert (
        "strategy_rank"
        in strategy
    )

    assert (
        "projected_total_time"
        in strategy
    )

    assert (
        "average_lap_time"
        in strategy
    )

    assert (
        "time_difference"
        in strategy
    )

    assert (
        "degradation_impact"
        in strategy
    )


# ------------------------------------------------------------
# RANKING VALIDATION
# ------------------------------------------------------------

assert (
    result[
        "strategies"
    ][0][
        "strategy_rank"
    ]
    ==
    1
), (
    "Best tyre strategy was not ranked first."
)


# ------------------------------------------------------------
# TIMES SHOULD BE SORTED
# ------------------------------------------------------------

times = [

    strategy[
        "projected_total_time"
    ]

    for strategy
    in result[
        "strategies"
    ]

]

assert (
    times
    ==
    sorted(times)
), (
    "Tyre strategies are not correctly ranked."
)


# ------------------------------------------------------------
# CONFIDENCE
# ------------------------------------------------------------

assert (
    0
    <=
    result["confidence"]
    <=
    100
), (
    "Confidence must be between 0 and 100."
)


# ------------------------------------------------------------
# REASONING
# ------------------------------------------------------------

assert (
    result["reason"]
), (
    "Recommendation reasoning missing."
)


print(
    "\n" + "=" * 72
)

print(
    "✅ PHASE 4.3 DYNAMIC TYRE STRATEGY TEST PASSED"
)

print(
    "=" * 72
)