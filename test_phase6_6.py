"""
F1 AI STRATEGIST
PHASE 6.6 — LIVE FRONTEND INTEGRATION TEST

Purpose
-------
Verify that the actual Live Strategy frontend is correctly
connected to the Phase 6.5 Flask Live API.

This test validates the real Phase 6.6 frontend architecture
instead of requiring duplicate or unused HTML elements.
"""


from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parent


FRONTEND_DIR = (
    PROJECT_ROOT
    /
    "frontend"
)


LIVE_HTML = (
    FRONTEND_DIR
    /
    "live.html"
)


# ============================================================
# HELPER
# ============================================================

def read_file(
    path: Path
) -> str:
    """
    Read text file safely.
    """

    if not path.exists():

        raise AssertionError(
            f"Required file does not exist: {path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 6.6 — LIVE FRONTEND INTEGRATION TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # STEP 1
    # VALIDATE FRONTEND FILE
    # ========================================================

    print(
        "\n[1/7] Validating frontend file..."
    )


    assert LIVE_HTML.exists(), (
        "frontend/live.html does not exist."
    )


    html = read_file(
        LIVE_HTML
    )


    assert html.strip(), (
        "frontend/live.html is empty."
    )


    print(
        "✅ Phase 6.6 live.html found."
    )


    # ========================================================
    # STEP 2
    # VALIDATE PHASE 6.5 API CONNECTION
    # ========================================================

    print(
        "\n[2/7] Validating Phase 6.5 API connection..."
    )


    assert (
        "/api/live"
        in html
    ), (
        "Phase 6.5 /api/live endpoint "
        "is not configured in live.html."
    )


    assert (
        "/strategy/"
        in html
    ), (
        "Phase 6.5 live strategy endpoint "
        "is missing."
    )


    assert (
        "/status"
        in html
    ), (
        "Phase 6.5 live status endpoint "
        "is missing."
    )


    assert (
        "fetch("
        in html
        or
        "fetch ("
        in html
    ), (
        "Frontend does not contain a fetch request "
        "for the live API."
    )


    print(
        "✅ Phase 6.5 live API connection configured."
    )


    # ========================================================
    # STEP 3
    # VALIDATE AUTOMATIC LIVE REFRESH
    # ========================================================

    print(
        "\n[3/7] Validating automatic live refresh..."
    )


    assert (
        "REFRESH_INTERVAL"
        in html
        or
        "LIVE_REFRESH_INTERVAL"
        in html
    ), (
        "Live refresh interval is missing."
    )


    assert (
        "setInterval"
        in html
    ), (
        "Automatic live refresh timer is missing."
    )


    assert (
        "loadLiveStrategy"
        in html
    ), (
        "loadLiveStrategy() is missing."
    )


    assert (
        "loadLiveStatus"
        in html
    ), (
        "loadLiveStatus() is missing."
    )


    print(
        "✅ Automatic live refresh configured."
    )


    # ========================================================
    # STEP 4
    # VALIDATE REAL LIVE RACE-STATE UI
    # ========================================================

    print(
        "\n[4/7] Validating live race-state UI..."
    )


    required_ids = [

        # ----------------------------------------------------
        # DRIVER
        # ----------------------------------------------------

        "raceDriver",

        "driver",


        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        "kpiLap",

        "kpiLapsRemaining",

        "kpiPosition",

        "kpiTyre",

        "kpiTyreLife",

        "kpiPace",

        "kpiPit",

        "kpiConfidence",

    ]


    for element_id in required_ids:

        assert (
            f'id="{element_id}"'
            in html
        ), (
            "Missing live dashboard element: "
            f"{element_id}"
        )


    print(
        "✅ Live race-state dashboard contract validated."
    )


    # ========================================================
    # STEP 5
    # VALIDATE AI STRATEGY UI
    # ========================================================

    print(
        "\n[5/7] Validating AI strategy UI..."
    )


    strategy_ids = [

        # ----------------------------------------------------
        # MAIN AI RECOMMENDATION
        # ----------------------------------------------------

        "recommendation",

        "recommendationConfidence",

        "recommendedTyre",

        "strategyType",

        "overallScore",

        "expectedBenefit",

        "recommendationReason",


        # ----------------------------------------------------
        # PIT DECISION
        # ----------------------------------------------------

        "pitDecision",

        "pitTyre",

        "pitLoss",

        "paceGain",

        "strategicBenefit",

        "trafficPenalty",

        "pitConfidence",


        # ----------------------------------------------------
        # TYRE STRATEGY
        # ----------------------------------------------------

        "tyreRecommendation",

        "tyreCompound",

        "tyreStrategyType",

        "tyreProjectedTime",

        "tyreAverageLap",

        "tyreDegradation",

        "tyreQuality",

        "tyreBenefit",

    ]


    for element_id in strategy_ids:

        assert (
            f'id="{element_id}"'
            in html
        ), (
            "Missing AI strategy dashboard element: "
            f"{element_id}"
        )


    print(
        "✅ Live AI strategy dashboard contract validated."
    )


    # ========================================================
    # STEP 6
    # VALIDATE CONTROLS AND STRATEGY OUTPUTS
    # ========================================================

    print(
        "\n[6/7] Validating live frontend controls and outputs..."
    )


    required_controls = [

        "refreshButton",

        "autoRefreshButton",

        "statusDot",

        "statusText",

        "lastUpdated",

    ]


    for element_id in required_controls:

        assert (
            f'id="{element_id}"'
            in html
        ), (
            "Missing live frontend control: "
            f"{element_id}"
        )


    required_outputs = [

        "simulationTable",

        "scoringTable",

        "comparisonGrid",

    ]


    for element_id in required_outputs:

        assert (
            f'id="{element_id}"'
            in html
        ), (
            "Missing strategy output element: "
            f"{element_id}"
        )


    print(
        "✅ Live frontend controls and strategy outputs validated."
    )


    # ========================================================
    # STEP 7
    # VALIDATE COMPLETE PHASE 6.6 INTEGRATION
    # ========================================================

    print(
        "\n[7/7] Validating Phase 6.6 integration..."
    )


    required_functions = [

        "loadLiveStatus",

        "loadLiveStrategy",

        "normalizeLiveResponse",

        "renderLiveDashboard",

        "renderSimulation",

        "renderScoring",

        "renderComparison",

    ]


    for function_name in required_functions:

        assert (
            function_name
            in html
        ), (
            "Missing Phase 6.6 frontend function: "
            f"{function_name}"
        )


    # ========================================================
    # OLD HISTORICAL ENDPOINT MUST BE REMOVED
    # ========================================================

    assert (
        "/api/dynamic-strategy/"
        not in html
    ), (
        "Old historical dynamic strategy API "
        "is still present in live.html."
    )


    # ========================================================
    # OLD HISTORICAL INPUTS MUST BE REMOVED
    # ========================================================

    forbidden_inputs = [

        'id="season"',

        'id="grandPrix"',

        'id="targetLap"',

        'id="session"',

    ]


    for forbidden in forbidden_inputs:

        assert (
            forbidden
            not in html
        ), (
            "Historical input still exists in "
            f"live.html: {forbidden}"
        )


    # ========================================================
    # VERIFY LIVE DRIVER REQUEST
    # ========================================================

    assert (
        "encodeURIComponent(driver)"
        in html
        or
        "encodeURIComponent("
        in html
    ), (
        "Live driver is not being safely passed "
        "to the strategy endpoint."
    )


    # ========================================================
    # VERIFY 5 SECOND REFRESH
    # ========================================================

    assert (
        "5000"
        in html
    ), (
        "Expected 5-second live refresh interval "
        "was not found."
    )


    print(
        "✅ Phase 6.5 → Phase 6.6 frontend integration validated."
    )


    # ========================================================
    # PIPELINE SUMMARY
    # ========================================================

    print(
        "\n" + "-" * 78
    )

    print(
        "LIVE FRONTEND PIPELINE"
    )

    print(
        "-" * 78
    )


    print(
        "6.1 Live Timing Client"
    )

    print(
        "        ↓"
    )

    print(
        "6.2 Live Data Parser"
    )

    print(
        "        ↓"
    )

    print(
        "6.3 Live Race-State Adapter"
    )

    print(
        "        ↓"
    )

    print(
        "6.4 Live Strategy Service"
    )

    print(
        "        ↓"
    )

    print(
        "6.5 Flask Live API"
    )

    print(
        "        ↓"
    )

    print(
        "6.6 Live Frontend Dashboard"
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "✅ PHASE 6.6 LIVE FRONTEND INTEGRATION TEST PASSED"
    )

    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()