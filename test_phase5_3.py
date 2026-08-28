"""
F1 AI STRATEGIST
PHASE 5.3 — FLASK DYNAMIC STRATEGY ROUTE TEST
"""


from api.app import app


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain_Grand_Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 5.3 — FLASK DYNAMIC STRATEGY ROUTE TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # STEP 1
    # CREATE FLASK TEST CLIENT
    # ========================================================

    print(
        "\n[1/4] Creating Flask test client..."
    )


    app.config[
        "TESTING"
    ] = True


    client = app.test_client()


    assert client is not None, (
        "Flask test client could not be created."
    )


    print(
        "✅ Flask test client created."
    )


    # ========================================================
    # STEP 2
    # BUILD ENDPOINT
    # ========================================================

    print(
        "\n[2/4] Building Phase 5.3 endpoint..."
    )


    endpoint = (
        f"/api/dynamic-strategy/"
        f"{SEASON}/"
        f"{GRAND_PRIX}/"
        f"{DRIVER}/"
        f"{TARGET_LAP}"
    )


    print(
        f"Endpoint: {endpoint}"
    )


    # ========================================================
    # STEP 3
    # CALL ENDPOINT
    # ========================================================

    print(
        "\n[3/4] Calling Flask dynamic strategy endpoint..."
    )


    response = client.get(
        endpoint
    )


    print(
        f"HTTP Status: "
        f"{response.status_code}"
    )


    assert (
        response.status_code
        == 200
    ), (
        f"Expected HTTP 200, "
        f"received {response.status_code}."
    )


    data = response.get_json()


    assert data is not None, (
        "Flask endpoint did not return JSON."
    )


    print(
        "✅ HTTP 200 received."
    )

    print(
        "✅ Valid JSON response received."
    )


    # ========================================================
    # STEP 4
    # VALIDATE RESPONSE
    # ========================================================

    print(
        "\n[4/4] Validating Phase 5.3 response..."
    )


    # --------------------------------------------------------
    # PHASE 5.2 METADATA
    # --------------------------------------------------------

    assert (
        data.get("api")
        == "dynamic_strategy"
    )

    print(
        "✅ Dynamic strategy API identifier validated."
    )


    assert (
        data.get("phase")
        == "5.2"
    )

    print(
        "✅ Phase 5.2 response preserved."
    )


    assert (
        data.get("status")
        == "SUCCESS"
    )

    print(
        "✅ API success status validated."
    )


    # --------------------------------------------------------
    # REQUEST
    # --------------------------------------------------------

    request = data.get(
        "request",
        {}
    )


    assert (
        request.get("season")
        == SEASON
    )


    assert (
        request.get("grand_prix")
        == "Bahrain Grand Prix"
    )


    assert (
        request.get("driver")
        == DRIVER
    )


    assert (
        request.get("lap")
        == TARGET_LAP
    )


    print(
        "✅ Flask route parameters validated."
    )


    # --------------------------------------------------------
    # RACE
    # --------------------------------------------------------

    race = data.get(
        "race",
        {}
    )


    assert (
        race.get("driver")
        == DRIVER
    )


    assert (
        int(
            race.get("lap")
        )
        == TARGET_LAP
    )


    assert (
        race.get(
            "laps_remaining"
        )
        is not None
    )


    assert (
        race.get(
            "position"
        )
        is not None
    )


    assert (
        race.get(
            "current_tyre"
        )
        is not None
    )


    print(
        "✅ Dynamic race state reached Flask successfully."
    )


    # --------------------------------------------------------
    # STRATEGY
    # --------------------------------------------------------

    strategy_state = data.get(
        "strategy_state",
        {}
    )


    assert (
        strategy_state.get(
            "race_situation"
        )
        is not None
    )


    assert (
        strategy_state.get(
            "pit_decision"
        )
        is not None
    )


    print(
        "✅ Dynamic strategy state validated."
    )


    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    recommendation = data.get(
        "recommendation",
        {}
    )


    assert (
        recommendation.get(
            "action"
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
            "confidence"
        )
        is not None
    )


    assert (
        recommendation.get(
            "dynamic_score"
        )
        is not None
    )


    assert (
        recommendation.get(
            "reasoning"
        )
    )


    print(
        "✅ AI recommendation reached Flask successfully."
    )


    # --------------------------------------------------------
    # SIMULATION + SCORING
    # --------------------------------------------------------

    assert data.get(
        "simulation"
    )


    assert data.get(
        "scoring"
    )


    print(
        "✅ Simulation and scoring data validated."
    )


    # --------------------------------------------------------
    # EXPECTED BAHRAIN RESULT
    # --------------------------------------------------------

    assert (
        recommendation.get(
            "action"
        )
        == "STAY OUT"
    )


    assert (
        recommendation.get(
            "recommended_tyre"
        )
        == "HARD"
    )


    print(
        "✅ Bahrain lap-35 behaviour preserved."
    )


    # --------------------------------------------------------
    # PIPELINE CONNECTION
    # --------------------------------------------------------

    print(
        "✅ Phase 4 → 5.1 → 5.2 → 5.3 pipeline validated."
    )


    # ========================================================
    # DISPLAY SUMMARY
    # ========================================================

    print(
        "\n" + "-" * 78
    )

    print(
        "FLASK RESPONSE SUMMARY"
    )

    print(
        "-" * 78
    )


    print(
        f"Driver: "
        f"{race.get('driver')}"
    )


    print(
        f"Lap: "
        f"{race.get('lap')}/"
        f"{race.get('total_laps')}"
    )


    print(
        f"Position: "
        f"P{race.get('position')}"
    )


    print(
        f"Tyre: "
        f"{race.get('current_tyre')}"
    )


    print(
        f"Race Situation: "
        f"{strategy_state.get('race_situation')}"
    )


    print(
        f"Pit Decision: "
        f"{strategy_state.get('pit_decision')}"
    )


    print(
        f"AI Recommendation: "
        f"{recommendation.get('action')}"
    )


    print(
        f"Recommended Tyre: "
        f"{recommendation.get('recommended_tyre')}"
    )


    print(
        f"Dynamic Score: "
        f"{recommendation.get('dynamic_score')}"
    )


    print(
        f"Confidence: "
        f"{recommendation.get('confidence')}%"
    )


    print(
        "-" * 78
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "✅ PHASE 5.3 FLASK DYNAMIC STRATEGY ROUTE TEST PASSED"
    )

    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()