"""
F1 AI STRATEGIST
PHASE 7.2 — AI STRATEGY ENGINEER SERVICE TEST
"""


from src.strategy_engineer.strategy_engineer_service import (
    prepare_phase4_manual_race_state,
    run_strategy_engineer_service,
    display_strategy_engineer_service,
)

from src.strategy_engineer.race_state_builder import (
    build_manual_race_state
)


# ============================================================
# TEST INPUT
# ============================================================

TEST_INPUT = {

    "driver":
        "LEC",

    "team":
        "Ferrari",

    "grand_prix":
        "Italian Grand Prix",

    "circuit":
        "Monza",

    "current_lap":
        32,

    "total_laps":
        53,

    "position":
        4,

    "current_tyre":
        "MEDIUM",

    "tyre_age":
        19,

    "gap_ahead":
        2.4,

    "gap_behind":
        1.8,

    "recent_pace":
        84.512,

    "average_pace":
        84.740,

    "degradation_rate":
        0.084,

    "weather":
        "DRY",

    "rainfall":
        0,

    "track_status":
        "GREEN",

    "safety_car":
        False,

    "virtual_safety_car":
        False,

    "pit_stops_completed":
        1,

}


# ============================================================
# FALLBACK INPUT
# ============================================================

FALLBACK_TEST_INPUT = dict(
    TEST_INPUT
)

FALLBACK_TEST_INPUT[
    "average_pace"
] = None


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.2 — AI STRATEGY ENGINEER SERVICE TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # 1
    # ========================================================

    print(
        "\n[1/8] Building Phase 7.1 manual race state..."
    )


    manual_state = (
        build_manual_race_state(
            TEST_INPUT
        )
    )


    assert manual_state

    assert manual_state[
        "Phase"
    ] == "7.1"


    print(
        "✅ Phase 7.1 manual race state generated."
    )


    # ========================================================
    # 2
    # ========================================================

    print(
        "\n[2/8] Preparing Phase 4 compatibility contract..."
    )


    prepared_state = (
        prepare_phase4_manual_race_state(
            manual_state
        )
    )


    assert prepared_state[
        "Phase4Compatible"
    ] is True


    assert prepared_state[
        "ManualData"
    ] is True


    assert prepared_state[
        "RecentPace"
    ] == 84.512


    assert prepared_state[
        "AveragePace"
    ] == 84.740


    assert prepared_state[
        "DegradationRate"
    ] == 0.084


    print(
        "✅ Phase 4 manual compatibility contract prepared."
    )


    # ========================================================
    # 3
    # ========================================================

    print(
        "\n[3/8] Testing AveragePace compatibility fallback..."
    )


    fallback_manual_state = (
        build_manual_race_state(
            FALLBACK_TEST_INPUT
        )
    )


    fallback_state = (
        prepare_phase4_manual_race_state(
            fallback_manual_state
        )
    )


    assert fallback_state[
        "AveragePace"
    ] == fallback_state[
        "RecentPace"
    ]


    assert fallback_state[
        "AveragePaceFallbackUsed"
    ] is True


    print(
        "✅ AveragePace fallback validated."
    )


    # ========================================================
    # 4
    # ========================================================

    print(
        "\n[4/8] Running complete AI Strategy Engineer service..."
    )


    result = (
        run_strategy_engineer_service(
            TEST_INPUT
        )
    )


    assert isinstance(
        result,
        dict
    )

    assert result


    print(
        "✅ AI Strategy Engineer service executed."
    )


    # ========================================================
    # 5
    # ========================================================

    print(
        "\n[5/8] Validating Phase 7.2 service contract..."
    )


    assert result[
        "service"
    ] == "strategy_engineer_service"


    assert result[
        "phase"
    ] == "7.2"


    assert result[
        "status"
    ] == "SUCCESS"


    assert result[
        "source"
    ] == "MANUAL"


    assert result[
        "manual"
    ] is True


    assert result[
        "phase4_compatible"
    ] is True


    print(
        "✅ Phase 7.2 service contract validated."
    )


    # ========================================================
    # 6
    # ========================================================

    print(
        "\n[6/8] Validating race and strategy context..."
    )


    assert result[
        "driver"
    ] == "LEC"


    assert result[
        "circuit"
    ] == "Monza"


    assert result[
        "current_lap"
    ] == 32


    assert result[
        "total_laps"
    ] == 53


    assert result[
        "laps_remaining"
    ] == 21


    assert result[
        "position"
    ] == 4


    assert result[
        "current_tyre"
    ] == "MEDIUM"


    assert result[
        "tyre_age"
    ] == 19.0


    print(
        "✅ Manual race context reached strategy engine."
    )


    # ========================================================
    # 7
    # ========================================================

    print(
        "\n[7/8] Validating AI strategy output..."
    )


    assert result.get(
        "race_situation"
    ) is not None


    assert result.get(
        "pit_decision"
    ) is not None


    assert result.get(
        "recommendation"
    ) is not None


    assert result.get(
        "recommended_tyre"
    ) is not None


    assert result.get(
        "dynamic_score"
    ) is not None


    assert result.get(
        "confidence"
    ) is not None


    assert result.get(
        "reasoning"
    )


    print(
        "✅ AI strategy recommendation validated."
    )


    # ========================================================
    # 8
    # ========================================================

    print(
        "\n[8/8] Validating complete strategy pipeline..."
    )


    pipeline = result[
        "pipeline"
    ]


    assert pipeline[
        "phase_7_1"
    ]


    assert pipeline[
        "phase_7_2_state"
    ]


    assert pipeline[
        "phase_4_2"
    ]


    assert pipeline[
        "phase_4_3"
    ]


    assert pipeline[
        "phase_4_4"
    ]


    assert pipeline[
        "phase_4_5"
    ]


    assert pipeline[
        "phase_4_6"
    ]


    assert pipeline[
        "phase_4_7"
    ]


    print(
        "✅ Complete 7.1 → 7.2 → 4.2–4.7 pipeline validated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_strategy_engineer_service(
        result
    )


    # ========================================================
    # FINAL
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "PHASE 7.2 VERIFICATION RESULTS"
    )

    print(
        "=" * 78
    )


    print(
        "7.1 Manual Race State            ✅"
    )


    print(
        "7.2 Compatibility Layer           ✅"
    )


    print(
        "4.2 Race Situation               ✅"
    )


    print(
        "4.3 Tyre Strategy                ✅"
    )


    print(
        "4.4 Pit Decision                 ✅"
    )


    print(
        "4.5 Strategy Simulation          ✅"
    )


    print(
        "4.6 Strategy Scoring             ✅"
    )


    print(
        "4.7 AI Recommendation            ✅"
    )


    print(
        "\n🏁 PHASE 7.2 VERIFICATION PASSED"
    )


    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()