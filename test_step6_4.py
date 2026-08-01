"""
V5 SPRINT 6 - STEP 4
DRIVER STRATEGY COMPARISON & STRATEGIC OPPORTUNITIES

Validation Test

This test:

1. Loads a real FastF1 session.
2. Discovers all drivers in the session.
3. Builds race states for every driver.
4. Runs the existing Sprint 5 decision engine.
5. Safely handles unavailable driver data.
6. Runs Sprint 6 Step 4 grid comparison.
7. Displays strategic groups and opportunities.
"""

from src.data_loader import load_session
from src.race_state import build_race_state
from src.strategy.decision_engine import (
    get_decision_from_race_state
)

from src.strategy.grid_comparison import (
    build_grid_strategy_comparison,
    print_grid_strategy_comparison
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2025

GRAND_PRIX = "British Grand Prix"

SESSION_TYPE = "R"


# ============================================================
# HEADER
# ============================================================

print(
    "=" * 100
)

print(
    "V5 SPRINT 6 - STEP 4"
)

print(
    "DRIVER STRATEGY COMPARISON & STRATEGIC OPPORTUNITIES"
)

print(
    "FULL-GRID VALIDATION"
)

print(
    "=" * 100
)

print(
    f"Season: {SEASON}"
)

print(
    f"Grand Prix: {GRAND_PRIX}"
)

print(
    f"Session: {SESSION_TYPE}"
)

print(
    "=" * 100
)


# ============================================================
# STEP 1
# LOAD FASTF1 SESSION
# ============================================================

print(
    "\n[1/5] Loading FastF1 session..."
)

try:

    session = load_session(

        SEASON,

        GRAND_PRIX,

        SESSION_TYPE

    )

except Exception as e:

    raise RuntimeError(

        f"Failed to load FastF1 session: {e}"

    ) from e


if session is None:

    raise RuntimeError(

        "FastF1 session returned None."

    )


print(
    "FastF1 session loaded successfully."
)


# ============================================================
# STEP 2
# DISCOVER FULL DRIVER GRID
# ============================================================

print(
    "\n[2/5] Discovering full driver grid..."
)


try:

    results = session.results

except Exception as e:

    raise RuntimeError(

        f"Failed to retrieve session results: {e}"

    ) from e


if results is None or results.empty:

    raise RuntimeError(

        "No driver results available in session."

    )


# ------------------------------------------------------------
# DISCOVER DRIVER ABBREVIATIONS
# ------------------------------------------------------------

drivers = []


if "Abbreviation" in results.columns:

    drivers = (

        results[
            "Abbreviation"
        ]

        .dropna()

        .astype(str)

        .str.strip()

        .tolist()

    )


# ------------------------------------------------------------
# FALLBACK TO DRIVER NUMBER
# ------------------------------------------------------------

elif "DriverNumber" in results.columns:

    drivers = (

        results[
            "DriverNumber"
        ]

        .dropna()

        .astype(str)

        .str.strip()

        .tolist()

    )


# ------------------------------------------------------------
# REMOVE DUPLICATES
# ------------------------------------------------------------

drivers = list(
    dict.fromkeys(
        drivers
    )
)


if not drivers:

    raise RuntimeError(

        "No drivers could be discovered from session results."

    )


print(
    f"Drivers discovered: {len(drivers)}"
)

print(
    "Grid: "
    + ", ".join(
        drivers
    )
)


# ============================================================
# STEP 3
# RUN FULL-GRID STRATEGY ANALYSIS
# ============================================================

print(
    "\n[3/5] Running full-grid strategy analysis..."
)


driver_results = []

failed_drivers = []


for index, driver in enumerate(
    drivers,
    start=1
):

    print(
        f"\n[{index}/{len(drivers)}] "
        f"Analyzing {driver}..."
    )

    try:

        # ----------------------------------------------------
        # BUILD RACE STATE
        # ----------------------------------------------------

        race_state = build_race_state(

            session,

            driver

        )


        if not isinstance(
            race_state,
            dict
        ):

            raise ValueError(

                "Race state generation returned "
                "an invalid result."

            )


        # ----------------------------------------------------
        # RUN DECISION ENGINE
        # ----------------------------------------------------

        decision = get_decision_from_race_state(

            race_state

        )


        if not isinstance(
            decision,
            dict
        ):

            raise ValueError(

                "Decision engine returned "
                "an invalid result."

            )


        # ----------------------------------------------------
        # NORMALIZE RESULT
        # ----------------------------------------------------

        result = {

            "driver":
                decision.get(
                    "driver",
                    driver
                ),

            "position":
                decision.get(
                    "position"
                ),

            "tyre_compound":
                decision.get(
                    "tyre_compound"
                ),

            "tyre_life":
                decision.get(
                    "tyre_life"
                ),

            "pit_probability":
                decision.get(
                    "pit_probability"
                ),

            "ml_recommendation":
                decision.get(
                    "ml_recommendation"
                ),

            "simulator_recommendation":
                decision.get(
                    "simulator_recommendation"
                ),

            "final_decision":
                decision.get(
                    "final_decision"
                ),

            "confidence":
                decision.get(
                    "confidence"
                ),

            "undercut_overcut":
                decision.get(
                    "undercut_overcut"
                )

        }


        driver_results.append(
            result
        )


        print(
            "Status: PASS"
        )


    except Exception as e:

        # ----------------------------------------------------
        # SAFE DATA-QUALITY HANDLING
        # ----------------------------------------------------

        error_message = str(
            e
        )


        failed_drivers.append(

            {

                "driver":
                    driver,

                "error":
                    error_message

            }

        )


        # ----------------------------------------------------
        # KEEP DRIVER IN COMPARISON
        # ----------------------------------------------------

        unavailable_result = {

            "driver":
                driver,

            "position":
                None,

            "tyre_compound":
                None,

            "tyre_life":
                None,

            "pit_probability":
                None,

            "ml_recommendation":
                None,

            "simulator_recommendation":
                "DATA UNAVAILABLE",

            "final_decision":
                "DATA UNAVAILABLE",

            "confidence":
                None,

            "undercut_overcut":
                None

        }


        driver_results.append(
            unavailable_result
        )


        print(
            "Status: SKIPPED"
        )

        print(
            f"Reason: {error_message}"
        )


# ============================================================
# STEP 4
# BUILD GRID COMPARISON
# ============================================================

print(
    "\n[4/5] Building grid strategy comparison..."
)


try:

    comparison = build_grid_strategy_comparison(

        driver_results

    )

except Exception as e:

    raise RuntimeError(

        f"Failed to build grid strategy comparison: {e}"

    ) from e


print(
    "Grid strategy comparison generated successfully."
)


# ============================================================
# DISPLAY COMPLETE COMPARISON
# ============================================================

print_grid_strategy_comparison(

    comparison

)


# ============================================================
# STEP 5
# VALIDATION SUMMARY
# ============================================================

print(
    "\n[5/5] STEP 6.4 VALIDATION SUMMARY"
)

print(
    "=" * 100
)


total_drivers = comparison.get(

    "total_drivers",

    0

)


successful_drivers = comparison.get(

    "successful_drivers",

    0

)


unavailable_drivers = comparison.get(

    "data_unavailable_drivers",

    0

)


high_confidence = comparison.get(

    "high_confidence_drivers",

    []

)


low_confidence = comparison.get(

    "low_confidence_drivers",

    []

)


pit_opportunities = comparison.get(

    "pit_opportunities",

    []

)


strategy_conflicts = comparison.get(

    "strategy_conflicts",

    []

)


undercut_opportunities = comparison.get(

    "undercut_opportunities",

    []

)


overcut_opportunities = comparison.get(

    "overcut_opportunities",

    []

)


print(
    f"Total Drivers: "
    f"{total_drivers}"
)


print(
    f"Successful Analyses: "
    f"{successful_drivers}"
)


print(
    f"Data Unavailable: "
    f"{unavailable_drivers}"
)


print(
    f"High-Confidence Decisions: "
    f"{len(high_confidence)}"
)


print(
    f"Low-Confidence Decisions: "
    f"{len(low_confidence)}"
)


print(
    f"Pit Opportunities: "
    f"{len(pit_opportunities)}"
)


print(
    f"ML/Simulator Conflicts: "
    f"{len(strategy_conflicts)}"
)


print(
    f"Undercut Opportunities: "
    f"{len(undercut_opportunities)}"
)


print(
    f"Overcut Opportunities: "
    f"{len(overcut_opportunities)}"
)


# ============================================================
# FAILED / DATA-UNAVAILABLE DRIVERS
# ============================================================

if failed_drivers:

    print(
        "\n"
        + "-" * 100
    )

    print(
        "DRIVERS WITH DATA-QUALITY EXCEPTIONS"
    )

    print(
        "-" * 100
    )


    for item in failed_drivers:

        print(

            f"{item['driver']}: "
            f"{item['error']}"

        )


# ============================================================
# FINAL VALIDATION
# ============================================================

print(
    "\n"
    + "=" * 100
)


if total_drivers == 0:

    print(
        "❌ STEP 6.4 VALIDATION FAILED"
    )

    print(
        "No drivers were available for comparison."
    )


elif successful_drivers == 0:

    print(
        "❌ STEP 6.4 VALIDATION FAILED"
    )

    print(
        "No successful driver analyses were available."
    )


else:

    print(
        "✅ STEP 6.4 - GRID STRATEGY COMPARISON "
        "VALIDATION COMPLETED"
    )

    print(
        "The full-grid strategy comparison engine "
        "executed successfully."
    )

    print(
        "Drivers with unavailable data were safely "
        "excluded from strategic recommendations."
    )


print(
    "=" * 100
)