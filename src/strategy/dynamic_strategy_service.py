"""
F1 AI STRATEGIST
PHASE 5.1 — DYNAMIC STRATEGY SERVICE

Purpose
-------
Provide one unified service that executes the complete
Phase 4 dynamic strategy pipeline.

Pipeline
--------

4.1 Dynamic Race State
        ↓
4.2 Dynamic Race Situation
        ↓
4.3 Dynamic Tyre Strategy
        ↓
4.4 Dynamic Pit Decision
        ↓
4.5 Dynamic Strategy Simulation
        ↓
4.6 Dynamic Strategy Scoring
        ↓
4.7 Dynamic AI Recommendation
        ↓
Phase 5.1 Unified Strategy Service

IMPORTANT
---------
Phase 5.1 does NOT modify the verified Phase 4 engines.

It only connects them together through one service function.
"""


# ============================================================
# PHASE 4.1
# DYNAMIC RACE STATE
# ============================================================

from src.strategy.dynamic_race_state import (
    build_dynamic_race_state
)


# ============================================================
# PHASE 4.2
# DYNAMIC RACE SITUATION
# ============================================================

from src.strategy.dynamic_race_situation import (
    analyze_dynamic_race_situation
)


# ============================================================
# PHASE 4.3
# DYNAMIC TYRE STRATEGY
# ============================================================

from src.strategy.dynamic_tyre_strategy import (
    generate_dynamic_tyre_strategy
)


# ============================================================
# PHASE 4.4
# DYNAMIC PIT DECISION
# ============================================================

from src.strategy.dynamic_pit_decision import (
    evaluate_dynamic_pit_decision
)


# ============================================================
# PHASE 4.5
# DYNAMIC STRATEGY SIMULATION
# ============================================================

from src.strategy.dynamic_strategy_simulation import (
    run_dynamic_strategy_simulation
)


# ============================================================
# PHASE 4.6
# DYNAMIC STRATEGY SCORING
# ============================================================

from src.strategy.dynamic_strategy_scoring import (
    run_dynamic_strategy_scoring
)


# ============================================================
# PHASE 4.7
# DYNAMIC AI RECOMMENDATION
# ============================================================

from src.strategy.dynamic_ai_recommendation import (
    generate_dynamic_ai_recommendation
)


# ============================================================
# HELPER
# ============================================================

def get_first_value(
    data,
    *keys,
    default=None
):
    """
    Return the first available non-None value
    from a dictionary.
    """

    if not isinstance(data, dict):
        return default

    for key in keys:

        value = data.get(key)

        if value is not None:
            return value

    return default


# ============================================================
# PHASE 5.1
# UNIFIED DYNAMIC STRATEGY SERVICE
# ============================================================

