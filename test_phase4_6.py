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
    run_dynamic_strategy_scoring,
    display_dynamic_strategy_scoring
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# PHASE 4.6 TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 72
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 4.6 — DYNAMIC STRATEGY SCORING TEST"
    )

    print(
        "=" * 72
    )


    # ========================================================
    # STEP 1
    # LOAD SESSION
    # ========================================================

    print(
        "\n[1/7] Loading race session..."
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
    # STEP 2
    # PHASE 4.1
    # ========================================================

    print(
        "\n[2/7] Building dynamic race state..."
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
    # STEP 3
    # PHASE 4.2
    # ========================================================

    print(
        "\n[3/7] Analyzing dynamic race situation..."
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
    # STEP 4
    # PHASE 4.3
    # ========================================================

    print(
        "\n[4/7] Generating dynamic tyre strategy..."
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
    # STEP 5
    # PHASE 4.4
    # ========================================================

    print(
        "\n[5/7] Evaluating dynamic pit decision..."
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
    # STEP 6
    # PHASE 4.5
    # ========================================================

    print(
        "\n[6/7] Running dynamic strategy simulation..."
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
    # STEP 7
    # PHASE 4.6
    # ========================================================

    print(
        "\n[7/7] Calculating dynamic strategy scores..."
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
    # DISPLAY RESULT
    # ========================================================

    display_dynamic_strategy_scoring(
        scoring_result
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    print(
        "\nValidating dynamic strategy scoring..."
    )


    strategies = scoring_result.get(
        "strategies",
        []
    )


    # --------------------------------------------------------
    # FOUR STRATEGIES
    # --------------------------------------------------------

    assert (
        len(strategies)
        ==
        4
    ), (
        "Expected exactly four scored strategies."
    )


    print(
        "✅ Four strategies scored."
    )


    # --------------------------------------------------------
    # DYNAMIC FLAG
    # --------------------------------------------------------

    assert (
        scoring_result.get(
            "dynamic_scoring"
        )
        is True
    ), (
        "Dynamic scoring flag missing."
    )


    print(
        "✅ Dynamic scoring mode validated."
    )


    # --------------------------------------------------------
    # CURRENT LAP
    # --------------------------------------------------------

    assert (
        scoring_result.get(
            "current_lap"
        )
        ==
        TARGET_LAP
    ), (
        "Dynamic scoring is using the wrong race lap."
    )


    print(
        "✅ Dynamic lap context validated."
    )


    # --------------------------------------------------------
    # REQUIRED SCORES
    # --------------------------------------------------------

    required_scores = [

        "pace_score",

        "tyre_score",

        "pit_score",

        "traffic_score",

        "position_score",

        "degradation_score",

        "risk_score",

        "overall_score",

        "decision_alignment_score",

        "tyre_alignment_score",

        "race_situation_score",

        "dynamic_context_score",

        "dynamic_overall_score",

        "dynamic_score_rank"

    ]


    for strategy in strategies:

        for field in required_scores:

            assert (
                field in strategy
            ), (
                f"Missing score field: {field}"
            )


    print(
        "✅ All score components validated."
    )


    # --------------------------------------------------------
    # SCORE RANGE
    # --------------------------------------------------------

    for strategy in strategies:

        dynamic_score = float(

            strategy[
                "dynamic_overall_score"
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
        "✅ Dynamic score range validated."
    )


    # --------------------------------------------------------
    # RANKING
    # --------------------------------------------------------

    assert (
        strategies[0][
            "dynamic_score_rank"
        ]
        ==
        1
    ), (
        "Highest dynamic strategy is not ranked first."
    )


    scores = [

        strategy[
            "dynamic_overall_score"
        ]

        for strategy in strategies

    ]


    assert (
        scores
        ==
        sorted(
            scores,
            reverse=True
        )
    ), (
        "Dynamic strategies are not ranked correctly."
    )


    print(
        "✅ Dynamic ranking validated."
    )


    # --------------------------------------------------------
    # BEST STRATEGY
    # --------------------------------------------------------

    best = scoring_result.get(
        "best_strategy"
    )


    assert best is not None, (
        "Best dynamic strategy is missing."
    )


    assert (
        best.get(
            "dynamic_score_rank"
        )
        ==
        1
    ), (
        "Best dynamic strategy must have rank 1."
    )


    print(
        "✅ Best strategy validated."
    )


    # --------------------------------------------------------
    # EXPECT CURRENT BAHRAIN RESULT
    # --------------------------------------------------------

    assert (
        best.get(
            "strategy"
        )
        ==
        "STAY_OUT"
    ), (
        "Expected STAY_OUT to remain the best strategy "
        "for the verified Bahrain lap-35 scenario."
    )


    assert (
        best.get(
            "final_tyre"
        )
        ==
        "HARD"
    ), (
        "Expected HARD to remain the selected tyre."
    )


    print(
        "✅ Phase 4.4 decision agrees with Phase 4.6 result."
    )


    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    assert (
        simulation_result.get(
            "dynamic_simulation"
        )
        is True
    )


    print(
        "✅ Phase 4.1 → 4.6 pipeline validated."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 72
    )

    print(
        "✅ PHASE 4.6 DYNAMIC STRATEGY SCORING TEST PASSED"
    )

    print(
        "=" * 72
    )


if __name__ == "__main__":

    main()