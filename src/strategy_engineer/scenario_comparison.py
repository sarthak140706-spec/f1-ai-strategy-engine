"""
F1 AI STRATEGIST
PHASE 7.8 — WHAT-IF SCENARIO COMPARISON ENGINE

Purpose
-------
Evaluate how the AI Strategy Engineer reacts when race
conditions change.

Examples
--------
What if degradation increases?
What if a Safety Car appears?
What if the gap behind becomes dangerous?
What if tyre condition improves?
What if weather changes?

Architecture
------------

Base Race State
        ↓
Phase 7.6 Strategy Engineer API
        ↓
Base Strategy Decision
        ↓
Apply Scenario Overrides
        ↓
Re-run Strategy Engineer API
        ↓
Compare Decisions
        ↓
Sensitivity Analysis
        ↓
Decision Stability

IMPORTANT
---------
Phase 7.8 does NOT modify:

7.1 Manual Race State
7.2 Strategy Engineer
7.3 Strategy Alternatives
7.4 Pit Window Optimizer
7.5 Explanation Engine
7.6 REST API
7.7 Frontend

It only consumes the already verified Phase 7 pipeline.
"""


from __future__ import annotations


from copy import deepcopy

from typing import (
    Any,
    Dict,
    List,
    Optional,
)


# ============================================================
# PHASE INFORMATION
# ============================================================

PHASE = "7.8"

COMPONENT = (
    "what_if_scenario_comparison_engine"
)


# ============================================================
# API ENDPOINT
# ============================================================

STRATEGY_ENGINEER_ENDPOINT = (
    "/api/engineer/analyse"
)


# ============================================================
# CUSTOM ERROR
# ============================================================

class ScenarioComparisonError(
    ValueError
):
    """
    Raised whenever Phase 7.8 receives invalid
    race-state or scenario information.
    """

    pass


# ============================================================
# BASIC HELPERS
# ============================================================

def _safe_dict(
    value: Any
) -> Dict[str, Any]:
    """
    Return value when it is a dictionary.
    Otherwise return an empty dictionary.
    """

    if isinstance(
        value,
        dict
    ):

        return value

    return {}


def _safe_list(
    value: Any
) -> List[Any]:
    """
    Return value when it is a list.
    Otherwise return an empty list.
    """

    if isinstance(
        value,
        list
    ):

        return value

    return []


