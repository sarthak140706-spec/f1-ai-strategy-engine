"""
Sprint 5 Edge Case Validation

Tests Race Situation Awareness modules:

1. Undercut scenario
2. Overcut scenario
3. Race Context Scoring
"""


from src.strategy.undercut_overcut import (
    analyse_undercut_overcut
)

from src.strategy.context_score import (
    calculate_race_context_score
)



# ============================================================
# TEST 1 - UNDERCUT SCENARIO
# ============================================================

def test_undercut_scenario():

    print("\n" + "=" * 70)

    print(
        "TEST 1: UNDERCUT SCENARIO"
    )

    print("=" * 70)


    race_state = {

        "GapAhead": 1.5,

        "GapBehind": 4.0,

        "CurrentTyreAge": 20,

        "OpponentTyreAge": 35,

        "TyreDegRate": 0.07,

        "FreshTyreBonus": 1.6,

        "PitLoss": 22,

        "TrafficRisk": "Low",

        "RemainingLaps": 20

    }


    result = analyse_undercut_overcut(
        race_state
    )


    print(result)


    assert result[
        "RecommendedAction"
    ] == "UNDERCUT"


    print(
        "✓ Undercut detection passed"
    )



# ============================================================
# TEST 2 - OVERCUT SCENARIO
# ============================================================

def test_overcut_scenario():

    print("\n" + "=" * 70)

    print(
        "TEST 2: OVERCUT SCENARIO"
    )

    print("=" * 70)


    race_state = {

        "GapAhead": 8.0,

        "GapBehind": 7.0,

        "CurrentTyreAge": 15,

        "OpponentTyreAge": 25,

        "TyreDegRate": 0.03,

        "FreshTyreBonus": 1.6,

        "PitLoss": 22,

        "TrafficRisk": "Low",

        "RemainingLaps": 25

    }


    result = analyse_undercut_overcut(
        race_state
    )


    print(result)


    assert result[
        "RecommendedAction"
    ] == "OVERCUT"


    print(
        "✓ Overcut detection passed"
    )



# ============================================================
# TEST 3 - RACE CONTEXT SCORE
# ============================================================

def test_context_score():

    print("\n" + "=" * 70)

    print(
        "TEST 3: RACE CONTEXT SCORE"
    )

    print("=" * 70)


    race_context = {

        "SafetyCar": False,

        "VSC": False,

        "WeatherFactor": 0.5,

        "TrafficRisk": "Low",

        "GapAhead": 1.8,

        "GapBehind": 6.0,

        "UndercutScore": 75,

        "OvercutScore": 55

    }


    result = calculate_race_context_score(
        race_context
    )


    print(result)


    assert result[
        "RaceContextScore"
    ] >= 0


    assert result[
        "Situation"
    ] in [

        "HIGHLY_FAVOURABLE",

        "FAVOURABLE",

        "NEUTRAL",

        "UNFAVOURABLE"

    ]


    assert result[
        "Confidence"
    ] in [

        "HIGH",

        "MEDIUM",

        "LOW"

    ]


    print(
        "✓ Context scoring passed"
    )



# ============================================================
# COMPLETE TEST RUNNER
# ============================================================

def run_edge_case_validation():

    print(
        "\n"
        + "=" * 70
    )

    print(
        "V5 SPRINT 5 EDGE CASE VALIDATION"
    )

    print(
        "=" * 70
    )


    test_undercut_scenario()

    test_overcut_scenario()

    test_context_score()


    print(
        "\n"
        + "=" * 70
    )

    print(
        "🏁 ALL SPRINT 5 EDGE CASE TESTS PASSED"
    )

    print(
        "=" * 70
    )



# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    run_edge_case_validation()