"""
F1 AI STRATEGIST

PHASE 7.10.5
LOADING / ERROR / FAILURE-SAFE INTEGRATION VERIFICATION

Purpose
-------
Verify that the Strategy Engineer frontend APIs behave safely
under valid and invalid conditions.

This step tests:

1. Main Strategy Engineer endpoint
2. What-If endpoint
3. Valid request handling
4. Invalid input rejection
5. Missing field rejection
6. Invalid tyre rejection
7. Invalid race lap rejection
8. SC + VSC conflict rejection
9. What-If result contract
10. Partial frontend failure safety

IMPORTANT
---------
This test does not modify any Phase 7 strategy logic.

It only verifies that the frontend-facing API layer is safe
and reliable before final browser testing.
"""


from __future__ import annotations


from copy import deepcopy

from typing import Any, Dict


# ============================================================
# FLASK APPLICATION
# ============================================================

from api.app import app


# ============================================================
# PHASE 7.8 CONTRACT
# ============================================================

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


# ============================================================
# VERIFIED BASE RACE INPUT
# ============================================================

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
# DISPLAY HELPERS
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


# ============================================================
# SAFE HELPERS
# ============================================================

def safe_dict(
    value: Any
) -> Dict[str, Any]:

    if isinstance(
        value,
        dict
    ):

        return value


    return {}


def assert_error_response(
    response,
    expected_statuses=(
        400,
        422
    )
) -> Dict[str, Any]:

    """
    Verify that an invalid request is rejected safely.
    """

    if (
        response.status_code
        not in
        expected_statuses
    ):

        raise AssertionError(

            "Expected validation failure, "
            f"received HTTP {response.status_code}."

        )


    payload = response.get_json()


    if not isinstance(
        payload,
        dict
    ):

        raise AssertionError(

            "Error response must be JSON."

        )


    status = str(

        payload.get(
            "status",
            ""
        )

    ).upper()


    if status != "ERROR":

        raise AssertionError(

            "Error response must contain "
            "status='ERROR'."

        )


    error = safe_dict(

        payload.get(
            "error"
        )

    )


    if not error.get(
        "message"
    ):

        raise AssertionError(

            "Error response does not contain "
            "a user-readable message."

        )


    return payload


# ============================================================
# CREATE CLIENT
# ============================================================

def create_client():

    app.config[
        "TESTING"
    ] = True


    return app.test_client()


# ============================================================
# MAIN
# ============================================================

