"""
F1 AI STRATEGIST
PHASE 6.7 — COMPLETE LIVE PIPELINE VERIFICATION

Purpose
-------
Perform final verification of the complete Phase 6
real-time strategy architecture.

Verified Pipeline
-----------------
6.1 Live Timing Client
        ↓
6.2 Live Data Parser
        ↓
6.3 Live Race-State Adapter
        ↓
6.4 Live Strategy Service
        ↓
6.5 Flask Live API
        ↓
6.6 Live Frontend Dashboard
        ↓
6.7 Complete Pipeline Verification

IMPORTANT
---------
This verification uses simulated live timing messages.

An active Formula One race is NOT required.

The purpose of this test is to confirm that the complete
Phase 6 architecture is internally consistent and that the
frontend/API/strategy layers are correctly connected.
"""


from pathlib import Path

from flask import Flask


# ============================================================
# PHASE 6.1
# LIVE TIMING CLIENT
# ============================================================

from src.live.live_timing_client import (
    F1LiveTimingClient,
    create_live_timing_client
)


# ============================================================
# PHASE 6.2
# LIVE DATA PARSER
# ============================================================

from src.live.live_data_parser import (
    F1LiveDataParser,
    create_live_data_parser
)


# ============================================================
# PHASE 6.3
# LIVE RACE-STATE ADAPTER
# ============================================================

from src.live.live_race_state_adapter import (
    build_live_race_state
)


# ============================================================
# PHASE 6.4
# LIVE STRATEGY SERVICE
# ============================================================

from src.live.live_strategy_service import (
    run_live_strategy_service
)


# ============================================================
# PHASE 6.5
# FLASK LIVE API
# ============================================================

from api.live_routes import (
    live_api,
    configure_live_api
)


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parent


FRONTEND_LIVE_HTML = (
    PROJECT_ROOT
    /
    "frontend"
    /
    "live.html"
)


# ============================================================
# DISPLAY HELPERS
# ============================================================

def print_header(
    title
):

    print(
        "\n" + "=" * 78
    )

    print(
        title
    )

    print(
        "=" * 78
    )


def print_success(
    text
):

    print(
        f"✅ {text}"
    )


# ============================================================
# SIMULATED LIVE MESSAGES
# ============================================================