def run_dynamic_strategy_service(
    session,
    driver,
    lap
):
    """
    Execute the complete Phase 4 dynamic strategy pipeline.

    Parameters
    ----------
    session
        Loaded FastF1 race session.

    driver
        Driver abbreviation.

        Example:
            VER

    lap
        Target race lap.

        Example:
            35

    Returns
    -------
    dict

        Unified dynamic strategy response containing:

        - race state
        - race situation
        - tyre strategy
        - pit decision
        - strategy simulation
        - strategy scoring
        - AI recommendation
    """


    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    if session is None:

        raise ValueError(
            "A valid FastF1 session is required."
        )


    if (
        driver is None
        or not str(driver).strip()
    ):

        raise ValueError(
            "A valid driver abbreviation is required."
        )


    driver = str(driver).strip().upper()


    try:

        lap = int(lap)

    except (TypeError, ValueError):

        raise ValueError(
            "lap must be a valid integer."
        )


    if lap <= 0:

        raise ValueError(
            "lap must be greater than zero."
        )


    # ========================================================
    # PHASE 4.1
    # BUILD DYNAMIC RACE STATE
    # ========================================================

    race_state = build_dynamic_race_state(
        session,
        driver,
        lap
    )


    if not race_state:

        raise RuntimeError(
            "Phase 4.1 failed: "
            "dynamic race state was not generated."
        )


    # ========================================================
    # PHASE 4.2
    # ANALYZE DYNAMIC RACE SITUATION
    # ========================================================

    race_situation = analyze_dynamic_race_situation(
        race_state
    )


    if not race_situation:

        raise RuntimeError(
            "Phase 4.2 failed: "
            "dynamic race situation was not generated."
        )


    # ========================================================
    # PHASE 4.3
    # GENERATE DYNAMIC TYRE STRATEGY
    # ========================================================

    tyre_strategy = generate_dynamic_tyre_strategy(
        race_state=race_state,
        race_situation=race_situation
    )


    if not tyre_strategy:

        raise RuntimeError(
            "Phase 4.3 failed: "
            "dynamic tyre strategy was not generated."
        )


    # ========================================================
    # PHASE 4.4
    # EVALUATE DYNAMIC PIT DECISION
    # ========================================================

    pit_decision = evaluate_dynamic_pit_decision(
        race_state=race_state,
        race_situation=race_situation,
        tyre_strategy=tyre_strategy
    )


    if not pit_decision:

        raise RuntimeError(
            "Phase 4.4 failed: "
            "dynamic pit decision was not generated."
        )


    # ========================================================
    # PHASE 4.5
    # DYNAMIC STRATEGY SIMULATION
    # ========================================================

    strategy_simulation = run_dynamic_strategy_simulation(
        race_state=race_state,
        race_situation=race_situation,
        tyre_strategy=tyre_strategy,
        pit_decision=pit_decision
    )


    if not strategy_simulation:

        raise RuntimeError(
            "Phase 4.5 failed: "
            "dynamic strategy simulation was not generated."
        )


    # ========================================================
    # PHASE 4.6
    # DYNAMIC STRATEGY SCORING
    # ========================================================

    strategy_scoring = run_dynamic_strategy_scoring(
        simulation_result=strategy_simulation,
        race_state=race_state,
        race_situation=race_situation,
        tyre_strategy=tyre_strategy,
        pit_decision=pit_decision
    )


    if not strategy_scoring:

        raise RuntimeError(
            "Phase 4.6 failed: "
            "dynamic strategy scoring was not generated."
        )


    # ========================================================
    # PHASE 4.7
    # DYNAMIC AI RECOMMENDATION
    # ========================================================

    ai_recommendation = generate_dynamic_ai_recommendation(
        race_state=race_state,
        race_situation=race_situation,
        tyre_strategy=tyre_strategy,
        pit_decision=pit_decision,
        simulation_result=strategy_simulation,
        scoring_result=strategy_scoring
    )


    if not ai_recommendation:

        raise RuntimeError(
            "Phase 4.7 failed: "
            "dynamic AI recommendation was not generated."
        )


    # ========================================================
    # EXTRACT RACE INFORMATION
    # ========================================================

    current_lap = get_first_value(
        race_state,
        "CurrentLap",
        "current_lap",
        default=lap
    )


    total_laps = get_first_value(
        race_state,
        "TotalLaps",
        "total_laps"
    )


    laps_remaining = get_first_value(
        race_state,
        "LapsRemaining",
        "laps_remaining"
    )


    position = get_first_value(
        race_state,
        "Position",
        "position"
    )


    current_tyre = get_first_value(
        race_state,
        "TyreCompound",
        "current_tyre",
        "CurrentTyre"
    )


    tyre_life = get_first_value(
        race_state,
        "TyreLife",
        "tyre_life",
        "tyre_age"
    )


    recent_pace = get_first_value(
        race_state,
        "RecentPace",
        "recent_pace"
    )


    degradation_rate = get_first_value(
        race_state,
        "DegradationRate",
        "degradation_rate"
    )


    # ========================================================
    # EXTRACT RACE SITUATION
    # ========================================================

    situation = get_first_value(
        race_situation,
        "race_situation",
        "RaceSituation",
        "situation"
    )


    # ========================================================
    # EXTRACT PIT DECISION
    # ========================================================

    pit_action = get_first_value(
        pit_decision,
        "decision",
        "action",
        "Decision",
        "Action"
    )


    # ========================================================
    # EXTRACT AI RECOMMENDATION
    # ========================================================

    recommendation = get_first_value(
        ai_recommendation,
        "recommendation",
        "Recommendation",
        "action",
        "Action"
    )


    recommended_tyre = get_first_value(
        ai_recommendation,
        "recommended_tyre",
        "RecommendedTyre",
        "recommended_compound",
        "compound"
    )


    confidence = get_first_value(
        ai_recommendation,
        "confidence",
        "Confidence"
    )


    dynamic_score = get_first_value(
        ai_recommendation,
        "dynamic_score",
        "DynamicScore",
        "strategy_score",
        "score"
    )


    reasoning = get_first_value(
        ai_recommendation,
        "reasoning",
        "Reasoning",
        "reason",
        "Reason"
    )


    # ========================================================
    # PHASE 5.1 RESPONSE
    # ========================================================

    result = {

        # ----------------------------------------------------
        # SERVICE INFORMATION
        # ----------------------------------------------------

        "service":
            "dynamic_strategy_service",

        "phase":
            "5.1",

        "status":
            "SUCCESS",


        # ----------------------------------------------------
        # REQUEST
        # ----------------------------------------------------

        "driver":
            driver,

        "lap":
            current_lap,


        # ----------------------------------------------------
        # RACE CONTEXT
        # ----------------------------------------------------

        "total_laps":
            total_laps,

        "laps_remaining":
            laps_remaining,

        "position":
            position,

        "current_tyre":
            current_tyre,

        "tyre_life":
            tyre_life,

        "recent_pace":
            recent_pace,

        "degradation_rate":
            degradation_rate,


        # ----------------------------------------------------
        # STRATEGIC CONTEXT
        # ----------------------------------------------------

        "race_situation":
            situation,

        "pit_decision":
            pit_action,


        # ----------------------------------------------------
        # FINAL AI RESULT
        # ----------------------------------------------------

        "recommendation":
            recommendation,

        "recommended_tyre":
            recommended_tyre,

        "confidence":
            confidence,

        "dynamic_score":
            dynamic_score,

        "reasoning":
            reasoning,


        # ----------------------------------------------------
        # COMPLETE PHASE 4 OUTPUT
        # ----------------------------------------------------

        "pipeline": {

            "phase_4_1":
                race_state,

            "phase_4_2":
                race_situation,

            "phase_4_3":
                tyre_strategy,

            "phase_4_4":
                pit_decision,

            "phase_4_5":
                strategy_simulation,

            "phase_4_6":
                strategy_scoring,

            "phase_4_7":
                ai_recommendation

        },


        # ----------------------------------------------------
        # DIRECT OUTPUT ACCESS
        # ----------------------------------------------------

        "race_state":
            race_state,

        "race_situation_analysis":
            race_situation,

        "tyre_strategy":
            tyre_strategy,

        "pit_decision_result":
            pit_decision,

        "strategy_simulation":
            strategy_simulation,

        "strategy_scoring":
            strategy_scoring,

        "ai_recommendation":
            ai_recommendation

    }


    return result


