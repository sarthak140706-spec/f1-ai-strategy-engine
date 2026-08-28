"""
F1 AI STRATEGIST
PHASE 7.6 — AI STRATEGY ENGINEER FLASK API
"""

from __future__ import annotations

from typing import Any, Dict

from flask import Blueprint, current_app, jsonify, request


# ============================================================
# PHASE 7 IMPORTS
# ============================================================

from src.strategy_engineer.race_state_builder import (
    build_manual_race_state
)

from src.strategy_engineer.strategy_engineer_service import (
    run_strategy_engineer_service
)

from src.strategy_engineer.strategy_alternatives_engine import (
    run_strategy_alternatives_engine
)

from src.strategy_engineer.pit_window_optimizer import (
    run_pit_window_optimizer
)

from src.strategy_engineer.strategy_explanation_engine import (
    run_strategy_explanation_engine
)

from src.strategy_engineer.scenario_comparison import (
    ScenarioComparisonError,
    run_scenario_comparison,
    validate_scenario_comparison_contract
)


# ============================================================
# BLUEPRINT
# ============================================================

strategy_engineer_api = Blueprint(
    "strategy_engineer_api",
    __name__
)


# ============================================================
# CONSTANTS
# ============================================================

API_PHASE = "7.6"

API_NAME = "ai_strategy_engineer"

API_VERSION = "1.0"


# ============================================================
# RESPONSE HELPERS
# ============================================================

def _success_response(
    data: Dict[str, Any],
    status_code: int = 200
):

    return jsonify({

        "api": API_NAME,
        "phase": API_PHASE,
        "version": API_VERSION,
        "status": "SUCCESS",
        "data": data,

    }), status_code


def _error_response(
    message: str,
    status_code: int = 400,
    error_type: str = "VALIDATION_ERROR"
):

    return jsonify({

        "api": API_NAME,
        "phase": API_PHASE,
        "version": API_VERSION,
        "status": "ERROR",

        "error": {

            "type": error_type,
            "message": str(message),

        }

    }), status_code


# ============================================================
# JSON BODY
# ============================================================

def _get_json_body() -> Dict[str, Any]:

    data = request.get_json(
        silent=True
    )

    if not isinstance(
        data,
        dict
    ):

        raise ValueError(
            "Request body must contain a valid JSON object."
        )

    return data


# ============================================================
# FIELD HELPERS
# ============================================================

def _require_field(
    data: Dict[str, Any],
    field: str
) -> Any:

    if field not in data:

        raise ValueError(
            f"Missing required field: {field}"
        )


    value = data[field]


    if value is None:

        raise ValueError(
            f"Field '{field}' cannot be null."
        )


    if (
        isinstance(value, str)
        and
        not value.strip()
    ):

        raise ValueError(
            f"Field '{field}' cannot be empty."
        )


    return value


def _optional_field(
    data: Dict[str, Any],
    field: str,
    default: Any = None
) -> Any:

    return data.get(
        field,
        default
    )


def _as_int(
    value: Any,
    field: str
) -> int:

    try:

        numeric_value = float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        raise ValueError(
            f"Field '{field}' must be an integer."
        )


    if not numeric_value.is_integer():

        raise ValueError(
            f"Field '{field}' must be an integer."
        )


    return int(
        numeric_value
    )


def _as_float(
    value: Any,
    field: str
) -> float:

    try:

        return float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        raise ValueError(
            f"Field '{field}' must be numeric."
        )


def _as_optional_float(
    value: Any,
    field: str
):

    if value is None:

        return None


    if (
        isinstance(value, str)
        and
        not value.strip()
    ):

        return None


    return _as_float(
        value,
        field
    )


def _as_bool(
    value: Any,
    field: str
) -> bool:

    if isinstance(
        value,
        bool
    ):

        return value


    if isinstance(
        value,
        int
    ):

        if value == 1:
            return True

        if value == 0:
            return False


    if isinstance(
        value,
        str
    ):

        cleaned = (
            value
            .strip()
            .lower()
        )


        if cleaned in {
            "true",
            "yes",
            "1",
            "on",
        }:

            return True


        if cleaned in {
            "false",
            "no",
            "0",
            "off",
        }:

            return False


    raise ValueError(
        f"Field '{field}' must be boolean."
    )


