"""
F1 AI STRATEGIST

PHASE 7.10.7
FINAL REGRESSION VERIFICATION

Purpose
-------
Verify that the complete frontend-integrated Phase 7 system
still preserves all previously verified behaviour.

This test checks:

1. Strategy Engineer API route registration
2. What-If API route registration
3. Main strategy pipeline
4. Race-state contract
5. Strategy alternatives
6. Pit-window output
7. Explanation layer
8. What-If scenario output
9. Decision stability
10. Cross-endpoint consistency
11. Deterministic repeatability
12. Invalid-input rejection
13. Scenario contract regression
14. Final Phase 7.10 integration contract
"""


from __future__ import annotations


from copy import deepcopy

from typing import Any, Dict


from api.app import app


from src.strategy_engineer.scenario_comparison import (
    validate_scenario_comparison_contract
)


# ============================================================
# CONSTANTS
# ============================================================

LINE = "=" * 100


STRATEGY_ENDPOINT = (
    "/api/engineer/analyse"
)


WHAT_IF_ENDPOINT = (
    "/api/engineer/what-if"
)


BASE_RACE_INPUT = {

    "driver":
        "LEC",

    "team":
        "Ferrari",

    "grand_prix":
        "Italian Grand Prix",

    "circuit":
        "Autodromo Nazionale Monza",

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


def success(
    message: str
) -> None:

    print(
        f"✅ {message}"
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


def create_client():

    app.config[
        "TESTING"
    ] = True


    return app.test_client()


# ============================================================
# ROUTE VERIFICATION
# ============================================================

def validate_routes() -> None:

    routes = {

        rule.rule

        for rule in
        app.url_map.iter_rules()

    }


    required_routes = {

        STRATEGY_ENDPOINT,

        WHAT_IF_ENDPOINT,

    }


    missing = (

        required_routes
        -
        routes

    )


    if missing:

        raise AssertionError(

            "Missing required routes: "
            +
            ", ".join(
                sorted(
                    missing
                )
            )

        )


# ============================================================
# MAIN STRATEGY REQUEST
# ============================================================

def run_strategy(
    client
) -> Dict[str, Any]:

    response = client.post(

        STRATEGY_ENDPOINT,

        json=deepcopy(
            BASE_RACE_INPUT
        )

    )


    if (
        response.status_code
        !=
        200
    ):

        raise AssertionError(

            "Strategy endpoint failed. "
            f"HTTP {response.status_code}: "
            f"{response.get_json()}"

        )


    payload = response.get_json()


    if (
        payload.get(
            "status"
        )
        !=
        "SUCCESS"
    ):

        raise AssertionError(

            "Strategy endpoint did not return SUCCESS."

        )


    return payload


# ============================================================
# WHAT-IF REQUEST
# ============================================================

def run_what_if(
    client
) -> Dict[str, Any]:

    response = client.post(

        WHAT_IF_ENDPOINT,

        json=deepcopy(
            BASE_RACE_INPUT
        )

    )


    if (
        response.status_code
        !=
        200
    ):

        raise AssertionError(

            "What-If endpoint failed. "
            f"HTTP {response.status_code}: "
            f"{response.get_json()}"

        )


    payload = response.get_json()


    if (
        payload.get(
            "status"
        )
        !=
        "SUCCESS"
    ):

        raise AssertionError(

            "What-If endpoint did not return SUCCESS."

        )


    return payload


# ============================================================
# MAIN PIPELINE EXTRACTION
# ============================================================

def extract_strategy_result(
    payload: Dict[str, Any]
) -> Dict[str, Any]:

    data = safe_dict(

        payload.get(
            "data"
        )

    )


    result = safe_dict(

        data.get(
            "result"
        )

    )


    if not result:

        raise AssertionError(

            "Strategy result is empty."

        )


    return result


# ============================================================
# WHAT-IF EXTRACTION
# ============================================================

def extract_what_if_result(
    payload: Dict[str, Any]
) -> Dict[str, Any]:

    data = safe_dict(

        payload.get(
            "data"
        )

    )


    result = safe_dict(

        data.get(
            "result"
        )

    )


    if not result:

        raise AssertionError(

            "What-If result is empty."

        )


    return result


# ============================================================
# MAIN PIPELINE CONTRACT
# ============================================================

def validate_main_pipeline(
    result: Dict[str, Any]
) -> None:

    required = [

        "race_state",

        "strategy_engineer",

        "alternatives",

        "pit_window",

        "explanation",

    ]


    missing = [

        field

        for field in required

        if field not in result

    ]


    if missing:

        raise AssertionError(

            "Main strategy result missing: "
            +
            ", ".join(
                missing
            )

        )


    for field in required:

        if not isinstance(
            result[
                field
            ],
            dict
        ):

            raise AssertionError(

                f"{field} must be a dictionary."

            )


# ============================================================
# RACE STATE REGRESSION
# ============================================================

def validate_race_state(
    result: Dict[str, Any]
) -> None:

    state = safe_dict(

        result.get(
            "race_state"
        )

    )


    expected = {

        "Driver":
            "LEC",

        "CurrentLap":
            32,

        "TotalLaps":
            53,

        "Position":
            4,

        "TyreCompound":
            "MEDIUM",

    }


    for key, value in expected.items():

        if (
            state.get(
                key
            )
            !=
            value
        ):

            raise AssertionError(

                f"Race-state regression detected for {key}. "
                f"Expected {value}, received {state.get(key)}."

            )


# ============================================================
# EXPLANATION REGRESSION
# ============================================================

def validate_explanation(
    result: Dict[str, Any]
) -> None:

    explanation = safe_dict(

        result.get(
            "explanation"
        )

    )


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

            "Final recommendation is missing."

        )


    confidence = (

        explanation.get(
            "confidence"
        )

        if explanation.get(
            "confidence"
        )
        is not None

        else

        explanation.get(
            "engineer_confidence"
        )

    )


    if confidence is None:

        raise AssertionError(

            "Confidence value is missing."

        )


    risk = (

        explanation.get(
            "risk_level"
        )

        or

        explanation.get(
            "strategic_risk"
        )

    )


    if not risk:

        raise AssertionError(

            "Risk classification is missing."

        )


# ============================================================
# ALTERNATIVES REGRESSION
# ============================================================

def validate_alternatives(
    result: Dict[str, Any]
) -> None:

    alternatives_data = safe_dict(

        result.get(
            "alternatives"
        )

    )


    alternatives = (

        alternatives_data.get(
            "alternatives"
        )

        or

        alternatives_data.get(
            "strategies"
        )

        or

        alternatives_data.get(
            "ranked_strategies"
        )

    )


    if not isinstance(
        alternatives,
        list
    ):

        raise AssertionError(

            "Strategy alternatives list missing."

        )


    if len(
        alternatives
    ) < 2:

        raise AssertionError(

            "Too few strategy alternatives returned."

        )


# ============================================================
# PIT WINDOW REGRESSION
# ============================================================

def validate_pit_window(
    result: Dict[str, Any]
) -> None:

    pit = safe_dict(

        result.get(
            "pit_window"
        )

    )


    urgency = (

        pit.get(
            "pit_urgency"
        )

        if pit.get(
            "pit_urgency"
        )
        is not None

        else

        pit.get(
            "PitUrgency"
        )

    )


    if urgency is None:

        raise AssertionError(

            "Pit urgency is missing."

        )


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

            "Pit urgency is outside valid range."

        )