def _first_value(
    data: Dict[str, Any],
    *keys: str,
    default: Any = None
) -> Any:
    """
    Return the first non-None value from
    the requested dictionary keys.
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


def _to_float(
    value: Any,
    default: Optional[float] = None
) -> Optional[float]:
    """
    Safely convert a value to float.
    """

    if value is None:

        return default


    try:

        return float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        return default


def _round_optional(
    value: Any,
    digits: int = 2
) -> Optional[float]:
    """
    Safely round numeric values.
    """

    number = _to_float(
        value
    )

    if number is None:

        return None


    return round(
        number,
        digits
    )


# ============================================================
# BASE RACE INPUT VALIDATION
# ============================================================

def validate_base_race_input(
    race_input: Dict[str, Any]
) -> None:
    """
    Validate the base Phase 7 race input.
    """

    if not isinstance(
        race_input,
        dict
    ):

        raise ScenarioComparisonError(

            "base_race_input must be a dictionary."

        )


    if not race_input:

        raise ScenarioComparisonError(

            "base_race_input cannot be empty."

        )


    required_fields = [

        "driver",
        "circuit",
        "current_lap",
        "total_laps",
        "position",
        "tyre_compound",
        "tyre_age",

    ]


    missing_fields = [

        field

        for field in required_fields

        if race_input.get(
            field
        )
        is None

    ]


    if missing_fields:

        raise ScenarioComparisonError(

            "Base race input is missing required fields: "
            +
            ", ".join(
                missing_fields
            )

        )


# ============================================================
# SCENARIO VALIDATION
# ============================================================

def validate_scenarios(
    scenarios: List[Dict[str, Any]]
) -> None:
    """
    Validate what-if scenario definitions.

    Expected format:

    {
        "name": "Higher Degradation",
        "description": "...",
        "overrides": {
            "degradation_rate": 0.12
        }
    }
    """

    if not isinstance(
        scenarios,
        list
    ):

        raise ScenarioComparisonError(

            "scenarios must be a list."

        )


    if not scenarios:

        raise ScenarioComparisonError(

            "At least one what-if scenario is required."

        )


    for index, scenario in enumerate(
        scenarios,
        start=1
    ):

        if not isinstance(
            scenario,
            dict
        ):

            raise ScenarioComparisonError(

                f"Scenario {index} must be a dictionary."

            )


        name = scenario.get(
            "name"
        )


        if (
            name is None
            or
            not str(
                name
            ).strip()
        ):

            raise ScenarioComparisonError(

                f"Scenario {index} requires a valid name."

            )


        overrides = scenario.get(
            "overrides"
        )


        if not isinstance(
            overrides,
            dict
        ):

            raise ScenarioComparisonError(

                f"Scenario '{name}' requires an "
                f"'overrides' dictionary."

            )


        if not overrides:

            raise ScenarioComparisonError(

                f"Scenario '{name}' does not contain "
                f"any race-state changes."

            )


# ============================================================
# CREATE FLASK TEST CLIENT
# ============================================================

def create_strategy_client():
    """
    Create an in-process Flask test client.

    Import is deliberately performed inside the function
    so Phase 7.8 does not create circular imports when the
    module itself is imported elsewhere.
    """

    from api.app import app


    app.config[
        "TESTING"
    ] = True


    return app.test_client()


# ============================================================
# CALL VERIFIED PHASE 7 API
# ============================================================

def run_strategy_request(
    race_input: Dict[str, Any],
    client=None
) -> Dict[str, Any]:
    """
    Submit one race state to the verified Phase 7.6
    Strategy Engineer endpoint.
    """

    validate_base_race_input(
        race_input
    )


    if client is None:

        client = (
            create_strategy_client()
        )


    response = client.post(

        STRATEGY_ENGINEER_ENDPOINT,

        json=race_input

    )


    try:

        response_data = (
            response.get_json()
        )

    except Exception as exc:

        raise RuntimeError(

            "Strategy Engineer API returned "
            "an invalid JSON response."

        ) from exc


    if response.status_code not in (
        200,
        201
    ):

        error_message = None


        if isinstance(
            response_data,
            dict
        ):

            error_message = (

                response_data.get(
                    "message"
                )

                or

                response_data.get(
                    "error"
                )

            )


        raise RuntimeError(

            error_message
            or
            (
                "Strategy Engineer API request failed "
                f"with HTTP {response.status_code}."
            )

        )


    if not isinstance(
        response_data,
        dict
    ):

        raise RuntimeError(

            "Strategy Engineer API returned "
            "an invalid response structure."

        )


    return response_data


# ============================================================
# EXTRACT COMPLETE PHASE 7 RESULT
# ============================================================

def extract_pipeline_result(
    response: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract:

        response
            ↓
        data
            ↓
        result

    from the Phase 7.6 API response.
    """

    response = _safe_dict(
        response
    )


    data = _safe_dict(
        response.get(
            "data"
        )
    )


    result = _safe_dict(
        data.get(
            "result"
        )
    )


    # --------------------------------------------------------
    # Compatibility fallback
    # --------------------------------------------------------

    if not result:

        result = _safe_dict(
            response.get(
                "result"
            )
        )


    if not result:

        raise RuntimeError(

            "Phase 7 pipeline result could not "
            "be extracted from API response."

        )


    return result


# ============================================================
# EXTRACT PIPELINE COMPONENTS
# ============================================================

