"""
F1 AI STRATEGIST
PHASE 7.5 — EXPLANATION & CONFIDENCE ENGINE TEST
"""

from src.strategy_engineer.strategy_explanation_engine import (
    run_strategy_explanation_engine,
    display_strategy_explanation,
    determine_strategy_risk,
)


TEST_INPUT = {

    "driver": "LEC",
    "team": "Ferrari",
    "grand_prix": "Italian Grand Prix",
    "circuit": "Monza",

    "current_lap": 32,
    "total_laps": 53,
    "position": 4,

    "current_tyre": "MEDIUM",
    "tyre_age": 19,

    "gap_ahead": 2.4,
    "gap_behind": 1.8,

    "recent_pace": 84.512,
    "average_pace": 84.740,
    "degradation_rate": 0.084,

    "weather": "DRY",
    "rainfall": 0,

    "track_status": "GREEN",

    "safety_car": False,
    "virtual_safety_car": False,

    "pit_stops_completed": 1,
}


def main():

    print(
        "\n" + "=" * 88
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.5 — EXPLANATION & CONFIDENCE ENGINE TEST"
    )

    print(
        "=" * 88
    )


    # ========================================================
    # 1
    # ========================================================

    print(
        "\n[1/8] Running complete Phase 7.5 pipeline..."
    )


    result = (
        run_strategy_explanation_engine(
            TEST_INPUT
        )
    )


    assert isinstance(
        result,
        dict
    )

    assert result


    print(
        "✅ Phase 7.5 explanation engine executed."
    )


    # ========================================================
    # 2
    # ========================================================

    print(
        "\n[2/8] Validating Phase 7.5 contract..."
    )


    assert (
        result["engine"]
        ==
        "strategy_explanation_engine"
    )


    assert (
        result["phase"]
        ==
        "7.5"
    )


    assert (
        result["status"]
        ==
        "SUCCESS"
    )


    print(
        "✅ Phase 7.5 contract validated."
    )


    # ========================================================
    # 3
    # ========================================================

    print(
        "\n[3/8] Validating final strategy recommendation..."
    )


    assert result.get(
        "final_recommendation"
    )


    assert result.get(
        "recommended_tyre"
    )


    print(
        "✅ Final recommendation validated."
    )


    # ========================================================
    # 4
    # ========================================================

    print(
        "\n[4/8] Validating engineer confidence..."
    )


    confidence = result[
        "confidence"
    ]


    assert (
        0
        <=
        confidence
        <=
        100
    )


    print(
        "✅ Engineer confidence validated."
    )


    # ========================================================
    # 5
    # ========================================================

    print(
        "\n[5/8] Validating strategic risk..."
    )


    assert result[
        "risk_level"
    ] in {

        "LOW",
        "MEDIUM",
        "HIGH",

    }


    high_risk = determine_strategy_risk(

        pit_window_result={
            "pit_urgency": 95,
            "degradation_rate": 0.15,
        },

        strategy_result={
            "tyre_condition": "CRITICAL",
            "wet_conditions": False,
            "safety_car": False,
            "virtual_safety_car": False,
        }

    )


    assert (
        high_risk
        ==
        "HIGH"
    )


    print(
        "✅ Strategic risk classification validated."
    )


    # ========================================================
    # 6
    # ========================================================

    print(
        "\n[6/8] Validating engineer explanation..."
    )


    assert result[
        "summary"
    ]


    assert result[
        "explanation"
    ]


    assert result[
        "pit_window_explanation"
    ]


    assert (
        result[
            "final_recommendation"
        ].lower()
        in
        result[
            "explanation"
        ].lower()
    )


    print(
        "✅ Engineer explanation validated."
    )


    # ========================================================
    # 7
    # ========================================================

    print(
        "\n[7/8] Validating strategic factors..."
    )


    factors = result[
        "key_factors"
    ]


    assert isinstance(
        factors,
        list
    )


    assert len(
        factors
    ) >= 5


    labels = {

        factor[
            "label"
        ]

        for factor
        in factors

    }


    assert (
        "Position"
        in labels
    )


    assert (
        "Current Tyre"
        in labels
    )


    assert (
        "Tyre Age"
        in labels
    )


    assert (
        "Degradation"
        in labels
    )


    assert (
        "Pit Urgency"
        in labels
    )


    print(
        "✅ Strategic factors validated."
    )


    # ========================================================
    # 8
    # ========================================================

    print(
        "\n[8/8] Validating strategy alternatives and warnings..."
    )


    assert isinstance(
        result[
            "strategy_alternatives"
        ],
        list
    )


    assert len(
        result[
            "strategy_alternatives"
        ]
    ) >= 2


    assert isinstance(
        result[
            "warnings"
        ],
        list
    )


    assert isinstance(
        result[
            "best_pit_alternative"
        ],
        dict
    )


    print(
        "✅ Alternatives and warning layer validated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_strategy_explanation(
        result
    )


    # ========================================================
    # FINAL
    # ========================================================

    print(
        "\n" + "=" * 88
    )

    print(
        "PHASE 7.5 VERIFICATION RESULTS"
    )

    print(
        "=" * 88
    )


    print(
        "7.1 Manual Race State              ✅"
    )


    print(
        "7.2 Strategy Engineer              ✅"
    )


    print(
        "7.3 Strategy Alternatives          ✅"
    )


    print(
        "7.4 Pit Window Optimizer           ✅"
    )


    print(
        "7.5 Explanation Engine             ✅"
    )


    print(
        "Final Recommendation               ✅"
    )


    print(
        "Confidence Calculation             ✅"
    )


    print(
        "Risk Classification               ✅"
    )


    print(
        "Engineer Explanation               ✅"
    )


    print(
        "Key Strategic Factors             ✅"
    )


    print(
        "Strategy Warning Layer            ✅"
    )


    print(
        "\n🏁 PHASE 7.5 VERIFICATION PASSED"
    )


    print(
        "=" * 88
    )


if __name__ == "__main__":

    main()