# ============================================================
# NORMALIZE REQUEST
# ============================================================

def normalize_strategy_request(
    data: Dict[str, Any]
) -> Dict[str, Any]:

    driver = str(
        _require_field(
            data,
            "driver"
        )
    ).strip().upper()


    circuit = str(
        _require_field(
            data,
            "circuit"
        )
    ).strip()


    current_lap = _as_int(
        _require_field(
            data,
            "current_lap"
        ),
        "current_lap"
    )


    total_laps = _as_int(
        _require_field(
            data,
            "total_laps"
        ),
        "total_laps"
    )


    position = _as_int(
        _require_field(
            data,
            "position"
        ),
        "position"
    )


    current_tyre = str(
        _require_field(
            data,
            "tyre_compound"
        )
    ).strip().upper()


    tyre_age = _as_float(
        _require_field(
            data,
            "tyre_age"
        ),
        "tyre_age"
    )


    team = _optional_field(
        data,
        "team",
        None
    )


    grand_prix = _optional_field(
        data,
        "grand_prix",
        None
    )


    gap_ahead = _as_optional_float(
        _optional_field(
            data,
            "gap_ahead",
            None
        ),
        "gap_ahead"
    )


    gap_behind = _as_optional_float(
        _optional_field(
            data,
            "gap_behind",
            None
        ),
        "gap_behind"
    )


    recent_pace = _as_optional_float(
        _optional_field(
            data,
            "recent_pace",
            None
        ),
        "recent_pace"
    )


    average_pace = _as_optional_float(
        _optional_field(
            data,
            "average_pace",
            None
        ),
        "average_pace"
    )


    degradation_rate = _as_optional_float(
        _optional_field(
            data,
            "degradation_rate",
            None
        ),
        "degradation_rate"
    )


    weather = str(
        _optional_field(
            data,
            "weather",
            "DRY"
        )
    ).strip().upper()


    rainfall = _as_float(
        _optional_field(
            data,
            "rainfall",
            0.0
        ),
        "rainfall"
    )


    track_status = str(
        _optional_field(
            data,
            "track_status",
            "GREEN"
        )
    ).strip().upper()


    safety_car = _as_bool(
        _optional_field(
            data,
            "safety_car",
            False
        ),
        "safety_car"
    )


    virtual_safety_car = _as_bool(
        _optional_field(
            data,
            "virtual_safety_car",
            False
        ),
        "virtual_safety_car"
    )


    pit_stops_completed = _as_int(
        _optional_field(
            data,
            "pit_stops",
            0
        ),
        "pit_stops"
    )


    return {

        "driver":
            driver,

        "team":
            team,

        "grand_prix":
            grand_prix,

        "circuit":
            circuit,

        "current_lap":
            current_lap,

        "total_laps":
            total_laps,

        "position":
            position,

        "current_tyre":
            current_tyre,

        "tyre_age":
            tyre_age,

        "gap_ahead":
            gap_ahead,

        "gap_behind":
            gap_behind,

        "recent_pace":
            recent_pace,

        "average_pace":
            average_pace,

        "degradation_rate":
            degradation_rate,

        "weather":
            weather,

        "rainfall":
            rainfall,

        "track_status":
            track_status,

        "safety_car":
            safety_car,

        "virtual_safety_car":
            virtual_safety_car,

        "pit_stops_completed":
            pit_stops_completed,

    }



# ============================================================
# PHASE 7.8 REQUEST COMPATIBILITY
# ============================================================

