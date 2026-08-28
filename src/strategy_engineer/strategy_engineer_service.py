"""
F1 AI STRATEGIST
PHASE 7.2 — AI STRATEGY ENGINEER SERVICE

Purpose
-------
Execute the existing verified F1 AI strategy pipeline using
a manually constructed race state from Phase 7.1.

Pipeline
--------

Manual Race Situation
        ↓
7.1 Manual Race-State Builder
        ↓
7.2 Strategy Engineer Compatibility Layer
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

IMPORTANT
---------
Phase 7.2 does NOT rebuild the verified Phase 4 engines.

It only adapts and connects the Phase 7.1 manually generated
race state to the existing strategy architecture.
"""


from __future__ import annotations

from typing import Any, Dict


# ============================================================
# PHASE 7.1
# ============================================================

from src.strategy_engineer.race_state_builder import (
    build_manual_race_state
)


# ============================================================
# PHASE 4.2
# ============================================================

from src.strategy.dynamic_race_situation import (
    analyze_dynamic_race_situation
)


# ============================================================
# PHASE 4.3
# ============================================================

from src.strategy.dynamic_tyre_strategy import (
    generate_dynamic_tyre_strategy
)


# ============================================================
# PHASE 4.4
# ============================================================

from src.strategy.dynamic_pit_decision import (
    evaluate_dynamic_pit_decision
)


# ============================================================
# PHASE 4.5
# ============================================================

from src.strategy.dynamic_strategy_simulation import (
    run_dynamic_strategy_simulation
)


# ============================================================
# PHASE 4.6
# ============================================================

from src.strategy.dynamic_strategy_scoring import (
    run_dynamic_strategy_scoring
)


# ============================================================
# PHASE 4.7
# ============================================================

from src.strategy.dynamic_ai_recommendation import (
    generate_dynamic_ai_recommendation
)


# ============================================================
# CONSTANTS
# ============================================================

PHASE = "7.2"

COMPONENT = "strategy_engineer_service"

SOURCE = "MANUAL"


# ============================================================
# GENERIC HELPER
# ============================================================

def _first_value(
    data: Dict[str, Any],
    *keys: str,
    default: Any = None
) -> Any:
    """
    Return the first non-None value found in a dictionary.
    """

    if not isinstance(
        data,
        dict
    ):

        return default


    for key in keys:

        value = data.get(
            key
        )


        if value is not None:

            return value


    return default


# ============================================================
# STRATEGY INPUT VALIDATION
# ============================================================

def validate_strategy_engineer_race_state(
    race_state: Dict[str, Any]
) -> None:
    """
    Validate the minimum manual race-state information required
    before entering the Phase 4 strategy pipeline.
    """

    if not isinstance(
        race_state,
        dict
    ):

        raise TypeError(
            "race_state must be a dictionary."
        )


    if not race_state:

        raise ValueError(
            "race_state cannot be empty."
        )


    required_fields = [

        "Driver",
        "Circuit",
        "CurrentLap",
        "TotalLaps",
        "LapsRemaining",
        "RaceProgress",
        "Position",
        "TyreCompound",
        "TyreLife",

    ]


    missing_fields = [

        field

        for field in required_fields

        if (
            field not in race_state
            or
            race_state.get(field) is None
        )

    ]


    if missing_fields:

        raise ValueError(

            "Manual race state is missing required field(s): "
            +
            ", ".join(
                missing_fields
            )

        )


    if not race_state.get(
        "ManualData",
        False
    ):

        raise ValueError(
            "Phase 7.2 requires a Phase 7.1 manual race state."
        )


# ============================================================
# PACE VALIDATION
# ============================================================

def validate_strategy_pace_inputs(
    race_state: Dict[str, Any]
) -> None:
    """
    Ensure sufficient pace information exists for the
    strategy engine.

    At least one pace value must be supplied.

    Phase 7.2 may safely mirror RecentPace and AveragePace
    when only one of them is provided, but it must not invent
    a lap time when neither exists.
    """

    recent_pace = race_state.get(
        "RecentPace"
    )


    average_pace = race_state.get(
        "AveragePace"
    )


    if (
        recent_pace is None
        and
        average_pace is None
    ):

        raise ValueError(

            "Strategy analysis requires at least one pace value: "
            "recent_pace or average_pace."

        )


    degradation_rate = race_state.get(
        "DegradationRate"
    )


    if degradation_rate is None:

        raise ValueError(

            "Strategy analysis requires degradation_rate. "
            "Phase 7.2 does not invent tyre degradation data."

        )


