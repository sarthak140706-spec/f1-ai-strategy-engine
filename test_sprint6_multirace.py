"""
V5 Sprint 6 - Step 6
Full-Grid Multi-Race Validation

F1 AI Strategist V5

Objectives:
1. Validate full-grid driver discovery across multiple races.
2. Run the existing Sprint 6 multi-driver strategy pipeline.
3. Safely handle unavailable driver data.
4. Validate multiple races without stopping on individual failures.
5. Produce a final multi-race validation summary.
"""

from __future__ import annotations

from typing import Any


# ============================================================
# IMPORTS
# ============================================================

from src.data_loader import load_session

from src.race_state import build_race_state

from src.strategy.grid_manager import (
    discover_drivers
)

from src.strategy.grid_comparison import (
    build_grid_strategy_comparison
)

from src.strategy.multi_driver_strategy import (
    build_multi_driver_strategy
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2025

SESSION_TYPE = "R"


# ============================================================
# MULTI-RACE TEST SET
# ============================================================

TEST_RACES = [

    "Bahrain Grand Prix",

    "British Grand Prix",

    "Monaco Grand Prix"

]


# ============================================================
# ANALYZE SINGLE DRIVER
# ============================================================

def analyze_driver(
    session: Any,
    driver_info: dict[str, Any]
) -> dict[str, Any]:
    """
    Build race state and run the existing V5 decision engine
    for one driver.

    Individual driver failures are converted into
    DATA UNAVAILABLE results so the full-grid test can
    continue.
    """

    driver = driver_info.get(
        "driver"
    )

    try:

        # ----------------------------------------------------
        # BUILD DRIVER RACE STATE
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
                "Race state generation returned invalid data."
            )

        # ----------------------------------------------------
        # RUN EXISTING DECISION ENGINE
        # ----------------------------------------------------

        from src.strategy.decision_engine import (
            get_decision_from_race_state
        )

        decision = get_decision_from_race_state(

            race_state

        )

        if not isinstance(
            decision,
            dict
        ):

            raise ValueError(
                "Decision engine returned invalid data."
            )

        # ----------------------------------------------------
        # NORMALIZE RESULT
        # ----------------------------------------------------

        return {

            "driver":
                driver,

            "position":
                decision.get(
                    "position",
                    driver_info.get(
                        "position"
                    )
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
                ),

            "status":
                "SUCCESS"

        }

    except Exception as error:

        return {

            "driver":
                driver,

            "position":
                driver_info.get(
                    "position"
                ),

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
                None,

            "status":
                "DATA UNAVAILABLE",

            "error":
                f"{type(error).__name__}: {error}"

        }


# ============================================================
# VALIDATE SINGLE RACE
# ============================================================

