# ============================================================
# V5 SPRINT 6 - STEP 6.3
# FULL-GRID STRATEGY ANALYSIS
# ROBUST FULL-GRID VALIDATION
# ============================================================

from src.data_loader import load_session
from src.race_state import build_race_state
from src.strategy.decision_engine import get_decision_from_race_state


# ============================================================
# CONFIGURATION
# ============================================================

SEASON = 2025

GRAND_PRIX = "British Grand Prix"

SESSION_TYPE = "R"


# ============================================================
# SUPPORTED TYRE COMPOUNDS
# ============================================================

SUPPORTED_TYRES = {

    "SOFT",
    "MEDIUM",
    "HARD"

}


# ============================================================
# HELPER - SAFE VALUE
# ============================================================

def safe_value(
    value,
    default="N/A"
):

    if value is None:

        return default

    return value


# ============================================================
# HELPER - FORMAT PIT PROBABILITY
# ============================================================

def format_probability(
    value
):

    if value is None:

        return "N/A"

    try:

        return f"{float(value):.4f}%"

    except Exception:

        return "N/A"


# ============================================================
# HELPER - GET DRIVER GRID
# ============================================================

def get_driver_grid(
    session
):

    drivers = []

    try:

        results = session.results

        if results is not None and not results.empty:

            for _, row in results.iterrows():

                abbreviation = row.get(
                    "Abbreviation"
                )

                if (

                    abbreviation is not None

                    and

                    str(abbreviation).strip()

                ):

                    driver = str(
                        abbreviation
                    ).strip().upper()

                    if driver not in drivers:

                        drivers.append(
                            driver
                        )

    except Exception:

        pass


    # --------------------------------------------------------
    # FALLBACK TO SESSION DRIVER LIST
    # --------------------------------------------------------

    if not drivers:

        try:

            drivers = [

                str(driver).strip().upper()

                for driver in session.drivers

                if driver is not None

            ]

        except Exception:

            drivers = []


    return drivers


# ============================================================
# HELPER - VALIDATE DRIVER DATA
# ============================================================

def validate_driver_data(
    race_state
):

    # --------------------------------------------------------
    # CHECK TYRE
    # --------------------------------------------------------

    tyre = race_state.get(
        "TyreCompound"
    )

    if tyre is None:

        return (

            False,

            "Missing tyre compound"

        )


    tyre = str(
        tyre
    ).strip().upper()


    if tyre not in SUPPORTED_TYRES:

        return (

            False,

            f"Unsupported tyre compound: {tyre}"

        )


    # --------------------------------------------------------
    # REQUIRED NUMERIC FEATURES
    # --------------------------------------------------------

    required_features = [

        "RecentPace",

        "AvgPaceLast5",

        "AvgPaceLast10",

        "DegradationRate",

        "LapsRemaining"

    ]


    missing_features = []


    for feature in required_features:

        value = race_state.get(
            feature
        )


        if value is None:

            missing_features.append(
                feature
            )

            continue


        try:

            # NaN check

            if value != value:

                missing_features.append(
                    feature
                )

        except Exception:

            pass


    if missing_features:

        return (

            False,

            "Missing values in race-state features: "

            + ", ".join(
                missing_features
            )

        )


    # --------------------------------------------------------
    # VALIDATE DRIVER
    # --------------------------------------------------------

    driver = race_state.get(
        "Driver"
    )


    if not driver:

        return (

            False,

            "Driver identifier is missing"

        )


    return (

        True,

        None

    )


# ============================================================
# HELPER - BUILD RESULT
# ============================================================

def build_result_record(
    race_state,
    decision
):

    return {

        "Driver":
            race_state.get(
                "Driver"
            ),

        "Position":
            race_state.get(
                "Position"
            ),

        "TyreCompound":
            race_state.get(
                "TyreCompound"
            ),

        "TyreLife":
            race_state.get(
                "TyreLife"
            ),

        "PitProbability":
            decision.get(
                "pit_probability"
            ),

        "Simulator":
            decision.get(
                "simulator_recommendation"
            ),

        "Final":
            decision.get(
                "final_decision"
            ),

        "Confidence":
            decision.get(
                "confidence"
            ),

        "Status":
            "PASS",

        "Reason":
            None

    }


