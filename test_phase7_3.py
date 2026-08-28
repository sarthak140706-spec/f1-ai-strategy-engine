"""
F1 AI STRATEGIST
PHASE 7.3 — STRATEGY ALTERNATIVES ENGINE TEST
"""


from src.strategy_engineer.strategy_alternatives_engine import (
    run_strategy_alternatives_engine,
    display_strategy_alternatives,
    build_strategy_display_name,
)


# ============================================================
# TEST RACE INPUT
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
# MAIN
# ============================================================

def main():

    print(
        "\n" + "=" * 86
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.3 — STRATEGY ALTERNATIVES ENGINE TEST"
    )

    print(
        "=" * 86
    )


    # ========================================================
    # 1
    # ========================================================

    print(
        "\n[1/7] Running Phase 7.3 alternatives engine..."
    )


    result = (
        run_strategy_alternatives_engine(
            TEST_INPUT
        )
    )


    assert isinstance(
        result,
        dict
    )


    assert result


    print(
        "✅ Strategy alternatives engine executed."
    )


    # ========================================================
    # 2
    # ========================================================

    print(
        "\n[2/7] Validating Phase 7.3 contract..."
    )


    assert result[
        "engine"
    ] == "strategy_alternatives_engine"


    assert result[
        "phase"
    ] == "7.3"


    assert result[
        "status"
    ] == "SUCCESS"


    assert result[
        "driver"
    ] == "LEC"


    assert result[
        "circuit"
    ] == "Monza"


    assert result[
        "current_lap"
    ] == 32


    print(
        "✅ Phase 7.3 contract validated."
    )


    # ========================================================
    # 3
    # ========================================================

    print(
        "\n[3/7] Validating available strategy alternatives..."
    )


    alternatives = result[
        "alternatives"
    ]


    assert isinstance(
        alternatives,
        list
    )


    assert len(
        alternatives
    ) >= 2


    assert result[
        "strategy_count"
    ] == len(
        alternatives
    )


    for alternative in alternatives:

        assert alternative.get(
            "display_name"
        )


        assert alternative.get(
            "strategy"
        )


        assert alternative.get(
            "comparison_rank"
        ) is not None


        assert alternative.get(
            "dynamic_score"
        ) is not None


    print(
        f"✅ {len(alternatives)} strategy alternatives validated."
    )


    # ========================================================
    # 4
    # ========================================================

    print(
        "\n[4/7] Validating strategy ranking..."
    )


    scores = [

        alternative[
            "dynamic_score"
        ]

        for alternative
        in alternatives

    ]


    assert scores == sorted(
        scores,
        reverse=True
    )


    ranks = [

        alternative[
            "comparison_rank"
        ]

        for alternative
        in alternatives

    ]


    assert ranks == list(

        range(
            1,
            len(alternatives) + 1
        )

    )


    print(
        "✅ Strategies ranked correctly by dynamic score."
    )


    # ========================================================
    # 5
    # ========================================================

    print(
        "\n[5/7] Validating best strategy comparison..."
    )


    best = result[
        "best_strategy"
    ]


    second = result[
        "second_best_strategy"
    ]


    assert best


    assert best[
        "comparison_rank"
    ] == 1


    assert second


    assert second[
        "comparison_rank"
    ] == 2


    assert (
        best[
            "dynamic_score"
        ]
        >=
        second[
            "dynamic_score"
        ]
    )


    assert result[
        "score_advantage"
    ] is not None


    print(
        "✅ Best and second-best strategies validated."
    )


    # ========================================================
    # 6
    # ========================================================

    print(
        "\n[6/7] Validating AI recommendation alignment..."
    )


    alignment = result[
        "ai_alignment"
    ]


    assert isinstance(
        alignment,
        dict
    )


    assert (
        "aligned"
        in
        alignment
    )


    assert alignment.get(
        "ai_recommendation"
    )


    assert alignment.get(
        "best_strategy"
    )


    print(
        "✅ AI recommendation alignment evaluated."
    )


    # ========================================================
    # 7
    # ========================================================

    print(
        "\n[7/7] Validating display-name normalization..."
    )


    assert (
        build_strategy_display_name(

            strategy=
                "STAY_OUT",

            final_tyre=
                "MEDIUM",

            tyre_plan=
                "MEDIUM"

        )
        ==
        "STAY OUT"
    )


    assert (
        build_strategy_display_name(

            strategy=
                "PIT",

            final_tyre=
                "HARD",

            tyre_plan=
                "PIT -> HARD"

        )
        ==
        "PIT → HARD"
    )


    assert (
        build_strategy_display_name(

            strategy=
                "PIT",

            final_tyre=
                "SOFT",

            tyre_plan=
                "PIT -> SOFT"

        )
        ==
        "PIT → SOFT"
    )


    print(
        "✅ Strategy names normalized."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_strategy_alternatives(
        result
    )


    # ========================================================
    # FINAL
    # ========================================================

    print(
        "\n" + "=" * 86
    )

    print(
        "PHASE 7.3 VERIFICATION RESULTS"
    )

    print(
        "=" * 86
    )


    print(
        "7.2 Strategy Engineer Service      ✅"
    )


    print(
        "Strategy Extraction                ✅"
    )


    print(
        "Alternative Normalisation          ✅"
    )


    print(
        "Dynamic Score Ranking              ✅"
    )


    print(
        "Best Strategy Selection            ✅"
    )


    print(
        "Score / Time Comparison            ✅"
    )


    print(
        "AI Recommendation Alignment        ✅"
    )


    print(
        "\n🏁 PHASE 7.3 VERIFICATION PASSED"
    )


    print(
        "=" * 86
    )


if __name__ == "__main__":

    main()