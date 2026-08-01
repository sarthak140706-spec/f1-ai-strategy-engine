"""
V5 SPRINT 6 - STEP 2
MULTI-DRIVER STRATEGY COMPARISON

Purpose:
    Analyze multiple drivers simultaneously and compare their
    strategic situations using the existing strategy engine.

Drivers:
    VER - Max Verstappen
    HAM - Lewis Hamilton
    LEC - Charles Leclerc
    ALO - Fernando Alonso
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

DRIVERS = [
    "VER",
    "HAM",
    "LEC",
    "ALO"
]


# ============================================================
# DISPLAY HELPERS
# ============================================================

def safe_value(value, default="N/A"):
    """
    Safely display values that may be missing or None.
    """
    if value is None:
        return default

    return value


def get_result_value(result, *keys, default="N/A"):
    """
    Retrieve a value from a dictionary using multiple possible keys.
    """

    if not isinstance(result, dict):
        return default

    for key in keys:

        if key in result:
            return safe_value(
                result[key],
                default
            )

    return default


# ============================================================
# DRIVER STRATEGY ANALYSIS
# ============================================================

def analyze_driver(
    session,
    driver
):
    """
    Build race state and generate strategy decision
    for a single driver.
    """

    race_state = build_race_state(
        session=session,
        driver=driver
    )

    decision = get_decision_from_race_state(
        race_state
    )

    return race_state, decision


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 90)

    print(
        "V5 SPRINT 6 - STEP 2"
    )

    print(
        "MULTI-DRIVER STRATEGY COMPARISON"
    )

    print("=" * 90)

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
        f"Drivers: {', '.join(DRIVERS)}"
    )

    print("=" * 90)


    # --------------------------------------------------------
    # LOAD SESSION
    # --------------------------------------------------------

    print(
        "\n[1/3] Loading FastF1 session..."
    )

    session = load_session(
        SEASON,
        GRAND_PRIX,
        SESSION_TYPE
    )

    print(
        "FastF1 session loaded successfully."
    )


    # --------------------------------------------------------
    # ANALYZE DRIVERS
    # --------------------------------------------------------

    print(
        "\n[2/3] Analyzing drivers..."
    )


    results = []


    for driver in DRIVERS:

        print(
            f"\nAnalyzing driver: {driver}"
        )

        try:

            race_state, decision = analyze_driver(
                session,
                driver
            )


            result = {

                "Driver": driver,

                "Position": get_result_value(
                    race_state,
                    "Position",
                    "position"
                ),

                "Tyre": get_result_value(
                    race_state,
                    "TyreCompound",
                    "tyre_compound",
                    "Tyre"
                ),

                "TyreLife": get_result_value(
                    race_state,
                    "TyreLife",
                    "tyre_life"
                ),

                "RecentPace": get_result_value(
                    race_state,
                    "RecentPace",
                    "recent_pace"
                ),

                "Degradation": get_result_value(
                    race_state,
                    "DegradationRate",
                    "degradation_rate"
                ),

                "PitProbability": get_result_value(
                    decision,
                    "PitProbability",
                    "pit_probability"
                ),

                "Simulator": get_result_value(
                    decision,
                    "SimulatorRecommendation",
                    "simulator_recommendation",
                    "Simulator"
                ),

                "FinalDecision": get_result_value(
                    decision,
                    "FinalDecision",
                    "final_decision",
                    "Decision"
                ),

                "Confidence": get_result_value(
                    decision,
                    "Confidence",
                    "confidence"
                )

            }


            results.append(
                result
            )


            print(
                f"Status: PASS"
            )


        except Exception as e:

            print(
                f"Status: FAIL"
            )

            print(
                f"Error: {type(e).__name__}: {e}"
            )


    # --------------------------------------------------------
    # COMPARISON
    # --------------------------------------------------------

    print(
        "\n[3/3] Building multi-driver comparison..."
    )

    print(
        "\n" + "=" * 90
    )

    print(
        "MULTI-DRIVER STRATEGY COMPARISON"
    )

    print(
        "=" * 90
    )


    if not results:

        print(
            "❌ No valid driver results generated."
        )

        return


    # --------------------------------------------------------
    # TABLE HEADER
    # --------------------------------------------------------

    print(

        f"{'Driver':<8}"

        f"{'Pos':<8}"

        f"{'Tyre':<12}"

        f"{'Tyre Age':<10}"

        f"{'Pit Prob.':<14}"

        f"{'Simulator':<15}"

        f"{'Final':<15}"

        f"{'Confidence':<12}"

    )


    print(
        "-" * 90
    )


    # --------------------------------------------------------
    # TABLE ROWS
    # --------------------------------------------------------

    for result in results:

        print(

            f"{str(result['Driver']):<8}"

            f"{str(result['Position']):<8}"

            f"{str(result['Tyre']):<12}"

            f"{str(result['TyreLife']):<10}"

            f"{str(result['PitProbability']):<14}"

            f"{str(result['Simulator']):<15}"

            f"{str(result['FinalDecision']):<15}"

            f"{str(result['Confidence']):<12}"

        )


    # ========================================================
    # STRATEGIC INSIGHTS
    # ========================================================

    print(
        "\n" + "=" * 90
    )

    print(
        "STRATEGIC COMPARISON INSIGHTS"
    )

    print(
        "=" * 90
    )


    # --------------------------------------------------------
    # HIGHEST CONFIDENCE
    # --------------------------------------------------------

    high_confidence = [

        result

        for result in results

        if str(
            result["Confidence"]
        ).upper() == "HIGH"

    ]


    if high_confidence:

        print(
            "\nHighest Confidence Drivers:"
        )

        print(

            ", ".join(

                result["Driver"]

                for result in high_confidence

            )

        )

    else:

        print(
            "\nHighest Confidence Drivers: None"
        )


    # --------------------------------------------------------
    # PIT RECOMMENDATIONS
    # --------------------------------------------------------

    pit_drivers = [

        result

        for result in results

        if "PIT" in str(
            result["FinalDecision"]
        ).upper()

    ]


    if pit_drivers:

        print(
            "\nDrivers Recommended to PIT:"
        )

        print(

            ", ".join(

                result["Driver"]

                for result in pit_drivers

            )

        )

    else:

        print(
            "\nDrivers Recommended to PIT: None"
        )


    # --------------------------------------------------------
    # STAY OUT RECOMMENDATIONS
    # --------------------------------------------------------

    stay_out_drivers = [

        result

        for result in results

        if "STAY" in str(
            result["FinalDecision"]
        ).upper()

    ]


    if stay_out_drivers:

        print(
            "\nDrivers Recommended to STAY OUT:"
        )

        print(

            ", ".join(

                result["Driver"]

                for result in stay_out_drivers

            )

        )

    else:

        print(
            "\nDrivers Recommended to STAY OUT: None"
        )


    # --------------------------------------------------------
    # FINAL VALIDATION
    # --------------------------------------------------------

    print(
        "\n" + "=" * 90
    )

    print(
        "STEP 6.2 VALIDATION SUMMARY"
    )

    print(
        "=" * 90
    )


    successful_drivers = len(
        results
    )

    total_drivers = len(
        DRIVERS
    )


    print(
        f"Drivers Tested: {total_drivers}"
    )

    print(
        f"Successful Analyses: {successful_drivers}"
    )


    if successful_drivers == total_drivers:

        print(
            "\n✅ STEP 6.2 - MULTI-DRIVER STRATEGY "
            "COMPARISON PASSED"
        )

    else:

        print(
            "\n⚠️ STEP 6.2 - PARTIAL VALIDATION"
        )


    print(
        "=" * 90
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()