# ============================================================
# PHASE 4 COMPATIBILITY LAYER
# ============================================================

def prepare_phase4_manual_race_state(
    race_state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert the Phase 7.1 manual race state into a complete
    Phase 4-compatible race state.

    No strategic decisions are made here.

    Only structural compatibility and safe aliases/defaults
    are added.
    """

    validate_strategy_engineer_race_state(
        race_state
    )


    validate_strategy_pace_inputs(
        race_state
    )


    prepared = dict(
        race_state
    )


    # ========================================================
    # PACE COMPATIBILITY
    # ========================================================

    recent_pace = prepared.get(
        "RecentPace"
    )


    average_pace = prepared.get(
        "AveragePace"
    )


    average_pace_fallback_used = False

    recent_pace_fallback_used = False


    if (
        average_pace is None
        and
        recent_pace is not None
    ):

        prepared[
            "AveragePace"
        ] = recent_pace

        average_pace_fallback_used = True


    if (
        recent_pace is None
        and
        average_pace is not None
    ):

        prepared[
            "RecentPace"
        ] = average_pace

        recent_pace_fallback_used = True


    # ========================================================
    # STANDARD PHASE 4 FIELDS
    # ========================================================

    prepared.setdefault(
        "PitLoss",
        22.0
    )


    prepared.setdefault(
        "SessionStatus",
        "Started"
    )


    prepared.setdefault(
        "InPit",
        False
    )


    prepared.setdefault(
        "PitOut",
        False
    )


    prepared.setdefault(
        "SafetyCar",
        False
    )


    prepared.setdefault(
        "VirtualSafetyCar",
        False
    )


    prepared.setdefault(
        "RedFlag",
        False
    )


    prepared.setdefault(
        "WetConditions",
        False
    )


    prepared.setdefault(
        "Rainfall",
        0.0
    )


    prepared.setdefault(
        "TrackStatus",
        "GREEN"
    )


    prepared.setdefault(
        "PitStopsCompleted",
        0
    )


    # ========================================================
    # GAP ALIASES
    # ========================================================

    gap_ahead = _first_value(

        prepared,

        "GapAhead",
        "GapToAhead"

    )


    gap_behind = _first_value(

        prepared,

        "GapBehind"

    )


    prepared.setdefault(
        "GapToAhead",
        gap_ahead
    )


    prepared.setdefault(
        "IntervalToAhead",
        gap_ahead
    )


    prepared.setdefault(
        "GapBehind",
        gap_behind
    )


    # ========================================================
    # TYRE ALIASES
    # ========================================================

    prepared.setdefault(

        "CurrentTyre",

        prepared.get(
            "TyreCompound"
        )

    )


    prepared.setdefault(

        "TyreAge",

        prepared.get(
            "TyreLife"
        )

    )


    # ========================================================
    # PHASE 7.2 METADATA
    # ========================================================

    prepared[
        "StrategyEngineerData"
    ] = True


    prepared[
        "Phase4Compatible"
    ] = True


    prepared[
        "AveragePaceFallbackUsed"
    ] = (
        average_pace_fallback_used
    )


    prepared[
        "RecentPaceFallbackUsed"
    ] = (
        recent_pace_fallback_used
    )


    return prepared


# ============================================================
# RUN PHASE 7.2
# ============================================================

def run_strategy_engineer_service(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute the complete AI Strategy Engineer pipeline.

    Parameters
    ----------
    race_input
        User supplied race situation accepted by Phase 7.1.

    Returns
    -------
    dict
        Complete AI Strategy Engineer result.
    """


    # ========================================================
    # PHASE 7.1
    # BUILD MANUAL RACE STATE
    # ========================================================

    manual_race_state = (
        build_manual_race_state(
            race_input
        )
    )


    if not manual_race_state:

        raise RuntimeError(
            "Phase 7.1 failed to build a manual race state."
        )


    # ========================================================
    # PHASE 7.2
    # PREPARE PHASE 4 CONTRACT
    # ========================================================

    race_state = (
        prepare_phase4_manual_race_state(
            manual_race_state
        )
    )


    if not race_state:

        raise RuntimeError(
            "Phase 7.2 failed to prepare the strategy race state."
        )


    # ========================================================
    # PHASE 4.2
    # RACE SITUATION
    # ========================================================

    race_situation = (
        analyze_dynamic_race_situation(
            race_state
        )
    )


    if not race_situation:

        raise RuntimeError(
            "Phase 4.2 failed: race situation was not generated."
        )


    # ========================================================
    # PHASE 4.3
    # TYRE STRATEGY
    # ========================================================

    tyre_strategy = (
        generate_dynamic_tyre_strategy(

            race_state=
                race_state,

            race_situation=
                race_situation

        )
    )


    if not tyre_strategy:

        raise RuntimeError(
            "Phase 4.3 failed: tyre strategy was not generated."
        )


    # ========================================================
    # PHASE 4.4
    # PIT DECISION
    # ========================================================

    pit_decision = (
        evaluate_dynamic_pit_decision(

            race_state=
                race_state,

            race_situation=
                race_situation,

            tyre_strategy=
                tyre_strategy

        )
    )


    if not pit_decision:

        raise RuntimeError(
            "Phase 4.4 failed: pit decision was not generated."
        )


    # ========================================================
    # PHASE 4.5
    # STRATEGY SIMULATION
    # ========================================================

    simulation_result = (
        run_dynamic_strategy_simulation(

            race_state=
                race_state,

            race_situation=
                race_situation,

            tyre_strategy=
                tyre_strategy,

            pit_decision=
                pit_decision

        )
    )


    if not simulation_result:

        raise RuntimeError(
            "Phase 4.5 failed: strategy simulation was not generated."
        )


    # ========================================================
    # PHASE 4.6
    # STRATEGY SCORING
    # ========================================================

    scoring_result = (
        run_dynamic_strategy_scoring(

            simulation_result=
                simulation_result,

            race_state=
                race_state,

            race_situation=
                race_situation,

            tyre_strategy=
                tyre_strategy,

            pit_decision=
                pit_decision

        )
    )


    if not scoring_result:

        raise RuntimeError(
            "Phase 4.6 failed: strategy scoring was not generated."
        )


    # ========================================================
    # PHASE 4.7
    # AI RECOMMENDATION
    # ========================================================

    ai_recommendation = (
        generate_dynamic_ai_recommendation(

            race_state=
                race_state,

            race_situation=
                race_situation,

            tyre_strategy=
                tyre_strategy,

            pit_decision=
                pit_decision,

            simulation_result=
                simulation_result,

            scoring_result=
                scoring_result

        )
    )


    if not ai_recommendation:

        raise RuntimeError(
            "Phase 4.7 failed: AI recommendation was not generated."
        )


    # ========================================================
    # EXTRACT STRATEGIC VALUES
    # ========================================================

    situation = _first_value(

        race_situation,

        "race_situation",
        "RaceSituation",
        "situation"

    )


    pit_action = _first_value(

        pit_decision,

        "decision",
        "action",
        "Decision",
        "Action"

    )


    recommendation = _first_value(

        ai_recommendation,

        "recommendation",
        "Recommendation",
        "action",
        "Action"

    )


    recommended_tyre = _first_value(

        ai_recommendation,

        "recommended_tyre",
        "RecommendedTyre",
        "recommended_compound",
        "compound"

    )


    confidence = _first_value(

        ai_recommendation,

        "confidence",
        "Confidence"

    )


    dynamic_score = _first_value(

        ai_recommendation,

        "dynamic_score",
        "DynamicScore",
        "strategy_score",
        "score"

    )


    reasoning = _first_value(

        ai_recommendation,

        "reasoning",
        "Reasoning",
        "reason",
        "Reason"

    )


    # ========================================================
    # COMPLETE PHASE 7.2 RESPONSE
    # ========================================================

    result = {

        # ----------------------------------------------------
        # SERVICE
        # ----------------------------------------------------

        "service":
            COMPONENT,

        "phase":
            PHASE,

        "status":
            "SUCCESS",

        "source":
            SOURCE,

        "manual":
            True,


        # ----------------------------------------------------
        # DRIVER / EVENT
        # ----------------------------------------------------

        "driver":
            race_state.get(
                "Driver"
            ),

        "team":
            race_state.get(
                "Team"
            ),

        "grand_prix":
            race_state.get(
                "GrandPrix"
            ),

        "circuit":
            race_state.get(
                "Circuit"
            ),


        # ----------------------------------------------------
        # RACE CONTEXT
        # ----------------------------------------------------

        "current_lap":
            race_state.get(
                "CurrentLap"
            ),

        "total_laps":
            race_state.get(
                "TotalLaps"
            ),

        "laps_remaining":
            race_state.get(
                "LapsRemaining"
            ),

        "race_progress":
            race_state.get(
                "RaceProgress"
            ),

        "race_phase":
            race_state.get(
                "RacePhase"
            ),

        "position":
            race_state.get(
                "Position"
            ),


        # ----------------------------------------------------
        # TYRE / PACE
        # ----------------------------------------------------

        "current_tyre":
            race_state.get(
                "TyreCompound"
            ),

        "tyre_age":
            race_state.get(
                "TyreAge"
            ),

        "tyre_condition":
            race_state.get(
                "TyreCondition"
            ),

        "recent_pace":
            race_state.get(
                "RecentPace"
            ),

        "average_pace":
            race_state.get(
                "AveragePace"
            ),

        "degradation_rate":
            race_state.get(
                "DegradationRate"
            ),


        # ----------------------------------------------------
        # GAP / CONDITIONS
        # ----------------------------------------------------

        "gap_ahead":
            race_state.get(
                "GapAhead"
            ),

        "gap_behind":
            race_state.get(
                "GapBehind"
            ),

        "track_status":
            race_state.get(
                "TrackStatus"
            ),

        "weather":
            race_state.get(
                "Weather"
            ),

        "wet_conditions":
            race_state.get(
                "WetConditions"
            ),

        "safety_car":
            race_state.get(
                "SafetyCar"
            ),

        "virtual_safety_car":
            race_state.get(
                "VirtualSafetyCar"
            ),


        # ----------------------------------------------------
        # AI STRATEGY RESULT
        # ----------------------------------------------------

        "race_situation":
            situation,

        "pit_decision":
            pit_action,

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
        # COMPATIBILITY
        # ----------------------------------------------------

        "phase4_compatible":
            race_state.get(
                "Phase4Compatible",
                False
            ),

        "average_pace_fallback_used":
            race_state.get(
                "AveragePaceFallbackUsed",
                False
            ),

        "recent_pace_fallback_used":
            race_state.get(
                "RecentPaceFallbackUsed",
                False
            ),


        # ----------------------------------------------------
        # PIPELINE
        # ----------------------------------------------------

        "pipeline": {

            "phase_7_1":
                manual_race_state,

            "phase_7_2_state":
                race_state,

            "phase_4_2":
                race_situation,

            "phase_4_3":
                tyre_strategy,

            "phase_4_4":
                pit_decision,

            "phase_4_5":
                simulation_result,

            "phase_4_6":
                scoring_result,

            "phase_4_7":
                ai_recommendation,

        },


        # ----------------------------------------------------
        # DIRECT OUTPUT ACCESS
        # ----------------------------------------------------

        "manual_race_state":
            manual_race_state,

        "strategy_race_state":
            race_state,

        "race_situation_analysis":
            race_situation,

        "tyre_strategy":
            tyre_strategy,

        "pit_decision_result":
            pit_decision,

        "strategy_simulation":
            simulation_result,

        "strategy_scoring":
            scoring_result,

        "ai_recommendation":
            ai_recommendation,

    }


    return result


# ============================================================
# ALIAS
# ============================================================

def generate_strategy_engineer_recommendation(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Alias for the main Phase 7.2 service.
    """

    return run_strategy_engineer_service(
        race_input
    )


# ============================================================
# DISPLAY
# ============================================================

def display_strategy_engineer_service(
    result: Dict[str, Any]
) -> None:
    """
    Display the Phase 7.2 AI Strategy Engineer result.
    """


    if not result:

        print(
            "No Phase 7.2 strategy result available."
        )

        return


    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.2 — AI STRATEGY ENGINEER"
    )

    print(
        "=" * 78
    )


    print(
        f"Driver:              "
        f"{result.get('driver', '--')}"
    )


    print(
        f"Team:                "
        f"{result.get('team') or '--'}"
    )


    print(
        f"Grand Prix:          "
        f"{result.get('grand_prix') or '--'}"
    )


    print(
        f"Circuit:             "
        f"{result.get('circuit', '--')}"
    )


    print(
        "-" * 78
    )


    print(
        f"Current Lap:         "
        f"{result.get('current_lap', '--')}"
        f"/"
        f"{result.get('total_laps', '--')}"
    )


    print(
        f"Laps Remaining:      "
        f"{result.get('laps_remaining', '--')}"
    )


    print(
        f"Race Phase:          "
        f"{result.get('race_phase', '--')}"
    )


    position = result.get(
        "position"
    )


    if position is not None:

        print(
            f"Position:            "
            f"P{position}"
        )

    else:

        print(
            "Position:            --"
        )


    print(
        "-" * 78
    )


    print(
        f"Current Tyre:        "
        f"{result.get('current_tyre', '--')}"
    )


    print(
        f"Tyre Age:            "
        f"{result.get('tyre_age', '--')}"
    )


    print(
        f"Tyre Condition:      "
        f"{result.get('tyre_condition', '--')}"
    )


    print(
        f"Recent Pace:         "
        f"{result.get('recent_pace', '--')}"
    )


    print(
        f"Average Pace:        "
        f"{result.get('average_pace', '--')}"
    )


    print(
        f"Degradation Rate:    "
        f"{result.get('degradation_rate', '--')}"
    )


    print(
        "-" * 78
    )


    print(
        f"Gap Ahead:           "
        f"{result.get('gap_ahead')}"
    )


    print(
        f"Gap Behind:          "
        f"{result.get('gap_behind')}"
    )


    print(
        f"Track Status:        "
        f"{result.get('track_status', '--')}"
    )


    print(
        f"Weather:             "
        f"{result.get('weather', '--')}"
    )


    print(
        "-" * 78
    )


    print(
        f"Race Situation:      "
        f"{result.get('race_situation', '--')}"
    )


    print(
        f"Pit Decision:        "
        f"{result.get('pit_decision', '--')}"
    )


    print(
        f"AI Recommendation:   "
        f"{result.get('recommendation', '--')}"
    )


    print(
        f"Recommended Tyre:    "
        f"{result.get('recommended_tyre', '--')}"
    )


    print(
        f"Dynamic Score:       "
        f"{result.get('dynamic_score', '--')}"
    )


    confidence = result.get(
        "confidence"
    )


    if confidence is not None:

        print(
            f"Confidence:          "
            f"{confidence}%"
        )

    else:

        print(
            "Confidence:          --"
        )


    print(
        "-" * 78
    )


    print(
        f"Phase 4 Compatible:  "
        f"{result.get('phase4_compatible')}"
    )


    print(
        f"Average Pace Fallback: "
        f"{result.get('average_pace_fallback_used')}"
    )


    print(
        "-" * 78
    )


    print(
        "AI REASONING"
    )


    print(
        "-" * 78
    )


    print(
        result.get(
            "reasoning"
        )
        or
        "--"
    )


    print(
        "-" * 78
    )


    print(
        "STRATEGY PIPELINE"
    )


    print(
        "-" * 78
    )


    print(
        "7.1 Manual Race-State Builder"
    )

    print(
        "        ↓"
    )

    print(
        "7.2 Strategy Engineer Service"
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


    print(
        "=" * 78
    )