# ============================================================
# WHAT-IF REGRESSION
# ============================================================

def validate_what_if(
    result: Dict[str, Any]
) -> None:

    validate_scenario_comparison_contract(

        result

    )


    if (
        result.get(
            "scenario_count"
        )
        !=
        5
    ):

        raise AssertionError(

            "Default scenario count changed."

        )


    scenarios = result.get(
        "scenarios"
    )


    if not isinstance(
        scenarios,
        list
    ):

        raise AssertionError(

            "Scenario results must be a list."

        )


    stability = safe_dict(

        result.get(
            "decision_stability"
        )

    )


    stability_percentage = float(

        stability.get(
            "stability_percentage"
        )

    )


    if not (
        0
        <=
        stability_percentage
        <=
        100
    ):

        raise AssertionError(

            "Decision stability is outside valid range."

        )


# ============================================================
# CROSS-ENDPOINT CONSISTENCY
# ============================================================

def validate_cross_endpoint_consistency(
    strategy_result: Dict[str, Any],
    what_if_result: Dict[str, Any]
) -> None:

    explanation = safe_dict(

        strategy_result.get(
            "explanation"
        )

    )


    main_recommendation = (

        explanation.get(
            "final_recommendation"
        )

        or

        explanation.get(
            "recommendation"
        )

    )


    base_decision = safe_dict(

        what_if_result.get(
            "base_decision"
        )

    )


    what_if_recommendation = (

        base_decision.get(
            "recommendation"
        )

    )


    if (
        main_recommendation
        !=
        what_if_recommendation
    ):

        raise AssertionError(

            "Main Strategy and What-If base recommendation differ."

        )


