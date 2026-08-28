from src.data_loader import load_session

from src.strategy.dynamic_race_state import (
    build_dynamic_race_state
)

from src.strategy.dynamic_race_situation import (
    analyze_dynamic_race_situation
)

from src.strategy.dynamic_tyre_strategy import (
    generate_dynamic_tyre_strategy
)

from src.strategy.dynamic_pit_decision import (
    evaluate_dynamic_pit_decision
)

from src.strategy.dynamic_strategy_simulation import (
    run_dynamic_strategy_simulation
)

from src.strategy.dynamic_strategy_scoring import (
    run_dynamic_strategy_scoring
)

from src.strategy.dynamic_ai_recommendation import (
    generate_dynamic_ai_recommendation,
    display_dynamic_ai_recommendation
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# PHASE 4.7 TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 72
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 4.7 — DYNAMIC AI RECOMMENDATION TEST"
    )

    print(
        "=" * 72
    )


    # ========================================================
    # 1 — LOAD SESSION
    # ========================================================

    print(
        "\n[1/8] Loading race session..."
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


    # ========================================================
    # 2 — PHASE 4.1
    # ========================================================

    print(
        "\n[2/8] Building dynamic race state..."
    )


    race_state = build_dynamic_race_state(

        session=session,

        driver=DRIVER,

        selected_lap=TARGET_LAP

    )


    assert race_state


    print(
        "✅ Phase 4.1 race state generated."
    )


    # ========================================================
    # 3 — PHASE 4.2
    # ========================================================

    print(
        "\n[3/8] Analyzing dynamic race situation..."
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


    # ========================================================
    # 4 — PHASE 4.3
    # ========================================================

    print(
        "\n[4/8] Generating dynamic tyre strategy..."
    )


    tyre_strategy = (
        generate_dynamic_tyre_strategy(

            race_state=race_state,

            race_situation=race_situation

        )
    )


    assert tyre_strategy


    print(
        "✅ Phase 4.3 tyre strategy generated."
    )


    # ========================================================
    # 5 — PHASE 4.4
    # ========================================================

    print(
        "\n[5/8] Evaluating dynamic pit decision..."
    )


    pit_decision = (
        evaluate_dynamic_pit_decision(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy

        )
    )


    assert pit_decision


    print(
        "✅ Phase 4.4 pit decision generated."
    )


    # ========================================================
    # 6 — PHASE 4.5
    # ========================================================

    print(
        "\n[6/8] Running dynamic strategy simulation..."
    )


    simulation_result = (
        run_dynamic_strategy_simulation(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy,

            pit_decision=pit_decision

        )
    )


    assert simulation_result


    print(
        "✅ Phase 4.5 strategy simulation generated."
    )


    # ========================================================
    # 7 — PHASE 4.6
    # ========================================================

    print(
        "\n[7/8] Calculating dynamic strategy scores..."
    )


    scoring_result = (
        run_dynamic_strategy_scoring(

            simulation_result=simulation_result,

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy,

            pit_decision=pit_decision

        )
    )


    assert scoring_result


    print(
        "✅ Phase 4.6 dynamic scoring generated."
    )


    # ========================================================
    # 8 — PHASE 4.7
    # ========================================================

    print(
        "\n[8/8] Generating dynamic AI recommendation..."
    )


    recommendation = (
        generate_dynamic_ai_recommendation(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy,

            pit_decision=pit_decision,

            simulation_result=simulation_result,

            scoring_result=scoring_result

        )
    )


    assert recommendation


    print(
        "✅ Phase 4.7 AI recommendation generated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_dynamic_ai_recommendation(
        recommendation
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    print(
        "\nValidating dynamic AI recommendation..."
    )


    # --------------------------------------------------------
    # DYNAMIC MODE
    # --------------------------------------------------------

    assert (
        recommendation.get(
            "dynamic_recommendation"
        )
        is True
    ), (
        "Dynamic recommendation flag is missing."
    )


    print(
        "✅ Dynamic recommendation mode validated."
    )


    # --------------------------------------------------------
    # LAP CONTEXT
    # --------------------------------------------------------

    assert (
        recommendation.get(
            "current_lap"
        )
        ==
        TARGET_LAP
    ), (
        "Recommendation is using the wrong lap."
    )


    print(
        "✅ Dynamic lap context validated."
    )


    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    action = recommendation.get(
        "recommendation"
    )


    assert action is not None, (
        "AI recommendation is missing."
    )


    assert action in {

        "STAY OUT",

        "PIT NOW"

    }, (
        f"Unexpected recommendation: {action}"
    )


    print(
        "✅ Recommendation action validated."
    )


    # --------------------------------------------------------
    # TYRE
    # --------------------------------------------------------

    assert (
        recommendation.get(
            "recommended_tyre"
        )
        is not None
    ), (
        "Recommended tyre is missing."
    )


    print(
        "✅ Recommended tyre validated."
    )


    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = float(

        recommendation[
            "confidence"
        ]

    )


    assert (
        0
        <=
        confidence
        <=
        100
    ), (
        "Confidence must be between 0 and 100."
    )


    print(
        "✅ Confidence validated."
    )


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    dynamic_score = float(

        recommendation[
            "dynamic_score"
        ]

    )


    assert (
        0
        <=
        dynamic_score
        <=
        100
    ), (
        "Dynamic score must be between 0 and 100."
    )


    print(
        "✅ Dynamic strategy score validated."
    )


    # --------------------------------------------------------
    # STRATEGY RANK
    # --------------------------------------------------------

    assert (
        recommendation.get(
            "strategy_rank"
        )
        ==
        1
    ), (
        "Final recommendation is not based on "
        "the top-ranked dynamic strategy."
    )


    print(
        "✅ Best-ranked strategy selected."
    )


    # --------------------------------------------------------
    # REASONING
    # --------------------------------------------------------

    reason = recommendation.get(
        "reason"
    )


    assert (
        isinstance(
            reason,
            str
        )
        and
        len(
            reason.strip()
        )
        >
        20
    ), (
        "AI reasoning is missing or too short."
    )


    print(
        "✅ AI reasoning validated."
    )


    # --------------------------------------------------------
    # STRATEGY COMPARISON
    # --------------------------------------------------------

    comparison = recommendation.get(
        "strategy_comparison",
        []
    )


    assert (
        len(comparison)
        ==
        4
    ), (
        "Expected four strategy comparison records."
    )


    print(
        "✅ Strategy comparison validated."
    )


    # --------------------------------------------------------
    # BAHRAIN LAP-35 EXPECTED RESULT
    # --------------------------------------------------------

    assert (
        recommendation.get(
            "recommendation"
        )
        ==
        "STAY OUT"
    ), (
        "Expected STAY OUT for verified "
        "Bahrain lap-35 scenario."
    )


    assert (
        recommendation.get(
            "recommended_tyre"
        )
        ==
        "HARD"
    ), (
        "Expected HARD tyre for verified "
        "Bahrain lap-35 scenario."
    )


    print(
        "✅ Bahrain lap-35 expected recommendation validated."
    )


    # --------------------------------------------------------
    # COMPLETE PIPELINE CONNECTION
    # --------------------------------------------------------

    assert (
        scoring_result.get(
            "dynamic_scoring"
        )
        is True
    )


    assert (
        simulation_result.get(
            "dynamic_simulation"
        )
        is True
    )


    print(
        "✅ Phase 4.1 → 4.7 pipeline validated."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 72
    )

    print(
        "✅ PHASE 4.7 DYNAMIC AI RECOMMENDATION TEST PASSED"
    )

    print(
        "=" * 72
    )


if __name__ == "__main__":

    main()