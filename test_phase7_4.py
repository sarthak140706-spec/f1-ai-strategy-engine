"""
F1 AI STRATEGIST
PHASE 7.4 — PIT WINDOW OPTIMIZER TEST
"""


from src.strategy_engineer.pit_window_optimizer import (
    run_pit_window_optimizer,
    display_pit_window,
    build_candidate_pit_laps,
    calculate_pit_urgency,
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
# MAIN
# ============================================================

def main():

    print(
        "\n" + "=" * 88
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.4 — PIT WINDOW OPTIMIZER TEST"
    )

    print(
        "=" * 88
    )


    # ========================================================
    # 1
    # ========================================================

    print(
        "\n[1/8] Running complete Phase 7.4 pipeline..."
    )


    result = run_pit_window_optimizer(
        TEST_INPUT
    )


    assert isinstance(
        result,
        dict
    )

    assert result


    print(
        "✅ Phase 7.4 optimizer executed."
    )


    # ========================================================
    # 2
    # ========================================================

    print(
        "\n[2/8] Validating Phase 7.4 contract..."
    )


    assert (
        result["engine"]
        ==
        "pit_window_optimizer"
    )


    assert (
        result["phase"]
        ==
        "7.4"
    )


    assert (
        result["status"]
        ==
        "SUCCESS"
    )


    assert (
        result["driver"]
        ==
        "LEC"
    )


    assert (
        result["circuit"]
        ==
        "Monza"
    )


    print(
        "✅ Phase 7.4 contract validated."
    )


    # ========================================================
    # 3
    # ========================================================

    print(
        "\n[3/8] Validating race-state propagation..."
    )


    assert (
        result["current_lap"]
        ==
        32
    )


    assert (
        result["total_laps"]
        ==
        53
    )


    assert (
        result["position"]
        ==
        4
    )


    assert (
        result["current_tyre"]
        ==
        "MEDIUM"
    )


    assert (
        result["tyre_age"]
        ==
        19.0
    )


    assert (
        round(
            result[
                "degradation_rate"
            ],
            3
        )
        ==
        0.084
    )


    print(
        "✅ Race state propagated into optimizer."
    )


    # ========================================================
    # 4
    # ========================================================

    print(
        "\n[4/8] Validating pit strategy selection..."
    )


    assert (
        result[
            "best_pit_strategy"
        ]
        is not None
    )


    assert (
        result[
            "best_pit_strategy"
        ][
            "strategy"
        ]
        ==
        "PIT"
    )


    assert (
        result[
            "recommended_tyre"
        ]
        is not None
    )


    assert (
        result[
            "recommended_tyre"
        ]
        in {
            "SOFT",
            "MEDIUM",
            "HARD",
            "INTERMEDIATE",
            "WET",
        }
    )


    print(
        "✅ Best available pit strategy selected."
    )


    # ========================================================
    # 5
    # ========================================================

    print(
        "\n[5/8] Validating pit urgency and candidate window..."
    )


    assert (
        0
        <=
        result[
            "pit_urgency"
        ]
        <=
        100
    )


    assert (
        result[
            "candidate_count"
        ]
        > 0
    )


    assert (
        len(
            result[
                "candidate_laps"
            ]
        )
        ==
        result[
            "candidate_count"
        ]
    )


    for candidate in result[
        "candidate_laps"
    ]:

        assert (
            candidate[
                "pit_lap"
            ]
            >=
            result[
                "current_lap"
            ]
        )


        assert (
            candidate[
                "pit_lap"
            ]
            <
            result[
                "total_laps"
            ]
        )


    print(
        "✅ Pit urgency and candidate window validated."
    )


    # ========================================================
    # 6
    # ========================================================

    print(
        "\n[6/8] Validating candidate ranking..."
    )


    scores = [

        candidate[
            "pit_window_score"
        ]

        for candidate
        in result[
            "candidate_laps"
        ]

    ]


    assert scores == sorted(
        scores,
        reverse=True
    )


    ranks = [

        candidate[
            "rank"
        ]

        for candidate
        in result[
            "candidate_laps"
        ]

    ]


    assert ranks == list(

        range(
            1,
            len(ranks) + 1
        )

    )


    assert (
        result[
            "recommended_pit_lap"
        ]
        ==
        result[
            "candidate_laps"
        ][0][
            "pit_lap"
        ]
    )


    print(
        "✅ Candidate pit laps ranked correctly."
    )


    # ========================================================
    # 7
    # ========================================================

    print(
        "\n[7/8] Validating optimal pit window..."
    )


    assert (
        result[
            "window_start"
        ]
        <=
        result[
            "recommended_pit_lap"
        ]
        <=
        result[
            "window_end"
        ]
    )


    assert (
        result[
            "window_start"
        ]
        >=
        result[
            "current_lap"
        ]
    )


    assert (
        result[
            "window_end"
        ]
        <
        result[
            "total_laps"
        ]
    )


    assert (
        0
        <=
        result[
            "window_confidence"
        ]
        <=
        100
    )


    assert (
        result[
            "reasoning"
        ]
    )


    print(
        "✅ Optimal pit window validated."
    )


    # ========================================================
    # 8
    # ========================================================

    print(
        "\n[8/8] Validating optimizer helper behaviour..."
    )


    high_urgency = calculate_pit_urgency(

        tyre_age=30,

        degradation_rate=0.15,

        pit_decision="PIT NOW",

        race_situation="NEUTRAL"

    )


    low_urgency = calculate_pit_urgency(

        tyre_age=5,

        degradation_rate=0.01,

        pit_decision="STAY OUT",

        race_situation="NEUTRAL"

    )


    assert (
        high_urgency
        >
        low_urgency
    )


    urgent_laps = build_candidate_pit_laps(

        current_lap=30,

        total_laps=50,

        urgency=90

    )


    relaxed_laps = build_candidate_pit_laps(

        current_lap=30,

        total_laps=50,

        urgency=20

    )


    assert urgent_laps

    assert relaxed_laps


    assert (
        urgent_laps[0]
        <=
        relaxed_laps[0]
    )


    assert (
        len(
            urgent_laps
        )
        <=
        len(
            relaxed_laps
        )
    )


    print(
        "✅ Optimizer helper behaviour validated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_pit_window(
        result
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print(
        "\n" + "=" * 88
    )

    print(
        "PHASE 7.4 VERIFICATION RESULTS"
    )

    print(
        "=" * 88
    )


    print(
        "7.1 Manual Race State             ✅"
    )


    print(
        "7.2 Strategy Engineer             ✅"
    )


    print(
        "7.3 Strategy Alternatives         ✅"
    )


    print(
        "7.4 Pit Window Optimizer          ✅"
    )


    print(
        "Pit Strategy Selection            ✅"
    )


    print(
        "Pit Urgency Calculation           ✅"
    )


    print(
        "Candidate Lap Generation          ✅"
    )


    print(
        "Candidate Lap Ranking             ✅"
    )


    print(
        "Optimal Pit Window                ✅"
    )


    print(
        "Window Confidence                 ✅"
    )


    print(
        "\n🏁 PHASE 7.4 VERIFICATION PASSED"
    )


    print(
        "=" * 88
    )


if __name__ == "__main__":

    main()