def validate_race(
    season: int,
    grand_prix: str,
    session_type: str
) -> dict[str, Any]:
    """
    Run the complete full-grid strategy pipeline
    for one race.
    """

    print(
        "\n"
        + "=" * 110
    )

    print(
        f"RACE VALIDATION: {grand_prix}"
    )

    print(
        "=" * 110
    )

    # --------------------------------------------------------
    # LOAD SESSION
    # --------------------------------------------------------

    print(
        "\n[1/5] Loading FastF1 session..."
    )

    session = load_session(

        season,

        grand_prix,

        session_type

    )

    if session is None:

        raise RuntimeError(
            "FastF1 session could not be loaded."
        )

    print(
        "FastF1 session loaded successfully."
    )

    # --------------------------------------------------------
    # DISCOVER FULL GRID
    # --------------------------------------------------------

    print(
        "\n[2/5] Discovering full driver grid..."
    )

    drivers = discover_drivers(

        session

    )

    print(
        f"Drivers discovered: "
        f"{len(drivers)}"
    )

    print(
        "Grid: "
        + ", ".join(

            driver[
                "driver"
            ]

            for driver in drivers

        )

    )

    # --------------------------------------------------------
    # ANALYZE ALL DRIVERS
    # --------------------------------------------------------

    print(
        "\n[3/5] Running full-grid strategy analysis..."
    )

    driver_results = []

    successful_drivers = []

    unavailable_drivers = []

    for index, driver_info in enumerate(

        drivers,

        start=1

    ):

        driver = driver_info.get(
            "driver"
        )

        print(
            f"\n[{index}/{len(drivers)}] "
            f"Analyzing {driver}..."
        )

        result = analyze_driver(

            session,

            driver_info

        )

        driver_results.append(
            result
        )

        if result.get(
            "status"
        ) == "SUCCESS":

            successful_drivers.append(
                driver
            )

            print(
                "Status: PASS"
            )

        else:

            unavailable_drivers.append(
                driver
            )

            print(
                "Status: DATA UNAVAILABLE"
            )

            print(
                "Reason: "
                + result.get(
                    "error",
                    "Unknown error"
                )
            )

    # --------------------------------------------------------
    # BUILD GRID COMPARISON
    # --------------------------------------------------------

    print(
        "\n[4/5] Building grid strategy comparison..."
    )

    comparison = build_grid_strategy_comparison(

        driver_results

    )

    # --------------------------------------------------------
    # BUILD GLOBAL MULTI-DRIVER STRATEGY
    # --------------------------------------------------------

    print(
        "\n[5/5] Building global multi-driver strategy..."
    )

    final_strategy = build_multi_driver_strategy(

        comparison

    )

    # --------------------------------------------------------
    # PRINT RACE SUMMARY
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 110
    )

    print(
        f"{grand_prix.upper()} VALIDATION SUMMARY"
    )

    print(
        "-" * 110
    )

    print(
        f"Total Drivers: "
        f"{len(drivers)}"
    )

    print(
        f"Successful Analyses: "
        f"{len(successful_drivers)}"
    )

    print(
        f"Data Unavailable: "
        f"{len(unavailable_drivers)}"
    )

    focus = final_strategy.get(
        "primary_strategic_focus",
        {}
    )

    print(
        f"Primary Focus: "
        f"{focus.get('primary_focus')}"
    )

    print(
        f"Priority Driver: "
        f"{focus.get('priority_driver')}"
    )

    # --------------------------------------------------------
    # DISPLAY STRATEGY GROUPS
    # --------------------------------------------------------

    groups = final_strategy.get(
        "strategy_groups",
        {}
    )

    print(
        "\nPIT NOW:"
    )

    print(

        ", ".join(

            groups.get(
                "pit_drivers",
                []
            )

        )

        or

        "None"

    )

    print(
        "\nSTAY OUT:"
    )

    print(

        ", ".join(

            groups.get(
                "stay_out_drivers",
                []
            )

        )

        or

        "None"

    )

    print(
        "\nDATA UNAVAILABLE:"
    )

    print(

        ", ".join(

            groups.get(
                "data_unavailable_drivers",
                []
            )

        )

        or

        "None"

    )

    return {

        "season":
            season,

        "grand_prix":
            grand_prix,

        "session_type":
            session_type,

        "total_drivers":
            len(
                drivers
            ),

        "successful_drivers":
            len(
                successful_drivers
            ),

        "data_unavailable_drivers":
            len(
                unavailable_drivers
            ),

        "successful_driver_list":
            successful_drivers,

        "unavailable_driver_list":
            unavailable_drivers,

        "driver_results":
            driver_results,

        "comparison":
            comparison,

        "final_strategy":
            final_strategy

    }


# ============================================================
# MULTI-RACE VALIDATION
# ============================================================

