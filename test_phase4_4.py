from src.data_loader import load_session

from src.strategy.dynamic_race_state import (
    build_dynamic_race_state
)

from src.strategy.dynamic_race_situation import (
    analyze_dynamic_race_situation
)

from src.strategy.dynamic_tyre_strategy import (
    generate_dynamic_tyre_strategy
)

from src.strategy.dynamic_pit_decision import (
    evaluate_dynamic_pit_decision
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# PHASE 4.4 TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 72
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 4.4 — DYNAMIC PIT-STOP DECISION ENGINE TEST"
    )

    print(
        "=" * 72
    )


    # ========================================================
    # STEP 1
    # LOAD SESSION
    # ========================================================

    print(
        "\n[1/5] Loading race session..."
    )

    session = load_session(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        session_type="R"

    )

    assert session is not None, (
        "Race session failed to load."
    )

    print(
        "✅ Race session loaded."
    )


    # ========================================================
    # STEP 2
    # DYNAMIC RACE STATE — PHASE 4.1
    # ========================================================

    print(
        "\n[2/5] Building dynamic race state..."
    )

    race_state = build_dynamic_race_state(

        session=session,

        driver=DRIVER,

        selected_lap=TARGET_LAP

    )

    assert race_state, (
        "Dynamic race state was not generated."
    )

    assert (
        race_state.get("CurrentLap")
        == TARGET_LAP
    ), (
        "Dynamic race state was generated "
        "for the wrong lap."
    )

    print(
        "✅ Phase 4.1 race state generated."
    )


    # ========================================================
    # STEP 3
    # DYNAMIC RACE SITUATION — PHASE 4.2
    # ========================================================

    print(
        "\n[3/5] Analyzing dynamic race situation..."
    )

    race_situation = (
        analyze_dynamic_race_situation(
            race_state
        )
    )

    assert race_situation, (
        "Dynamic race situation was not generated."
    )

    print(
        "✅ Phase 4.2 race situation generated."
    )


    # ========================================================
    # STEP 4
    # DYNAMIC TYRE STRATEGY — PHASE 4.3
    # ========================================================

    print(
        "\n[4/5] Generating dynamic tyre strategy..."
    )

    tyre_strategy = (
        generate_dynamic_tyre_strategy(

            race_state=race_state,

            race_situation=race_situation

        )
    )

    assert tyre_strategy, (
        "Dynamic tyre strategy was not generated."
    )

    print(
        "✅ Phase 4.3 tyre strategy generated."
    )


    # ========================================================
    # STEP 5
    # DYNAMIC PIT DECISION — PHASE 4.4
    # ========================================================

    print(
        "\n[5/5] Evaluating dynamic pit-stop decision..."
    )

    pit_decision = (
        evaluate_dynamic_pit_decision(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy

        )
    )

    assert pit_decision, (
        "Dynamic pit-stop decision was not generated."
    )

    print(
        "✅ Phase 4.4 pit-stop decision generated."
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print(
        "\n" + "=" * 72
    )

    print(
        "PHASE 4.4 — DYNAMIC PIT-STOP DECISION"
    )

    print(
        "=" * 72
    )


    print(
        f"Driver: "
        f"{race_state.get('Driver')}"
    )

    print(
        f"Current Lap: "
        f"{race_state.get('CurrentLap')}"
        f"/"
        f"{race_state.get('TotalLaps')}"
    )

    print(
        f"Laps Remaining: "
        f"{race_state.get('LapsRemaining')}"
    )

    print(
        f"Position: P"
        f"{race_state.get('Position')}"
    )

    print(
        f"Current Tyre: "
        f"{race_state.get('TyreCompound')}"
    )

    print(
        f"Tyre Life: "
        f"{race_state.get('TyreLife')}"
    )

    print(
        f"Recent Pace: "
        f"{race_state.get('RecentPace')}"
    )

    print(
        f"Degradation Rate: "
        f"{race_state.get('DegradationRate')}"
    )


    print(
        "-" * 72
    )


    # ========================================================
    # EXTRACT DECISION
    # ========================================================

    decision = (

        pit_decision.get(
            "decision"
        )

        or pit_decision.get(
            "action"
        )

    )


    print(
        f"Pit Decision: "
        f"{decision}"
    )


    print(
        f"Recommended Tyre: "
        f"{pit_decision.get('recommended_tyre')}"
    )


    print(
        f"Pit Loss: "
        f"{pit_decision.get('pit_loss')}s"
    )


    print(
        f"Pace Gain / Lap: "
        f"{pit_decision.get('pace_gain_per_lap')}s"
    )


    print(
        f"Estimated Benefit: "
        f"{pit_decision.get('estimated_benefit')}s"
    )


    print(
        f"Traffic Penalty: "
        f"{pit_decision.get('traffic_penalty')}s"
    )


    print(
        f"Confidence: "
        f"{pit_decision.get('confidence')}%"
    )


    print(
        f"Race Situation: "
        f"{pit_decision.get('race_situation')}"
    )


    print(
        "\nReason:"
    )


    print(
        pit_decision.get(
            "reason",
            "--"
        )
    )


    print(
        "=" * 72
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    print(
        "\nValidating dynamic pit-stop decision..."
    )


    # --------------------------------------------------------
    # DECISION EXISTS
    # --------------------------------------------------------

    assert decision is not None, (
        "Pit decision is missing."
    )


    # --------------------------------------------------------
    # DECISION IS VALID
    # --------------------------------------------------------

    normalized_decision = (
        str(decision)
        .strip()
        .upper()
        .replace("_", " ")
    )


    assert normalized_decision in {

        "PIT",

        "PIT NOW",

        "STAY OUT"

    }, (
        f"Unexpected pit decision: {decision}"
    )


    # --------------------------------------------------------
    # RECOMMENDED TYRE
    # --------------------------------------------------------

    assert (
        pit_decision.get(
            "recommended_tyre"
        )
        is not None
    ), (
        "Recommended tyre is missing."
    )


    # --------------------------------------------------------
    # PIT LOSS
    # --------------------------------------------------------

    assert (
        pit_decision.get(
            "pit_loss"
        )
        is not None
    ), (
        "Pit loss is missing."
    )


    pit_loss = float(
        pit_decision[
            "pit_loss"
        ]
    )


    assert pit_loss >= 0, (
        "Pit loss cannot be negative."
    )


    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    assert (
        pit_decision.get(
            "confidence"
        )
        is not None
    ), (
        "Decision confidence is missing."
    )


    confidence = float(
        pit_decision[
            "confidence"
        ]
    )


    assert (
        0 <= confidence <= 100
    ), (
        "Confidence must be between 0 and 100."
    )


    # --------------------------------------------------------
    # ESTIMATED BENEFIT
    # --------------------------------------------------------

    assert (
        pit_decision.get(
            "estimated_benefit"
        )
        is not None
    ), (
        "Estimated pit benefit is missing."
    )


    # --------------------------------------------------------
    # PACE GAIN
    # --------------------------------------------------------

    assert (
        pit_decision.get(
            "pace_gain_per_lap"
        )
        is not None
    ), (
        "Pace gain per lap is missing."
    )


    # --------------------------------------------------------
    # RACE SITUATION
    # --------------------------------------------------------

    assert (
        pit_decision.get(
            "race_situation"
        )
        is not None
    ), (
        "Race situation is missing "
        "from pit decision."
    )


    # ========================================================
    # PIPELINE VALIDATION
    # ========================================================

    assert (
        race_state.get(
            "DynamicState"
        )
        is True
    ), (
        "Phase 4.1 dynamic-state flag missing."
    )


    assert (
        race_state.get(
            "LapsRemaining"
        )
        is not None
    ), (
        "Laps remaining is unavailable."
    )


    assert (
        race_state.get(
            "TyreCompound"
        )
        is not None
    ), (
        "Current tyre is unavailable."
    )


    assert (
        race_state.get(
            "RecentPace"
        )
        is not None
    ), (
        "Recent pace is unavailable."
    )


    print(
        "✅ Decision validation passed."
    )

    print(
        "✅ Recommended tyre validation passed."
    )

    print(
        "✅ Pit-loss validation passed."
    )

    print(
        "✅ Confidence validation passed."
    )

    print(
        "✅ Dynamic race-state connection passed."
    )

    print(
        "✅ Dynamic race-situation connection passed."
    )

    print(
        "✅ Dynamic tyre-strategy connection passed."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 72
    )

    print(
        "✅ PHASE 4.4 DYNAMIC PIT-STOP DECISION TEST PASSED"
    )

    print(
        "=" * 72
    )


if __name__ == "__main__":

    main()