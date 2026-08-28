"""
F1 AI STRATEGIST
PHASE 7.5 — STRATEGY EXPLANATION & CONFIDENCE ENGINE

Purpose
-------
Convert the numerical outputs from Phases 7.2, 7.3 and 7.4
into a clear engineer-style recommendation.

Pipeline
--------

7.1 Manual Race-State Builder
        ↓
7.2 Strategy Engineer Service
        ↓
7.3 Strategy Alternatives Engine
        ↓
7.4 Pit Window Optimizer
        ↓
7.5 Explanation & Confidence Engine
        ↓
Final Engineer Recommendation

Outputs
-------
- Final recommendation
- Recommended tyre
- Strategy confidence
- Risk level
- Explanation
- Key strategic factors
- Alternative strategy summary
- Pit-window summary

IMPORTANT
---------
Phase 7.5 does not change the underlying strategy decision.

It explains and packages the verified outputs from the
earlier phases.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.strategy_engineer.pit_window_optimizer import (
    run_pit_window_optimizer,
)


# ============================================================
# CONSTANTS
# ============================================================

PHASE = "7.5"

COMPONENT = "strategy_explanation_engine"


# ============================================================
# GENERIC HELPERS
# ============================================================

def _safe_float(
    value: Any,
    default: Optional[float] = None
) -> Optional[float]:

    try:

        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):

        return default


def _safe_int(
    value: Any,
    default: Optional[int] = None
) -> Optional[int]:

    try:

        if value is None:
            return default

        return int(value)

    except (TypeError, ValueError):

        return default


def _normalise_text(
    value: Any
) -> str:

    if value is None:
        return ""

    return str(value).strip().upper()


# ============================================================
# EXTRACT PHASE 7.3
# ============================================================

def extract_alternatives_result(
    pit_window_result: Dict[str, Any]
) -> Dict[str, Any]:

    result = pit_window_result.get(
        "phase_7_3_result",
        {}
    )

    if isinstance(result, dict):
        return result

    return {}


# ============================================================
# EXTRACT PHASE 7.2
# ============================================================

def extract_strategy_result(
    pit_window_result: Dict[str, Any]
) -> Dict[str, Any]:

    alternatives = extract_alternatives_result(
        pit_window_result
    )

    result = alternatives.get(
        "phase_7_2_result",
        {}
    )

    if isinstance(result, dict):
        return result

    return {}


# ============================================================
# FINAL ACTION
# ============================================================

def determine_final_action(
    strategy_result: Dict[str, Any],
    alternatives_result: Dict[str, Any]
) -> str:
    """
    Final action follows the verified final AI recommendation.

    Strategy ranking is used only as a fallback.
    """

    recommendation = _normalise_text(
        strategy_result.get(
            "recommendation"
        )
    )


    if recommendation:

        if recommendation == "STAY_OUT":
            return "STAY OUT"

        return recommendation.replace(
            "_",
            " "
        )


    best_strategy = alternatives_result.get(
        "best_strategy"
    )


    if isinstance(
        best_strategy,
        dict
    ):

        display_name = best_strategy.get(
            "display_name"
        )

        if display_name:
            return str(display_name)


    return "UNKNOWN"


# ============================================================
# FINAL TYRE
# ============================================================

def determine_final_tyre(
    strategy_result: Dict[str, Any],
    pit_window_result: Dict[str, Any]
) -> Optional[str]:

    tyre = _normalise_text(
        strategy_result.get(
            "recommended_tyre"
        )
    )


    if tyre:
        return tyre


    tyre = _normalise_text(
        pit_window_result.get(
            "recommended_tyre"
        )
    )


    return tyre or None


# ============================================================
# CONFIDENCE
# ============================================================

def calculate_engineer_confidence(
    strategy_result: Dict[str, Any],
    alternatives_result: Dict[str, Any],
    pit_window_result: Dict[str, Any]
) -> float:
    """
    Combine existing strategy confidence with ranking/window
    confidence.

    This is a presentation-level confidence score.
    """

    ai_confidence = _safe_float(
        strategy_result.get(
            "confidence"
        ),
        50.0
    )


    window_confidence = _safe_float(
        pit_window_result.get(
            "window_confidence"
        ),
        50.0
    )


    score_advantage = _safe_float(
        alternatives_result.get(
            "score_advantage"
        ),
        0.0
    )


    alignment = alternatives_result.get(
        "ai_alignment",
        {}
    )


    aligned = bool(
        alignment.get(
            "aligned"
        )
    )


    confidence = (

        ai_confidence * 0.60

        +

        window_confidence * 0.20

        +

        min(
            score_advantage * 1.5,
            15.0
        )

    )


    if aligned:

        confidence += 5.0


    confidence = max(
        0.0,
        min(
            99.0,
            confidence
        )
    )


    return round(
        confidence,
        1
    )


# ============================================================
# RISK LEVEL
# ============================================================

def determine_strategy_risk(
    pit_window_result: Dict[str, Any],
    strategy_result: Dict[str, Any]
) -> str:
    """
    Estimate strategic risk from tyre degradation, urgency,
    race position and environmental conditions.
    """

    urgency = _safe_float(
        pit_window_result.get(
            "pit_urgency"
        ),
        0.0
    )


    degradation = _safe_float(
        pit_window_result.get(
            "degradation_rate"
        ),
        0.0
    )


    tyre_condition = _normalise_text(
        strategy_result.get(
            "tyre_condition"
        )
    )


    safety_car = bool(
        strategy_result.get(
            "safety_car"
        )
    )


    virtual_safety_car = bool(
        strategy_result.get(
            "virtual_safety_car"
        )
    )


    wet_conditions = bool(
        strategy_result.get(
            "wet_conditions"
        )
    )


    score = 0.0


    if urgency >= 80:
        score += 35

    elif urgency >= 60:
        score += 25

    elif urgency >= 40:
        score += 15


    if degradation >= 0.12:
        score += 30

    elif degradation >= 0.08:
        score += 20

    elif degradation >= 0.04:
        score += 10


    if tyre_condition == "CRITICAL":
        score += 30

    elif tyre_condition in {
        "WORN",
        "AGING"
    }:
        score += 15


    if wet_conditions:
        score += 15


    if safety_car or virtual_safety_car:
        score -= 5


    if score >= 65:
        return "HIGH"

    if score >= 35:
        return "MEDIUM"

    return "LOW"


# ============================================================
# BEST PIT ALTERNATIVE
# ============================================================

def build_best_pit_alternative(
    pit_window_result: Dict[str, Any]
) -> Dict[str, Any]:

    strategy = pit_window_result.get(
        "best_pit_strategy"
    )


    if not isinstance(
        strategy,
        dict
    ):

        return {}


    return {

        "strategy":
            strategy.get(
                "display_name"
            ),

        "tyre":
            strategy.get(
                "final_tyre"
            ),

        "dynamic_score":
            strategy.get(
                "dynamic_score"
            ),

        "projected_total_time":
            strategy.get(
                "projected_total_time"
            ),

        "pit_lap":
            pit_window_result.get(
                "recommended_pit_lap"
            ),

        "window_start":
            pit_window_result.get(
                "window_start"
            ),

        "window_end":
            pit_window_result.get(
                "window_end"
            ),

    }


# ============================================================
# KEY FACTORS
# ============================================================

def build_key_factors(
    strategy_result: Dict[str, Any],
    pit_window_result: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Build frontend-friendly strategic factors.
    """

    factors = []


    def add_factor(
        label: str,
        value: Any,
        unit: Optional[str] = None
    ) -> None:

        if value is None:
            return


        factors.append({

            "label":
                label,

            "value":
                value,

            "unit":
                unit,

        })


    add_factor(

        "Position",

        strategy_result.get(
            "position"
        )

    )


    add_factor(

        "Current Lap",

        strategy_result.get(
            "current_lap"
        )

    )


    add_factor(

        "Laps Remaining",

        strategy_result.get(
            "laps_remaining"
        )

    )


    add_factor(

        "Current Tyre",

        strategy_result.get(
            "current_tyre"
        )

    )


    add_factor(

        "Tyre Age",

        strategy_result.get(
            "tyre_age"
        ),

        "laps"

    )


    add_factor(

        "Tyre Condition",

        strategy_result.get(
            "tyre_condition"
        )

    )


    add_factor(

        "Degradation",

        strategy_result.get(
            "degradation_rate"
        ),

        "s/lap"

    )


    add_factor(

        "Gap Ahead",

        strategy_result.get(
            "gap_ahead"
        ),

        "s"

    )


    add_factor(

        "Gap Behind",

        strategy_result.get(
            "gap_behind"
        ),

        "s"

    )


    add_factor(

        "Pit Urgency",

        pit_window_result.get(
            "pit_urgency"
        ),

        "/100"

    )


    return factors


