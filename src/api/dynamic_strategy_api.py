"""
F1 AI STRATEGIST
PHASE 5.2 — DYNAMIC STRATEGY API

Purpose
-------
Expose the verified Phase 5.1 Dynamic Strategy Service
through a reusable backend API function.

Request
-------
Season
Grand Prix
Driver
Lap

        ↓

FastF1 Session

        ↓

Phase 5.1 Dynamic Strategy Service

        ↓

API-safe structured response
"""


from typing import Any, Dict

from src.data_loader import load_session

from src.strategy.dynamic_strategy_service import (
    run_dynamic_strategy_service
)


# ============================================================
# HELPERS
# ============================================================

def _safe_value(value):
    """
    Convert values into JSON-safe Python values.
    """

    if value is None:
        return None

    # NumPy / Pandas scalar support
    if hasattr(value, "item"):

        try:
            return value.item()

        except Exception:
            pass

    # Datetime-like support
    if hasattr(value, "isoformat"):

        try:
            return value.isoformat()

        except Exception:
            pass

    return value


def _json_safe(data):
    """
    Recursively convert dictionaries and lists
    into JSON-safe structures.
    """

    if isinstance(data, dict):

        return {
            str(key): _json_safe(value)
            for key, value in data.items()
        }

    if isinstance(data, (list, tuple)):

        return [
            _json_safe(value)
            for value in data
        ]

    return _safe_value(data)


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_dynamic_strategy_request(
    season,
    grand_prix,
    driver,
    lap
):
    """
    Validate Phase 5.2 API inputs.
    """

    try:

        season = int(season)

    except (TypeError, ValueError):

        raise ValueError(
            "season must be a valid integer."
        )

    if season < 2018:

        raise ValueError(
            "season must be 2018 or later."
        )

    if (
        grand_prix is None
        or not str(grand_prix).strip()
    ):

        raise ValueError(
            "grand_prix is required."
        )

    grand_prix = str(
        grand_prix
    ).strip()

    if (
        driver is None
        or not str(driver).strip()
    ):

        raise ValueError(
            "driver is required."
        )

    driver = (
        str(driver)
        .strip()
        .upper()
    )

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

    return {
        "season": season,
        "grand_prix": grand_prix,
        "driver": driver,
        "lap": lap
    }


# ============================================================
# BUILD API RESPONSE
# ============================================================

def build_dynamic_strategy_api_response(
    service_result: Dict[str, Any]
):
    """
    Convert the complete Phase 5.1 result into a
    frontend-friendly Phase 5.2 API response.
    """

    if not service_result:

        raise ValueError(
            "Phase 5.1 service result is empty."
        )


    # ========================================================
    # COMPLETE PHASE 4 OUTPUTS
    # ========================================================

    race_state = (
        service_result.get(
            "race_state"
        )
        or {}
    )

    race_situation = (
        service_result.get(
            "race_situation_analysis"
        )
        or {}
    )

    tyre_strategy = (
        service_result.get(
            "tyre_strategy"
        )
        or {}
    )

    pit_decision_result = (
        service_result.get(
            "pit_decision_result"
        )
        or {}
    )

    simulation = (
        service_result.get(
            "strategy_simulation"
        )
        or {}
    )

    scoring = (
        service_result.get(
            "strategy_scoring"
        )
        or {}
    )

    recommendation = (
        service_result.get(
            "ai_recommendation"
        )
        or {}
    )


    # ========================================================
    # RACE INFORMATION
    # ========================================================

    response = {

        # ----------------------------------------------------
        # API METADATA
        # ----------------------------------------------------

        "api":
            "dynamic_strategy",

        "phase":
            "5.2",

        "status":
            "SUCCESS",


        # ----------------------------------------------------
        # COMPACT RACE CONTEXT
        # ----------------------------------------------------

        "race": {

            "driver":
                service_result.get(
                    "driver"
                ),

            "lap":
                service_result.get(
                    "lap"
                ),

            "total_laps":
                service_result.get(
                    "total_laps"
                ),

            "laps_remaining":
                service_result.get(
                    "laps_remaining"
                ),

            "position":
                service_result.get(
                    "position"
                ),

            "current_tyre":
                service_result.get(
                    "current_tyre"
                ),

            "tyre_life":
                service_result.get(
                    "tyre_life"
                ),

            "recent_pace":
                service_result.get(
                    "recent_pace"
                ),

            "degradation_rate":
                service_result.get(
                    "degradation_rate"
                ),

            # ================================================
            # PHASE 4.1 ADDITIONAL DATA
            # ================================================

            "team":
                race_state.get(
                    "Team"
                ),

            "circuit":
                race_state.get(
                    "Circuit"
                ),

            "average_pace":
                race_state.get(
                    "AveragePace"
                ),

            "pit_stops_completed":
                race_state.get(
                    "PitStopsCompleted"
                ),

            "current_stint":
                race_state.get(
                    "CurrentStint"
                ),

            "current_stint_length":
                race_state.get(
                    "CurrentStintLength"
                )
        },


        # ----------------------------------------------------
        # STRATEGIC STATE
        # ----------------------------------------------------

        "strategy_state": {

            "race_situation":
                service_result.get(
                    "race_situation"
                ),

            "pit_decision":
                service_result.get(
                    "pit_decision"
                )
        },


        # ----------------------------------------------------
        # COMPLETE PIT DETAILS
        # PHASE 4.4
        # ----------------------------------------------------

        "pit_details": {

            "decision":
                (
                    pit_decision_result.get(
                        "decision"
                    )
                    or
                    pit_decision_result.get(
                        "action"
                    )
                ),

            "action":
                pit_decision_result.get(
                    "action"
                ),

            "recommended_tyre":
                pit_decision_result.get(
                    "recommended_tyre"
                ),

            "pit_loss":
                pit_decision_result.get(
                    "pit_loss"
                ),

            "pace_gain_per_lap":
                pit_decision_result.get(
                    "pace_gain_per_lap"
                ),

            "estimated_benefit":
                pit_decision_result.get(
                    "estimated_benefit"
                ),

            "traffic_penalty":
                pit_decision_result.get(
                    "traffic_penalty"
                ),

            "confidence":
                pit_decision_result.get(
                    "confidence"
                ),

            "reason":
                pit_decision_result.get(
                    "reason"
                ),

            "race_situation":
                pit_decision_result.get(
                    "race_situation"
                )
        },


        # ----------------------------------------------------
        # FINAL AI RECOMMENDATION
        # ----------------------------------------------------

        "recommendation": {

            "action":
                service_result.get(
                    "recommendation"
                ),

            "recommended_tyre":
                service_result.get(
                    "recommended_tyre"
                ),

            "confidence":
                service_result.get(
                    "confidence"
                ),

            "dynamic_score":
                service_result.get(
                    "dynamic_score"
                ),

            "reasoning":
                service_result.get(
                    "reasoning"
                )
        },


        # ----------------------------------------------------
        # COMPLETE PHASE OUTPUTS
        # ----------------------------------------------------

        "race_state":
            race_state,

        "race_situation_analysis":
            race_situation,

        "tyre_strategy":
            tyre_strategy,

        "simulation":
            simulation,

        "scoring":
            scoring,

        "ai_result":
            recommendation
    }


    return _json_safe(
        response
    )


