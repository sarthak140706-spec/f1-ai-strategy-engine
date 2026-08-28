"""
F1 AI STRATEGIST
PHASE 7.6 — STRATEGY ENGINEER FLASK API TEST
"""


from __future__ import annotations


from api.app import app


# ============================================================
# TEST PAYLOAD
# ============================================================

VALID_PAYLOAD = {

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

    "tyre_compound":
        "MEDIUM",

    "tyre_age":
        19.0,

    "pit_stops":
        1,

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

    "track_status":
        "GREEN",

    "safety_car":
        False,

    "virtual_safety_car":
        False,

    "weather":
        "DRY",

    "wet_conditions":
        False,

    "rainfall":
        0.0,

}


# ============================================================
# SECTION
# ============================================================

def section(
    number: str,
    title: str
) -> None:

    print(
        f"\n[{number}] {title}"
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print(
        "\n" + "=" * 88
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.6 — STRATEGY ENGINEER FLASK API TEST"
    )

    print(
        "=" * 88
    )


    client = app.test_client()


    # ========================================================
    # 1. ROOT ENDPOINT
    # ========================================================

    section(
        "1/8",
        "Testing Strategy Engineer API root..."
    )


    response = client.get(
        "/api/engineer/"
    )


    assert (
        response.status_code
        ==
        200
    )


    root_data = (
        response.get_json()
    )


    assert (
        root_data[
            "status"
        ]
        ==
        "SUCCESS"
    )


    assert (
        root_data[
            "phase"
        ]
        ==
        "7.6"
    )


    print(
        "✅ Strategy Engineer API root available."
    )


    # ========================================================
    # 2. HEALTH
    # ========================================================

    section(
        "2/8",
        "Testing Phase 7.6 health endpoint..."
    )


    response = client.get(
        "/api/engineer/health"
    )


    assert (
        response.status_code
        ==
        200
    )


    health = (
        response.get_json()
    )


    assert (
        health[
            "data"
        ][
            "operational"
        ]
        is True
    )


    assert (
        health[
            "data"
        ][
            "live_timing_required"
        ]
        is False
    )


    print(
        "✅ Phase 7.6 API health validated."
    )


    # ========================================================
    # 3. RACE STATE ENDPOINT
    # ========================================================

    section(
        "3/8",
        "Testing manual race-state endpoint..."
    )


    response = client.post(

        "/api/engineer/race-state",

        json=
            VALID_PAYLOAD

    )


    assert (
        response.status_code
        ==
        200
    )


    race_response = (
        response.get_json()
    )


    race_state = (
        race_response[
            "data"
        ][
            "race_state"
        ]
    )


    assert (
        race_state[
            "Driver"
        ]
        ==
        "LEC"
    )


    assert (
        race_state[
            "CurrentLap"
        ]
        ==
        32
    )


    assert (
        race_state[
            "TotalLaps"
        ]
        ==
        53
    )


    assert (
        race_state[
            "TyreCompound"
        ]
        ==
        "MEDIUM"
    )


    print(
        "✅ Phase 7.1 race state exposed through API."
    )


    # ========================================================
    # 4. COMPLETE ANALYSIS
    # ========================================================

    section(
        "4/8",
        "Running complete Strategy Engineer API..."
    )


    response = client.post(

        "/api/engineer/analyse",

        json=
            VALID_PAYLOAD

    )


    assert (
        response.status_code
        ==
        200
    )


    analysis = (
        response.get_json()
    )


    assert (
        analysis[
            "status"
        ]
        ==
        "SUCCESS"
    )


    result = (
        analysis[
            "data"
        ][
            "result"
        ]
    )


    print(
        "✅ Complete Strategy Engineer API executed."
    )


    # ========================================================
    # 5. PIPELINE
    # ========================================================

    section(
        "5/8",
        "Validating Phase 7 pipeline..."
    )


    pipeline = (
        result[
            "pipeline"
        ]
    )


    for phase in [

        "phase_7_1",

        "phase_7_2",

        "phase_7_3",

        "phase_7_4",

        "phase_7_5",

        "phase_7_6",

    ]:

        assert (
            pipeline[
                phase
            ]
            is True
        )


    print(
        "✅ 7.1 → 7.6 API pipeline validated."
    )


    # ========================================================
    # 6. STRATEGY RESULTS
    # ========================================================

    section(
        "6/8",
        "Validating strategy-engineer results..."
    )


    assert (
        result[
            "strategy_engineer"
        ]
    )


    assert (
        result[
            "alternatives"
        ]
    )


    assert (
        result[
            "pit_window"
        ]
    )


    assert (
        result[
            "explanation"
        ]
    )


    explanation = (
        result[
            "explanation"
        ]
    )


    assert (
        explanation.get(
            "final_recommendation"
        )
        is not None
    )


    assert (
        explanation.get(
            "confidence"
        )
        is not None
    )


    print(
        "✅ Strategy results exposed successfully."
    )


    # ========================================================
    # 7. INVALID INPUT
    # ========================================================

    section(
        "7/8",
        "Testing API validation..."
    )


    invalid_payload = (
        dict(
            VALID_PAYLOAD
        )
    )


    invalid_payload[
        "current_lap"
    ] = 60


    invalid_payload[
        "total_laps"
    ] = 53


    response = client.post(

        "/api/engineer/analyse",

        json=
            invalid_payload

    )


    assert (
        response.status_code
        in {
            400,
            500
        }
    )


    error = (
        response.get_json()
    )


    assert (
        error[
            "status"
        ]
        ==
        "ERROR"
    )


    print(
        "✅ Invalid race state safely rejected."
    )


    # ========================================================
    # 8. MISSING INPUT
    # ========================================================

    section(
        "8/8",
        "Testing missing required input..."
    )


    missing_payload = (
        dict(
            VALID_PAYLOAD
        )
    )


    missing_payload.pop(
        "driver"
    )


    response = client.post(

        "/api/engineer/analyse",

        json=
            missing_payload

    )


    assert (
        response.status_code
        ==
        400
    )


    error = (
        response.get_json()
    )


    assert (
        error[
            "status"
        ]
        ==
        "ERROR"
    )


    print(
        "✅ Missing required input safely rejected."
    )


    # ========================================================
    # RESULTS
    # ========================================================

    print(
        "\n" + "=" * 88
    )

    print(
        "PHASE 7.6 VERIFICATION RESULTS"
    )

    print(
        "=" * 88
    )


    print(
        "Strategy Engineer API Root          ✅"
    )

    print(
        "API Health Endpoint                 ✅"
    )

    print(
        "7.1 Race-State Endpoint             ✅"
    )

    print(
        "7.2 Strategy Engineer               ✅"
    )

    print(
        "7.3 Strategy Alternatives           ✅"
    )

    print(
        "7.4 Pit Window Optimizer            ✅"
    )

    print(
        "7.5 Explanation Engine              ✅"
    )

    print(
        "7.6 REST API                        ✅"
    )

    print(
        "Input Validation                    ✅"
    )

    print(
        "Failure-Safe API                    ✅"
    )


    print(
        "\n🏁 PHASE 7.6 VERIFICATION PASSED"
    )


    print(
        "=" * 88
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()