# ============================================================
# STRATEGY SUMMARY
# ============================================================

def build_strategy_summary(
    final_action: str,
    final_tyre: Optional[str],
    pit_window_result: Dict[str, Any]
) -> str:
    """
    Build a short headline-style strategy summary.
    """

    if final_action == "STAY OUT":

        return (
            "Maintain the current strategy and remain on track."
        )


    if "PIT" in final_action:

        if final_tyre:

            return (
                f"Pit and switch to {final_tyre} tyres."
            )

        return (
            "Make a pit stop at the recommended opportunity."
        )


    return (
        "Follow the highest-ranked AI strategy."
    )


# ============================================================
# MAIN EXPLANATION
# ============================================================

def build_strategy_explanation(
    final_action: str,
    final_tyre: Optional[str],
    strategy_result: Dict[str, Any],
    alternatives_result: Dict[str, Any],
    pit_window_result: Dict[str, Any]
) -> str:
    """
    Generate the primary engineer-style reasoning.
    """

    parts: List[str] = []


    current_lap = strategy_result.get(
        "current_lap"
    )


    total_laps = strategy_result.get(
        "total_laps"
    )


    position = strategy_result.get(
        "position"
    )


    tyre = strategy_result.get(
        "current_tyre"
    )


    tyre_age = _safe_float(
        strategy_result.get(
            "tyre_age"
        )
    )


    degradation = _safe_float(
        strategy_result.get(
            "degradation_rate"
        )
    )


    race_situation = strategy_result.get(
        "race_situation"
    )


    best = alternatives_result.get(
        "best_strategy",
        {}
    )


    best_name = (
        best.get(
            "display_name"
        )
        if isinstance(
            best,
            dict
        )
        else None
    )


    score_advantage = _safe_float(
        alternatives_result.get(
            "score_advantage"
        )
    )


    # ========================================================
    # ACTION
    # ========================================================

    if final_action == "STAY OUT":

        parts.append(
            "The AI recommends staying out on the current strategy"
        )

    elif "PIT" in final_action:

        if final_tyre:

            parts.append(
                f"The AI recommends pitting and switching to "
                f"{final_tyre} tyres"
            )

        else:

            parts.append(
                "The AI recommends making a pit stop"
            )

    else:

        parts.append(
            f"The AI recommends {final_action.lower()}"
        )


    # ========================================================
    # RACE CONTEXT
    # ========================================================

    if (
        current_lap is not None
        and
        total_laps is not None
        and
        position is not None
    ):

        parts.append(
            f"At lap {current_lap}/{total_laps}, "
            f"the driver is running P{position}"
        )


    # ========================================================
    # TYRE CONTEXT
    # ========================================================

    if (
        tyre
        and
        tyre_age is not None
    ):

        parts.append(
            f"The current {tyre} tyres are "
            f"{tyre_age:.1f} laps old"
        )


    if degradation is not None:

        parts.append(
            f"Measured degradation is "
            f"{degradation:.3f} seconds per lap"
        )


    # ========================================================
    # SITUATION
    # ========================================================

    if race_situation:

        parts.append(
            f"The race situation is classified as "
            f"{str(race_situation).replace('_', ' ')}"
        )


    # ========================================================
    # STRATEGY RANKING
    # ========================================================

    if best_name:

        parts.append(
            f"{best_name} is the highest-ranked strategy"
        )


    if score_advantage is not None:

        parts.append(
            f"It leads the next-best alternative by "
            f"{score_advantage:.2f} strategy-score points"
        )


    return ". ".join(
        parts
    ) + "."


