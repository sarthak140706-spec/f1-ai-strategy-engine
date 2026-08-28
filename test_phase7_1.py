"""
F1 AI STRATEGIST
PHASE 7.1 — MANUAL RACE-STATE BUILDER TEST
"""


from src.strategy_engineer.race_state_builder import (
    RaceStateValidationError,
    build_manual_race_state,
    display_manual_race_state,
    normalise_tyre,
    normalise_track_status,
    normalise_weather,
)


# ============================================================
# VALID TEST INPUT
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
# TEST ERROR
# ============================================================

def expect_validation_error(
    race_input,
    description
):

    try:

        build_manual_race_state(
            race_input
        )

    except RaceStateValidationError:

        print(
            f"✅ Rejected invalid input: {description}"
        )

        return


    raise AssertionError(

        f"Expected validation error: {description}"

    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.1 — MANUAL RACE-STATE BUILDER TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # 1
    # ========================================================

    print(
        "\n[1/7] Building manual race state..."
    )


    race_state = build_manual_race_state(
        TEST_INPUT
    )


    assert isinstance(
        race_state,
        dict
    )

    assert race_state


    print(
        "✅ Manual race state created."
    )


    # ========================================================
    # 2
    # ========================================================

    print(
        "\n[2/7] Validating race information..."
    )


    assert race_state[
        "Driver"
    ] == "LEC"


    assert race_state[
        "Circuit"
    ] == "Monza"


    assert race_state[
        "CurrentLap"
    ] == 32


    assert race_state[
        "TotalLaps"
    ] == 53


    assert race_state[
        "LapsRemaining"
    ] == 21


    assert race_state[
        "Position"
    ] == 4


    print(
        "✅ Race information validated."
    )


    # ========================================================
    # 3
    # ========================================================

    print(
        "\n[3/7] Validating tyre state..."
    )


    assert race_state[
        "TyreCompound"
    ] == "MEDIUM"


    assert race_state[
        "TyreAge"
    ] == 19.0


    assert race_state[
        "TyreCondition"
    ] == "WORN"


    assert race_state[
        "PitStopsCompleted"
    ] == 1


    print(
        "✅ Tyre state validated."
    )


    # ========================================================
    # 4
    # ========================================================

    print(
        "\n[4/7] Validating derived race features..."
    )


    assert race_state[
        "RaceProgress"
    ] == round(
        32 / 53,
        4
    )


    assert race_state[
        "RacePhase"
    ] == "MIDDLE"


    assert race_state[
        "WetConditions"
    ] is False


    assert race_state[
        "SafetyCar"
    ] is False


    assert race_state[
        "VirtualSafetyCar"
    ] is False


    print(
        "✅ Derived race features validated."
    )


    # ========================================================
    # 5
    # ========================================================

    print(
        "\n[5/7] Validating input normalisation..."
    )


    assert normalise_tyre(
        "m"
    ) == "MEDIUM"


    assert normalise_tyre(
        "inter"
    ) == "INTERMEDIATE"


    assert normalise_track_status(
        "SC"
    ) == "SAFETY_CAR"


    assert normalise_track_status(
        "virtual safety car"
    ) == "VSC"


    assert normalise_weather(
        "light rain"
    ) == "DAMP"


    print(
        "✅ Input normalisation validated."
    )


    # ========================================================
    # 6
    # ========================================================

    print(
        "\n[6/7] Testing invalid race situations..."
    )


    invalid = dict(
        TEST_INPUT
    )

    invalid[
        "current_lap"
    ] = 70


    expect_validation_error(

        invalid,

        "current lap greater than total laps"

    )


    invalid = dict(
        TEST_INPUT
    )

    invalid[
        "position"
    ] = -4


    expect_validation_error(

        invalid,

        "invalid race position"

    )


    invalid = dict(
        TEST_INPUT
    )

    invalid[
        "current_tyre"
    ] = "BANANA"


    expect_validation_error(

        invalid,

        "unsupported tyre compound"

    )


    invalid = dict(
        TEST_INPUT
    )

    invalid[
        "tyre_age"
    ] = -10


    expect_validation_error(

        invalid,

        "negative tyre age"

    )


    invalid = dict(
        TEST_INPUT
    )

    invalid[
        "driver"
    ] = ""


    expect_validation_error(

        invalid,

        "missing driver"

    )


    invalid = dict(
        TEST_INPUT
    )

    invalid[
        "safety_car"
    ] = True

    invalid[
        "virtual_safety_car"
    ] = True


    expect_validation_error(

        invalid,

        "SC and VSC simultaneously active"

    )


    print(
        "✅ Invalid race situations rejected."
    )


    # ========================================================
    # 7
    # ========================================================

    print(
        "\n[7/7] Validating Phase 7.1 contract..."
    )


    assert race_state[
        "Phase"
    ] == "7.1"


    assert race_state[
        "Source"
    ] == "MANUAL"


    assert race_state[
        "ManualData"
    ] is True


    assert race_state[
        "LiveData"
    ] is False


    assert race_state[
        "Component"
    ] == "manual_race_state_builder"


    print(
        "✅ Phase 7.1 race-state contract validated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_manual_race_state(
        race_state
    )


    # ========================================================
    # RESULT
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "PHASE 7.1 VERIFICATION RESULTS"
    )

    print(
        "=" * 78
    )


    print(
        "Manual Race-State Builder       ✅"
    )

    print(
        "Input Validation                ✅"
    )

    print(
        "Driver/Circuit Support          ✅"
    )

    print(
        "Tyre Normalisation              ✅"
    )

    print(
        "Race Feature Calculation        ✅"
    )

    print(
        "Weather/Track State             ✅"
    )

    print(
        "Failure-Safe Validation         ✅"
    )


    print(
        "\n🏁 PHASE 7.1 VERIFICATION PASSED"
    )


    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()