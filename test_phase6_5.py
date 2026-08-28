"""
F1 AI STRATEGIST
PHASE 6.5 — FLASK LIVE API TEST
"""


from flask import Flask


from api.live_routes import (
    live_api,
    configure_live_api
)


# ============================================================
# MOCK PHASE 6.1 CLIENT
# ============================================================

class MockLiveTimingClient:

    def __init__(self):

        self.connected = True

        self.running = True

        self.messages_received = 128

        self.connection_error = None


    def get_status(self):

        return {

            "connected":
                True,

            "running":
                True,

            "background_thread":
                True,

            "messages_received":
                128,

            "connection_error":
                None

        }


# ============================================================
# MOCK PHASE 6.2 PARSER
# ============================================================

class MockLiveDataParser:

    def __init__(self):

        self.state = self._build_state()


    def _build_state(self):

        return {

            "phase":
                "6.2",

            "component":
                "live_data_parser",

            "live_data":
                True,

            "message_count":
                9,

            "last_update":
                "2026-08-23T14:10:00Z",

            "last_topic":
                "RaceControlMessages",


            # ====================================================
            # SESSION
            # ====================================================

            "session": {

                "name":
                    "Race",

                "type":
                    "Race",

                "meeting_name":
                    "Belgian Grand Prix",

                "official_name":
                    "FORMULA 1 BELGIAN GRAND PRIX",

                "location":
                    "Spa-Francorchamps",

                "country":
                    "Belgium",

                "country_code":
                    "BEL",

                "circuit_name":
                    "Spa-Francorchamps"

            },


            # ====================================================
            # SESSION STATUS
            # ====================================================

            "session_status": {

                "status":
                    "Started"

            },


            # ====================================================
            # LAP COUNT
            # ====================================================

            "lap_count": {

                "current_lap":
                    32,

                "total_laps":
                    44

            },


            # ====================================================
            # DRIVERS
            # ====================================================

            "drivers": {

                "1": {

                    "driver_number":
                        "1",

                    "abbreviation":
                        "VER",

                    "first_name":
                        "Max",

                    "last_name":
                        "Verstappen",

                    "full_name":
                        "Max Verstappen",

                    "broadcast_name":
                        "M VERSTAPPEN",

                    "team_name":
                        "Red Bull Racing",

                    "team_colour":
                        "3671C6"

                },

                "4": {

                    "driver_number":
                        "4",

                    "abbreviation":
                        "NOR",

                    "first_name":
                        "Lando",

                    "last_name":
                        "Norris",

                    "full_name":
                        "Lando Norris",

                    "broadcast_name":
                        "L NORRIS",

                    "team_name":
                        "McLaren",

                    "team_colour":
                        "FF8700"

                }

            },


            # ====================================================
            # TIMING
            # ====================================================

            "timing": {

                "1": {

                    "driver_number":
                        "1",

                    "position":
                        1,

                    "completed_laps":
                        32,

                    "gap_to_leader":
                        "",

                    "interval_to_ahead":
                        "",

                    "last_lap_time":
                        "1:48.512",

                    "best_lap_time":
                        "1:46.921",

                    "in_pit":
                        False,

                    "pit_out":
                        False,

                    "retired":
                        False,

                    "stopped":
                        False

                },

                "4": {

                    "driver_number":
                        "4",

                    "position":
                        2,

                    "completed_laps":
                        32,

                    "gap_to_leader":
                        "+3.481",

                    "interval_to_ahead":
                        "+3.481",

                    "last_lap_time":
                        "1:48.104",

                    "best_lap_time":
                        "1:47.012",

                    "in_pit":
                        False,

                    "pit_out":
                        False,

                    "retired":
                        False,

                    "stopped":
                        False

                }

            },


            # ====================================================
            # TYRES
            # ====================================================

            "tyres": {

                "1": {

                    "driver_number":
                        "1",

                    "compound":
                        "HARD",

                    "tyre_age":
                        14.0,

                    "start_laps":
                        18,

                    "new_tyre":
                        "true",

                    "stint": {

                        "Compound":
                            "HARD",

                        "TotalLaps":
                            14,

                        "StartLaps":
                            18,

                        "New":
                            "true"

                    }

                },

                "4": {

                    "driver_number":
                        "4",

                    "compound":
                        "HARD",

                    "tyre_age":
                        12.0,

                    "start_laps":
                        20,

                    "new_tyre":
                        "true",

                    "stint": {

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

            },


            # ====================================================
            # WEATHER
            # ====================================================

            "weather": {

                "air_temperature":
                    21.4,

                "track_temperature":
                    31.8,

                "humidity":
                    61.0,

                "pressure":
                    970.2,

                "rainfall":
                    "0",

                "wind_direction":
                    210.0,

                "wind_speed":
                    2.7

            },


            # ====================================================
            # TRACK
            # ====================================================

            "track": {

                "status":
                    "1",

                "message":
                    "AllClear"

            },


            # ====================================================
            # RACE CONTROL
            # ====================================================

            "race_control": [

                {

                    "utc":
                        "2026-08-23T14:10:00Z",

                    "lap":
                        30,

                    "category":
                        "Flag",

                    "message":
                        "GREEN LIGHT - PIT EXIT OPEN",

                    "flag":
                        "GREEN",

                    "scope":
                        "Track",

                    "sector":
                        None,

                    "racing_number":
                        None

                }

            ],


            # ====================================================
            # OPTIONAL LIVE TOPICS
            # ====================================================

            "clock": {},

            "top_three": {},

            "timing_stats": {},

            "session_data": {},

            "heartbeat": {},

            "raw_topics": {}

        }


    def get_state(self):

        return self.state


    def get_live_state(self):

        return self.state


# ============================================================
# TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 6.5 — FLASK LIVE API TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # STEP 1
    # CREATE COMPONENTS
    # ========================================================

    print(
        "\n[1/7] Creating live API components..."
    )


    timing_client = (
        MockLiveTimingClient()
    )


    data_parser = (
        MockLiveDataParser()
    )


    configure_live_api(

        timing_client=timing_client,

        data_parser=data_parser

    )


    print(
        "✅ Live API components configured."
    )


    # ========================================================
    # STEP 2
    # CREATE FLASK APP
    # ========================================================

    print(
        "\n[2/7] Creating Flask test application..."
    )


    app = Flask(
        __name__
    )


    app.register_blueprint(
        live_api
    )


    app.config[
        "TESTING"
    ] = True


    client = (
        app.test_client()
    )


    print(
        "✅ Flask test client created."
    )


    # ========================================================
    # STEP 3
    # ROOT ENDPOINT
    # ========================================================

    print(
        "\n[3/7] Testing live API root..."
    )


    response = client.get(
        "/api/live"
    )


    assert response.status_code == 200


    root_data = (
        response.get_json()
    )


    assert root_data is not None

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


    print(
        "✅ Live API root validated."
    )


    # ========================================================
    # STEP 4
    # STATUS ENDPOINT
    # ========================================================

    print(
        "\n[4/7] Testing live timing status endpoint..."
    )


    response = client.get(
        "/api/live/status"
    )


    assert response.status_code == 200


    status_data = (
        response.get_json()
    )


    assert status_data is not None

    assert (
        status_data.get(
            "status"
        )
        ==
        "SUCCESS"
    )


    timing = (
        status_data.get(
            "timing"
        )
    )


    assert isinstance(
        timing,
        dict
    )


    assert (
        timing.get(
            "connected"
        )
        is True
    )


    assert (
        timing.get(
            "running"
        )
        is True
    )


    print(
        "✅ Live timing status endpoint validated."
    )


    # ========================================================
    # STEP 5
    # LIVE STATE ENDPOINT
    # ========================================================

    print(
        "\n[5/7] Testing live race-state endpoint..."
    )


    response = client.get(
        "/api/live/state"
    )


    assert response.status_code == 200


    state_data = (
        response.get_json()
    )


    assert state_data is not None


    assert (
        state_data.get(
            "status"
        )
        ==
        "SUCCESS"
    )


    state = (
        state_data.get(
            "state"
        )
    )


    assert isinstance(
        state,
        dict
    )


    print(
        "✅ Live race-state endpoint validated."
    )


    # ========================================================
    # STEP 6
    # STRATEGY ENDPOINT
    # ========================================================

    print(
        "\n[6/7] Testing live strategy endpoint..."
    )


    response = client.get(
        "/api/live/strategy/VER"
    )


    print(
        f"HTTP Status: "
        f"{response.status_code}"
    )


    strategy_data = (
        response.get_json()
    )


    if response.status_code != 200:

        print(
            "Response:"
        )

        print(
            strategy_data
        )


    assert response.status_code == 200


    assert strategy_data is not None


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


    race = (
        strategy_data.get(
            "race"
        )
    )


    strategy = (
        strategy_data.get(
            "strategy"
        )
    )


    assert isinstance(
        race,
        dict
    )


    assert isinstance(
        strategy,
        dict
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


    print(
        "✅ Live strategy endpoint validated."
    )


    # ========================================================
    # STEP 7
    # PIPELINE VALIDATION
    # ========================================================

    print(
        "\n[7/7] Validating complete live API pipeline..."
    )


    result = (
        strategy_data.get(
            "result"
        )
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


    pipeline = (
        result.get(
            "pipeline"
        )
    )


    assert isinstance(
        pipeline,
        dict
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
            pipeline.get(
                step
            )
            is not None
        )


    print(
        "✅ Phase 6.3 live state reached Flask."
    )

    print(
        "✅ Phase 6.4 live strategy service reached Flask."
    )

    print(
        "✅ Phase 4.2 → 4.7 strategy pipeline reached Flask."
    )

    print(
        "✅ Live AI recommendation reached Flask."
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        "\n" + "-" * 78
    )

    print(
        "LIVE API RESPONSE SUMMARY"
    )

    print(
        "-" * 78
    )


    print(
        f"Driver: "
        f"{strategy_data.get('driver')}"
    )


    print(
        f"Lap: "
        f"{race.get('lap')}/"
        f"{race.get('total_laps')}"
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
        f"Track Status: "
        f"{race.get('track_status')}"
    )


    print(
        f"Race Situation: "
        f"{strategy.get('race_situation')}"
    )


    print(
        f"Pit Decision: "
        f"{strategy.get('pit_decision')}"
    )


    print(
        f"AI Recommendation: "
        f"{strategy.get('recommendation')}"
    )


    print(
        f"Recommended Tyre: "
        f"{strategy.get('recommended_tyre')}"
    )


    print(
        f"Dynamic Score: "
        f"{strategy.get('dynamic_score')}"
    )


    print(
        f"Confidence: "
        f"{strategy.get('confidence')}%"
    )


    print(
        "-" * 78
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "✅ PHASE 6.5 FLASK LIVE API TEST PASSED"
    )

    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()