# ============================================================
# PIT-WINDOW EXPLANATION
# ============================================================

def build_pit_window_explanation(
    pit_window_result: Dict[str, Any]
) -> str:
    """
    Explain the best pit alternative separately from the
    final action.
    """

    best_pit = pit_window_result.get(
        "best_pit_strategy"
    )


    if not isinstance(
        best_pit,
        dict
    ):

        return (
            "No viable pit alternative was identified."
        )


    tyre = pit_window_result.get(
        "recommended_tyre"
    )


    pit_lap = pit_window_result.get(
        "recommended_pit_lap"
    )


    start = pit_window_result.get(
        "window_start"
    )


    end = pit_window_result.get(
        "window_end"
    )


    if start == end:

        window_text = (
            f"lap {start}"
        )

    else:

        window_text = (
            f"laps {start}–{end}"
        )


    if tyre:

        return (
            f"If a stop is required, the strongest pit "
            f"alternative is {best_pit.get('display_name')}. "
            f"The optimizer targets {window_text}, with "
            f"lap {pit_lap} as the preferred stop."
        )


    return (
        f"If a stop is required, the preferred pit window "
        f"is {window_text}, with lap {pit_lap} as the "
        f"highest-ranked stop."
    )


# ============================================================
# WARNINGS
# ============================================================