def build_simulated_live_messages():
    """
    Build deterministic F1-style timing messages.

    Scenario
    --------
    Grand Prix:
        Belgian Grand Prix

    Driver:
        VER

    Lap:
        32 / 44

    Position:
        P1

    Tyre:
        HARD

    Tyre Age:
        14 laps
    """

    return [

        (
            "SessionInfo",

            {

                "Name":
                    "Race",

                "Type":
                    "Race",

                "Meeting": {

                    "Name":
                        "Belgian Grand Prix",

                    "OfficialName":
                        "FORMULA 1 BELGIAN GRAND PRIX",

                    "Location":
                        "Spa-Francorchamps",

                    "Country": {

                        "Name":
                            "Belgium",

                        "Code":
                            "BEL"

                    },

                    "Circuit": {

                        "ShortName":
                            "Spa-Francorchamps"

                    }

                }

            }

        ),


        (
            "SessionStatus",

            {

                "Status":
                    "Started"

            }

        ),


        (
            "LapCount",

            {

                "CurrentLap":
                    32,

                "TotalLaps":
                    44

            }

        ),


        (
            "DriverList",

            {

                "1": {

                    "RacingNumber":
                        "1",

                    "Tla":
                        "VER",

                    "FirstName":
                        "Max",

                    "LastName":
                        "Verstappen",

                    "FullName":
                        "Max Verstappen",

                    "BroadcastName":
                        "M VERSTAPPEN",

                    "TeamName":
                        "Red Bull Racing",

                    "TeamColour":
                        "3671C6"

                },


                "4": {

                    "RacingNumber":
                        "4",

                    "Tla":
                        "NOR",

                    "FirstName":
                        "Lando",

                    "LastName":
                        "Norris",

                    "FullName":
                        "Lando Norris",

                    "BroadcastName":
                        "L NORRIS",

                    "TeamName":
                        "McLaren",

                    "TeamColour":
                        "FF8700"

                }

            }

        ),


        (
            "TimingData",

            {

                "Lines": {

                    "1": {

                        "Position":
                            "1",

                        "NumberOfLaps":
                            32,

                        "GapToLeader":
                            "",

                        "IntervalToPositionAhead": {

                            "Value":
                                ""

                        },

                        "LastLapTime": {

                            "Value":
                                "1:48.512"

                        },

                        "BestLapTime": {

                            "Value":
                                "1:46.921"

                        },

                        "InPit":
                            False,

                        "PitOut":
                            False,

                        "Retired":
                            False,

                        "Stopped":
                            False

                    },


                    "4": {

                        "Position":
                            "2",

                        "NumberOfLaps":
                            32,

                        "GapToLeader":
                            "+3.481",

                        "IntervalToPositionAhead": {

                            "Value":
                                "+3.481"

                        },

                        "LastLapTime": {

                            "Value":
                                "1:48.104"

                        },

                        "BestLapTime": {

                            "Value":
                                "1:47.012"

                        },

                        "InPit":
                            False,

                        "PitOut":
                            False,

                        "Retired":
                            False,

                        "Stopped":
                            False

                    }

                }

            }

        ),


        (
            "TimingAppData",

            {

                "Lines": {

                    "1": {

                        "Stints": {

                            "0": {

                                "Compound":
                                    "MEDIUM",

                                "TotalLaps":
                                    18,

                                "StartLaps":
                                    0,

                                "New":
                                    "true"

                            },


                            "1": {

                                "Compound":
                                    "HARD",

                                "TotalLaps":
                                    14,

                                "StartLaps":
                                    18,

                                "New":
                                    "true"

                            }

                        }

                    },


                    "4": {

                        "Stints": {

                            "0": {

                                "Compound":
                                    "MEDIUM",

                                "TotalLaps":
                                    20,

                                "StartLaps":
                                    0,

                                "New":
                                    "true"

                            },


                            "1": {

                                "Compound":
                                    "HARD",

                                "TotalLaps":
                                    12,

                                "StartLaps":
                                    20,

                                "New":
                                    "true"

                            }

                        }

                    }

                }

            }

        ),


        (
            "WeatherData",

            {

                "AirTemp":
                    "21.4",

                "TrackTemp":
                    "31.8",

                "Humidity":
                    "61.0",

                "Pressure":
                    "970.2",

                "Rainfall":
                    "0",

                "WindDirection":
                    "210",

                "WindSpeed":
                    "2.7"

            }

        ),


        (
            "TrackStatus",

            {

                "Status":
                    "1",

                "Message":
                    "AllClear"

            }

        ),


        (
            "RaceControlMessages",

            {

                "Messages": {

                    "0": {

                        "Utc":
                            "2026-08-23T14:10:00Z",

                        "Lap":
                            30,

                        "Category":
                            "Flag",

                        "Flag":
                            "GREEN",

                        "Scope":
                            "Track",

                        "Message":
                            "GREEN LIGHT - PIT EXIT OPEN"

                    }

                }

            }

        )

    ]


# ============================================================
# BUILD PARSED LIVE STATE
# ============================================================

def build_parsed_live_state():
    """
    Build Phase 6.2 parsed live state using the actual
    F1LiveDataParser interface.
    """

    parser = create_live_data_parser()


    assert isinstance(
        parser,
        F1LiveDataParser
    )


    messages = (
        build_simulated_live_messages()
    )


    for topic, data in messages:

        parser.parse_message(
            topic,
            data
        )


    state = parser.get_state()


    assert isinstance(
        state,
        dict
    )


    assert state


    return (
        parser,
        state
    )


# ============================================================
# PHASE 6.1
# ============================================================

def verify_phase_6_1():

    print(
        "\n[6.1] Testing Live Timing Client..."
    )


    client = create_live_timing_client(

        output_file=(
            "data/live/"
            "phase6_verification_timing.txt"
        ),

        timeout=10,

        no_auth=False

    )


    assert isinstance(
        client,
        F1LiveTimingClient
    )


    client.validate_environment()


    status = client.get_status()


    assert isinstance(
        status,
        dict
    )


    assert (
        status.get(
            "phase"
        )
        ==
        "6.1"
    )


    assert (
        status.get(
            "component"
        )
        ==
        "live_timing_client"
    )


    assert (
        status.get(
            "fastf1_live_available"
        )
        is True
    )


    assert isinstance(
        status.get(
            "topics"
        ),
        list
    )


    required_topics = {

        "DriverList",

        "TimingData",

        "TimingAppData",

        "WeatherData",

        "TrackStatus",

        "RaceControlMessages",

        "LapCount"

    }


    assert required_topics.issubset(
        set(
            status.get(
                "topics",
                []
            )
        )
    )


    print_success(
        "6.1 PASSED — Live timing infrastructure available."
    )


    return client


