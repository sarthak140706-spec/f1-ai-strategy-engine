"""
F1 AI STRATEGIST
PHASE 5.2 — DYNAMIC STRATEGY API TEST
"""


import json


from src.api.dynamic_strategy_api import (
    get_dynamic_strategy,
    display_dynamic_strategy_api
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 76
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 5.2 — DYNAMIC STRATEGY API TEST"
    )

    print(
        "=" * 76
    )


    # ========================================================
    # STEP 1
    # EXECUTE API SERVICE
    # ========================================================

    print(
        "\n[1/3] Executing dynamic strategy API..."
    )


    result = get_dynamic_strategy(
        season=SEASON,
        grand_prix=GRAND_PRIX,
        driver=DRIVER,
        lap=TARGET_LAP
    )


    assert result, (
        "Phase 5.2 API returned no result."
    )


    print(
        "✅ Dynamic strategy API executed."
    )


    # ========================================================
    # STEP 2
    # DISPLAY RESPONSE
    # ========================================================

    print(
        "\n[2/3] Displaying API response..."
    )


    display_dynamic_strategy_api(
        result
    )


    # ========================================================
    # STEP 3
    # VALIDATION
    # ========================================================

    print(
        "\n[3/3] Validating API response..."
    )


    assert (
        result.get("api")
        == "dynamic_strategy"
    )

    print(
        "✅ API identifier validated."
    )


    assert (
        result.get("phase")
        == "5.2"
    )

    print(
        "✅ Phase metadata validated."
    )


    assert (
        result.get("status")
        == "SUCCESS"
    )

    print(
        "✅ API status validated."
    )


    # ========================================================
    # REQUEST
    # ========================================================

    request = result.get(
        "request",
        {}
    )


    assert (
        request.get("season")
        == SEASON
    )


    assert (
        request.get("grand_prix")
        == GRAND_PRIX
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
        "✅ API request metadata validated."
    )


    # ========================================================
    # RACE DATA
    # ========================================================

    race = result.get(
        "race",
        {}
    )


    assert (
        race.get("driver")
        == DRIVER
    )


    assert (
        int(race.get("lap"))
        == TARGET_LAP
    )


    assert (
        race.get("total_laps")
        is not None
    )


    assert (
        race.get("laps_remaining")
        is not None
    )


    assert (
        race.get("position")
        is not None
    )


    assert (
        race.get("current_tyre")
        is not None
    )


    print(
        "✅ Dynamic race context validated."
    )


    # ========================================================
    # STRATEGIC STATE
    # ========================================================

    strategy_state = result.get(
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
        "✅ Strategic state validated."
    )


    # ========================================================
    # AI RECOMMENDATION
    # ========================================================

    recommendation = result.get(
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
        "✅ AI recommendation validated."
    )


    # ========================================================
    # SIMULATION
    # ========================================================

    assert (
        result.get(
            "simulation"
        )
    )


    print(
        "✅ Strategy simulation available."
    )


    # ========================================================
    # SCORING
    # ========================================================

    assert (
        result.get(
            "scoring"
        )
    )


    print(
        "✅ Strategy scoring available."
    )


    # ========================================================
    # JSON SERIALIZATION
    # ========================================================

    json_output = json.dumps(
        result
    )


    assert json_output


    print(
        "✅ Complete response is JSON serializable."
    )


    # ========================================================
    # EXPECTED BAHRAIN TEST
    # ========================================================

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
        "✅ Bahrain lap-35 recommendation preserved."
    )


    # ========================================================
    # PHASE 5.1 → 5.2 CONNECTION
    # ========================================================

    assert (
        float(
            recommendation.get(
                "confidence"
            )
        )
        >= 0
    )


    assert (
        float(
            recommendation.get(
                "confidence"
            )
        )
        <= 100
    )


    print(
        "✅ Phase 5.1 → Phase 5.2 connection validated."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 76
    )

    print(
        "✅ PHASE 5.2 DYNAMIC STRATEGY API TEST PASSED"
    )

    print(
        "=" * 76
    )


if __name__ == "__main__":

    main()