def build_strategy_warnings(
    strategy_result: Dict[str, Any],
    alternatives_result: Dict[str, Any],
    pit_window_result: Dict[str, Any]
) -> List[str]:

    warnings = []


    pit_decision = _normalise_text(
        strategy_result.get(
            "pit_decision"
        )
    )


    recommendation = _normalise_text(
        strategy_result.get(
            "recommendation"
        )
    )


    if (
        pit_decision
        and
        recommendation
        and
        pit_decision.replace(
            "_",
            " "
        )
        !=
        recommendation.replace(
            "_",
            " "
        )
    ):

        warnings.append(
            "The pit-decision layer and final AI recommendation "
            "differ because the final decision includes strategy "
            "simulation and scoring."
        )


    time_advantage = _safe_float(
        alternatives_result.get(
            "time_advantage_seconds"
        )
    )


    if (
        time_advantage is not None
        and
        abs(
            time_advantage
        ) < 0.5
    ):

        warnings.append(
            "The projected time difference between the leading "
            "strategies is small, so the recommendation is "
            "sensitive to changing race conditions."
        )


    urgency = _safe_float(
        pit_window_result.get(
            "pit_urgency"
        ),
        0.0
    )


    if urgency >= 80:

        warnings.append(
            "Pit urgency is very high; delaying the stop can "
            "rapidly reduce tyre performance."
        )


    return warnings


# ============================================================
# BUILD COMPLETE EXPLANATION
# ============================================================