def build_scenario_comparison_request(
    request_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build the canonical race-state dictionary expected by
    Phase 7.8.

    The Phase 7.6 API normalizer uses internal names such as
    `current_tyre` and `pit_stops_completed`, while the
    Phase 7.8 scenario engine deliberately consumes the public
    request contract used by `/api/engineer/analyse`.

    This helper validates the request through the existing
    Phase 7.6 normalizer and then maps it back to the canonical
    public field names required by the scenario engine.
    """

    normalized = normalize_strategy_request(
        request_data
    )


    return {

        "driver":
            normalized["driver"],

        "team":
            normalized.get(
                "team"
            ),

        "grand_prix":
            normalized.get(
                "grand_prix"
            ),

        "circuit":
            normalized["circuit"],

        "current_lap":
            normalized["current_lap"],

        "total_laps":
            normalized["total_laps"],

        "position":
            normalized["position"],

        "pit_stops":
            normalized.get(
                "pit_stops_completed",
                0
            ),

        "tyre_compound":
            normalized["current_tyre"],

        "tyre_age":
            normalized["tyre_age"],

        "recent_pace":
            normalized.get(
                "recent_pace"
            ),

        "average_pace":
            normalized.get(
                "average_pace"
            ),

        "degradation_rate":
            normalized.get(
                "degradation_rate"
            ),

        "gap_ahead":
            normalized.get(
                "gap_ahead"
            ),

        "gap_behind":
            normalized.get(
                "gap_behind"
            ),

        "weather":
            normalized.get(
                "weather",
                "DRY"
            ),

        "rainfall":
            normalized.get(
                "rainfall",
                0.0
            ),

        "track_status":
            normalized.get(
                "track_status",
                "GREEN"
            ),

        "safety_car":
            normalized.get(
                "safety_car",
                False
            ),

        "virtual_safety_car":
            normalized.get(
                "virtual_safety_car",
                False
            ),

    }


# ============================================================
# COMPLETE PHASE 7 PIPELINE
# ============================================================

def run_complete_strategy_engineer_pipeline(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:

    # ========================================================
    # 7.1
    # ========================================================

    race_state = (
        build_manual_race_state(
            race_input
        )
    )


    # ========================================================
    # 7.2
    # ========================================================

    strategy_engineer = (
        run_strategy_engineer_service(
            race_input
        )
    )


    # ========================================================
    # 7.3
    # ========================================================

    alternatives = (
        run_strategy_alternatives_engine(
            race_input
        )
    )


    # ========================================================
    # 7.4
    # ========================================================

    pit_window = (
        run_pit_window_optimizer(
            race_input
        )
    )


    # ========================================================
    # 7.5
    # ========================================================

    explanation = (
        run_strategy_explanation_engine(
            race_input
        )
    )


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "pipeline": {

            "phase_7_1":
                True,

            "phase_7_2":
                True,

            "phase_7_3":
                True,

            "phase_7_4":
                True,

            "phase_7_5":
                True,

            "phase_7_6":
                True,

        },

        "race_state":
            race_state,

        "strategy_engineer":
            strategy_engineer,

        "alternatives":
            alternatives,

        "pit_window":
            pit_window,

        "explanation":
            explanation,

    }


# ============================================================
# ROOT
# ============================================================

@strategy_engineer_api.route(
    "/",
    methods=["GET"]
)
def strategy_engineer_root():

    return _success_response({

        "component":
            "AI Strategy Engineer API",

        "live_timing_required":
            False,

        "endpoints": {

            "health":
                "/api/engineer/health",

            "race_state":
                "/api/engineer/race-state",

            "analyse":
                "/api/engineer/analyse",

            "what_if":
                "/api/engineer/what-if",

        }

    })


# ============================================================
# HEALTH
# ============================================================

@strategy_engineer_api.route(
    "/health",
    methods=["GET"]
)
def strategy_engineer_health():

    return _success_response({

        "component":
            "strategy_engineer_api",

        "operational":
            True,

        "live_timing_required":
            False,

        "phase_7_1":
            "AVAILABLE",

        "phase_7_2":
            "AVAILABLE",

        "phase_7_3":
            "AVAILABLE",

        "phase_7_4":
            "AVAILABLE",

        "phase_7_5":
            "AVAILABLE",

        "phase_7_6":
            "OPERATIONAL",

        "phase_7_8":
            "AVAILABLE",

    })


# ============================================================
# RACE STATE
# ============================================================

@strategy_engineer_api.route(
    "/race-state",
    methods=["POST"]
)
def preview_race_state():

    try:

        request_data = (
            _get_json_body()
        )


        race_input = (
            normalize_strategy_request(
                request_data
            )
        )


        race_state = (
            build_manual_race_state(
                race_input
            )
        )


        return _success_response({

            "request":
                race_input,

            "race_state":
                race_state,

        })


    except ValueError as exc:

        return _error_response(
            str(exc),
            400,
            "VALIDATION_ERROR"
        )


    except Exception as exc:

        return _error_response(
            str(exc),
            500,
            "RACE_STATE_ERROR"
        )


# ============================================================
# ANALYSE
# ============================================================

@strategy_engineer_api.route(
    "/analyse",
    methods=["POST"]
)
def analyse_strategy():

    try:

        request_data = (
            _get_json_body()
        )


        race_input = (
            normalize_strategy_request(
                request_data
            )
        )


        result = (
            run_complete_strategy_engineer_pipeline(
                race_input
            )
        )


        return _success_response({

            "request":
                race_input,

            "result":
                result,

        })


    except ValueError as exc:

        return _error_response(
            str(exc),
            400,
            "VALIDATION_ERROR"
        )


    except Exception as exc:

        return _error_response(
            str(exc),
            500,
            "STRATEGY_ENGINE_ERROR"
        )


# ============================================================
# WHAT-IF SCENARIO COMPARISON — PHASE 7.8
# ============================================================

@strategy_engineer_api.route(
    "/what-if",
    methods=["POST"]
)
def analyse_what_if_scenarios():
    """
    Execute the Phase 7.8 What-If Scenario Comparison Engine.

    Request body
    ------------
    Uses the same public race-state contract as:

        POST /api/engineer/analyse

    Optional custom scenarios may be supplied as:

        {
            ...race state fields...,
            "scenarios": [
                {
                    "name": "CUSTOM SCENARIO",
                    "description": "...",
                    "overrides": {
                        "degradation_rate": 0.12
                    }
                }
            ]
        }

    When `scenarios` is omitted, Phase 7.8 automatically
    generates its verified default scenario set.
    """

    try:

        request_data = (
            _get_json_body()
        )


        # ----------------------------------------------------
        # Optional custom scenarios
        # ----------------------------------------------------

        scenarios = request_data.get(
            "scenarios"
        )


        if (
            scenarios is not None
            and
            not isinstance(
                scenarios,
                list
            )
        ):

            raise ValueError(
                "Field 'scenarios' must be a list when provided."
            )


        # ----------------------------------------------------
        # Build validated Phase 7.8-compatible race input
        # ----------------------------------------------------

        race_input = (
            build_scenario_comparison_request(
                request_data
            )
        )


        # ----------------------------------------------------
        # Reuse the already registered Flask application.
        #
        # Phase 7.8 internally exercises the verified
        # /api/engineer/analyse endpoint for the base state and
        # for every hypothetical scenario. Passing a shared
        # test client avoids importing api.app again here.
        # ----------------------------------------------------

        strategy_client = (
            current_app.test_client()
        )


        result = (
            run_scenario_comparison(

                base_race_input=
                    race_input,

                scenarios=
                    scenarios,

                client=
                    strategy_client,

            )
        )


        validate_scenario_comparison_contract(
            result
        )


        return _success_response({

            "request":
                race_input,

            "result":
                result,

        })


    except (
        ScenarioComparisonError,
        ValueError
    ) as exc:

        return _error_response(
            str(exc),
            400,
            "SCENARIO_VALIDATION_ERROR"
        )


    except Exception as exc:

        return _error_response(
            str(exc),
            500,
            "SCENARIO_ENGINE_ERROR"
        )

