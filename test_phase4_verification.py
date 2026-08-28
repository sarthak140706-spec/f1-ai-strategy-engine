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
    generate_dynamic_ai_recommendation
)


# ============================================================
# PHASE 4 VERIFICATION CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# MAIN VERIFICATION
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 4.8 — COMPLETE DYNAMIC STRATEGY VERIFICATION"
    )

    print(
        "=" * 78
    )


    results = {}


    # ========================================================
    # PHASE 4.1
    # ========================================================

    print(
        "\n[4.1] Testing Dynamic Race State..."
    )


    session = load_session(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        session_type="R"

    )


    assert session is not None, (
        "Phase 4.1 failed: session not loaded."
    )


    race_state = build_dynamic_race_state(

        session=session,

        driver=DRIVER,

        selected_lap=TARGET_LAP

    )


    assert race_state, (
        "Phase 4.1 failed: race state missing."
    )


    assert (
        race_state.get("CurrentLap")
        ==
        TARGET_LAP
    ), (
        "Phase 4.1 failed: wrong dynamic lap."
    )


    assert (
        race_state.get("LapsRemaining")
        is not None
    )


    assert (
        race_state.get("TyreCompound")
        is not None
    )


    assert (
        race_state.get("RecentPace")
        is not None
    )


    results["4.1"] = True


    print(
        "✅ 4.1 PASSED — Dynamic race state reconstructed."
    )


    # ========================================================
    # PHASE 4.2
    # ========================================================

    print(
        "\n[4.2] Testing Dynamic Race Situation..."
    )


    race_situation = (
        analyze_dynamic_race_situation(
            race_state
        )
    )


    assert race_situation, (
        "Phase 4.2 failed: race situation missing."
    )


    assert (
        race_situation.get(
            "race_situation"
        )
        is not None
    )


    assert (
        race_situation.get(
            "pit_urgency"
        )
        is not None
    )


    assert (
        race_situation.get(
            "tyre_status"
        )
        is not None
    )


    results["4.2"] = True


    print(
        "✅ 4.2 PASSED — Dynamic race situation analyzed."
    )


    # ========================================================
    # PHASE 4.3
    # ========================================================

    print(
        "\n[4.3] Testing Dynamic Tyre Strategy..."
    )


    tyre_strategy = (
        generate_dynamic_tyre_strategy(

            race_state=race_state,

            race_situation=race_situation

        )
    )


    assert tyre_strategy, (
        "Phase 4.3 failed: tyre strategy missing."
    )


    # --------------------------------------------------------
    # SUPPORT ACTUAL PHASE 4.3 RESPONSE FIELD NAMES
    # --------------------------------------------------------

    tyre_recommendation = (

        tyre_strategy.get(
            "recommendation"
        )

        or

        tyre_strategy.get(
            "Recommendation"
        )

        or

        tyre_strategy.get(
            "action"
        )

    )


    recommended_compound = (

        tyre_strategy.get(
            "recommended_compound"
        )

        or

        tyre_strategy.get(
            "recommended_tyre"
        )

        or

        tyre_strategy.get(
            "compound"
        )

        or

        tyre_strategy.get(
            "Compound"
        )

    )


    strategies = (

        tyre_strategy.get(
            "strategies"
        )

        or

        tyre_strategy.get(
            "Strategies"
        )

        or

        tyre_strategy.get(
            "strategy_comparison"
        )

        or

        []

    )


    assert tyre_recommendation is not None, (
        "Phase 4.3 failed: tyre recommendation missing."
    )


    assert recommended_compound is not None, (
        "Phase 4.3 failed: recommended compound missing."
    )


    assert (
        len(strategies)
        ==
        4
    ), (
        f"Phase 4.3 failed: expected 4 tyre strategies, "
        f"received {len(strategies)}."
    )


    results["4.3"] = True


    print(
        "✅ 4.3 PASSED — Dynamic tyre strategy verified."
    )


    print(
        f"   Recommendation: "
        f"{tyre_recommendation}"
    )


    print(
        f"   Recommended Compound: "
        f"{recommended_compound}"
    )


    print(
        f"   Strategies Evaluated: "
        f"{len(strategies)}"
    )


    # ========================================================
    # PHASE 4.4
    # ========================================================

    print(
        "\n[4.4] Testing Dynamic Pit Decision..."
    )


    pit_decision = (
        evaluate_dynamic_pit_decision(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy

        )
    )


    assert pit_decision, (
        "Phase 4.4 failed: pit decision missing."
    )


    pit_action = (

        pit_decision.get(
            "decision"
        )

        or

        pit_decision.get(
            "action"
        )

    )


    assert pit_action is not None


    assert str(
        pit_action
    ).upper() in {

        "PIT",

        "PIT NOW",

        "STAY OUT",

        "STAY_OUT"

    }


    assert (
        pit_decision.get(
            "confidence"
        )
        is not None
    )


    results["4.4"] = True


    print(
        f"✅ 4.4 PASSED — Pit decision: {pit_action}"
    )


    # ========================================================
    # PHASE 4.5
    # ========================================================

    print(
        "\n[4.5] Testing Dynamic Strategy Simulation..."
    )


    simulation_result = (
        run_dynamic_strategy_simulation(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy,

            pit_decision=pit_decision

        )
    )


    assert simulation_result, (
        "Phase 4.5 failed: simulation missing."
    )


    simulation_strategies = (
        simulation_result.get(
            "strategies",
            []
        )
    )


    assert (
        len(simulation_strategies)
        ==
        4
    ), (
        "Phase 4.5 failed: expected four simulations."
    )


    assert (
        simulation_result.get(
            "best_strategy"
        )
        is not None
    )


    assert (
        simulation_result.get(
            "dynamic_simulation"
        )
        is True
    )


    for strategy in simulation_strategies:

        assert (
            strategy.get(
                "strategy_rank"
            )
            is not None
        )

        assert (
            strategy.get(
                "projected_total_time"
            )
            is not None
        )

        assert (
            strategy.get(
                "time_difference"
            )
            is not None
        )


    results["4.5"] = True


    print(
        "✅ 4.5 PASSED — Four dynamic strategies simulated."
    )


    # ========================================================
    # PHASE 4.6
    # ========================================================

    print(
        "\n[4.6] Testing Dynamic Strategy Scoring..."
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


    assert scoring_result, (
        "Phase 4.6 failed: scoring missing."
    )


    scored_strategies = (
        scoring_result.get(
            "strategies",
            []
        )
    )


    assert (
        len(scored_strategies)
        ==
        4
    )


    assert (
        scoring_result.get(
            "dynamic_scoring"
        )
        is True
    )


    best_scored_strategy = (
        scoring_result.get(
            "best_strategy"
        )
    )


    assert (
        best_scored_strategy
        is not None
    )


    assert (
        best_scored_strategy.get(
            "dynamic_score_rank"
        )
        ==
        1
    )


    for strategy in scored_strategies:

        score = float(

            strategy[
                "dynamic_overall_score"
            ]

        )


        assert (
            0
            <=
            score
            <=
            100
        )


    results["4.6"] = True


    print(
        "✅ 4.6 PASSED — Dynamic strategies scored and ranked."
    )


    # ========================================================
    # PHASE 4.7
    # ========================================================

    print(
        "\n[4.7] Testing Dynamic AI Recommendation..."
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


    assert recommendation, (
        "Phase 4.7 failed: recommendation missing."
    )


    assert (
        recommendation.get(
            "dynamic_recommendation"
        )
        is True
    )


    assert (
        recommendation.get(
            "recommendation"
        )
        is not None
    )


    assert (
        recommendation.get(
            "recommended_tyre"
        )
        is not None
    )


    assert (
        recommendation.get(
            "strategy_rank"
        )
        ==
        1
    )


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
    )


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
    )


    results["4.7"] = True


    print(
        "✅ 4.7 PASSED — Final dynamic AI recommendation generated."
    )


    # ========================================================
    # CROSS-PHASE CONSISTENCY
    # ========================================================

    print(
        "\n[4.8] Testing Full Pipeline Consistency..."
    )


    # Same lap must travel through complete pipeline

    assert (
        recommendation.get(
            "current_lap"
        )
        ==
        race_state.get(
            "CurrentLap"
        )
        ==
        TARGET_LAP
    )


    # Final selected strategy must be scoring winner

    selected_strategy = (
        recommendation.get(
            "selected_strategy"
        )
    )


    assert selected_strategy is not None


    assert (
        selected_strategy.get(
            "dynamic_score_rank"
        )
        ==
        1
    )


    assert (
        selected_strategy.get(
            "dynamic_overall_score"
        )
        ==
        best_scored_strategy.get(
            "dynamic_overall_score"
        )
    )


    # Strategy list consistency

    recommendation_comparison = (
        recommendation.get(
            "strategy_comparison",
            []
        )
    )


    assert (
        len(
            recommendation_comparison
        )
        ==
        len(
            scored_strategies
        )
        ==
        4
    )


    # Bahrain lap 35 frozen expected context

    assert (
        race_state.get(
            "Position"
        )
        ==
        1
    )


    assert (
        race_state.get(
            "TyreCompound"
        )
        ==
        "HARD"
    )


    assert (
        race_state.get(
            "LapsRemaining"
        )
        ==
        22
    )


    assert (
        recommendation.get(
            "recommendation"
        )
        ==
        "STAY OUT"
    )


    assert (
        recommendation.get(
            "recommended_tyre"
        )
        ==
        "HARD"
    )


    results["4.8"] = True


    print(
        "✅ 4.8 PASSED — Complete Phase 4 pipeline is consistent."
    )


    # ========================================================
    # FINAL RESULTS
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "PHASE 4 VERIFICATION RESULTS"
    )

    print(
        "=" * 78
    )


    print(
        "4.1 Dynamic Race State          ✅"
    )

    print(
        "4.2 Dynamic Race Situation      ✅"
    )

    print(
        "4.3 Dynamic Tyre Strategy       ✅"
    )

    print(
        "4.4 Dynamic Pit Decision        ✅"
    )

    print(
        "4.5 Dynamic Simulation          ✅"
    )

    print(
        "4.6 Dynamic Strategy Scoring    ✅"
    )

    print(
        "4.7 Dynamic AI Recommendation   ✅"
    )

    print(
        "4.8 Pipeline Verification       ✅"
    )


    # ========================================================
    # FINAL PHASE STATUS
    # ========================================================

    assert all(
        results.values()
    )


    print(
        "\n🏁 PHASE 4.8 VERIFICATION PASSED"
    )


    print(
        "\n✅ PHASE 4 — 100% COMPLETE"
    )


    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()