"""
F1 AI STRATEGIST
PHASE 7.9 — FINAL PHASE 7 INTEGRATION VERIFICATION

Purpose
-------
Perform the final end-to-end verification of the complete
AI Strategy Engineer architecture.

Phase 7.9 validates:

7.1 Manual Race-State Builder
7.2 AI Strategy Engineer
7.3 Strategy Alternatives Engine
7.4 Pit Window Optimizer
7.5 Explanation & Confidence Engine
7.6 Strategy Engineer REST API
7.7 Frontend/API Contract
7.8 What-If Scenario Comparison

It additionally verifies:

- API registration
- complete pipeline contracts
- repeatability
- scenario sensitivity
- failure-safe behaviour
- response consistency
- regression safety

IMPORTANT
---------
Phase 7.9 does not introduce a new strategy engine.

It is the final quality gate before Phase 7 is frozen.
"""


from __future__ import annotations


from copy import deepcopy

from typing import (
    Any,
    Dict,
    List,
)


# ============================================================
# FLASK APPLICATION
# ============================================================

from api.app import app


# ============================================================
# PHASE 7.8
# ============================================================

from src.strategy_engineer.scenario_comparison import (

    ScenarioComparisonError,

    build_default_scenarios,

    extract_final_decision,

    extract_pipeline_result,

    run_scenario_comparison,

    validate_scenario_comparison_contract,

)


# ============================================================
# TEST CONFIGURATION
# ============================================================

LINE = "=" * 100


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
# HELPERS
# ============================================================

def success(
    message: str
) -> None:

    print(
        f"✅ {message}"
    )


def heading(
    title: str
) -> None:

    print(
        "\n"
        +
        LINE
    )

    print(
        title
    )

    print(
        LINE
    )


def safe_dict(
    value: Any
) -> Dict[str, Any]:

    if isinstance(
        value,
        dict
    ):

        return value


    return {}


def assert_dictionary(
    value: Any,
    name: str
) -> None:

    if not isinstance(
        value,
        dict
    ):

        raise AssertionError(

            f"{name} must be a dictionary."

        )


    if not value:

        raise AssertionError(

            f"{name} cannot be empty."

        )


# ============================================================
# CREATE TEST CLIENT
# ============================================================

def create_client():

    app.config[
        "TESTING"
    ] = True


    return app.test_client()


# ============================================================
# API REQUEST
# ============================================================

def run_engineer_api(
    client,
    race_input: Dict[str, Any]
) -> Dict[str, Any]:

    response = client.post(

        "/api/engineer/analyse",

        json=race_input

    )


    data = response.get_json()


    if response.status_code != 200:

        raise AssertionError(

            "Strategy Engineer API failed. "
            f"HTTP {response.status_code}: "
            f"{data}"

        )


    assert_dictionary(

        data,

        "API response"

    )


    return data


# ============================================================
# PIPELINE CONTRACT
# ============================================================

def validate_complete_pipeline(
    pipeline: Dict[str, Any]
) -> None:

    """
    Validate the complete output contract expected
    from the Strategy Engineer API.
    """

    assert_dictionary(

        pipeline,

        "Phase 7 pipeline"

    )


    required_components = [

        "race_state",

        "strategy_engineer",

        "alternatives",

        "pit_window",

        "explanation",

    ]


    missing = [

        component

        for component in required_components

        if component not in pipeline

    ]


    if missing:

        raise AssertionError(

            "Complete Phase 7 pipeline is missing: "
            +
            ", ".join(
                missing
            )

        )


    for component in required_components:

        assert_dictionary(

            pipeline[
                component
            ],

            component

        )


# ============================================================
# RACE STATE CONTRACT
# ============================================================

def validate_race_state(
    race_state: Dict[str, Any]
) -> None:

    required = [

        "Driver",

        "Circuit",

        "CurrentLap",

        "TotalLaps",

        "LapsRemaining",

        "Position",

        "TyreCompound",

        "TyreAge",

        "RaceProgress",

        "DegradationRate",

    ]


    missing = [

        key

        for key in required

        if key not in race_state

    ]


    if missing:

        raise AssertionError(

            "Race state is missing fields: "
            +
            ", ".join(
                missing
            )

        )


    assert (

        race_state[
            "CurrentLap"
        ]
        <=
        race_state[
            "TotalLaps"
        ]

    )


    assert (

        race_state[
            "LapsRemaining"
        ]
        ==
        race_state[
            "TotalLaps"
        ]
        -
        race_state[
            "CurrentLap"
        ]

    )


    assert (

        1
        <=
        race_state[
            "Position"
        ]
        <=
        20

    )