def build_strategy_explanation_result(
    pit_window_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build the complete Phase 7.5 explanation result.
    """

    if not isinstance(
        pit_window_result,
        dict
    ):

        raise TypeError(
            "pit_window_result must be a dictionary."
        )


    if pit_window_result.get(
        "phase"
    ) != "7.4":

        raise ValueError(
            "Phase 7.5 requires a Phase 7.4 pit-window result."
        )


    alternatives_result = extract_alternatives_result(
        pit_window_result
    )


    strategy_result = extract_strategy_result(
        pit_window_result
    )


    if not alternatives_result:

        raise RuntimeError(
            "Phase 7.3 strategy alternatives are unavailable."
        )


    if not strategy_result:

        raise RuntimeError(
            "Phase 7.2 strategy result is unavailable."
        )


    # ========================================================
    # FINAL ACTION
    # ========================================================

    final_action = determine_final_action(

        strategy_result=
            strategy_result,

        alternatives_result=
            alternatives_result

    )


    # ========================================================
    # TYRE
    # ========================================================

    final_tyre = determine_final_tyre(

        strategy_result=
            strategy_result,

        pit_window_result=
            pit_window_result

    )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = calculate_engineer_confidence(

        strategy_result=
            strategy_result,

        alternatives_result=
            alternatives_result,

        pit_window_result=
            pit_window_result

    )


    # ========================================================
    # RISK
    # ========================================================

    risk = determine_strategy_risk(

        pit_window_result=
            pit_window_result,

        strategy_result=
            strategy_result

    )


    # ========================================================
    # EXPLANATION
    # ========================================================

    explanation = build_strategy_explanation(

        final_action=
            final_action,

        final_tyre=
            final_tyre,

        strategy_result=
            strategy_result,

        alternatives_result=
            alternatives_result,

        pit_window_result=
            pit_window_result

    )


    pit_window_explanation = (
        build_pit_window_explanation(
            pit_window_result
        )
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    summary = build_strategy_summary(

        final_action=
            final_action,

        final_tyre=
            final_tyre,

        pit_window_result=
            pit_window_result

    )


    # ========================================================
    # FACTORS
    # ========================================================

    key_factors = build_key_factors(

        strategy_result=
            strategy_result,

        pit_window_result=
            pit_window_result

    )


    # ========================================================
    # WARNINGS
    # ========================================================

    warnings = build_strategy_warnings(

        strategy_result=
            strategy_result,

        alternatives_result=
            alternatives_result,

        pit_window_result=
            pit_window_result

    )


    # ========================================================
    # BEST PIT ALTERNATIVE
    # ========================================================

    best_pit_alternative = (
        build_best_pit_alternative(
            pit_window_result
        )
    )


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "engine":
            COMPONENT,

        "phase":
            PHASE,

        "status":
            "SUCCESS",

        "driver":
            strategy_result.get(
                "driver"
            ),

        "team":
            strategy_result.get(
                "team"
            ),

        "grand_prix":
            strategy_result.get(
                "grand_prix"
            ),

        "circuit":
            strategy_result.get(
                "circuit"
            ),

        "current_lap":
            strategy_result.get(
                "current_lap"
            ),

        "total_laps":
            strategy_result.get(
                "total_laps"
            ),

        "position":
            strategy_result.get(
                "position"
            ),

        "current_tyre":
            strategy_result.get(
                "current_tyre"
            ),

        "tyre_age":
            strategy_result.get(
                "tyre_age"
            ),

        "race_situation":
            strategy_result.get(
                "race_situation"
            ),

        "final_recommendation":
            final_action,

        "recommended_tyre":
            final_tyre,

        "confidence":
            confidence,

        "risk_level":
            risk,

        "summary":
            summary,

        "explanation":
            explanation,

        "pit_window_explanation":
            pit_window_explanation,

        "recommended_pit_lap":
            pit_window_result.get(
                "recommended_pit_lap"
            ),

        "window_start":
            pit_window_result.get(
                "window_start"
            ),

        "window_end":
            pit_window_result.get(
                "window_end"
            ),

        "pit_urgency":
            pit_window_result.get(
                "pit_urgency"
            ),

        "key_factors":
            key_factors,

        "warnings":
            warnings,

        "best_pit_alternative":
            best_pit_alternative,

        "strategy_alternatives":
            alternatives_result.get(
                "alternatives",
                []
            ),

        "phase_7_4_result":
            pit_window_result,

    }


# ============================================================
# COMPLETE SERVICE
# ============================================================

def run_strategy_explanation_engine(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute complete Phase 7.1 → 7.5 pipeline.
    """

    pit_window_result = (
        run_pit_window_optimizer(
            race_input
        )
    )


    return build_strategy_explanation_result(
        pit_window_result
    )


# ============================================================
# DISPLAY
# ============================================================

def display_strategy_explanation(
    result: Dict[str, Any]
) -> None:

    print(
        "\n" + "=" * 88
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.5 — AI STRATEGY EXPLANATION"
    )

    print(
        "=" * 88
    )


    print(
        f"Driver:              "
        f"{result.get('driver', '--')}"
    )


    print(
        f"Circuit:             "
        f"{result.get('circuit', '--')}"
    )


    print(
        f"Lap:                 "
        f"{result.get('current_lap', '--')}"
        f"/"
        f"{result.get('total_laps', '--')}"
    )


    print(
        f"Position:            "
        f"P{result.get('position', '--')}"
    )


    print(
        "-" * 88
    )


    print(
        f"FINAL RECOMMENDATION: "
        f"{result.get('final_recommendation', '--')}"
    )


    print(
        f"Recommended Tyre:     "
        f"{result.get('recommended_tyre', '--')}"
    )


    print(
        f"Confidence:           "
        f"{result.get('confidence', '--')}%"
    )


    print(
        f"Risk Level:           "
        f"{result.get('risk_level', '--')}"
    )


    print(
        "-" * 88
    )


    print(
        "STRATEGY SUMMARY"
    )


    print(
        "-" * 88
    )


    print(
        result.get(
            "summary",
            "--"
        )
    )


    print(
        "-" * 88
    )


    print(
        "ENGINEER EXPLANATION"
    )


    print(
        "-" * 88
    )


    print(
        result.get(
            "explanation",
            "--"
        )
    )


    print(
        "-" * 88
    )


    print(
        "PIT WINDOW"
    )


    print(
        "-" * 88
    )


    print(
        result.get(
            "pit_window_explanation",
            "--"
        )
    )


    print(
        "-" * 88
    )


    print(
        "KEY FACTORS"
    )


    print(
        "-" * 88
    )


    for factor in result.get(
        "key_factors",
        []
    ):

        unit = factor.get(
            "unit"
        )


        unit_text = (
            f" {unit}"
            if unit
            else ""
        )


        print(
            f"{factor.get('label')}: "
            f"{factor.get('value')}"
            f"{unit_text}"
        )


    warnings = result.get(
        "warnings",
        []
    )


    if warnings:

        print(
            "-" * 88
        )


        print(
            "STRATEGY WARNINGS"
        )


        print(
            "-" * 88
        )


        for warning in warnings:

            print(
                f"- {warning}"
            )


    print(
        "=" * 88
    )