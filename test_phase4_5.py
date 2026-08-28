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

from src.strategy.dynamic_strategy_simulation import (
    run_dynamic_strategy_simulation,
    display_dynamic_strategy_simulation
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# PHASE 4.5 TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 72
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 4.5 — DYNAMIC STRATEGY SIMULATION TEST"
    )

    print(
        "=" * 72
    )


    # ========================================================
    # STEP 1
    # LOAD SESSION
    # ========================================================

    print(
        "\n[1/6] Loading race session..."
    )

    session = load_session(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        session_type="R"

    )

    assert session is not None

    print(
        "✅ Race session loaded."
    )


    # ========================================================
    # STEP 2
    # PHASE 4.1
    # ========================================================

    print(
        "\n[2/6] Building dynamic race state..."
    )

    race_state = build_dynamic_race_state(

        session=session,

        driver=DRIVER,

        selected_lap=TARGET_LAP

    )

    assert race_state

    print(
        "✅ Phase 4.1 race state generated."
    )


    # ========================================================
    # STEP 3
    # PHASE 4.2
    # ========================================================

    print(
        "\n[3/6] Analyzing dynamic race situation..."
    )

    race_situation = (
        analyze_dynamic_race_situation(
            race_state
        )
    )

    assert race_situation

    print(
        "✅ Phase 4.2 race situation generated."
    )


    # ========================================================
    # STEP 4
    # PHASE 4.3
    # ========================================================

    print(
        "\n[4/6] Generating dynamic tyre strategy..."
    )

    tyre_strategy = (
        generate_dynamic_tyre_strategy(

            race_state=race_state,

            race_situation=race_situation

        )
    )

    assert tyre_strategy

    print(
        "✅ Phase 4.3 tyre strategy generated."
    )


    # ========================================================
    # STEP 5
    # PHASE 4.4
    # ========================================================

    print(
        "\n[5/6] Evaluating dynamic pit decision..."
    )

    pit_decision = (
        evaluate_dynamic_pit_decision(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy

        )
    )

    assert pit_decision

    print(
        "✅ Phase 4.4 pit decision generated."
    )


    # ========================================================
    # STEP 6
    # PHASE 4.5
    # ========================================================

    print(
        "\n[6/6] Simulating dynamic strategies..."
    )

    simulation = (
        run_dynamic_strategy_simulation(

            race_state=race_state,

            race_situation=race_situation,

            tyre_strategy=tyre_strategy,

            pit_decision=pit_decision

        )
    )

    assert simulation

    print(
        "✅ Phase 4.5 strategy simulation generated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_dynamic_strategy_simulation(
        simulation
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    print(
        "\nValidating dynamic strategy simulation..."
    )


    strategies = simulation.get(
        "strategies",
        []
    )


    # --------------------------------------------------------
    # EXPECT FOUR STRATEGIES
    # --------------------------------------------------------

    assert (
        len(strategies)
        ==
        4
    ), (
        "Phase 4.5 must generate four strategies."
    )


    # --------------------------------------------------------
    # DYNAMIC FLAG
    # --------------------------------------------------------

    assert (
        simulation.get(
            "dynamic_simulation"
        )
        is True
    ), (
        "Dynamic simulation flag missing."
    )


    # --------------------------------------------------------
    # CORRECT LAP
    # --------------------------------------------------------

    assert (
        simulation.get(
            "current_lap"
        )
        ==
        TARGET_LAP
    ), (
        "Simulation was generated "
        "for the wrong race lap."
    )


    # --------------------------------------------------------
    # REMAINING LAPS
    # --------------------------------------------------------

    assert (
        simulation.get(
            "remaining_laps"
        )
        >
        0
    ), (
        "Remaining laps must be greater than zero."
    )


    # --------------------------------------------------------
    # REQUIRED STRATEGY DATA
    # --------------------------------------------------------

    for strategy in strategies:

        assert (
            strategy.get(
                "strategy"
            )
            is not None
        )

        assert (
            strategy.get(
                "tyre_plan"
            )
            is not None
        )

        assert (
            strategy.get(
                "projected_total_time"
            )
            is not None
        )

        assert (
            strategy.get(
                "strategy_rank"
            )
            is not None
        )

        assert (
            strategy.get(
                "time_difference"
            )
            is not None
        )


    # --------------------------------------------------------
    # BEST STRATEGY
    # --------------------------------------------------------

    best = simulation.get(
        "best_strategy"
    )


    assert best is not None, (
        "Best dynamic strategy is missing."
    )


    assert (
        best.get(
            "strategy_rank"
        )
        ==
        1
    ), (
        "Best strategy must have rank 1."
    )


    # --------------------------------------------------------
    # ORDER CHECK
    # --------------------------------------------------------

    projected_times = [

        strategy[
            "projected_total_time"
        ]

        for strategy in strategies

    ]


    assert (
        projected_times
        ==
        sorted(
            projected_times
        )
    ), (
        "Strategies are not correctly ranked "
        "by projected total time."
    )


    # --------------------------------------------------------
    # EXPECT STAY OUT + 3 PIT STRATEGIES
    # --------------------------------------------------------

    stay_out_count = sum(

        1

        for strategy in strategies

        if strategy.get(
            "strategy"
        )
        ==
        "STAY_OUT"

    )


    pit_count = sum(

        1

        for strategy in strategies

        if strategy.get(
            "strategy"
        )
        ==
        "PIT"

    )


    assert (
        stay_out_count
        ==
        1
    ), (
        "Expected exactly one STAY_OUT strategy."
    )


    assert (
        pit_count
        ==
        3
    ), (
        "Expected exactly three PIT strategies."
    )


    # --------------------------------------------------------
    # DYNAMIC CONTEXT
    # --------------------------------------------------------

    assert all(

        strategy.get(
            "simulation_lap"
        )
        ==
        TARGET_LAP

        for strategy in strategies

    ), (
        "Dynamic lap context is missing "
        "from one or more strategies."
    )


    assert all(

        strategy.get(
            "dynamic_simulation"
        )
        is True

        for strategy in strategies

    ), (
        "Dynamic simulation flag missing "
        "from strategy records."
    )


    print(
        "✅ Four candidate strategies generated."
    )

    print(
        "✅ Strategy ranking validated."
    )

    print(
        "✅ Projected race times validated."
    )

    print(
        "✅ Strategy time differences validated."
    )

    print(
        "✅ Best strategy validated."
    )

    print(
        "✅ Dynamic lap context validated."
    )

    print(
        "✅ Phase 4.1 → 4.5 pipeline validated."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 72
    )

    print(
        "✅ PHASE 4.5 DYNAMIC STRATEGY SIMULATION TEST PASSED"
    )

    print(
        "=" * 72
    )


if __name__ == "__main__":

    main()