# ============================================================
# DISPLAY PHASE 5.1 RESULT
# ============================================================

def display_dynamic_strategy_service(
    result
):
    """
    Display the unified Phase 5.1 strategy response.
    """


    if not result:

        print(
            "No Phase 5.1 result available."
        )

        return


    print(
        "\n" + "=" * 76
    )

    print(
        "PHASE 5.1 — DYNAMIC STRATEGY SERVICE"
    )

    print(
        "=" * 76
    )


    # ========================================================
    # RACE
    # ========================================================

    print(
        f"Driver: "
        f"{result.get('driver')}"
    )


    current_lap = result.get(
        "lap"
    )


    total_laps = result.get(
        "total_laps"
    )


    if total_laps is not None:

        print(
            f"Current Lap: "
            f"{current_lap}/{total_laps}"
        )

    else:

        print(
            f"Current Lap: "
            f"{current_lap}"
        )


    print(
        f"Laps Remaining: "
        f"{result.get('laps_remaining')}"
    )


    position = result.get(
        "position"
    )


    if position is not None:

        print(
            f"Position: "
            f"P{position}"
        )

    else:

        print(
            "Position: --"
        )


    print(
        f"Current Tyre: "
        f"{result.get('current_tyre')}"
    )


    print(
        f"Tyre Life: "
        f"{result.get('tyre_life')}"
    )


    print(
        f"Recent Pace: "
        f"{result.get('recent_pace')}"
    )


    print(
        f"Degradation Rate: "
        f"{result.get('degradation_rate')}"
    )


    # ========================================================
    # STRATEGY
    # ========================================================

    print(
        "-" * 76
    )


    print(
        f"Race Situation: "
        f"{result.get('race_situation')}"
    )


    print(
        f"Pit Decision: "
        f"{result.get('pit_decision')}"
    )


    print(
        f"AI Recommendation: "
        f"{result.get('recommendation')}"
    )


    print(
        f"Recommended Tyre: "
        f"{result.get('recommended_tyre')}"
    )


    print(
        f"Dynamic Score: "
        f"{result.get('dynamic_score')}"
    )


    confidence = result.get(
        "confidence"
    )

    if confidence is not None:

        print(
            f"Confidence: "
            f"{confidence}%"
        )

    else:

        print(
            "Confidence: --"
        )


    # ========================================================
    # PIPELINE
    # ========================================================

    print(
        "-" * 76
    )


    print(
        "PHASE 5.1 PIPELINE"
    )


    print(
        "-" * 76
    )


    print(
        "4.1 Dynamic Race State"
    )

    print(
        "        ↓"
    )

    print(
        "4.2 Dynamic Race Situation"
    )

    print(
        "        ↓"
    )

    print(
        "4.3 Dynamic Tyre Strategy"
    )

    print(
        "        ↓"
    )

    print(
        "4.4 Dynamic Pit Decision"
    )

    print(
        "        ↓"
    )

    print(
        "4.5 Dynamic Strategy Simulation"
    )

    print(
        "        ↓"
    )

    print(
        "4.6 Dynamic Strategy Scoring"
    )

    print(
        "        ↓"
    )

    print(
        "4.7 Dynamic AI Recommendation"
    )


    # ========================================================
    # REASONING
    # ========================================================

    print(
        "-" * 76
    )


    print(
        "AI REASONING"
    )


    print(
        "-" * 76
    )


    print(
        result.get(
            "reasoning",
            "--"
        )
    )


    print(
        "=" * 76
    )