# ============================================================
# PHASE 6.2
# ============================================================

def verify_phase_6_2():

    print(
        "\n[6.2] Testing Live Data Parser..."
    )


    parser, live_state = (
        build_parsed_live_state()
    )


    summary = parser.get_summary()


    assert (
        summary.get(
            "phase"
        )
        ==
        "6.2"
    )


    assert (
        summary.get(
            "component"
        )
        ==
        "live_data_parser"
    )


    assert (
        summary.get(
            "current_lap"
        )
        ==
        32
    )


    assert (
        summary.get(
            "total_laps"
        )
        ==
        44
    )


    assert (
        summary.get(
            "driver_count"
        )
        ==
        2
    )


    assert (
        summary.get(
            "timing_driver_count"
        )
        ==
        2
    )


    assert (
        summary.get(
            "tyre_driver_count"
        )
        ==
        2
    )


    driver_number = (
        parser.find_driver_number(
            "VER"
        )
    )


    assert (
        driver_number
        ==
        "1"
    )


    driver_state = (
        parser.get_driver_by_abbreviation(
            "VER"
        )
    )


    assert (
        driver_state[
            "driver"
        ][
            "abbreviation"
        ]
        ==
        "VER"
    )


    assert (
        driver_state[
            "timing"
        ][
            "position"
        ]
        ==
        1
    )


    assert (
        driver_state[
            "tyre"
        ][
            "compound"
        ]
        ==
        "HARD"
    )


    print_success(
        "6.2 PASSED — Live timing messages parsed successfully."
    )


    return (
        parser,
        live_state
    )


# ============================================================
# PHASE 6.3
# ============================================================

def verify_phase_6_3(
    live_state
):

    print(
        "\n[6.3] Testing Live Race-State Adapter..."
    )


    race_state = build_live_race_state(

        live_state=live_state,

        driver="VER"

    )


    assert isinstance(
        race_state,
        dict
    )


    assert (
        race_state.get(
            "Source"
        )
        ==
        "LIVE"
    )


    assert (
        race_state.get(
            "LiveData"
        )
        is True
    )


    assert (
        race_state.get(
            "Adapter"
        )
        ==
        "live_race_state_adapter"
    )


    assert (
        race_state.get(
            "Driver"
        )
        ==
        "VER"
    )


    assert (
        race_state.get(
            "CurrentLap"
        )
        ==
        32
    )


    assert (
        race_state.get(
            "TotalLaps"
        )
        ==
        44
    )


    assert (
        race_state.get(
            "LapsRemaining"
        )
        ==
        12
    )


    assert (
        race_state.get(
            "Position"
        )
        ==
        1
    )


    assert (
        race_state.get(
            "TyreCompound"
        )
        ==
        "HARD"
    )


    assert (
        race_state.get(
            "TyreLife"
        )
        ==
        14.0
    )


    assert (
        race_state.get(
            "RecentPace"
        )
        ==
        108.512
    )


    assert (
        race_state.get(
            "TrackStatus"
        )
        ==
        "GREEN"
    )


    assert (
        race_state.get(
            "WetConditions"
        )
        is False
    )


    required_fields = [

        "Driver",

        "CurrentLap",

        "TotalLaps",

        "LapsRemaining",

        "Position",

        "TyreCompound",

        "TyreLife",

        "RecentPace",

        "DegradationRate",

        "RaceProgress"

    ]


    for field in required_fields:

        assert (
            field
            in race_state
        ), (
            f"Missing Phase 6.3 field: {field}"
        )


    print_success(
        "6.3 PASSED — Live race state adapted successfully."
    )


    return race_state


# ============================================================
# PHASE 6.4
# ============================================================

