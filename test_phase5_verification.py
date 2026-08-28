"""
F1 AI STRATEGIST
PHASE 5.5 — COMPLETE INTEGRATION VERIFICATION

Purpose
-------
Verify the complete Phase 5 dynamic strategy integration.

Verification Pipeline
---------------------

5.1 Dynamic Strategy Service
        ↓
5.2 Dynamic Strategy API
        ↓
5.3 Flask Dynamic Route
        ↓
5.4 Frontend Integration
        ↓
5.5 Complete Verification
"""


import json
from pathlib import Path


# ============================================================
# PHASE 5.1
# ============================================================

from src.data_loader import load_session

from src.strategy.dynamic_strategy_service import (
    run_dynamic_strategy_service
)


# ============================================================
# PHASE 5.2
# ============================================================

from src.api.dynamic_strategy_api import (
    get_dynamic_strategy
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain Grand Prix"

GRAND_PRIX_URL = "Bahrain_Grand_Prix"

DRIVER = "VER"

TARGET_LAP = 35


# ============================================================
# HELPER
# ============================================================

def section(title):

    print(
        "\n" +
        "=" * 78
    )

    print(
        title
    )

    print(
        "=" * 78
    )


def success(message):

    print(
        f"✅ {message}"
    )


# ============================================================
# FLASK APP LOADER
# ============================================================

def get_flask_app():
    """
    Load Flask application while supporting either:

        app = Flask(...)

    or

        create_app()
    """

    import api.app as api_app_module


    # --------------------------------------------------------
    # DIRECT APP
    # --------------------------------------------------------

    flask_app = getattr(
        api_app_module,
        "app",
        None
    )


    if flask_app is not None:

        return flask_app


    # --------------------------------------------------------
    # APP FACTORY
    # --------------------------------------------------------

    create_app = getattr(
        api_app_module,
        "create_app",
        None
    )


    if callable(
        create_app
    ):

        return create_app()


    raise RuntimeError(
        "Unable to find Flask app or create_app() "
        "inside api/app.py."
    )


# ============================================================
# MAIN VERIFICATION
# ============================================================

def main():

    section(
        "F1 AI STRATEGIST\n"
        "PHASE 5.5 — COMPLETE INTEGRATION VERIFICATION"
    )


    results = {

        "5.1 Dynamic Service":
            False,

        "5.2 Dynamic API":
            False,

        "5.3 Flask Route":
            False,

        "5.4 Frontend Integration":
            False,

        "5.5 Pipeline Verification":
            False

    }


    # ========================================================
    # 5.1
    # DYNAMIC STRATEGY SERVICE
    # ========================================================

    print(
        "\n[5.1] Testing Dynamic Strategy Service..."
    )


    session = load_session(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        session_type="R"

    )


    assert session is not None, (
        "5.1 failed: session was not loaded."
    )


    service_result = (
        run_dynamic_strategy_service(

            session=session,

            driver=DRIVER,

            lap=TARGET_LAP

        )
    )


    assert service_result, (
        "5.1 failed: service returned empty result."
    )


    assert (
        service_result.get(
            "status"
        )
        ==
        "SUCCESS"
    ), (
        "5.1 failed: service status is not SUCCESS."
    )


    assert (
        service_result.get(
            "lap"
        )
        ==
        TARGET_LAP
    ), (
        "5.1 failed: incorrect dynamic lap."
    )


    assert (
        service_result.get(
            "driver"
        )
        ==
        DRIVER
    ), (
        "5.1 failed: incorrect driver."
    )


    assert (
        service_result.get(
            "race_state"
        )
    ), (
        "5.1 failed: race state missing."
    )


    assert (
        service_result.get(
            "strategy_simulation"
        )
    ), (
        "5.1 failed: simulation missing."
    )


    assert (
        service_result.get(
            "strategy_scoring"
        )
    ), (
        "5.1 failed: scoring missing."
    )


    assert (
        service_result.get(
            "ai_recommendation"
        )
    ), (
        "5.1 failed: AI recommendation missing."
    )


    results[
        "5.1 Dynamic Service"
    ] = True


    success(
        "5.1 PASSED — Complete Phase 4 pipeline "
        "executed through unified service."
    )


    # ========================================================
    # 5.2
    # DYNAMIC STRATEGY API
    # ========================================================

    print(
        "\n[5.2] Testing Dynamic Strategy API..."
    )


    api_result = (
        get_dynamic_strategy(

            season=SEASON,

            grand_prix=GRAND_PRIX,

            driver=DRIVER,

            lap=TARGET_LAP

        )
    )


    assert api_result, (
        "5.2 failed: API returned empty result."
    )


    assert (
        api_result.get(
            "api"
        )
        ==
        "dynamic_strategy"
    ), (
        "5.2 failed: incorrect API identifier."
    )


    assert (
        api_result.get(
            "phase"
        )
        ==
        "5.2"
    ), (
        "5.2 failed: incorrect API phase."
    )


    assert (
        api_result.get(
            "status"
        )
        ==
        "SUCCESS"
    ), (
        "5.2 failed: API status is not SUCCESS."
    )


    # --------------------------------------------------------
    # JSON SERIALIZATION
    # --------------------------------------------------------

    json.dumps(
        api_result
    )


    race = (
        api_result.get(
            "race"
        )
        or {}
    )


    recommendation = (
        api_result.get(
            "recommendation"
        )
        or {}
    )


    pit_details = (
        api_result.get(
            "pit_details"
        )
        or {}
    )


    simulation = (
        api_result.get(
            "simulation"
        )
        or {}
    )


    scoring = (
        api_result.get(
            "scoring"
        )
        or {}
    )


    assert (
        race.get(
            "lap"
        )
        ==
        TARGET_LAP
    )


    assert (
        race.get(
            "total_laps"
        )
        is not None
    )


    assert (
        race.get(
            "position"
        )
        is not None
    )


    assert (
        race.get(
            "current_tyre"
        )
        is not None
    )


    # ========================================================
    # NEW 5.4 FIELD CONTRACT
    # ========================================================

    assert (
        race.get(
            "team"
        )
        is not None
    ), (
        "5.2 failed: team is missing."
    )


    assert (
        race.get(
            "circuit"
        )
        is not None
    ), (
        "5.2 failed: circuit is missing."
    )


    assert (
        race.get(
            "average_pace"
        )
        is not None
    ), (
        "5.2 failed: average pace is missing."
    )


    assert (
        race.get(
            "pit_stops_completed"
        )
        is not None
    ), (
        "5.2 failed: pit-stop count is missing."
    )


    assert (
        pit_details.get(
            "pit_loss"
        )
        is not None
    ), (
        "5.2 failed: pit loss missing."
    )


    assert (
        pit_details.get(
            "pace_gain_per_lap"
        )
        is not None
    ), (
        "5.2 failed: pace gain missing."
    )


    assert (
        pit_details.get(
            "traffic_penalty"
        )
        is not None
    ), (
        "5.2 failed: traffic penalty missing."
    )


    assert (
        pit_details.get(
            "confidence"
        )
        is not None
    ), (
        "5.2 failed: pit confidence missing."
    )


    assert (
        recommendation.get(
            "action"
        )
        is not None
    )


    assert (
        recommendation.get(
            "recommended_tyre"
        )
        is not None
    )


    assert (
        recommendation.get(
            "dynamic_score"
        )
        is not None
    )


    assert (
        recommendation.get(
            "confidence"
        )
        is not None
    )


    simulation_strategies = (
        simulation.get(
            "strategies"
        )
        or []
    )


    scoring_strategies = (
        scoring.get(
            "strategies"
        )
        or []
    )


    assert (
        len(
            simulation_strategies
        )
        ==
        4
    ), (
        "5.2 failed: expected 4 simulated strategies."
    )


    assert (
        len(
            scoring_strategies
        )
        ==
        4
    ), (
        "5.2 failed: expected 4 scored strategies."
    )


    results[
        "5.2 Dynamic API"
    ] = True


    success(
        "5.2 PASSED — Complete frontend-ready "
        "dynamic API contract verified."
    )


    # ========================================================
    # 5.3
    # FLASK ROUTE
    # ========================================================

    print(
        "\n[5.3] Testing Flask Dynamic Strategy Route..."
    )


    flask_app = (
        get_flask_app()
    )


    flask_app.config[
        "TESTING"
    ] = True


    client = (
        flask_app.test_client()
    )


    endpoint = (

        f"/api/dynamic-strategy/"
        f"{SEASON}/"
        f"{GRAND_PRIX_URL}/"
        f"{DRIVER}/"
        f"{TARGET_LAP}"

    )


    print(
        f"Endpoint: {endpoint}"
    )


    response = (
        client.get(
            endpoint
        )
    )


    print(
        f"HTTP Status: "
        f"{response.status_code}"
    )


    assert (
        response.status_code
        ==
        200
    ), (
        f"5.3 failed: HTTP "
        f"{response.status_code}"
    )


    route_data = (
        response.get_json()
    )


    assert route_data, (
        "5.3 failed: Flask returned no JSON."
    )


    assert (
        route_data.get(
            "status"
        )
        ==
        "SUCCESS"
    )


    assert (
        route_data.get(
            "api"
        )
        ==
        "dynamic_strategy"
    )


    route_race = (
        route_data.get(
            "race"
        )
        or {}
    )


    route_pit = (
        route_data.get(
            "pit_details"
        )
        or {}
    )


    route_recommendation = (
        route_data.get(
            "recommendation"
        )
        or {}
    )


    assert (
        route_race.get(
            "lap"
        )
        ==
        TARGET_LAP
    )


    assert (
        route_race.get(
            "team"
        )
        is not None
    )


    assert (
        route_race.get(
            "pit_stops_completed"
        )
        is not None
    )


    assert (
        route_pit.get(
            "pace_gain_per_lap"
        )
        is not None
    )


    assert (
        route_pit.get(
            "traffic_penalty"
        )
        is not None
    )


    assert (
        route_recommendation.get(
            "action"
        )
        is not None
    )


    assert (
        len(
            route_data
            .get(
                "simulation",
                {}
            )
            .get(
                "strategies",
                []
            )
        )
        ==
        4
    )


    assert (
        len(
            route_data
            .get(
                "scoring",
                {}
            )
            .get(
                "strategies",
                []
            )
        )
        ==
        4
    )


    results[
        "5.3 Flask Route"
    ] = True


    success(
        "5.3 PASSED — HTTP 200 and complete "
        "dynamic JSON response received."
    )


    # ========================================================
    # 5.4
    # FRONTEND INTEGRATION CONTRACT
    # ========================================================

    print(
        "\n[5.4] Testing Frontend Dynamic Integration..."
    )


    frontend_path = Path(
        "frontend/live.html"
    )


    assert (
        frontend_path.exists()
    ), (
        "5.4 failed: frontend/live.html not found."
    )


    frontend = (
        frontend_path.read_text(
            encoding="utf-8"
        )
    )


    # --------------------------------------------------------
    # TARGET LAP CONTROL
    # --------------------------------------------------------

    assert (
        'id="targetLap"'
        in frontend
    ), (
        "5.4 failed: target lap input missing."
    )


    # --------------------------------------------------------
    # NEW API ENDPOINT
    # --------------------------------------------------------

    assert (
        "/dynamic-strategy/"
        in frontend
    ), (
        "5.4 failed: dynamic endpoint missing."
    )


    # --------------------------------------------------------
    # REQUIRED DASHBOARD ELEMENTS
    # --------------------------------------------------------

    required_frontend_ids = [

        'id="stateTeam"',

        'id="statePitStops"',

        'id="paceGain"',

        'id="trafficPenalty"',

        'id="simulationTable"',

        'id="scoringTable"',

        'id="recommendation"',

        'id="recommendationConfidence"'

    ]


    for element_id in (
        required_frontend_ids
    ):

        assert (
            element_id
            in frontend
        ), (
            f"5.4 failed: "
            f"{element_id} missing."
        )


    # --------------------------------------------------------
    # REQUIRED DATA MAPPINGS
    # --------------------------------------------------------

    required_mappings = [

        "pit_details",

        "pace_gain_per_lap",

        "traffic_penalty",

        "pit_stops_completed",

        "dynamic_overall_score",

        "projected_total_time",

        "strategy_comparison"

    ]


    for mapping in (
        required_mappings
    ):

        assert (
            mapping
            in frontend
        ), (
            f"5.4 failed: frontend mapping "
            f"'{mapping}' missing."
        )


    results[
        "5.4 Frontend Integration"
    ] = True


    success(
        "5.4 PASSED — Dynamic frontend data "
        "contract is correctly connected."
    )


    # ========================================================
    # 5.5
    # END-TO-END CONSISTENCY
    # ========================================================

    print(
        "\n[5.5] Testing Complete Pipeline Consistency..."
    )


    # --------------------------------------------------------
    # DRIVER
    # --------------------------------------------------------

    assert (
        service_result.get(
            "driver"
        )
        ==
        api_result[
            "race"
        ][
            "driver"
        ]
        ==
        route_data[
            "race"
        ][
            "driver"
        ]
        ==
        DRIVER
    )


    # --------------------------------------------------------
    # LAP
    # --------------------------------------------------------

    assert (
        service_result.get(
            "lap"
        )
        ==
        api_result[
            "race"
        ][
            "lap"
        ]
        ==
        route_data[
            "race"
        ][
            "lap"
        ]
        ==
        TARGET_LAP
    )


    # --------------------------------------------------------
    # POSITION
    # --------------------------------------------------------

    assert (
        service_result.get(
            "position"
        )
        ==
        api_result[
            "race"
        ][
            "position"
        ]
        ==
        route_data[
            "race"
        ][
            "position"
        ]
    )


    # --------------------------------------------------------
    # TYRE
    # --------------------------------------------------------

    assert (
        service_result.get(
            "current_tyre"
        )
        ==
        api_result[
            "race"
        ][
            "current_tyre"
        ]
        ==
        route_data[
            "race"
        ][
            "current_tyre"
        ]
    )


    # --------------------------------------------------------
    # RECOMMENDATION
    # --------------------------------------------------------

    assert (
        service_result.get(
            "recommendation"
        )
        ==
        api_result[
            "recommendation"
        ][
            "action"
        ]
        ==
        route_data[
            "recommendation"
        ][
            "action"
        ]
    )


    # --------------------------------------------------------
    # RECOMMENDED TYRE
    # --------------------------------------------------------

    assert (
        service_result.get(
            "recommended_tyre"
        )
        ==
        api_result[
            "recommendation"
        ][
            "recommended_tyre"
        ]
        ==
        route_data[
            "recommendation"
        ][
            "recommended_tyre"
        ]
    )


    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    assert (
        float(
            service_result.get(
                "dynamic_score"
            )
        )
        ==
        float(
            api_result[
                "recommendation"
            ][
                "dynamic_score"
            ]
        )
        ==
        float(
            route_data[
                "recommendation"
            ][
                "dynamic_score"
            ]
        )
    )


    # --------------------------------------------------------
    # BAHRAIN LAP 35 KNOWN BEHAVIOUR
    # --------------------------------------------------------

    assert (
        route_data[
            "recommendation"
        ][
            "action"
        ]
        ==
        "STAY OUT"
    ), (
        "Expected Bahrain lap-35 "
        "recommendation to remain STAY OUT."
    )


    assert (
        route_data[
            "recommendation"
        ][
            "recommended_tyre"
        ]
        ==
        "HARD"
    ), (
        "Expected Bahrain lap-35 "
        "recommended tyre to remain HARD."
    )


    assert (
        route_data[
            "race"
        ][
            "position"
        ]
        ==
        1
    )


    assert (
        route_data[
            "race"
        ][
            "laps_remaining"
        ]
        ==
        22
    )


    results[
        "5.5 Pipeline Verification"
    ] = True


    success(
        "5.5 PASSED — Complete dynamic strategy "
        "pipeline is consistent end-to-end."
    )


    # ========================================================
    # FINAL RESULTS
    # ========================================================

    section(
        "PHASE 5 VERIFICATION RESULTS"
    )


    for step, passed in (
        results.items()
    ):

        symbol = (
            "✅"
            if passed
            else "❌"
        )

        print(
            f"{step:<32} {symbol}"
        )


    # ========================================================
    # COMPLETE
    # ========================================================

    assert all(
        results.values()
    )


    print(
        "\n🏁 PHASE 5.5 VERIFICATION PASSED"
    )


    print(
        "\n✅ PHASE 5 — 100% COMPLETE"
    )


    print(
        "=" * 78
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()