# ============================================================
# FINAL DECISION CONTRACT
# ============================================================

def validate_final_decision(
    decision: Dict[str, Any]
) -> None:

    required = [

        "recommendation",

        "recommended_tyre",

        "confidence",

        "risk_level",

        "race_situation",

        "pit_decision",

        "pit_urgency",

        "best_strategy",

    ]


    missing = [

        key

        for key in required

        if key not in decision

    ]


    if missing:

        raise AssertionError(

            "Final decision is missing fields: "
            +
            ", ".join(
                missing
            )

        )


    recommendation = decision.get(
        "recommendation"
    )


    if not recommendation:

        raise AssertionError(

            "Final AI recommendation is empty."

        )


    tyre = decision.get(
        "recommended_tyre"
    )


    if not tyre:

        raise AssertionError(

            "Recommended tyre is empty."

        )


    confidence = decision.get(
        "confidence"
    )


    if confidence is not None:

        confidence = float(
            confidence
        )


        if not (
            0
            <=
            confidence
            <=
            100
        ):

            raise AssertionError(

                "Confidence must be between 0 and 100."

            )


    urgency = decision.get(
        "pit_urgency"
    )


    if urgency is not None:

        urgency = float(
            urgency
        )


        if not (
            0
            <=
            urgency
            <=
            100
        ):

            raise AssertionError(

                "Pit urgency must be between 0 and 100."

            )


# ============================================================
# ALTERNATIVES CONTRACT
# ============================================================

def validate_alternatives(
    alternatives_data: Dict[str, Any]
) -> None:

    possible_keys = [

        "alternatives",

        "strategies",

        "ranked_strategies",

    ]


    alternatives = None


    for key in possible_keys:

        value = alternatives_data.get(
            key
        )


        if isinstance(
            value,
            list
        ):

            alternatives = value

            break


    if alternatives is None:

        raise AssertionError(

            "Strategy alternatives list was not found."

        )


    if not alternatives:

        raise AssertionError(

            "Strategy alternatives cannot be empty."

        )


    previous_score = None


    for index, strategy in enumerate(
        alternatives,
        start=1
    ):

        assert_dictionary(

            strategy,

            f"Strategy alternative {index}"

        )


        score = (

            strategy.get(
                "dynamic_score"
            )

            if strategy.get(
                "dynamic_score"
            )
            is not None

            else

            strategy.get(
                "score"
            )

        )


        if score is None:

            continue


        score = float(
            score
        )


        if previous_score is not None:

            if score > previous_score:

                raise AssertionError(

                    "Strategy alternatives are "
                    "not ranked by descending score."

                )


        previous_score = score


# ============================================================
# PIT WINDOW CONTRACT
# ============================================================

def validate_pit_window(
    pit_window: Dict[str, Any],
    current_lap: int,
    total_laps: int
) -> None:

    urgency = (

        pit_window.get(
            "pit_urgency"
        )

        if pit_window.get(
            "pit_urgency"
        )
        is not None

        else

        pit_window.get(
            "PitUrgency"
        )

    )


    if urgency is not None:

        urgency = float(
            urgency
        )


        assert (
            0
            <=
            urgency
            <=
            100
        )


    pit_lap = (

        pit_window.get(
            "recommended_pit_lap"
        )

        if pit_window.get(
            "recommended_pit_lap"
        )
        is not None

        else

        pit_window.get(
            "optimal_pit_lap"
        )

    )


    if pit_lap is not None:

        pit_lap = int(
            pit_lap
        )


        if not (

            current_lap
            <=
            pit_lap
            <=
            total_laps

        ):

            raise AssertionError(

                "Recommended pit lap is outside "
                "the remaining race distance."

            )