# ============================================================
# DETERMINISTIC REPEATABILITY
# ============================================================

def validate_repeatability(
    first_result: Dict[str, Any],
    second_result: Dict[str, Any]
) -> None:

    first_explanation = safe_dict(

        first_result.get(
            "explanation"
        )

    )


    second_explanation = safe_dict(

        second_result.get(
            "explanation"
        )

    )


    fields = [

        "final_recommendation",

        "recommended_tyre",

        "risk_level",

    ]


    for field in fields:

        first = (

            first_explanation.get(
                field
            )

        )


        second = (

            second_explanation.get(
                field
            )

        )


        if (
            first
            !=
            second
        ):

            raise AssertionError(

                f"Repeatability regression detected for {field}."

            )


# ============================================================
# INVALID INPUT REGRESSION
# ============================================================

def validate_invalid_input(
    client
) -> None:

    invalid_cases = [

        {},


        {
            **BASE_RACE_INPUT,

            "current_lap":
                60,

        },


        {
            **BASE_RACE_INPUT,

            "position":
                21,

        },


        {
            **BASE_RACE_INPUT,

            "tyre_compound":
                "INVALID",

        },


        {
            **BASE_RACE_INPUT,

            "safety_car":
                True,

            "virtual_safety_car":
                True,

        },

    ]


    for index, payload in enumerate(
        invalid_cases,
        start=1
    ):

        response = client.post(

            STRATEGY_ENDPOINT,

            json=payload

        )


        if (
            response.status_code
            ==
            200
        ):

            result = response.get_json()


            if (
                isinstance(
                    result,
                    dict
                )
                and
                str(
                    result.get(
                        "status",
                        ""
                    )
                ).upper()
                ==
                "ERROR"
            ):

                continue


            raise AssertionError(

                f"Invalid input case {index} was accepted."

            )


# ============================================================
# MAIN
# ============================================================

