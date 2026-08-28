"""
F1 AI STRATEGIST
PHASE 6.3 — LIVE RACE-STATE ADAPTER TEST

Purpose
-------
Verify that clean Phase 6.2 live timing data can be converted
into the race-state contract required by the existing dynamic
strategy pipeline.
"""


from src.live.live_data_parser import (
    create_live_data_parser
)

from src.live.live_race_state_adapter import (
    build_live_race_state,
    display_live_race_state,
    lap_time_to_seconds,
    gap_to_seconds
)


# ============================================================
# TEST DATA
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
# MAIN
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 6.3 — LIVE RACE-STATE ADAPTER TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # STEP 1
    # CREATE PHASE 6.2 PARSER
    # ========================================================

    print(
        "\n[1/7] Creating Phase 6.2 live parser..."
    )


    parser = create_live_data_parser()


    assert parser is not None


    print(
        "✅ Phase 6.2 parser created."
    )


    # ========================================================
    # STEP 2
    # BUILD CLEAN LIVE STATE
    # ========================================================

    print(
        "\n[2/7] Building clean Phase 6.2 live state..."
    )


    parser.parse_message(
        "SessionInfo",
        SESSION_INFO
    )

    parser.parse_message(
        "SessionStatus",
        SESSION_STATUS
    )

    parser.parse_message(
        "LapCount",
        LAP_COUNT
    )

    parser.parse_message(
        "DriverList",
        DRIVER_LIST
    )

    parser.parse_message(
        "TimingData",
        TIMING_DATA
    )

    parser.parse_message(
        "TimingAppData",
        TIMING_APP_DATA
    )

    parser.parse_message(
        "WeatherData",
        WEATHER_DATA
    )

    parser.parse_message(
        "TrackStatus",
        TRACK_STATUS
    )

    parser.parse_message(
        "RaceControlMessages",
        RACE_CONTROL
    )


    live_state = parser.get_state()


    assert live_state


    assert (
        live_state[
            "lap_count"
        ][
            "current_lap"
        ]
        ==
        32
    )


    assert (
        live_state[
            "drivers"
        ][
            "1"
        ][
            "abbreviation"
        ]
        ==
        "VER"
    )


    print(
        "✅ Clean Phase 6.2 live state generated."
    )


    # ========================================================
    # STEP 3
    # TEST CONVERSION HELPERS
    # ========================================================

    print(
        "\n[3/7] Validating live timing conversions..."
    )


    assert (
        lap_time_to_seconds(
            "1:48.512"
        )
        ==
        108.512
    )


    assert (
        lap_time_to_seconds(
            "96.005"
        )
        ==
        96.005
    )


    assert (
        gap_to_seconds(
            "+3.481"
        )
        ==
        3.481
    )


    assert (
        gap_to_seconds(
            ""
        )
        ==
        0.0
    )


    print(
        "✅ Live timing conversions validated."
    )


    # ========================================================
    # STEP 4
    # BUILD LIVE RACE STATE
    # ========================================================

    print(
        "\n[4/7] Adapting live data into dynamic race state..."
    )


    race_state = build_live_race_state(

        live_state=live_state,

        driver="VER"

    )


    assert race_state


    print(
        "✅ Phase 6.3 live race state generated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_live_race_state(
        race_state
    )


    # ========================================================
    # STEP 5
    # CORE RACE STATE
    # ========================================================

    print(
        "\n[5/7] Validating core dynamic race-state fields..."
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
            "LiveData"
        ]
        is True
    )


    assert (
        race_state[
            "Driver"
        ]
        ==
        "VER"
    )


    assert (
        race_state[
            "DriverNumber"
        ]
        ==
        "1"
    )


    assert (
        race_state[
            "CurrentLap"
        ]
        ==
        32
    )


    assert (
        race_state[
            "TotalLaps"
        ]
        ==
        44
    )


    assert (
        race_state[
            "LapsRemaining"
        ]
        ==
        12
    )


    assert (
        race_state[
            "Position"
        ]
        ==
        1
    )


    print(
        "✅ Core dynamic race-state fields validated."
    )


    # ========================================================
    # STEP 6
    # TYRE / PACE / TRACK
    # ========================================================

    print(
        "\n[6/7] Validating live strategic context..."
    )


    assert (
        race_state[
            "TyreCompound"
        ]
        ==
        "HARD"
    )


    assert (
        race_state[
            "TyreLife"
        ]
        ==
        14.0
    )


    assert (
        race_state[
            "TyreCondition"
        ]
        ==
        "HEALTHY"
    )


    assert (
        race_state[
            "RecentPace"
        ]
        ==
        108.512
    )


    assert (
        race_state[
            "TrackStatus"
        ]
        ==
        "GREEN"
    )


    assert (
        race_state[
            "WetConditions"
        ]
        is False
    )


    assert (
        race_state[
            "PitUrgency"
        ]
        ==
        "LOW"
    )


    assert (
        race_state[
            "SessionStatus"
        ]
        ==
        "Started"
    )


    print(
        "✅ Live strategic context validated."
    )


    # ========================================================
    # STEP 7
    # PHASE 4 CONTRACT
    # ========================================================

    print(
        "\n[7/7] Validating Phase 4 compatibility contract..."
    )


    required_phase4_fields = [

        "Driver",
        "CurrentLap",
        "TotalLaps",
        "LapsRemaining",
        "Position",
        "TyreCompound",
        "TyreLife",
        "RecentPace",
        "DegradationRate",
        "RaceProgress",

    ]


    for field in required_phase4_fields:

        assert (
            field
            in race_state
        ), (
            f"Missing Phase 4 field: {field}"
        )


    assert (
        race_state[
            "RecentPace"
        ]
        >
        0
    )


    assert (
        race_state[
            "DegradationRate"
        ]
        >=
        0
    )


    assert (
        0
        <=
        race_state[
            "RaceProgress"
        ]
        <=
        1
    )


    print(
        "✅ Phase 4 compatibility contract validated."
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "✅ PHASE 6.3 LIVE RACE-STATE ADAPTER TEST PASSED"
    )

    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()