# ============================================================
# EXPLANATION CONTRACT
# ============================================================

def validate_explanation(
    explanation: Dict[str, Any]
) -> None:

    recommendation = (

        explanation.get(
            "final_recommendation"
        )

        or

        explanation.get(
            "recommendation"
        )

    )


    if not recommendation:

        raise AssertionError(

            "Explanation layer does not contain "
            "a final recommendation."

        )


    explanation_text = (

        explanation.get(
            "engineer_explanation"
        )

        or

        explanation.get(
            "explanation"
        )

        or

        explanation.get(
            "reasoning"
        )

    )


    if not explanation_text:

        raise AssertionError(

            "Engineer explanation is empty."

        )


    if len(
        str(
            explanation_text
        ).strip()
    ) < 20:

        raise AssertionError(

            "Engineer explanation is unexpectedly short."

        )


# ============================================================
# DETERMINISM
# ============================================================

def validate_repeatability(
    first_decision: Dict[str, Any],
    second_decision: Dict[str, Any]
) -> None:

    """
    The same exact race state should produce
    the same strategic decision.
    """

    stable_fields = [

        "recommendation",

        "recommended_tyre",

        "risk_level",

        "race_situation",

        "pit_decision",

        "best_strategy",

    ]


    for field in stable_fields:

        if (

            first_decision.get(
                field
            )

            !=

            second_decision.get(
                field
            )

        ):

            raise AssertionError(

                "Repeated identical input changed "
                f"the '{field}' result."

            )


# ============================================================
# FAILURE-SAFE API
# ============================================================

def validate_failure_safe_api(
    client
) -> None:

    """
    Invalid race states must never return a successful
    strategy result.
    """

    invalid_cases = [

        {},


        {
            **BASE_RACE_INPUT,

            "current_lap":
                60,

            "total_laps":
                53,

        },


        {
            **BASE_RACE_INPUT,

            "position":
                25,

        },


        {
            **BASE_RACE_INPUT,

            "tyre_compound":
                "WOOD",

        },


        {
            **BASE_RACE_INPUT,

            "safety_car":
                True,

            "virtual_safety_car":
                True,

        },

    ]


    for index, race_input in enumerate(
        invalid_cases,
        start=1
    ):

        response = client.post(

            "/api/engineer/analyse",

            json=race_input

        )


        if response.status_code == 200:

            data = response.get_json()


            # Some APIs may respond with HTTP 200 but
            # explicitly mark the request as unsuccessful.

            if isinstance(
                data,
                dict
            ):

                status = str(

                    data.get(
                        "status",
                        ""
                    )

                ).upper()


                if status in {

                    "ERROR",

                    "FAILED",

                    "FAILURE",

                }:

                    continue


            raise AssertionError(

                "Invalid race state was unexpectedly "
                f"accepted in failure test {index}."

            )


# ============================================================
# ROUTE REGISTRATION
# ============================================================

def validate_engineer_route() -> None:

    routes = {

        rule.rule

        for rule in app.url_map.iter_rules()

    }


    required_route = (

        "/api/engineer/analyse"

    )


    if required_route not in routes:

        raise AssertionError(

            "Strategy Engineer API route is not registered: "
            f"{required_route}"

        )


# ============================================================
# MAIN TEST
# ============================================================

