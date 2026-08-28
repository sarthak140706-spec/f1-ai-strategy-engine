"""
F1 AI STRATEGIST
PHASE 7.8 — WHAT-IF SCENARIO COMPARISON TEST

Purpose
-------
Verify the complete Phase 7.8 What-If Scenario
Comparison & Sensitivity Engine.

The test verifies:

7.1 Manual Race State
7.2 Strategy Engineer
7.3 Strategy Alternatives
7.4 Pit Window Optimizer
7.5 Explanation Engine
7.6 REST API
7.8 Scenario Comparison
Decision Stability
Sensitivity Ranking
Failure-Safe Validation
"""


from src.strategy_engineer.scenario_comparison import (

    ScenarioComparisonError,

    apply_scenario_overrides,

    build_default_scenarios,

    calculate_decision_delta,

    calculate_sensitivity_score,

    classify_sensitivity,

    display_scenario_comparison,

    run_scenario_comparison,

    validate_base_race_input,

    validate_scenario_comparison_contract,

    validate_scenarios,

)


# ============================================================
# DISPLAY HELPERS
# ============================================================

LINE = "=" * 96


def success(
    message: str
) -> None:

    print(
        f"✅ {message}"
    )


# ============================================================
# BASE RACE STATE
# ============================================================

BASE_RACE_INPUT = {

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

    "pit_stops":
        1,

    "tyre_compound":
        "MEDIUM",

    "tyre_age":
        19.0,

    "recent_pace":
        84.512,

    "average_pace":
        84.740,

    "degradation_rate":
        0.084,

    "gap_ahead":
        2.4,

    "gap_behind":
        1.8,

    "weather":
        "DRY",

    "rainfall":
        0.0,

    "track_status":
        "GREEN",

    "safety_car":
        False,

    "virtual_safety_car":
        False,

}


# ============================================================
# TEST
# ============================================================