def verify_phase_6_4(
    live_state
):

    print(
        "\n[6.4] Testing Live Strategy Service..."
    )


    result = run_live_strategy_service(

        live_state=live_state,

        driver="VER"

    )


    assert isinstance(
        result,
        dict
    )


    assert (
        result.get(
            "service"
        )
        ==
        "live_strategy_service"
    )


    assert (
        result.get(
            "phase"
        )
        ==
        "6.4"
    )


    assert (
        result.get(
            "status"
        )
        ==
        "SUCCESS"
    )


    assert (
        result.get(
            "source"
        )
        ==
        "LIVE"
    )


    assert (
        result.get(
            "live"
        )
        is True
    )


    assert (
        result.get(
            "driver"
        )
        ==
        "VER"
    )


    assert (
        result.get(
            "lap"
        )
        ==
        32
    )


    assert (
        result.get(
            "total_laps"
        )
        ==
        44
    )


    assert (
        result.get(
            "position"
        )
        ==
        1
    )


    assert (
        result.get(
            "current_tyre"
        )
        ==
        "HARD"
    )


    assert (
        result.get(
            "average_pace"
        )
        is not None
    )


    assert (
        result.get(
            "phase4_compatible"
        )
        is True
    )


    assert (
        result.get(
            "race_situation"
        )
        is not None
    )


    assert (
        result.get(
            "pit_decision"
        )
        is not None
    )


    assert (
        result.get(
            "recommendation"
        )
        is not None
    )


    assert (
        result.get(
            "recommended_tyre"
        )
        is not None
    )


    assert (
        result.get(
            "confidence"
        )
        is not None
    )


    assert (
        result.get(
            "dynamic_score"
        )
        is not None
    )


    assert (
        result.get(
            "reasoning"
        )
    )


    pipeline = result.get(
        "pipeline",
        {}
    )


    required_pipeline_steps = [

        "phase_6_3",

        "phase_4_2",

        "phase_4_3",

        "phase_4_4",

        "phase_4_5",

        "phase_4_6",

        "phase_4_7"

    ]


    for step in required_pipeline_steps:

        assert (
            step
            in pipeline
        ), (
            f"Missing Phase 6.4 pipeline step: "
            f"{step}"
        )


        assert pipeline[
            step
        ], (
            f"Empty Phase 6.4 pipeline result: "
            f"{step}"
        )


    print_success(
        "6.4 PASSED — Live race state executed through the complete AI strategy engine."
    )


    return result


# ============================================================
# PHASE 6.5
# ============================================================

def verify_phase_6_5(
    timing_client,
    parser
):

    print(
        "\n[6.5] Testing Flask Live API..."
    )


    configure_live_api(

        timing_client=timing_client,

        data_parser=parser

    )


    app = Flask(
        __name__
    )


    app.config[
        "TESTING"
    ] = True


    app.register_blueprint(
        live_api
    )


    client = app.test_client()


    # --------------------------------------------------------
    # ROOT
    # --------------------------------------------------------

    root_response = client.get(
        "/api/live"
    )


    assert (
        root_response.status_code
        ==
        200
    )


    root_data = (
        root_response.get_json()
    )


    assert (
        root_data.get(
            "phase"
        )
        ==
        "6.5"
    )


    assert (
        root_data.get(
            "status"
        )
        ==
        "SUCCESS"
    )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    status_response = client.get(
        "/api/live/status"
    )


    assert (
        status_response.status_code
        ==
        200
    )


    status_data = (
        status_response.get_json()
    )


    assert (
        status_data.get(
            "status"
        )
        ==
        "SUCCESS"
    )


    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    state_response = client.get(
        "/api/live/state"
    )


    assert (
        state_response.status_code
        ==
        200
    )


    state_data = (
        state_response.get_json()
    )


    assert isinstance(
        state_data.get(
            "state"
        ),
        dict
    )


    # --------------------------------------------------------
    # STRATEGY
    # --------------------------------------------------------

    strategy_response = client.get(
        "/api/live/strategy/VER"
    )


    assert (
        strategy_response.status_code
        ==
        200
    )


    strategy_data = (
        strategy_response.get_json()
    )


    assert (
        strategy_data.get(
            "api"
        )
        ==
        "live_strategy"
    )


    assert (
        strategy_data.get(
            "phase"
        )
        ==
        "6.5"
    )


    assert (
        strategy_data.get(
            "status"
        )
        ==
        "SUCCESS"
    )


    assert (
        strategy_data.get(
            "live"
        )
        is True
    )


    assert (
        strategy_data.get(
            "driver"
        )
        ==
        "VER"
    )


    race = strategy_data.get(
        "race",
        {}
    )


    strategy = strategy_data.get(
        "strategy",
        {}
    )


    assert (
        race.get(
            "lap"
        )
        ==
        32
    )


    assert (
        race.get(
            "total_laps"
        )
        ==
        44
    )


    assert (
        race.get(
            "position"
        )
        ==
        1
    )


    assert (
        race.get(
            "current_tyre"
        )
        ==
        "HARD"
    )


    assert (
        strategy.get(
            "recommendation"
        )
        is not None
    )


    assert (
        strategy.get(
            "recommended_tyre"
        )
        is not None
    )


    assert (
        strategy.get(
            "confidence"
        )
        is not None
    )


    assert (
        strategy.get(
            "dynamic_score"
        )
        is not None
    )


    assert (
        strategy.get(
            "reasoning"
        )
    )


    print_success(
        "6.5 PASSED — Flask live API returned HTTP 200 and complete live strategy data."
    )


    return strategy_data