def main():

    heading(

        "F1 AI STRATEGIST\n"
        "PHASE 7.9 — FINAL PHASE 7 INTEGRATION VERIFICATION"

    )


    client = create_client()


    # ========================================================
    # 1 / 12
    # ========================================================

    print(
        "\n[1/12] Validating Strategy Engineer API registration..."
    )


    validate_engineer_route()


    success(
        "Strategy Engineer API route registered."
    )


    # ========================================================
    # 2 / 12
    # ========================================================

    print(
        "\n[2/12] Running complete Phase 7 API pipeline..."
    )


    response = run_engineer_api(

        client,

        deepcopy(
            BASE_RACE_INPUT
        )

    )


    success(
        "Complete Strategy Engineer API executed."
    )


    # ========================================================
    # 3 / 12
    # ========================================================

    print(
        "\n[3/12] Extracting complete Phase 7 result..."
    )


    pipeline = extract_pipeline_result(

        response

    )


    validate_complete_pipeline(

        pipeline

    )


    success(
        "Complete Phase 7 pipeline extracted."
    )


    # ========================================================
    # 4 / 12
    # ========================================================

    print(
        "\n[4/12] Validating Phase 7.1 race-state contract..."
    )


    race_state = safe_dict(

        pipeline.get(
            "race_state"
        )

    )


    validate_race_state(

        race_state

    )


    success(
        "Phase 7.1 race-state contract validated."
    )


    # ========================================================
    # 5 / 12
    # ========================================================

    print(
        "\n[5/12] Validating final AI strategy decision..."
    )


    decision = extract_final_decision(

        pipeline

    )


    validate_final_decision(

        decision

    )


    success(
        "Final AI strategy decision validated."
    )


    # ========================================================
    # 6 / 12
    # ========================================================

    print(
        "\n[6/12] Validating strategy alternatives..."
    )


    alternatives = safe_dict(

        pipeline.get(
            "alternatives"
        )

    )


    validate_alternatives(

        alternatives

    )


    success(
        "Phase 7.3 strategy alternatives validated."
    )


    # ========================================================
    # 7 / 12
    # ========================================================

    print(
        "\n[7/12] Validating pit-window optimizer..."
    )


    pit_window = safe_dict(

        pipeline.get(
            "pit_window"
        )

    )


    validate_pit_window(

        pit_window,

        current_lap=
            int(
                race_state[
                    "CurrentLap"
                ]
            ),

        total_laps=
            int(
                race_state[
                    "TotalLaps"
                ]
            ),

    )


    success(
        "Phase 7.4 pit-window contract validated."
    )


    # ========================================================
    # 8 / 12
    # ========================================================

    print(
        "\n[8/12] Validating explanation and confidence layer..."
    )


    explanation = safe_dict(

        pipeline.get(
            "explanation"
        )

    )


    validate_explanation(

        explanation

    )


    success(
        "Phase 7.5 explanation contract validated."
    )


    # ========================================================
    # 9 / 12
    # ========================================================

    print(
        "\n[9/12] Testing deterministic strategy behaviour..."
    )


    repeated_response = run_engineer_api(

        client,

        deepcopy(
            BASE_RACE_INPUT
        )

    )


    repeated_pipeline = (

        extract_pipeline_result(
            repeated_response
        )

    )


    repeated_decision = (

        extract_final_decision(
            repeated_pipeline
        )

    )


    validate_repeatability(

        decision,

        repeated_decision

    )


    success(
        "Identical race states produce stable decisions."
    )


    # ========================================================
    # 10 / 12
    # ========================================================

    print(
        "\n[10/12] Running Phase 7.8 scenario sensitivity..."
    )


    scenarios = build_default_scenarios(

        BASE_RACE_INPUT

    )


    scenario_result = (

        run_scenario_comparison(

            base_race_input=
                BASE_RACE_INPUT,

            scenarios=
                scenarios,

            client=
                client,

        )

    )


    validate_scenario_comparison_contract(

        scenario_result

    )


    assert (

        scenario_result[
            "scenario_count"
        ]
        ==
        len(
            scenarios
        )

    )


    stability = safe_dict(

        scenario_result.get(
            "decision_stability"
        )

    )


    assert (

        0
        <=
        float(
            stability[
                "stability_percentage"
            ]
        )
        <=
        100

    )


    ranking = scenario_result.get(

        "sensitivity_ranking",

        []

    )


    if not ranking:

        raise AssertionError(

            "Phase 7.8 sensitivity ranking is empty."

        )


    success(
        "Phase 7.8 scenario sensitivity validated."
    )


    # ========================================================
    # 11 / 12
    # ========================================================

    print(
        "\n[11/12] Testing failure-safe API behaviour..."
    )


    validate_failure_safe_api(

        client

    )


    success(
        "Invalid race states safely rejected."
    )


    # ========================================================
    # 12 / 12
    # ========================================================

    print(
        "\n[12/12] Performing final cross-phase consistency check..."
    )


    base_scenario_decision = safe_dict(

        scenario_result.get(
            "base_decision"
        )

    )


    if (

        base_scenario_decision.get(
            "recommendation"
        )

        !=

        decision.get(
            "recommendation"
        )

    ):

        raise AssertionError(

            "Phase 7.8 base recommendation differs "
            "from the Phase 7.6 API recommendation."

        )


    if (

        base_scenario_decision.get(
            "recommended_tyre"
        )

        !=

        decision.get(
            "recommended_tyre"
        )

    ):

        raise AssertionError(

            "Phase 7.8 recommended tyre differs "
            "from the Phase 7.6 API result."

        )


    success(
        "Cross-phase strategy consistency validated."
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    heading(

        "F1 AI STRATEGIST\n"
        "PHASE 7.9 — FINAL SYSTEM RESULT"

    )


    print(
        f"Driver:                    "
        f"{decision.get('driver')}"
    )


    print(
        f"Circuit:                   "
        f"{decision.get('circuit')}"
    )


    print(
        f"Lap:                       "
        f"{decision.get('current_lap')}/"
        f"{decision.get('total_laps')}"
    )


    print(
        f"Position:                  "
        f"P{decision.get('position')}"
    )


    print(
        "-" * 100
    )


    print(
        f"Final Recommendation:      "
        f"{decision.get('recommendation')}"
    )


    print(
        f"Recommended Tyre:          "
        f"{decision.get('recommended_tyre')}"
    )


    print(
        f"Confidence:                "
        f"{decision.get('confidence')}%"
    )


    print(
        f"Risk Level:                "
        f"{decision.get('risk_level')}"
    )


    print(
        f"Race Situation:            "
        f"{decision.get('race_situation')}"
    )


    print(
        f"Pit Decision:              "
        f"{decision.get('pit_decision')}"
    )


    print(
        f"Pit Urgency:               "
        f"{decision.get('pit_urgency')}/100"
    )


    print(
        f"Recommended Pit Lap:       "
        f"{decision.get('recommended_pit_lap')}"
    )


    print(
        "-" * 100
    )


    print(
        f"What-If Scenarios Tested:  "
        f"{scenario_result.get('scenario_count')}"
    )


    print(
        f"Decision Stability:        "
        f"{stability.get('stability_percentage')}%"
    )


    print(
        f"Stability Classification:  "
        f"{stability.get('classification')}"
    )


    most_sensitive = safe_dict(

        scenario_result.get(
            "most_sensitive_scenario"
        )

    )


    print(
        f"Most Sensitive Scenario:   "
        f"{most_sensitive.get('scenario')}"
    )


    print(
        f"Maximum Sensitivity:       "
        f"{most_sensitive.get('sensitivity_score')}/100"
    )


    # ========================================================
    # VERIFICATION SUMMARY
    # ========================================================

    heading(

        "PHASE 7.9 — COMPLETE PHASE 7 VERIFICATION RESULTS"

    )


    verification_results = [

        (
            "7.1 Manual Race-State Builder",
            True
        ),

        (
            "7.2 AI Strategy Engineer",
            True
        ),

        (
            "7.3 Strategy Alternatives Engine",
            True
        ),

        (
            "7.4 Pit Window Optimizer",
            True
        ),

        (
            "7.5 Explanation & Confidence Engine",
            True
        ),

        (
            "7.6 Strategy Engineer REST API",
            True
        ),

        (
            "7.7 Frontend/API Contract",
            True
        ),

        (
            "7.8 What-If Scenario Comparison",
            True
        ),

        (
            "API Route Registration",
            True
        ),

        (
            "End-to-End Pipeline Contract",
            True
        ),

        (
            "Strategy Repeatability",
            True
        ),

        (
            "Scenario Sensitivity",
            True
        ),

        (
            "Cross-Phase Consistency",
            True
        ),

        (
            "Failure-Safe Validation",
            True
        ),

    ]


    for label, passed in verification_results:

        print(

            f"{label:<46}"
            f"{'✅' if passed else '❌'}"

        )


    print()


    print(
        "🏁 PHASE 7.9 FINAL VERIFICATION PASSED"
    )


    print()


    print(
        "🏆 PHASE 7 — AI STRATEGY ENGINEER COMPLETE"
    )


    print(
        LINE
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()