def extract_race_state(
    pipeline: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract Phase 7.1 race state.
    """

    return _safe_dict(

        pipeline.get(
            "race_state"
        )

    )


def extract_strategy_engineer(
    pipeline: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract Phase 7.2 strategy-engineer output.
    """

    return _safe_dict(

        pipeline.get(
            "strategy_engineer"
        )

    )


def extract_alternatives(
    pipeline: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract Phase 7.3 alternatives result.
    """

    return _safe_dict(

        pipeline.get(
            "alternatives"
        )

    )


def extract_pit_window(
    pipeline: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract Phase 7.4 pit-window result.
    """

    return _safe_dict(

        pipeline.get(
            "pit_window"
        )

    )


def extract_explanation(
    pipeline: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract Phase 7.5 explanation result.
    """

    return _safe_dict(

        pipeline.get(
            "explanation"
        )

    )


# ============================================================
# EXTRACT FINAL DECISION
# ============================================================

def extract_final_decision(
    pipeline: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Produce a compact comparable representation of
    a complete Phase 7 strategy result.
    """

    race_state = extract_race_state(
        pipeline
    )


    engineer = extract_strategy_engineer(
        pipeline
    )


    alternatives = extract_alternatives(
        pipeline
    )


    pit_window = extract_pit_window(
        pipeline
    )


    explanation = extract_explanation(
        pipeline
    )


    # --------------------------------------------------------
    # FINAL RECOMMENDATION
    # --------------------------------------------------------

    recommendation = _first_value(

        explanation,

        "final_recommendation",
        "recommendation",

        default=None

    )


    if recommendation is None:

        recommendation = _first_value(

            engineer,

            "recommendation",
            "ai_recommendation",
            "final_recommendation",

            default="UNKNOWN"

        )


    recommendation = str(
        recommendation
    ).strip().upper()


    # --------------------------------------------------------
    # TYRE
    # --------------------------------------------------------

    recommended_tyre = _first_value(

        explanation,

        "recommended_tyre",

        default=None

    )


    if recommended_tyre is None:

        recommended_tyre = _first_value(

            engineer,

            "recommended_tyre",
            "tyre",
            "recommended_compound",

            default="UNKNOWN"

        )


    recommended_tyre = str(
        recommended_tyre
    ).strip().upper()


    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = _first_value(

        explanation,

        "confidence",
        "engineer_confidence",

        default=None

    )


    if confidence is None:

        confidence = _first_value(

            engineer,

            "confidence",

            default=None

        )


    confidence = _round_optional(
        confidence
    )


    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk = _first_value(

        explanation,

        "risk_level",
        "strategic_risk",

        default="UNKNOWN"

    )


    risk = str(
        risk
    ).strip().upper()


    # --------------------------------------------------------
    # RACE SITUATION
    # --------------------------------------------------------

    race_situation = _first_value(

        engineer,

        "race_situation",
        "situation",

        default="UNKNOWN"

    )


    race_situation = str(
        race_situation
    ).strip().upper()


    # --------------------------------------------------------
    # PIT DECISION
    # --------------------------------------------------------

    pit_decision = _first_value(

        engineer,

        "pit_decision",
        "pit_action",
        "pit_recommendation",

        default="UNKNOWN"

    )


    pit_decision = str(
        pit_decision
    ).strip().upper()


    # --------------------------------------------------------
    # PIT URGENCY
    # --------------------------------------------------------

    pit_urgency = _first_value(

        pit_window,

        "pit_urgency",
        "PitUrgency",

        default=None

    )


    pit_urgency = _round_optional(
        pit_urgency
    )


    # --------------------------------------------------------
    # RECOMMENDED PIT LAP
    # --------------------------------------------------------

    recommended_pit_lap = _first_value(

        pit_window,

        "recommended_pit_lap",
        "optimal_pit_lap",

        default=None

    )


    if recommended_pit_lap is not None:

        try:

            recommended_pit_lap = int(
                recommended_pit_lap
            )

        except (
            TypeError,
            ValueError
        ):

            recommended_pit_lap = None


    # --------------------------------------------------------
    # WINDOW CONFIDENCE
    # --------------------------------------------------------

    window_confidence = _first_value(

        pit_window,

        "window_confidence",
        "confidence",

        default=None

    )


    window_confidence = _round_optional(
        window_confidence
    )


    # --------------------------------------------------------
    # BEST STRATEGY
    # --------------------------------------------------------

    best_strategy = _first_value(

        alternatives,

        "best_strategy",
        "best_strategy_name",
        "recommended_strategy",

        default=None

    )


    if isinstance(
        best_strategy,
        dict
    ):

        best_strategy = _first_value(

            best_strategy,

            "strategy",
            "name",
            "display_name",

            default="UNKNOWN"

        )


    if best_strategy is None:

        best_strategy = recommendation


    best_strategy = str(
        best_strategy
    ).strip().upper()


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    dynamic_score = _first_value(

        engineer,

        "dynamic_score",
        "score",
        "strategy_score",

        default=None

    )


    dynamic_score = _round_optional(
        dynamic_score
    )


    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    return {

        "driver":
            race_state.get(
                "Driver"
            ),

        "circuit":
            race_state.get(
                "Circuit"
            ),

        "current_lap":
            race_state.get(
                "CurrentLap"
            ),

        "total_laps":
            race_state.get(
                "TotalLaps"
            ),

        "position":
            race_state.get(
                "Position"
            ),

        "current_tyre":
            race_state.get(
                "TyreCompound"
            ),

        "tyre_age":
            _first_value(

                race_state,

                "TyreAge",
                "TyreLife",

                default=None

            ),

        "degradation_rate":
            race_state.get(
                "DegradationRate"
            ),

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

        "recommendation":
            recommendation,

        "recommended_tyre":
            recommended_tyre,

        "confidence":
            confidence,

        "risk_level":
            risk,

        "race_situation":
            race_situation,

        "pit_decision":
            pit_decision,

        "pit_urgency":
            pit_urgency,

        "recommended_pit_lap":
            recommended_pit_lap,

        "window_confidence":
            window_confidence,

        "best_strategy":
            best_strategy,

        "dynamic_score":
            dynamic_score,

    }


# ============================================================
# APPLY WHAT-IF OVERRIDES
# ============================================================

def apply_scenario_overrides(
    base_race_input: Dict[str, Any],
    overrides: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a new race state without modifying
    the original race-state dictionary.
    """

    scenario_input = deepcopy(
        base_race_input
    )


    for key, value in overrides.items():

        scenario_input[
            key
        ] = value


    # --------------------------------------------------------
    # TRACK STATUS CONSISTENCY
    # --------------------------------------------------------

    safety_car = bool(

        scenario_input.get(
            "safety_car",
            False
        )

    )


    virtual_safety_car = bool(

        scenario_input.get(
            "virtual_safety_car",
            False
        )

    )


    # --------------------------------------------------------
    # SC and VSC can never be active simultaneously.
    # --------------------------------------------------------

    if (
        safety_car
        and
        virtual_safety_car
    ):

        raise ScenarioComparisonError(

            "Scenario cannot activate Safety Car "
            "and Virtual Safety Car simultaneously."

        )


    # --------------------------------------------------------
    # Automatically keep track-status consistent.
    # --------------------------------------------------------

    if safety_car:

        scenario_input[
            "track_status"
        ] = "SC"


    elif virtual_safety_car:

        scenario_input[
            "track_status"
        ] = "VSC"


    return scenario_input


# ============================================================
# DECISION DELTA
# ============================================================

def calculate_decision_delta(
    base_decision: Dict[str, Any],
    scenario_decision: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compare a scenario decision against the base
    Strategy Engineer decision.
    """

    base_confidence = _to_float(

        base_decision.get(
            "confidence"
        )

    )


    scenario_confidence = _to_float(

        scenario_decision.get(
            "confidence"
        )

    )


    confidence_delta = None


    if (
        base_confidence is not None
        and
        scenario_confidence is not None
    ):

        confidence_delta = round(

            scenario_confidence
            -
            base_confidence,

            2

        )


    base_score = _to_float(

        base_decision.get(
            "dynamic_score"
        )

    )


    scenario_score = _to_float(

        scenario_decision.get(
            "dynamic_score"
        )

    )


    score_delta = None


    if (
        base_score is not None
        and
        scenario_score is not None
    ):

        score_delta = round(

            scenario_score
            -
            base_score,

            2

        )


    base_urgency = _to_float(

        base_decision.get(
            "pit_urgency"
        )

    )


    scenario_urgency = _to_float(

        scenario_decision.get(
            "pit_urgency"
        )

    )


    urgency_delta = None


    if (
        base_urgency is not None
        and
        scenario_urgency is not None
    ):

        urgency_delta = round(

            scenario_urgency
            -
            base_urgency,

            2

        )


    base_lap = base_decision.get(
        "recommended_pit_lap"
    )


    scenario_lap = scenario_decision.get(
        "recommended_pit_lap"
    )


    pit_lap_delta = None


    if (
        base_lap is not None
        and
        scenario_lap is not None
    ):

        pit_lap_delta = (

            int(
                scenario_lap
            )

            -

            int(
                base_lap
            )

        )


    recommendation_changed = (

        base_decision.get(
            "recommendation"
        )

        !=

        scenario_decision.get(
            "recommendation"
        )

    )


    tyre_changed = (

        base_decision.get(
            "recommended_tyre"
        )

        !=

        scenario_decision.get(
            "recommended_tyre"
        )

    )


    risk_changed = (

        base_decision.get(
            "risk_level"
        )

        !=

        scenario_decision.get(
            "risk_level"
        )

    )


    pit_decision_changed = (

        base_decision.get(
            "pit_decision"
        )

        !=

        scenario_decision.get(
            "pit_decision"
        )

    )


    race_situation_changed = (

        base_decision.get(
            "race_situation"
        )

        !=

        scenario_decision.get(
            "race_situation"
        )

    )


    return {

        "recommendation_changed":
            recommendation_changed,

        "tyre_changed":
            tyre_changed,

        "risk_changed":
            risk_changed,

        "pit_decision_changed":
            pit_decision_changed,

        "race_situation_changed":
            race_situation_changed,

        "confidence_delta":
            confidence_delta,

        "dynamic_score_delta":
            score_delta,

        "pit_urgency_delta":
            urgency_delta,

        "pit_lap_delta":
            pit_lap_delta,

    }


# ============================================================
# SENSITIVITY SCORE
# ============================================================

def calculate_sensitivity_score(
    decision_delta: Dict[str, Any]
) -> float:
    """
    Calculate how strongly a scenario affected
    the AI strategy.

    Score range:
        0 → 100
    """

    score = 0.0


    # --------------------------------------------------------
    # Major strategic decision changed
    # --------------------------------------------------------

    if decision_delta.get(
        "recommendation_changed"
    ):

        score += 35.0


    # --------------------------------------------------------
    # Pit decision changed
    # --------------------------------------------------------

    if decision_delta.get(
        "pit_decision_changed"
    ):

        score += 20.0


    # --------------------------------------------------------
    # Recommended compound changed
    # --------------------------------------------------------

    if decision_delta.get(
        "tyre_changed"
    ):

        score += 15.0


    # --------------------------------------------------------
    # Risk changed
    # --------------------------------------------------------

    if decision_delta.get(
        "risk_changed"
    ):

        score += 10.0


    # --------------------------------------------------------
    # Race situation changed
    # --------------------------------------------------------

    if decision_delta.get(
        "race_situation_changed"
    ):

        score += 10.0


    # --------------------------------------------------------
    # Confidence movement
    # --------------------------------------------------------

    confidence_delta = _to_float(

        decision_delta.get(
            "confidence_delta"
        ),

        default=0.0

    )


    score += min(

        abs(
            confidence_delta
        )
        * 0.25,

        5.0

    )


    # --------------------------------------------------------
    # Pit urgency movement
    # --------------------------------------------------------

    urgency_delta = _to_float(

        decision_delta.get(
            "pit_urgency_delta"
        ),

        default=0.0

    )


    score += min(

        abs(
            urgency_delta
        )
        * 0.10,

        5.0

    )


    return round(

        min(
            100.0,
            score
        ),

        2

    )


# ============================================================
# SENSITIVITY LEVEL
# ============================================================

def classify_sensitivity(
    score: float
) -> str:
    """
    Convert numerical sensitivity into
    strategist-friendly classification.
    """

    score = float(
        score
    )


    if score >= 60:

        return "VERY HIGH"


    if score >= 40:

        return "HIGH"


    if score >= 20:

        return "MEDIUM"


    if score > 0:

        return "LOW"


    return "STABLE"


# ============================================================
# RUN SINGLE SCENARIO
# ============================================================

def run_single_scenario(
    base_race_input: Dict[str, Any],
    base_decision: Dict[str, Any],
    scenario: Dict[str, Any],
    client
) -> Dict[str, Any]:
    """
    Run one hypothetical race scenario.
    """

    scenario_name = str(

        scenario.get(
            "name"
        )

    ).strip()


    description = str(

        scenario.get(
            "description",
            ""
        )

    ).strip()


    overrides = deepcopy(

        scenario.get(
            "overrides",
            {}
        )

    )


    scenario_input = apply_scenario_overrides(

        base_race_input,

        overrides

    )


    api_response = run_strategy_request(

        scenario_input,

        client=client

    )


    pipeline = extract_pipeline_result(

        api_response

    )


    scenario_decision = extract_final_decision(

        pipeline

    )


    delta = calculate_decision_delta(

        base_decision,

        scenario_decision

    )


    sensitivity_score = (
        calculate_sensitivity_score(
            delta
        )
    )


    sensitivity_level = (
        classify_sensitivity(
            sensitivity_score
        )
    )


    return {

        "name":
            scenario_name,

        "description":
            description,

        "overrides":
            overrides,

        "decision":
            scenario_decision,

        "comparison":
            delta,

        "sensitivity_score":
            sensitivity_score,

        "sensitivity_level":
            sensitivity_level,

        "pipeline":
            pipeline,

    }


# ============================================================
# DECISION STABILITY
# ============================================================

def calculate_decision_stability(
    base_decision: Dict[str, Any],
    scenario_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Measure how frequently hypothetical scenarios retain
    the original strategy recommendation.
    """

    scenario_count = len(
        scenario_results
    )


    if scenario_count == 0:

        return {

            "scenario_count":
                0,

            "stable_scenarios":
                0,

            "changed_scenarios":
                0,

            "stability_percentage":
                100.0,

            "classification":
                "STABLE",

        }


    base_recommendation = (

        base_decision.get(
            "recommendation"
        )

    )


    stable_count = 0


    for scenario in scenario_results:

        decision = _safe_dict(

            scenario.get(
                "decision"
            )

        )


        if (
            decision.get(
                "recommendation"
            )
            ==
            base_recommendation
        ):

            stable_count += 1


    changed_count = (

        scenario_count
        -
        stable_count

    )


    stability_percentage = round(

        (
            stable_count
            /
            scenario_count
        )
        *
        100.0,

        2

    )


    if stability_percentage >= 80:

        classification = (
            "VERY STABLE"
        )


    elif stability_percentage >= 60:

        classification = (
            "STABLE"
        )


    elif stability_percentage >= 40:

        classification = (
            "MODERATELY SENSITIVE"
        )


    elif stability_percentage >= 20:

        classification = (
            "HIGHLY SENSITIVE"
        )


    else:

        classification = (
            "VERY HIGHLY SENSITIVE"
        )


    return {

        "scenario_count":
            scenario_count,

        "stable_scenarios":
            stable_count,

        "changed_scenarios":
            changed_count,

        "stability_percentage":
            stability_percentage,

        "classification":
            classification,

    }


# ============================================================
# RANK SCENARIOS BY STRATEGIC IMPACT
# ============================================================

def rank_scenario_sensitivity(
    scenario_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Rank scenarios from most strategically disruptive
    to least disruptive.
    """

    ranked = sorted(

        scenario_results,

        key=lambda item: float(

            item.get(
                "sensitivity_score",
                0.0
            )

        ),

        reverse=True

    )


    ranking = []


    for index, scenario in enumerate(
        ranked,
        start=1
    ):

        ranking.append({

            "rank":
                index,

            "scenario":
                scenario.get(
                    "name"
                ),

            "sensitivity_score":
                scenario.get(
                    "sensitivity_score"
                ),

            "sensitivity_level":
                scenario.get(
                    "sensitivity_level"
                ),

            "recommendation":
                _safe_dict(
                    scenario.get(
                        "decision"
                    )
                ).get(
                    "recommendation"
                ),

            "recommendation_changed":
                _safe_dict(
                    scenario.get(
                        "comparison"
                    )
                ).get(
                    "recommendation_changed"
                ),

        })


    return ranking


# ============================================================
# FIND MOST SENSITIVE SCENARIO
# ============================================================

def get_most_sensitive_scenario(
    ranked_scenarios: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Return scenario with largest strategic impact.
    """

    if not ranked_scenarios:

        return None


    return deepcopy(
        ranked_scenarios[0]
    )


# ============================================================
# DEFAULT WHAT-IF SCENARIOS
# ============================================================

def build_default_scenarios(
    base_race_input: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Generate useful default F1 what-if scenarios
    from the current race state.
    """

    validate_base_race_input(
        base_race_input
    )


    current_degradation = _to_float(

        base_race_input.get(
            "degradation_rate"
        ),

        default=0.08

    )


    current_tyre_age = _to_float(

        base_race_input.get(
            "tyre_age"
        ),

        default=0.0

    )


    gap_ahead = _to_float(

        base_race_input.get(
            "gap_ahead"
        ),

        default=2.0

    )


    gap_behind = _to_float(

        base_race_input.get(
            "gap_behind"
        ),

        default=2.0

    )


    return [

        {

            "name":
                "HIGHER TYRE DEGRADATION",

            "description":
                (
                    "Tests how the strategy changes if "
                    "the current tyre begins degrading "
                    "significantly faster."
                ),

            "overrides": {

                "degradation_rate":
                    round(
                        max(
                            current_degradation
                            * 1.6,
                            current_degradation
                            + 0.04
                        ),
                        3
                    ),

            },

        },


        {

            "name":
                "SAFETY CAR",

            "description":
                (
                    "Tests whether a Safety Car creates "
                    "an immediate strategic pit opportunity."
                ),

            "overrides": {

                "safety_car":
                    True,

                "virtual_safety_car":
                    False,

                "track_status":
                    "SC",

            },

        },


        {

            "name":
                "UNDERCUT THREAT",

            "description":
                (
                    "Simulates a rival closing rapidly "
                    "from behind and increasing the "
                    "risk of an undercut."
                ),

            "overrides": {

                "gap_behind":
                    round(
                        min(
                            gap_behind,
                            0.7
                        ),
                        2
                    ),

                "gap_ahead":
                    round(
                        min(
                            gap_ahead,
                            1.5
                        ),
                        2
                    ),

            },

        },


        {

            "name":
                "OLDER TYRES",

            "description":
                (
                    "Tests the effect of extending the "
                    "current stint several additional laps."
                ),

            "overrides": {

                "tyre_age":
                    round(
                        current_tyre_age
                        +
                        5.0,
                        1
                    ),

            },

        },


        {

            "name":
                "DAMP CONDITIONS",

            "description":
                (
                    "Tests how the strategy reacts when "
                    "light rainfall creates damp-track "
                    "conditions."
                ),

            "overrides": {

                "weather":
                    "DAMP",

                "rainfall":
                    0.8,

            },

        },

    ]


# ============================================================
# PHASE 7.8 MAIN ENGINE
# ============================================================

def run_scenario_comparison(
    base_race_input: Dict[str, Any],
    scenarios: Optional[
        List[
            Dict[str, Any]
        ]
    ] = None,
    client=None
) -> Dict[str, Any]:
    """
    Execute the complete Phase 7.8 What-If
    Scenario Comparison Engine.
    """

    # ========================================================
    # 1. VALIDATE BASE INPUT
    # ========================================================

    validate_base_race_input(
        base_race_input
    )


    # ========================================================
    # 2. BUILD DEFAULT SCENARIOS
    # ========================================================

    if scenarios is None:

        scenarios = (
            build_default_scenarios(
                base_race_input
            )
        )


    validate_scenarios(
        scenarios
    )


    # ========================================================
    # 3. CREATE SHARED API CLIENT
    # ========================================================

    if client is None:

        client = (
            create_strategy_client()
        )


    # ========================================================
    # 4. RUN BASE STRATEGY
    # ========================================================

    base_response = (
        run_strategy_request(

            base_race_input,

            client=client

        )
    )


    base_pipeline = (
        extract_pipeline_result(
            base_response
        )
    )


    base_decision = (
        extract_final_decision(
            base_pipeline
        )
    )


    # ========================================================
    # 5. RUN WHAT-IF SCENARIOS
    # ========================================================

    scenario_results = []


    for scenario in scenarios:

        result = run_single_scenario(

            base_race_input=
                base_race_input,

            base_decision=
                base_decision,

            scenario=
                scenario,

            client=
                client

        )


        scenario_results.append(
            result
        )


    # ========================================================
    # 6. DECISION STABILITY
    # ========================================================

    stability = (
        calculate_decision_stability(

            base_decision,

            scenario_results

        )
    )


    # ========================================================
    # 7. SENSITIVITY RANKING
    # ========================================================

    ranking = (
        rank_scenario_sensitivity(
            scenario_results
        )
    )


    # ========================================================
    # 8. MOST IMPORTANT SCENARIO
    # ========================================================

    most_sensitive = (
        get_most_sensitive_scenario(
            ranking
        )
    )


    # ========================================================
    # 9. PHASE 7.8 RESULT
    # ========================================================

    return {

        "phase":
            PHASE,

        "component":
            COMPONENT,

        "status":
            "SUCCESS",

        "base_input":
            deepcopy(
                base_race_input
            ),

        "base_decision":
            base_decision,

        "base_pipeline":
            base_pipeline,

        "scenario_count":
            len(
                scenario_results
            ),

        "scenarios":
            scenario_results,

        "sensitivity_ranking":
            ranking,

        "most_sensitive_scenario":
            most_sensitive,

        "decision_stability":
            stability,

        "pipeline": [

            "7.1 Manual Race-State Builder",

            "7.2 AI Strategy Engineer",

            "7.3 Strategy Alternatives",

            "7.4 Pit Window Optimizer",

            "7.5 Explanation & Confidence",

            "7.6 Strategy Engineer API",

            "7.8 What-If Scenario Comparison",

        ],

    }


# ============================================================
# PHASE 7.8 CONTRACT VALIDATION
# ============================================================

def validate_scenario_comparison_contract(
    result: Dict[str, Any]
) -> None:
    """
    Validate the Phase 7.8 result contract.
    """

    if not isinstance(
        result,
        dict
    ):

        raise RuntimeError(

            "Phase 7.8 result must be a dictionary."

        )


    required_fields = [

        "phase",

        "component",

        "status",

        "base_decision",

        "scenario_count",

        "scenarios",

        "sensitivity_ranking",

        "most_sensitive_scenario",

        "decision_stability",

        "pipeline",

    ]


    missing = [

        field

        for field in required_fields

        if field not in result

    ]


    if missing:

        raise RuntimeError(

            "Phase 7.8 result is missing fields: "
            +
            ", ".join(
                missing
            )

        )


    if result.get(
        "phase"
    ) != "7.8":

        raise RuntimeError(

            "Invalid Phase 7.8 identifier."

        )


    if result.get(
        "status"
    ) != "SUCCESS":

        raise RuntimeError(

            "Phase 7.8 did not return SUCCESS."

        )


    scenarios = result.get(
        "scenarios"
    )


    if not isinstance(
        scenarios,
        list
    ):

        raise RuntimeError(

            "Phase 7.8 scenarios must be a list."

        )


    if (
        result.get(
            "scenario_count"
        )
        !=
        len(
            scenarios
        )
    ):

        raise RuntimeError(

            "Scenario count does not match "
            "scenario results."

        )


# ============================================================
# DISPLAY PHASE 7.8
# ============================================================

def display_scenario_comparison(
    result: Dict[str, Any]
) -> None:
    """
    Display Phase 7.8 in console-friendly format.
    """

    validate_scenario_comparison_contract(
        result
    )


    base = _safe_dict(

        result.get(
            "base_decision"
        )

    )


    print(
        "\n"
        +
        "=" * 96
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.8 — WHAT-IF SCENARIO COMPARISON"
    )

    print(
        "=" * 96
    )


    print(
        f"Driver:                 "
        f"{base.get('driver') or '--'}"
    )

    print(
        f"Circuit:                "
        f"{base.get('circuit') or '--'}"
    )

    print(
        f"Lap:                    "
        f"{base.get('current_lap')}/"
        f"{base.get('total_laps')}"
    )

    print(
        f"Position:               "
        f"P{base.get('position')}"
    )

    print(
        "-" * 96
    )

    print(
        f"BASE RECOMMENDATION:     "
        f"{base.get('recommendation')}"
    )

    print(
        f"Recommended Tyre:        "
        f"{base.get('recommended_tyre')}"
    )

    print(
        f"Confidence:              "
        f"{base.get('confidence')}%"
    )

    print(
        f"Risk Level:              "
        f"{base.get('risk_level')}"
    )

    print(
        f"Pit Decision:            "
        f"{base.get('pit_decision')}"
    )

    print(
        f"Pit Urgency:             "
        f"{base.get('pit_urgency')}"
    )


    print(
        "-" * 96
    )

    print(
        "WHAT-IF SCENARIOS"
    )

    print(
        "-" * 96
    )


    print(

        f"{'RANK':<7}"
        f"{'SCENARIO':<29}"
        f"{'RECOMMENDATION':<19}"
        f"{'TYRE':<11}"
        f"{'RISK':<11}"
        f"{'SENSITIVITY':<14}"

    )


    print(
        "-" * 96
    )


    ranking_lookup = {

        item.get(
            "scenario"
        ):
            item.get(
                "rank"
            )

        for item in result.get(
            "sensitivity_ranking",
            []
        )

    }


    ordered_scenarios = sorted(

        result.get(
            "scenarios",
            []
        ),

        key=lambda item:

            ranking_lookup.get(
                item.get(
                    "name"
                ),
                999
            )

    )


    for scenario in ordered_scenarios:

        decision = _safe_dict(

            scenario.get(
                "decision"
            )

        )


        rank = ranking_lookup.get(

            scenario.get(
                "name"
            ),

            "--"

        )


        print(

            f"{str(rank):<7}"
            f"{str(scenario.get('name')):<29}"
            f"{str(decision.get('recommendation')):<19}"
            f"{str(decision.get('recommended_tyre')):<11}"
            f"{str(decision.get('risk_level')):<11}"
            f"{str(scenario.get('sensitivity_score')):<14}"

        )


    print(
        "-" * 96
    )


    stability = _safe_dict(

        result.get(
            "decision_stability"
        )

    )


    print(
        f"Decision Stability:      "
        f"{stability.get('stability_percentage')}%"
    )

    print(
        f"Stability Classification:"
        f" {stability.get('classification')}"
    )

    print(
        f"Stable Scenarios:        "
        f"{stability.get('stable_scenarios')}"
    )

    print(
        f"Changed Scenarios:       "
        f"{stability.get('changed_scenarios')}"
    )


    most_sensitive = _safe_dict(

        result.get(
            "most_sensitive_scenario"
        )

    )


    print(
        f"Most Sensitive Scenario: "
        f"{most_sensitive.get('scenario') or '--'}"
    )

    print(
        f"Maximum Sensitivity:     "
        f"{most_sensitive.get('sensitivity_score') or 0}/100"
    )


    print(
        "-" * 96
    )

    print(
        "STRATEGY PIPELINE"
    )

    print(
        "-" * 96
    )


    pipeline = result.get(
        "pipeline",
        []
    )


    for index, item in enumerate(
        pipeline
    ):

        print(
            item
        )

        if index < len(
            pipeline
        ) - 1:

            print(
                "        ↓"
            )


    print(
        "=" * 96
    )