def main():

    heading(

        "F1 AI STRATEGIST\n"
        "PHASE 7.10.5 — LOADING & FAILURE-SAFE INTEGRATION TEST"

    )


    client = create_client()


    # ========================================================
    # 1 / 10
    # MAIN STRATEGY ENDPOINT
    # ========================================================

    print(

        "\n[1/10] Testing main Strategy Engineer endpoint..."

    )


    strategy_response = client.post(

        STRATEGY_ENDPOINT,

        json=deepcopy(
            BASE_RACE_INPUT
        )

    )


    if (
        strategy_response.status_code
        !=
        200
    ):

        raise AssertionError(

            "Main Strategy Engineer endpoint failed. "
            f"HTTP {strategy_response.status_code}: "
            f"{strategy_response.get_json()}"

        )


    strategy_payload = (
        strategy_response.get_json()
    )


    if (
        strategy_payload.get(
            "status"
        )
        !=
        "SUCCESS"
    ):

        raise AssertionError(

            "Main Strategy Engineer did not "
            "return SUCCESS."

        )


    success(

        "Main Strategy Engineer endpoint operational."

    )


    # ========================================================
    # 2 / 10
    # WHAT-IF ENDPOINT
    # ========================================================

    print(

        "\n[2/10] Testing What-If Scenario endpoint..."

    )


    what_if_response = client.post(

        WHAT_IF_ENDPOINT,

        json=deepcopy(
            BASE_RACE_INPUT
        )

    )


    if (
        what_if_response.status_code
        !=
        200
    ):

        raise AssertionError(

            "What-If endpoint failed. "
            f"HTTP {what_if_response.status_code}: "
            f"{what_if_response.get_json()}"

        )


    what_if_payload = (
        what_if_response.get_json()
    )


    if (
        what_if_payload.get(
            "status"
        )
        !=
        "SUCCESS"
    ):

        raise AssertionError(

            "What-If endpoint did not return SUCCESS."

        )


    success(

        "What-If Scenario endpoint operational."

    )


    # ========================================================
    # 3 / 10
    # WHAT-IF RESULT CONTRACT
    # ========================================================

    print(

        "\n[3/10] Validating What-If frontend result contract..."

    )


    what_if_data = safe_dict(

        what_if_payload.get(
            "data"
        )

    )


    what_if_result = safe_dict(

        what_if_data.get(
            "result"
        )

    )


    validate_scenario_comparison_contract(

        what_if_result

    )


    required_frontend_fields = [

        "base_decision",

        "scenario_count",

        "scenarios",

        "sensitivity_ranking",

        "most_sensitive_scenario",

        "decision_stability",

    ]


    missing = [

        field

        for field in required_frontend_fields

        if field not in what_if_result

    ]


    if missing:

        raise AssertionError(

            "What-If frontend response missing: "
            +
            ", ".join(
                missing
            )

        )


    success(

        "What-If frontend contract validated."

    )


    # ========================================================
    # 4 / 10
    # FIVE DEFAULT SCENARIOS
    # ========================================================

    print(

        "\n[4/10] Validating default scenario results..."

    )


    scenarios = what_if_result.get(
        "scenarios",
        []
    )


    if len(
        scenarios
    ) != 5:

        raise AssertionError(

            "Expected 5 default What-If scenarios, "
            f"received {len(scenarios)}."

        )


    scenario_names = {

        scenario.get(
            "name"
        )

        for scenario in scenarios

    }


    required_scenarios = {

        "HIGHER TYRE DEGRADATION",

        "SAFETY CAR",

        "UNDERCUT THREAT",

        "OLDER TYRES",

        "DAMP CONDITIONS",

    }


    if (
        scenario_names
        !=
        required_scenarios
    ):

        raise AssertionError(

            "Default What-If scenario set "
            "does not match Phase 7.8."

        )


    success(

        "Five default What-If scenarios validated."

    )


    # ========================================================
    # 5 / 10
    # MISSING FIELD
    # ========================================================

    print(

        "\n[5/10] Testing missing required field handling..."

    )


    invalid_input = deepcopy(
        BASE_RACE_INPUT
    )


    invalid_input.pop(
        "driver"
    )


    response = client.post(

        STRATEGY_ENDPOINT,

        json=invalid_input

    )


    assert_error_response(
        response
    )


    success(

        "Missing driver safely rejected."

    )


    # ========================================================
    # 6 / 10
    # INVALID LAP
    # ========================================================

    print(

        "\n[6/10] Testing invalid lap handling..."

    )


    invalid_input = deepcopy(
        BASE_RACE_INPUT
    )


    invalid_input[
        "current_lap"
    ] = 60


    invalid_input[
        "total_laps"
    ] = 53


    response = client.post(

        STRATEGY_ENDPOINT,

        json=invalid_input

    )


    assert_error_response(
        response
    )


    success(

        "Current lap greater than total laps safely rejected."

    )


    # ========================================================
    # 7 / 10
    # INVALID TYRE
    # ========================================================

    print(

        "\n[7/10] Testing invalid tyre handling..."

    )


    invalid_input = deepcopy(
        BASE_RACE_INPUT
    )


    invalid_input[
        "tyre_compound"
    ] = "WOOD"


    response = client.post(

        STRATEGY_ENDPOINT,

        json=invalid_input

    )


    assert_error_response(
        response
    )


    success(

        "Unsupported tyre compound safely rejected."

    )


    # ========================================================
    # 8 / 10
    # SC + VSC
    # ========================================================

    print(

        "\n[8/10] Testing conflicting race-control state..."

    )


    invalid_input = deepcopy(
        BASE_RACE_INPUT
    )


    invalid_input[
        "safety_car"
    ] = True


    invalid_input[
        "virtual_safety_car"
    ] = True


    response = client.post(

        STRATEGY_ENDPOINT,

        json=invalid_input

    )


    assert_error_response(
        response
    )


    success(

        "Simultaneous Safety Car and VSC safely rejected."

    )


    # ========================================================
    # 9 / 10
    # WHAT-IF FAILURE-SAFE VALIDATION
    # ========================================================

    print(

        "\n[9/10] Testing What-If validation safety..."

    )


    invalid_input = deepcopy(
        BASE_RACE_INPUT
    )


    invalid_input[
        "scenarios"
    ] = "INVALID"


    response = client.post(

        WHAT_IF_ENDPOINT,

        json=invalid_input

    )


    assert_error_response(
        response
    )


    success(

        "Invalid What-If scenario payload safely rejected."

    )


    # ========================================================
    # 10 / 10
    # FRONTEND PARTIAL FAILURE CONTRACT
    # ========================================================

    print(

        "\n[10/10] Validating partial-failure frontend contract..."

    )


    strategy_data = safe_dict(

        strategy_payload.get(
            "data"
        )

    )


    main_result = safe_dict(

        strategy_data.get(
            "result"
        )

    )


    if not main_result:

        raise AssertionError(

            "Main Strategy result is empty."

        )


    if not what_if_result:

        raise AssertionError(

            "What-If result is empty."

        )


    


    success(

        "Primary strategy and What-If results are independently accessible."

    )


    # ========================================================
    # FINAL INFORMATION
    # ========================================================

    stability = safe_dict(

        what_if_result.get(
            "decision_stability"
        )

    )


    most_sensitive = safe_dict(

        what_if_result.get(
            "most_sensitive_scenario"
        )

    )


    base_decision = safe_dict(

        what_if_result.get(
            "base_decision"
        )

    )


    heading(

        "PHASE 7.10.5 — FRONTEND INTEGRATION RESULT"

    )


    print(

        f"Base Recommendation:       "
        f"{base_decision.get('recommendation')}"

    )


    print(

        f"Recommended Tyre:          "
        f"{base_decision.get('recommended_tyre')}"

    )


    print(

        f"Confidence:                "
        f"{base_decision.get('confidence')}%"

    )


    print(

        f"What-If Scenarios:         "
        f"{what_if_result.get('scenario_count')}"

    )


    print(

        f"Decision Stability:        "
        f"{stability.get('stability_percentage')}%"

    )


    print(

        f"Stability Classification:  "
        f"{stability.get('classification')}"

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
    # SUMMARY
    # ========================================================

    heading(

        "PHASE 7.10.5 VERIFICATION RESULTS"

    )


    checks = [

        (
            "Main Strategy API",
            True
        ),

        (
            "What-If API",
            True
        ),

        (
            "What-If Frontend Contract",
            True
        ),

        (
            "Default Scenario Generation",
            True
        ),

        (
            "Missing Input Handling",
            True
        ),

        (
            "Invalid Lap Handling",
            True
        ),

        (
            "Invalid Tyre Handling",
            True
        ),

        (
            "SC / VSC Conflict Handling",
            True
        ),

        (
            "What-If Validation",
            True
        ),

        (
            "Partial Failure Safety",
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

            f"{label:<42}"
            f"{status}"

        )


    print()


    print(

        "🏁 PHASE 7.10.5 VERIFICATION PASSED"

    )


    print(
        LINE
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()