def main():

    heading(

        "F1 AI STRATEGIST\n"
        "PHASE 7.10.7 — FINAL REGRESSION VERIFICATION"

    )


    client = create_client()


    # ========================================================
    # 1 / 14
    # ========================================================

    print(

        "\n[1/14] Validating API route registration..."

    )


    validate_routes()


    success(

        "Strategy and What-If routes registered."

    )


    # ========================================================
    # 2 / 14
    # ========================================================

    print(

        "\n[2/14] Running main Strategy Engineer pipeline..."

    )


    strategy_payload = run_strategy(

        client

    )


    strategy_result = (

        extract_strategy_result(
            strategy_payload
        )

    )


    success(

        "Main Strategy Engineer pipeline operational."

    )


    # ========================================================
    # 3 / 14
    # ========================================================

    print(

        "\n[3/14] Validating complete strategy contract..."

    )


    validate_main_pipeline(

        strategy_result

    )


    success(

        "Main pipeline contract preserved."

    )


    # ========================================================
    # 4 / 14
    # ========================================================

    print(

        "\n[4/14] Checking race-state regression..."

    )


    validate_race_state(

        strategy_result

    )


    success(

        "Race-state behaviour preserved."

    )


    # ========================================================
    # 5 / 14
    # ========================================================

    print(

        "\n[5/14] Checking strategy alternatives regression..."

    )


    validate_alternatives(

        strategy_result

    )


    success(

        "Strategy alternatives preserved."

    )


    # ========================================================
    # 6 / 14
    # ========================================================

    print(

        "\n[6/14] Checking pit-window regression..."

    )


    validate_pit_window(

        strategy_result

    )


    success(

        "Pit-window behaviour preserved."

    )


    # ========================================================
    # 7 / 14
    # ========================================================

    print(

        "\n[7/14] Checking explanation regression..."

    )


    validate_explanation(

        strategy_result

    )


    success(

        "Explanation and confidence layer preserved."

    )


    # ========================================================
    # 8 / 14
    # ========================================================

    print(

        "\n[8/14] Running What-If scenario pipeline..."

    )


    what_if_payload = run_what_if(

        client

    )


    what_if_result = (

        extract_what_if_result(
            what_if_payload
        )

    )


    success(

        "What-If scenario pipeline operational."

    )


    # ========================================================
    # 9 / 14
    # ========================================================

    print(

        "\n[9/14] Validating What-If regression contract..."

    )


    validate_what_if(

        what_if_result

    )


    success(

        "What-If scenario contract preserved."

    )


    # ========================================================
    # 10 / 14
    # ========================================================

    print(

        "\n[10/14] Checking decision stability output..."

    )


    stability = safe_dict(

        what_if_result.get(
            "decision_stability"
        )

    )


    if not stability.get(
        "classification"
    ):

        raise AssertionError(

            "Decision stability classification missing."

        )


    success(

        "Decision stability output preserved."

    )


    # ========================================================
    # 11 / 14
    # ========================================================

    print(

        "\n[11/14] Checking cross-endpoint consistency..."

    )


    validate_cross_endpoint_consistency(

        strategy_result,

        what_if_result

    )


    success(

        "Main and What-If recommendations are consistent."

    )


    # ========================================================
    # 12 / 14
    # ========================================================

    print(

        "\n[12/14] Testing deterministic repeatability..."

    )


    repeat_payload = run_strategy(

        client

    )


    repeat_result = (

        extract_strategy_result(
            repeat_payload
        )

    )


    validate_repeatability(

        strategy_result,

        repeat_result

    )


    success(

        "Repeated identical race state remains deterministic."

    )


    # ========================================================
    # 13 / 14
    # ========================================================

    print(

        "\n[13/14] Re-running invalid-input regression tests..."

    )


    validate_invalid_input(

        client

    )


    success(

        "Invalid race states remain safely rejected."

    )


    # ========================================================
    # 14 / 14
    # ========================================================

    print(

        "\n[14/14] Performing final Phase 7.10 integration check..."

    )


    base_decision = safe_dict(

        what_if_result.get(
            "base_decision"
        )

    )


    most_sensitive = safe_dict(

        what_if_result.get(
            "most_sensitive_scenario"
        )

    )


    if not base_decision:

        raise AssertionError(

            "What-If base decision missing."

        )


    if not most_sensitive:

        raise AssertionError(

            "Most-sensitive scenario missing."

        )


    success(

        "Complete frontend integration contract verified."

    )


    # ========================================================
    # FINAL SYSTEM SUMMARY
    # ========================================================

    heading(

        "PHASE 7.10.7 — FINAL SYSTEM REGRESSION RESULT"

    )


    print(

        f"Recommendation:             "
        f"{base_decision.get('recommendation')}"

    )


    print(

        f"Recommended Tyre:           "
        f"{base_decision.get('recommended_tyre')}"

    )


    print(

        f"Confidence:                 "
        f"{base_decision.get('confidence')}%"

    )


    print(

        f"Decision Stability:         "
        f"{stability.get('stability_percentage')}%"

    )


    print(

        f"Stability Classification:   "
        f"{stability.get('classification')}"

    )


    print(

        f"Most Sensitive Scenario:    "
        f"{most_sensitive.get('scenario')}"

    )


    print(

        f"Maximum Sensitivity:        "
        f"{most_sensitive.get('sensitivity_score')}/100"

    )


    # ========================================================
    # FINAL VERIFICATION TABLE
    # ========================================================

    heading(

        "PHASE 7.10.7 VERIFICATION RESULTS"

    )


    checks = [

        (
            "Strategy API Registration",
            True
        ),

        (
            "What-If API Registration",
            True
        ),

        (
            "Main Strategy Pipeline",
            True
        ),

        (
            "Race-State Contract",
            True
        ),

        (
            "Strategy Alternatives",
            True
        ),

        (
            "Pit Window",
            True
        ),

        (
            "Explanation & Confidence",
            True
        ),

        (
            "What-If Scenario Pipeline",
            True
        ),

        (
            "Scenario Contract",
            True
        ),

        (
            "Decision Stability",
            True
        ),

        (
            "Cross-Endpoint Consistency",
            True
        ),

        (
            "Deterministic Repeatability",
            True
        ),

        (
            "Invalid Input Safety",
            True
        ),

        (
            "Frontend Integration Contract",
            True
        ),

    ]


    for label, passed in checks:

        print(

            f"{label:<44}"
            f"{'✅' if passed else '❌'}"

        )


    print()


    print(

        "🏁 PHASE 7.10.7 FINAL REGRESSION PASSED"

    )


    print(
        LINE
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()