# ============================================================
# PHASE 6.6
# ============================================================

def verify_phase_6_6():

    print(
        "\n[6.6] Testing Live Frontend Integration..."
    )


    assert FRONTEND_LIVE_HTML.exists(), (
        "frontend/live.html does not exist."
    )


    html = FRONTEND_LIVE_HTML.read_text(
        encoding="utf-8"
    )


    # --------------------------------------------------------
    # API CONNECTION
    # --------------------------------------------------------

    assert (
        "/api/live"
        in html
    )


    assert (
        "/strategy/"
        in html
    )


    assert (
        "/status"
        in html
    )


    # --------------------------------------------------------
    # AUTO REFRESH
    # --------------------------------------------------------

    assert (
        "setInterval"
        in html
    )


    assert (
        "5000"
        in html
    )


    assert (
        "loadLiveStrategy"
        in html
    )


    assert (
        "loadLiveStatus"
        in html
    )


    # --------------------------------------------------------
    # LIVE KPI CONTRACT
    # --------------------------------------------------------

    required_ids = [

        "driver",

        "raceDriver",

        "kpiLap",

        "kpiLapsRemaining",

        "kpiPosition",

        "kpiTyre",

        "kpiTyreLife",

        "kpiPace",

        "kpiPit",

        "kpiConfidence",

        "recommendation",

        "recommendedTyre",

        "overallScore",

        "recommendationReason",

        "simulationTable",

        "scoringTable",

        "comparisonGrid",

        "refreshButton",

        "autoRefreshButton",

        "statusDot",

        "statusText",

        "lastUpdated"

    ]


    for element_id in required_ids:

        assert (
            f'id="{element_id}"'
            in html
        ), (
            "Missing Phase 6.6 frontend element: "
            f"{element_id}"
        )


    # --------------------------------------------------------
    # LIVE FUNCTIONS
    # --------------------------------------------------------

    required_functions = [

        "normalizeLiveResponse",

        "renderLiveDashboard",

        "renderSimulation",

        "renderScoring",

        "renderComparison"

    ]


    for function_name in required_functions:

        assert (
            function_name
            in html
        ), (
            "Missing Phase 6.6 function: "
            f"{function_name}"
        )


    # --------------------------------------------------------
    # OLD HISTORICAL LIVE MODE MUST BE GONE
    # --------------------------------------------------------

    assert (
        "/api/dynamic-strategy/"
        not in html
    )


    forbidden_inputs = [

        'id="season"',

        'id="grandPrix"',

        'id="targetLap"',

        'id="session"'

    ]


    for forbidden in forbidden_inputs:

        assert (
            forbidden
            not in html
        ), (
            "Historical input still exists: "
            f"{forbidden}"
        )


    print_success(
        "6.6 PASSED — Live dashboard is connected to the Phase 6.5 API."
    )


# ============================================================
# PHASE 6.7
# COMPLETE CONSISTENCY
# ============================================================

