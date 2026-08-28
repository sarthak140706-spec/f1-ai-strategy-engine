"""
F1 AI STRATEGIST
PHASE 6.4 — LIVE STRATEGY SERVICE TEST

Purpose
-------
Verify that Phase 6.2 clean live data can travel through:

6.2 Live Data Parser
        ↓
6.3 Live Race-State Adapter
        ↓
6.4 Live Strategy Service
        ↓
4.2 Race Situation
        ↓
4.3 Tyre Strategy
        ↓
4.4 Pit Decision
        ↓
4.5 Strategy Simulation
        ↓
4.6 Strategy Scoring
        ↓
4.7 AI Recommendation
"""


from src.live.live_data_parser import (
    create_live_data_parser
)

from src.live.live_strategy_service import (
    run_live_strategy_service,
    display_live_strategy_service
)


# ============================================================
# TEST LIVE DATA
# ============================================================

SESSION_INFO = {

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


SESSION_STATUS = {

    "Status":
        "Started"

}


LAP_COUNT = {

    "CurrentLap":
        32,

    "TotalLaps":
        44

}


DRIVER_LIST = {

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


TIMING_DATA = {

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


TIMING_APP_DATA = {

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


WEATHER_DATA = {

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


TRACK_STATUS = {

    "Status":
        "1",

    "Message":
        "AllClear"

}


RACE_CONTROL = {

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


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 6.4 — LIVE STRATEGY SERVICE TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # 1
    # CREATE PARSER
    # ========================================================

    print(
        "\n[1/8] Creating Phase 6.2 live parser..."
    )


    parser = create_live_data_parser()


    assert parser is not None


    print(
        "✅ Phase 6.2 parser created."
    )


    # ========================================================
    # 2
    # FEED LIVE MESSAGES
    # ========================================================

    print(
        "\n[2/8] Building simulated live race feed..."
    )


    messages = [

        (
            "SessionInfo",
            SESSION_INFO
        ),

        (
            "SessionStatus",
            SESSION_STATUS
        ),

        (
            "LapCount",
            LAP_COUNT
        ),

        (
            "DriverList",
            DRIVER_LIST
        ),

        (
            "TimingData",
            TIMING_DATA
        ),

        (
            "TimingAppData",
            TIMING_APP_DATA
        ),

        (
            "WeatherData",
            WEATHER_DATA
        ),

        (
            "TrackStatus",
            TRACK_STATUS
        ),

        (
            "RaceControlMessages",
            RACE_CONTROL
        ),

    ]


    for topic, payload in messages:

        parser.parse_message(
            topic,
            payload
        )


    live_state = parser.get_state()


    assert live_state


    print(
        "✅ Simulated live race feed parsed."
    )


    # ========================================================
    # 3
    # RUN LIVE STRATEGY SERVICE
    # ========================================================

    print(
        "\n[3/8] Running Phase 6.4 live strategy service..."
    )


    result = run_live_strategy_service(

        live_state=live_state,

        driver="VER"

    )


    assert result


    print(
        "✅ Live strategy service executed."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_live_strategy_service(
        result
    )


    # ========================================================
    # 4
    # SERVICE CONTRACT
    # ========================================================

    print(
        "\n[4/8] Validating Phase 6.4 service contract..."
    )


    assert (
        result[
            "service"
        ]
        ==
        "live_strategy_service"
    )


    assert (
        result[
            "phase"
        ]
        ==
        "6.4"
    )


    assert (
        result[
            "status"
        ]
        ==
        "SUCCESS"
    )


    assert (
        result[
            "source"
        ]
        ==
        "LIVE"
    )


    assert (
        result[
            "live"
        ]
        is True
    )


    print(
        "✅ Phase 6.4 service contract validated."
    )


    # ========================================================
    # 5
    # LIVE RACE CONTEXT
    # ========================================================

    print(
        "\n[5/8] Validating live race context..."
    )


    assert (
        result[
            "driver"
        ]
        ==
        "VER"
    )


    assert (
        result[
            "lap"
        ]
        ==
        32
    )


    assert (
        result[
            "total_laps"
        ]
        ==
        44
    )


    assert (
        result[
            "laps_remaining"
        ]
        ==
        12
    )


    assert (
        result[
            "position"
        ]
        ==
        1
    )


    assert (
        result[
            "current_tyre"
        ]
        ==
        "HARD"
    )


    assert (
        result[
            "tyre_life"
        ]
        ==
        14.0
    )


    assert (
        result[
            "track_status"
        ]
        ==
        "GREEN"
    )


    assert (
        result[
            "wet_conditions"
        ]
        is False
    )


    print(
        "✅ Live race context validated."
    )


    # ========================================================
    # 6
    # PHASE 4 PIPELINE
    # ========================================================

    print(
        "\n[6/8] Validating live Phase 4 strategy pipeline..."
    )


    pipeline = result[
        "pipeline"
    ]


    required_pipeline_steps = [

        "phase_6_3",
        "phase_4_2",
        "phase_4_3",
        "phase_4_4",
        "phase_4_5",
        "phase_4_6",
        "phase_4_7",

    ]


    for step in required_pipeline_steps:

        assert (
            step
            in pipeline
        ), (
            f"Missing pipeline step: {step}"
        )


        assert (
            pipeline[
                step
            ]
        ), (
            f"Empty pipeline output: {step}"
        )


    print(
        "✅ Live Phase 4 strategy pipeline validated."
    )


    # ========================================================
    # 7
    # AI RESULT
    # ========================================================

    print(
        "\n[7/8] Validating live AI recommendation..."
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


    print(
        "✅ Live AI recommendation validated."
    )


    # ========================================================
    # 8
    # CRITICAL LIVE VALIDATION
    # ========================================================

    print(
        "\n[8/8] Validating historical-session independence..."
    )


    race_state = result[
        "race_state"
    ]


    assert (
        race_state[
            "LiveData"
        ]
        is True
    )


    assert (
        race_state[
            "Source"
        ]
        ==
        "LIVE"
    )


    assert (
        race_state[
            "Adapter"
        ]
        ==
        "live_race_state_adapter"
    )


    # The live service must work entirely from live_state.
    # No FastF1 historical Session object is passed here.

    print(
        "✅ Live strategy pipeline operates without a "
        "historical FastF1 Session object."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "✅ PHASE 6.4 LIVE STRATEGY SERVICE TEST PASSED"
    )

    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()