# ============================================================
# HELPER - BUILD SKIPPED RESULT
# ============================================================

def build_skipped_record(
    driver,
    race_state=None,
    reason=None
):

    if race_state is None:

        race_state = {}


    return {

        "Driver":
            driver,

        "Position":
            race_state.get(
                "Position"
            ),

        "TyreCompound":
            race_state.get(
                "TyreCompound"
            ),

        "TyreLife":
            race_state.get(
                "TyreLife"
            ),

        "PitProbability":
            None,

        "Simulator":
            "DATA UNAVAILABLE",

        "Final":
            "DATA UNAVAILABLE",

        "Confidence":
            "N/A",

        "Status":
            "SKIPPED",

        "Reason":
            reason

    }


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "=" * 100
    )

    print(
        "V5 SPRINT 6 - STEP 3"
    )

    print(
        "FULL-GRID STRATEGY ANALYSIS"
    )

    print(
        "ROBUST FULL-GRID VALIDATION"
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


    # ========================================================
    # STEP 1 - LOAD SESSION
    # ========================================================

    print(
        "\n[1/4] Loading FastF1 session..."
    )


    try:

        session = load_session(

            SEASON,

            GRAND_PRIX,

            SESSION_TYPE

        )


        if session is None:

            raise RuntimeError(

                "FastF1 session returned None."

            )


        print(
            "FastF1 session loaded successfully."
        )


    except Exception as e:

        print(
            f"❌ Failed to load session: {type(e).__name__}: {e}"
        )

        return


    # ========================================================
    # STEP 2 - DISCOVER FULL GRID
    # ========================================================

    print(
        "\n[2/4] Discovering full driver grid..."
    )


    drivers = get_driver_grid(
        session
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


    if not drivers:

        print(
            "❌ No drivers discovered."
        )

        return


    # ========================================================
    # STEP 3 - FULL GRID ANALYSIS
    # ========================================================

    print(
        "\n[3/4] Running full-grid strategy analysis..."
    )


    results = []

    skipped_results = []


    for index, driver in enumerate(

        drivers,

        start=1

    ):

        print(
            f"\n[{index}/{len(drivers)}] "
            f"Analyzing {driver}..."
        )


        race_state = None


        try:

            # ------------------------------------------------
            # BUILD DRIVER RACE STATE
            # ------------------------------------------------

            race_state = build_race_state(

                session,

                driver

            )


            # ------------------------------------------------
            # VALIDATE DRIVER DATA
            # ------------------------------------------------

            is_valid, validation_error = (

                validate_driver_data(

                    race_state

                )

            )


            if not is_valid:

                skipped_record = (

                    build_skipped_record(

                        driver,

                        race_state,

                        validation_error

                    )

                )


                skipped_results.append(
                    skipped_record
                )


                print(
                    "Status: SKIPPED"
                )


                print(
                    "Reason: "
                    + str(
                        validation_error
                    )
                )


                continue


            # ------------------------------------------------
            # RUN DECISION ENGINE
            # ------------------------------------------------

            decision = (

                get_decision_from_race_state(

                    race_state

                )

            )


            result = build_result_record(

                race_state,

                decision

            )


            results.append(
                result
            )


            print(
                "Status: PASS"
            )


        except Exception as e:

            error_message = (

                f"{type(e).__name__}: {e}"

            )


            skipped_record = (

                build_skipped_record(

                    driver,

                    race_state,

                    error_message

                )

            )


            skipped_results.append(

                skipped_record

            )


            print(
                "Status: SKIPPED"
            )


            print(
                "Reason: "
                + error_message
            )


    # ========================================================
    # STEP 4 - FULL GRID COMPARISON
    # ========================================================

    print(
        "\n[4/4] Building full-grid strategy comparison..."
    )


    print(
        "\n"
        + "=" * 100
    )


    print(
        "FULL-GRID STRATEGY COMPARISON"
    )


    print(
        "=" * 100
    )


    print(

        f"{'Driver':<8}"

        f"{'Pos':<6}"

        f"{'Tyre':<15}"

        f"{'Age':<6}"

        f"{'Pit Prob.':<15}"

        f"{'Simulator':<15}"

        f"{'Final':<18}"

        f"{'Confidence':<12}"

    )


    print(
        "-" * 100
    )


    # --------------------------------------------------------
    # SUCCESSFUL RESULTS
    # --------------------------------------------------------

    for result in results:

        print(

            f"{str(safe_value(result['Driver'])):<8}"

            f"{str(safe_value(result['Position'])):<6}"

            f"{str(safe_value(result['TyreCompound'])):<15}"

            f"{str(safe_value(result['TyreLife'])):<6}"

            f"{format_probability(result['PitProbability']):<15}"

            f"{str(safe_value(result['Simulator'])):<15}"

            f"{str(safe_value(result['Final'])):<18}"

            f"{str(safe_value(result['Confidence'])):<12}"

        )


    # --------------------------------------------------------
    # SKIPPED RESULTS
    # --------------------------------------------------------

    for result in skipped_results:

        print(

            f"{str(safe_value(result['Driver'])):<8}"

            f"{str(safe_value(result['Position'])):<6}"

            f"{str(safe_value(result['TyreCompound'])):<15}"

            f"{str(safe_value(result['TyreLife'])):<6}"

            f"{'N/A':<15}"

            f"{'DATA UNAVAILABLE':<15}"

            f"{'DATA UNAVAILABLE':<18}"

            f"{'N/A':<12}"

        )


    # ========================================================
    # STRATEGIC GROUPS
    # ========================================================

    print(
        "\n"
        + "=" * 100
    )


    print(
        "FULL-GRID STRATEGIC GROUPS"
    )


    print(
        "=" * 100
    )


    pit_drivers = [

        result["Driver"]

        for result in results

        if result["Final"] == "PIT NOW"

    ]


    stay_out_drivers = [

        result["Driver"]

        for result in results

        if result["Final"] == "STAY OUT"

    ]


    high_confidence_drivers = [

        result["Driver"]

        for result in results

        if result["Confidence"] == "HIGH"

    ]


    print(
        "\nDrivers Recommended to PIT:"
    )


    print(

        ", ".join(

            pit_drivers

        )

        if pit_drivers

        else "None"

    )


    print(
        "\nDrivers Recommended to STAY OUT:"
    )


    print(

        ", ".join(

            stay_out_drivers

        )

        if stay_out_drivers

        else "None"

    )


    print(
        "\nHigh-Confidence Strategy Decisions:"
    )


    print(

        ", ".join(

            high_confidence_drivers

        )

        if high_confidence_drivers

        else "None"

    )


    # ========================================================
    # SKIPPED / DATA UNAVAILABLE
    # ========================================================

    if skipped_results:

        print(
            "\n"
            + "=" * 100
        )


        print(
            "DRIVERS REQUIRING FURTHER VALIDATION"
        )


        print(
            "=" * 100
        )


        for result in skipped_results:

            print(

                f"{result['Driver']}: "

                f"{result['Reason']}"

            )


    # ========================================================
    # VALIDATION SUMMARY
    # ========================================================

    total_drivers = len(
        drivers
    )


    successful = len(
        results
    )


    skipped = len(
        skipped_results
    )


    print(
        "\n"
        + "=" * 100
    )


    print(
        "STEP 6.3 VALIDATION SUMMARY"
    )


    print(
        "=" * 100
    )


    print(

        f"Total Drivers Discovered: "

        f"{total_drivers}"

    )


    print(

        f"Successful Analyses:      "

        f"{successful}"

    )


    print(

        f"Skipped / Data Unavailable: "

        f"{skipped}"

    )


    if skipped_results:

        print(
            "\nDrivers Requiring Further Validation:"
        )


        print(

            ", ".join(

                result["Driver"]

                for result in skipped_results

            )

        )


        print(
            "\n⚠️ STEP 6.3 - FULL-GRID ANALYSIS "
            "COMPLETED WITH DATA-QUALITY EXCEPTIONS"
        )


        print(

            "The strategy engine remained operational. "

            "Drivers without sufficient or supported data "

            "were safely classified as DATA UNAVAILABLE."

        )


    else:

        print(
            "\n"
            "✅ STEP 6.3 - FULL-GRID ANALYSIS "
            "COMPLETED SUCCESSFULLY"
        )


        print(

            "All discovered drivers were successfully "
            "analyzed."

        )


    print(
        "=" * 100
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()