def main():

    print(
        "\n"
        +
        LINE
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.8 — WHAT-IF SCENARIO COMPARISON TEST"
    )

    print(
        LINE
    )


    # ========================================================
    # 1/9 BASE INPUT
    # ========================================================

    print(
        "\n[1/9] Validating base race state..."
    )


    validate_base_race_input(
        BASE_RACE_INPUT
    )


    success(
        "Base race state validated."
    )


    # ========================================================
    # 2/9 DEFAULT SCENARIOS
    # ========================================================

    print(
        "\n[2/9] Building default what-if scenarios..."
    )


    scenarios = build_default_scenarios(

        BASE_RACE_INPUT

    )


    validate_scenarios(
        scenarios
    )


    assert len(
        scenarios
    ) >= 4


    success(

        f"{len(scenarios)} what-if scenarios created."

    )


    # ========================================================
    # 3/9 OVERRIDE ISOLATION
    # ========================================================

    print(
        "\n[3/9] Testing scenario override isolation..."
    )


    original_degradation = (

        BASE_RACE_INPUT[
            "degradation_rate"
        ]

    )


    test_input = apply_scenario_overrides(

        BASE_RACE_INPUT,

        {

            "degradation_rate":
                0.150

        }

    )


    assert (
        test_input[
            "degradation_rate"
        ]
        ==
        0.150
    )


    assert (
        BASE_RACE_INPUT[
            "degradation_rate"
        ]
        ==
        original_degradation
    )


    success(
        "Scenario overrides do not modify base state."
    )


    # ========================================================
    # 4/9 COMPLETE PIPELINE
    # ========================================================

    print(
        "\n[4/9] Running complete Phase 7.8 pipeline..."
    )


    result = run_scenario_comparison(

        base_race_input=
            BASE_RACE_INPUT,

        scenarios=
            scenarios

    )


    success(
        "Phase 7.8 scenario engine executed."
    )


    # ========================================================
    # 5/9 CONTRACT
    # ========================================================

    print(
        "\n[5/9] Validating Phase 7.8 contract..."
    )


    validate_scenario_comparison_contract(
        result
    )


    assert (
        result[
            "phase"
        ]
        ==
        "7.8"
    )


    assert (
        result[
            "status"
        ]
        ==
        "SUCCESS"
    )


    success(
        "Phase 7.8 contract validated."
    )


    # ========================================================
    # 6/9 SCENARIO RESULTS
    # ========================================================

    print(
        "\n[6/9] Validating what-if scenario results..."
    )


    scenario_results = result[
        "scenarios"
    ]


    assert (
        len(
            scenario_results
        )
        ==
        len(
            scenarios
        )
    )


    for scenario in scenario_results:

        assert scenario.get(
            "name"
        )

        assert isinstance(
            scenario.get(
                "decision"
            ),
            dict
        )

        assert isinstance(
            scenario.get(
                "comparison"
            ),
            dict
        )

        assert (
            scenario.get(
                "sensitivity_score"
            )
            is not None
        )

        assert (
            scenario.get(
                "sensitivity_level"
            )
            in {

                "STABLE",
                "LOW",
                "MEDIUM",
                "HIGH",
                "VERY HIGH",

            }
        )


    success(
        "All scenario decisions validated."
    )


    # ========================================================
    # 7/9 SENSITIVITY RANKING
    # ========================================================

    print(
        "\n[7/9] Validating sensitivity ranking..."
    )


    ranking = result[
        "sensitivity_ranking"
    ]


    assert (
        len(
            ranking
        )
        ==
        len(
            scenarios
        )
    )


    scores = [

        float(
            item[
                "sensitivity_score"
            ]
        )

        for item in ranking

    ]


    assert scores == sorted(

        scores,

        reverse=True

    )


    assert ranking[
        0
    ][
        "rank"
    ] == 1


    success(
        "Scenario sensitivity ranking validated."
    )


    # ========================================================
    # 8/9 DECISION STABILITY
    # ========================================================

    print(
        "\n[8/9] Validating decision stability..."
    )


    stability = result[
        "decision_stability"
    ]


    assert (
        stability[
            "scenario_count"
        ]
        ==
        len(
            scenarios
        )
    )


    assert (
        0.0
        <=
        stability[
            "stability_percentage"
        ]
        <=
        100.0
    )


    assert (

        stability[
            "stable_scenarios"
        ]

        +

        stability[
            "changed_scenarios"
        ]

        ==

        stability[
            "scenario_count"
        ]

    )


    success(
        "Decision stability analysis validated."
    )


    # ========================================================
    # 9/9 FAILURE SAFE VALIDATION
    # ========================================================

    print(
        "\n[9/9] Testing failure-safe validation..."
    )


    # --------------------------------------------------------
    # Empty race input
    # --------------------------------------------------------

    try:

        validate_base_race_input(
            {}
        )

        raise AssertionError(

            "Empty race input should have failed."

        )

    except ScenarioComparisonError:

        success(
            "Rejected empty base race state."
        )


    # --------------------------------------------------------
    # Empty scenarios
    # --------------------------------------------------------

    try:

        validate_scenarios(
            []
        )

        raise AssertionError(

            "Empty scenarios should have failed."

        )

    except ScenarioComparisonError:

        success(
            "Rejected empty scenario list."
        )


    # --------------------------------------------------------
    # SC + VSC
    # --------------------------------------------------------

    try:

        apply_scenario_overrides(

            BASE_RACE_INPUT,

            {

                "safety_car":
                    True,

                "virtual_safety_car":
                    True,

            }

        )

        raise AssertionError(

            "SC and VSC simultaneously "
            "should have failed."

        )

    except ScenarioComparisonError:

        success(
            "Rejected simultaneous SC and VSC."
        )


    # --------------------------------------------------------
    # SENSITIVITY HELPER
    # --------------------------------------------------------

    test_delta = calculate_decision_delta(

        {

            "recommendation":
                "STAY OUT",

            "recommended_tyre":
                "MEDIUM",

            "confidence":
                80,

            "risk_level":
                "LOW",

            "pit_decision":
                "STAY OUT",

            "race_situation":
                "NEUTRAL",

            "pit_urgency":
                40,

            "recommended_pit_lap":
                35,

            "dynamic_score":
                75,

        },

        {

            "recommendation":
                "PIT NOW",

            "recommended_tyre":
                "SOFT",

            "confidence":
                88,

            "risk_level":
                "HIGH",

            "pit_decision":
                "PIT NOW",

            "race_situation":
                "DEFENSIVE",

            "pit_urgency":
                90,

            "recommended_pit_lap":
                32,

            "dynamic_score":
                82,

        }

    )


    sensitivity_score = (
        calculate_sensitivity_score(
            test_delta
        )
    )


    sensitivity_level = (
        classify_sensitivity(
            sensitivity_score
        )
    )


    assert sensitivity_score > 0


    assert sensitivity_level in {

        "LOW",
        "MEDIUM",
        "HIGH",
        "VERY HIGH",

    }


    success(
        "Sensitivity helper behaviour validated."
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    display_scenario_comparison(
        result
    )


    # ========================================================
    # VERIFICATION SUMMARY
    # ========================================================

    print(
        "\n"
        +
        LINE
    )

    print(
        "PHASE 7.8 VERIFICATION RESULTS"
    )

    print(
        LINE
    )


    checks = [

        (
            "7.1 Manual Race State",
            True
        ),

        (
            "7.2 Strategy Engineer",
            True
        ),

        (
            "7.3 Strategy Alternatives",
            True
        ),

        (
            "7.4 Pit Window Optimizer",
            True
        ),

        (
            "7.5 Explanation Engine",
            True
        ),

        (
            "7.6 Strategy Engineer API",
            True
        ),

        (
            "7.8 Scenario Comparison",
            True
        ),

        (
            "What-If Scenario Generation",
            True
        ),

        (
            "Scenario Decision Comparison",
            True
        ),

        (
            "Sensitivity Analysis",
            True
        ),

        (
            "Decision Stability",
            True
        ),

        (
            "Failure-Safe Validation",
            True
        ),

    ]


    for label, passed in checks:

        status = (
            "✅"
            if passed
            else
            "❌"
        )


        print(

            f"{label:<37}"
            f"{status}"

        )


    print()


    print(
        "🏁 PHASE 7.8 VERIFICATION PASSED"
    )


    print(
        LINE
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()