def verify_phase_6_7(
    race_state,
    service_result,
    api_result
):

    print(
        "\n[6.7] Testing Complete Live Pipeline Consistency..."
    )


    # --------------------------------------------------------
    # LIVE SOURCE
    # --------------------------------------------------------

    assert (
        race_state.get(
            "Source"
        )
        ==
        "LIVE"
    )


    assert (
        service_result.get(
            "source"
        )
        ==
        "LIVE"
    )


    assert (
        service_result.get(
            "live"
        )
        is True
    )


    assert (
        api_result.get(
            "live"
        )
        is True
    )


    # --------------------------------------------------------
    # DRIVER
    # --------------------------------------------------------

    assert (
        race_state.get(
            "Driver"
        )
        ==
        service_result.get(
            "driver"
        )
        ==
        api_result.get(
            "driver"
        )
    )


    # --------------------------------------------------------
    # LAP
    # --------------------------------------------------------

    assert (
        race_state.get(
            "CurrentLap"
        )
        ==
        service_result.get(
            "lap"
        )
        ==
        api_result[
            "race"
        ][
            "lap"
        ]
    )


    assert (
        race_state.get(
            "TotalLaps"
        )
        ==
        service_result.get(
            "total_laps"
        )
        ==
        api_result[
            "race"
        ][
            "total_laps"
        ]
    )


    # --------------------------------------------------------
    # POSITION
    # --------------------------------------------------------

    assert (
        race_state.get(
            "Position"
        )
        ==
        service_result.get(
            "position"
        )
        ==
        api_result[
            "race"
        ][
            "position"
        ]
    )


    # --------------------------------------------------------
    # TYRE
    # --------------------------------------------------------

    assert (
        race_state.get(
            "TyreCompound"
        )
        ==
        service_result.get(
            "current_tyre"
        )
        ==
        api_result[
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
            "strategy"
        ][
            "recommendation"
        ]
    )


    assert (
        service_result.get(
            "recommended_tyre"
        )
        ==
        api_result[
            "strategy"
        ][
            "recommended_tyre"
        ]
    )


    assert (
        service_result.get(
            "dynamic_score"
        )
        ==
        api_result[
            "strategy"
        ][
            "dynamic_score"
        ]
    )


    assert (
        service_result.get(
            "confidence"
        )
        ==
        api_result[
            "strategy"
        ][
            "confidence"
        ]
    )


    # --------------------------------------------------------
    # REASONING
    # --------------------------------------------------------

    assert (
        service_result.get(
            "reasoning"
        )
    )


    assert (
        api_result[
            "strategy"
        ][
            "reasoning"
        ]
    )


    # --------------------------------------------------------
    # PHASE 4 PIPELINE
    # --------------------------------------------------------

    pipeline = service_result.get(
        "pipeline",
        {}
    )


    required_pipeline_steps = [

        "phase_6_3",

        "phase_4_2",

        "phase_4_3",

        "phase_4_4",

        "phase_4_5",

        "phase_4_6",

        "phase_4_7"

    ]


    for step in required_pipeline_steps:

        assert (
            step
            in pipeline
        )


    print_success(
        "6.7 PASSED — Complete live strategy architecture is consistent end-to-end."
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print_header(
        "F1 AI STRATEGIST\n"
        "PHASE 6.7 — COMPLETE LIVE PIPELINE VERIFICATION"
    )


    # ========================================================
    # 6.1
    # ========================================================

    timing_client = (
        verify_phase_6_1()
    )


    # ========================================================
    # 6.2
    # ========================================================

    parser, live_state = (
        verify_phase_6_2()
    )


    # ========================================================
    # 6.3
    # ========================================================

    race_state = (
        verify_phase_6_3(
            live_state
        )
    )


    # ========================================================
    # 6.4
    # ========================================================

    service_result = (
        verify_phase_6_4(
            live_state
        )
    )


    # ========================================================
    # 6.5
    # ========================================================

    api_result = (
        verify_phase_6_5(

            timing_client,

            parser

        )
    )


    # ========================================================
    # 6.6
    # ========================================================

    verify_phase_6_6()


    # ========================================================
    # 6.7
    # ========================================================

    verify_phase_6_7(

        race_state,

        service_result,

        api_result

    )


    # ========================================================
    # RESULTS
    # ========================================================

    print_header(
        "PHASE 6 VERIFICATION RESULTS"
    )


    print(
        "6.1 Live Timing Client          ✅"
    )

    print(
        "6.2 Live Data Parser            ✅"
    )

    print(
        "6.3 Live Race-State Adapter     ✅"
    )

    print(
        "6.4 Live Strategy Service       ✅"
    )

    print(
        "6.5 Flask Live API              ✅"
    )

    print(
        "6.6 Live Frontend Dashboard     ✅"
    )

    print(
        "6.7 Pipeline Verification       ✅"
    )


    print()


    print(
        "🏁 PHASE 6.7 VERIFICATION PASSED"
    )


    print()


    print(
        "✅ PHASE 6 — 100% COMPLETE"
    )


    print(
        "=" * 78
    )


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    main()