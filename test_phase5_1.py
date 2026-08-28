"""
F1 AI STRATEGIST
PHASE 5.1 — DYNAMIC STRATEGY SERVICE TEST
"""


from src.data_loader import (
    load_session
)

from src.strategy.dynamic_strategy_service import (
    run_dynamic_strategy_service,
    display_dynamic_strategy_service
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# PHASE 5.1 TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 76
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 5.1 — DYNAMIC STRATEGY SERVICE TEST"
    )

    print(
        "=" * 76
    )


    # ========================================================
    # 1. LOAD SESSION
    # ========================================================

    print(
        "\n[1/3] Loading race session..."
    )


    session = load_session(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        session_type="R"

    )


    assert session is not None, (
        "Race session failed to load."
    )


    print(
        "✅ Race session loaded."
    )


    # ========================================================
    # 2. RUN COMPLETE SERVICE
    # ========================================================

    print(
        "\n[2/3] Running unified dynamic strategy service..."
    )


    result = run_dynamic_strategy_service(

        session=session,

        driver=DRIVER,

        lap=TARGET_LAP

    )


    assert result, (
        "Phase 5.1 strategy service returned no result."
    )


    print(
        "✅ Complete Phase 4 pipeline executed through "
        "one Phase 5.1 service call."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_dynamic_strategy_service(
        result
    )


    # ========================================================
    # 3. VALIDATION
    # ========================================================

    print(
        "\n[3/3] Validating unified service response..."
    )


    # --------------------------------------------------------
    # SERVICE
    # --------------------------------------------------------

    assert (
        result.get("service")
        ==
        "dynamic_strategy_service"
    ), (
        "Incorrect service identifier."
    )


    assert (
        result.get("phase")
        ==
        "5.1"
    ), (
        "Incorrect Phase identifier."
    )


    assert (
        result.get("status")
        ==
        "SUCCESS"
    ), (
        "Strategy service did not report SUCCESS."
    )


    print(
        "✅ Service metadata validated."
    )


    # --------------------------------------------------------
    # DRIVER / LAP
    # --------------------------------------------------------

    assert (
        result.get("driver")
        ==
        DRIVER
    ), (
        "Driver mismatch."
    )


    assert (
        int(result.get("lap"))
        ==
        TARGET_LAP
    ), (
        "Dynamic lap mismatch."
    )


    print(
        "✅ Driver and dynamic lap validated."
    )


    # --------------------------------------------------------
    # PHASE 4.1
    # --------------------------------------------------------

    assert result.get(
        "race_state"
    ), (
        "Phase 4.1 race state missing."
    )


    print(
        "✅ Phase 4.1 output available."
    )


    # --------------------------------------------------------
    # PHASE 4.2
    # --------------------------------------------------------

    assert result.get(
        "race_situation_analysis"
    ), (
        "Phase 4.2 race situation missing."
    )


    print(
        "✅ Phase 4.2 output available."
    )


    # --------------------------------------------------------
    # PHASE 4.3
    # --------------------------------------------------------

    assert result.get(
        "tyre_strategy"
    ), (
        "Phase 4.3 tyre strategy missing."
    )


    print(
        "✅ Phase 4.3 output available."
    )


    # --------------------------------------------------------
    # PHASE 4.4
    # --------------------------------------------------------

    assert result.get(
        "pit_decision"
    ), (
        "Phase 4.4 pit decision missing."
    )


    print(
        "✅ Phase 4.4 output available."
    )


    # --------------------------------------------------------
    # PHASE 4.5
    # --------------------------------------------------------

    assert result.get(
        "strategy_simulation"
    ), (
        "Phase 4.5 simulation missing."
    )


    print(
        "✅ Phase 4.5 output available."
    )


    # --------------------------------------------------------
    # PHASE 4.6
    # --------------------------------------------------------

    assert result.get(
        "strategy_scoring"
    ), (
        "Phase 4.6 strategy scoring missing."
    )


    print(
        "✅ Phase 4.6 output available."
    )


    # --------------------------------------------------------
    # PHASE 4.7
    # --------------------------------------------------------

    assert result.get(
        "ai_recommendation"
    ), (
        "Phase 4.7 AI recommendation missing."
    )


    print(
        "✅ Phase 4.7 output available."
    )


    # --------------------------------------------------------
    # FINAL RECOMMENDATION
    # --------------------------------------------------------

    recommendation = result.get(
        "recommendation"
    )


    assert recommendation is not None, (
        "Final recommendation missing."
    )


    assert str(
        recommendation
    ).upper() in {

        "PIT",
        "PIT NOW",
        "STAY OUT",
        "STAY_OUT"

    }, (
        f"Unexpected recommendation: {recommendation}"
    )


    print(
        "✅ Final recommendation validated."
    )


    # --------------------------------------------------------
    # RECOMMENDED TYRE
    # --------------------------------------------------------

    assert result.get(
        "recommended_tyre"
    ) is not None, (
        "Recommended tyre missing."
    )


    print(
        "✅ Recommended tyre validated."
    )


    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = result.get(
        "confidence"
    )


    assert confidence is not None, (
        "Confidence missing."
    )


    confidence = float(
        confidence
    )


    assert (
        0 <= confidence <= 100
    ), (
        "Confidence must be between 0 and 100."
    )


    print(
        "✅ Confidence validated."
    )


    # --------------------------------------------------------
    # DYNAMIC SCORE
    # --------------------------------------------------------

    dynamic_score = result.get(
        "dynamic_score"
    )


    assert dynamic_score is not None, (
        "Dynamic strategy score missing."
    )


    dynamic_score = float(
        dynamic_score
    )


    assert (
        0 <= dynamic_score <= 100
    ), (
        "Dynamic strategy score must be between 0 and 100."
    )


    print(
        "✅ Dynamic strategy score validated."
    )


    # --------------------------------------------------------
    # REASONING
    # --------------------------------------------------------

    reasoning = result.get(
        "reasoning"
    )


    assert reasoning is not None, (
        "AI reasoning missing."
    )


    assert len(
        str(reasoning).strip()
    ) > 0, (
        "AI reasoning is empty."
    )


    print(
        "✅ AI reasoning validated."
    )


    # --------------------------------------------------------
    # EXPECTED BAHRAIN LAP-35 RESULT
    # --------------------------------------------------------

    assert (
        str(recommendation).upper()
        in {
            "STAY OUT",
            "STAY_OUT"
        }
    ), (
        "Expected Bahrain lap-35 recommendation "
        "to remain STAY OUT."
    )


    assert (
        str(
            result.get(
                "recommended_tyre"
            )
        ).upper()
        ==
        "HARD"
    ), (
        "Expected Bahrain lap-35 recommended tyre "
        "to remain HARD."
    )


    print(
        "✅ Bahrain lap-35 Phase 4 behaviour preserved."
    )


    # --------------------------------------------------------
    # COMPLETE PIPELINE
    # --------------------------------------------------------

    required_pipeline_outputs = [

        "race_state",

        "race_situation_analysis",

        "tyre_strategy",

        "pit_decision",

        "strategy_simulation",

        "strategy_scoring",

        "ai_recommendation"

    ]


    for output in required_pipeline_outputs:

        assert result.get(
            output
        ) is not None, (
            f"Pipeline output missing: {output}"
        )


    print(
        "✅ Complete Phase 4.1 → 4.7 pipeline validated."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 76
    )

    print(
        "✅ PHASE 5.1 DYNAMIC STRATEGY SERVICE TEST PASSED"
    )

    print(
        "=" * 76
    )


if __name__ == "__main__":

    main()