# ============================================================
# PHASE 5.2 API SERVICE
# ============================================================

def get_dynamic_strategy(
    season,
    grand_prix,
    driver,
    lap
):
    """
    Execute the complete dynamic strategy request.

    Pipeline
    --------
    API Request
        ↓
    Load FastF1 Session
        ↓
    Phase 5.1 Service
        ↓
    Phase 5.2 API Response
    """

    request = validate_dynamic_strategy_request(
        season=season,
        grand_prix=grand_prix,
        driver=driver,
        lap=lap
    )


    # ========================================================
    # LOAD RACE SESSION
    # ========================================================

    session = load_session(
        season=request["season"],
        grand_prix=request["grand_prix"],
        session_type="R"
    )


    if session is None:

        raise RuntimeError(
            "Race session could not be loaded."
        )


    # ========================================================
    # RUN PHASE 5.1
    # ========================================================

    service_result = run_dynamic_strategy_service(
        session=session,
        driver=request["driver"],
        lap=request["lap"]
    )


    if not service_result:

        raise RuntimeError(
            "Phase 5.1 dynamic strategy service "
            "returned no result."
        )


    # ========================================================
    # BUILD PHASE 5.2 RESPONSE
    # ========================================================

    response = build_dynamic_strategy_api_response(
        service_result
    )


    # ========================================================
    # REQUEST METADATA
    # ========================================================

    response["request"] = {

        "season":
            request["season"],

        "grand_prix":
            request["grand_prix"],

        "driver":
            request["driver"],

        "lap":
            request["lap"]
    }


    return response


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_dynamic_strategy_api(
    result
):
    """
    Display Phase 5.2 API result.
    """

    if not result:

        print(
            "No Phase 5.2 API result available."
        )

        return


    race = result.get(
        "race",
        {}
    )

    state = result.get(
        "strategy_state",
        {}
    )

    pit = result.get(
        "pit_details",
        {}
    )

    recommendation = result.get(
        "recommendation",
        {}
    )

    request = result.get(
        "request",
        {}
    )


    print(
        "\n" + "=" * 76
    )

    print(
        "PHASE 5.2 — DYNAMIC STRATEGY API"
    )

    print(
        "=" * 76
    )


    print(
        f"Season: "
        f"{request.get('season')}"
    )

    print(
        f"Grand Prix: "
        f"{request.get('grand_prix')}"
    )

    print(
        f"Driver: "
        f"{race.get('driver')}"
    )

    print(
        f"Team: "
        f"{race.get('team')}"
    )

    print(
        f"Circuit: "
        f"{race.get('circuit')}"
    )

    print(
        f"Current Lap: "
        f"{race.get('lap')}/"
        f"{race.get('total_laps')}"
    )

    print(
        f"Laps Remaining: "
        f"{race.get('laps_remaining')}"
    )

    print(
        f"Position: "
        f"P{race.get('position')}"
    )

    print(
        f"Current Tyre: "
        f"{race.get('current_tyre')}"
    )

    print(
        f"Pit Stops: "
        f"{race.get('pit_stops_completed')}"
    )


    print(
        "-" * 76
    )


    print(
        f"Race Situation: "
        f"{state.get('race_situation')}"
    )

    print(
        f"Pit Decision: "
        f"{state.get('pit_decision')}"
    )

    print(
        f"Pit Loss: "
        f"{pit.get('pit_loss')}s"
    )

    print(
        f"Pace Gain / Lap: "
        f"{pit.get('pace_gain_per_lap')}s"
    )

    print(
        f"Traffic Penalty: "
        f"{pit.get('traffic_penalty')}s"
    )

    print(
        f"AI Recommendation: "
        f"{recommendation.get('action')}"
    )

    print(
        f"Recommended Tyre: "
        f"{recommendation.get('recommended_tyre')}"
    )

    print(
        f"Dynamic Score: "
        f"{recommendation.get('dynamic_score')}"
    )

    print(
        f"Confidence: "
        f"{recommendation.get('confidence')}%"
    )


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
        recommendation.get(
            "reasoning",
            "--"
        )
    )


    print(
        "=" * 76
    )