def run_multi_race_validation() -> dict[str, Any]:
    """
    Run Sprint 6 Step 6 validation across multiple races.

    The test continues if one race fails to load or process.
    """

    print(
        "=" * 110
    )

    print(
        "V5 SPRINT 6 - STEP 6"
    )

    print(
        "FULL-GRID MULTI-RACE VALIDATION"
    )

    print(
        "=" * 110
    )

    print(
        f"Season: {SEASON}"
    )

    print(
        f"Session: {SESSION_TYPE}"
    )

    print(
        f"Races Under Test: "
        f"{len(TEST_RACES)}"
    )

    print(
        "=" * 110
    )

    race_results = []

    failed_races = []

    total_drivers = 0

    total_successful = 0

    total_unavailable = 0

    # --------------------------------------------------------
    # RUN EACH RACE
    # --------------------------------------------------------

    for race_index, grand_prix in enumerate(

        TEST_RACES,

        start=1

    ):

        print(
            "\n"
            + "#" * 110
        )

        print(
            f"RACE {race_index}/{len(TEST_RACES)}"
        )

        print(
            f"{grand_prix}"
        )

        print(
            "#" * 110
        )

        try:

            result = validate_race(

                SEASON,

                grand_prix,

                SESSION_TYPE

            )

            race_results.append(
                result
            )

            total_drivers += result[
                "total_drivers"
            ]

            total_successful += result[
                "successful_drivers"
            ]

            total_unavailable += result[
                "data_unavailable_drivers"
            ]

        except Exception as error:

            failed_races.append(

                {

                    "grand_prix":
                        grand_prix,

                    "error":
                        f"{type(error).__name__}: {error}"

                }

            )

            print(
                "\nRACE STATUS: FAILED"
            )

            print(
                "Reason: "
                + f"{type(error).__name__}: {error}"
            )

            print(
                "Continuing with next race..."
            )

    # ========================================================
    # FINAL MULTI-RACE SUMMARY
    # ========================================================

    print(
        "\n"
        + "=" * 110
    )

    print(
        "SPRINT 6 STEP 6 - MULTI-RACE VALIDATION SUMMARY"
    )

    print(
        "=" * 110
    )

    print(
        f"Races Requested: "
        f"{len(TEST_RACES)}"
    )

    print(
        f"Races Successfully Validated: "
        f"{len(race_results)}"
    )

    print(
        f"Races Failed: "
        f"{len(failed_races)}"
    )

    print(
        f"Total Driver Analyses: "
        f"{total_drivers}"
    )

    print(
        f"Successful Driver Analyses: "
        f"{total_successful}"
    )

    print(
        f"Data-Unavailable Driver Analyses: "
        f"{total_unavailable}"
    )

    # --------------------------------------------------------
    # PER-RACE SUMMARY TABLE
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 110
    )

    print(
        "PER-RACE VALIDATION RESULTS"
    )

    print(
        "-" * 110
    )

    print(

        f"{'Race':<25}"

        f"{'Drivers':<10}"

        f"{'Success':<10}"

        f"{'Unavailable':<15}"

        f"{'Status':<15}"

    )

    print(
        "-" * 80
    )

    for result in race_results:

        status = (

            "PASS"

            if result[
                "total_drivers"
            ] > 0

            else

            "FAILED"

        )

        print(

            f"{result['grand_prix']:<25}"

            f"{result['total_drivers']:<10}"

            f"{result['successful_drivers']:<10}"

            f"{result['data_unavailable_drivers']:<15}"

            f"{status:<15}"

        )

    # --------------------------------------------------------
    # FAILED RACES
    # --------------------------------------------------------

    if failed_races:

        print(
            "\n"
            + "-" * 110
        )

        print(
            "RACES REQUIRING FURTHER VALIDATION"
        )

        print(
            "-" * 110
        )

        for failed in failed_races:

            print(

                f"{failed['grand_prix']}: "

                f"{failed['error']}"

            )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    print(
        "\n"
        + "=" * 110
    )

    if (

        len(
            race_results
        )

        ==

        len(
            TEST_RACES
        )

        and

        total_drivers > 0

    ):

        print(
            "STEP 6.6 - MULTI-RACE VALIDATION COMPLETED"
        )

        print(
            "The full-grid strategy pipeline successfully "
            "processed all configured races."
        )

    elif race_results:

        print(
            "STEP 6.6 - MULTI-RACE VALIDATION COMPLETED "
            "WITH PARTIAL RESULTS"
        )

        print(
            "Some races could not be processed, but the "
            "strategy engine remained operational."
        )

    else:

        print(
            "STEP 6.6 - MULTI-RACE VALIDATION FAILED"
        )

        print(
            "No race completed successfully."
        )

    print(
        "=" * 110
    )

    return {

        "races_requested":
            len(
                TEST_RACES
            ),

        "races_successful":
            len(
                race_results
            ),

        "races_failed":
            len(
                failed_races
            ),

        "total_driver_analyses":
            total_drivers,

        "successful_driver_analyses":
            total_successful,

        "data_unavailable_driver_analyses":
            total_unavailable,

        "race_results":
            race_results,

        "failed_races":
            failed_races

    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_multi_race_validation()