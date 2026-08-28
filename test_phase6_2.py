"""
F1 AI STRATEGIST
PHASE 6.2 — LIVE DATA PARSER TEST

Purpose
-------
Verify that raw F1-style live timing messages can be converted
into a clean structured state.

Phase 6.1 is frozen.
Phase 6.2 only tests parsing and state management.
"""


from src.live.live_data_parser import (

    F1LiveDataParser,

    create_live_data_parser,

    display_live_data_parser

)


# ============================================================
# SAMPLE LIVE DATA
# ============================================================

SESSION_INFO = {

    "Name":
        "Race",

    "Type":
        "Race",

    "StartDate":
        "2026-08-23T13:00:00Z",

    "GmtOffset":
        "00:00:00",

    "Meeting": {

        "Name":
            "Belgian Grand Prix",

        "OfficialName":
            "FORMULA 1 BELGIAN GRAND PRIX 2026",

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
        "PHASE 6.2 — LIVE DATA PARSER TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # 1
    # CREATE PARSER
    # ========================================================

    print(
        "\n[1/8] Creating live data parser..."
    )


    parser = create_live_data_parser()


    assert isinstance(

        parser,

        F1LiveDataParser

    )


    print(
        "✅ Live data parser created."
    )


    # ========================================================
    # 2
    # SESSION
    # ========================================================

    print(
        "\n[2/8] Parsing live session state..."
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


    state = parser.get_state()


    assert (
        state[
            "session"
        ][
            "name"
        ]
        ==
        "Race"
    )


    assert (
        state[
            "session_status"
        ][
            "status"
        ]
        ==
        "Started"
    )


    assert (
        state[
            "lap_count"
        ][
            "current_lap"
        ]
        ==
        32
    )


    assert (
        state[
            "lap_count"
        ][
            "total_laps"
        ]
        ==
        44
    )


    print(
        "✅ Live session state parsed."
    )


    # ========================================================
    # 3
    # DRIVERS
    # ========================================================

    print(
        "\n[3/8] Parsing live driver data..."
    )


    parser.parse_message(
        "DriverList",
        DRIVER_LIST
    )


    state = parser.get_state()


    assert (
        len(
            state[
                "drivers"
            ]
        )
        ==
        2
    )


    assert (
        state[
            "drivers"
        ][
            "1"
        ][
            "abbreviation"
        ]
        ==
        "VER"
    )


    assert (
        state[
            "drivers"
        ][
            "4"
        ][
            "abbreviation"
        ]
        ==
        "NOR"
    )


    print(
        "✅ Live driver data parsed."
    )


    # ========================================================
    # 4
    # TIMING
    # ========================================================

    print(
        "\n[4/8] Parsing live timing data..."
    )


    parser.parse_message(
        "TimingData",
        TIMING_DATA
    )


    state = parser.get_state()


    assert (
        state[
            "timing"
        ][
            "1"
        ][
            "position"
        ]
        ==
        1
    )


    assert (
        state[
            "timing"
        ][
            "4"
        ][
            "position"
        ]
        ==
        2
    )


    assert (
        state[
            "timing"
        ][
            "4"
        ][
            "gap_to_leader"
        ]
        ==
        "+3.481"
    )


    print(
        "✅ Live timing data parsed."
    )


    # ========================================================
    # 5
    # TYRES
    # ========================================================

    print(
        "\n[5/8] Parsing live tyre data..."
    )


    parser.parse_message(
        "TimingAppData",
        TIMING_APP_DATA
    )


    state = parser.get_state()


    assert (
        state[
            "tyres"
        ][
            "1"
        ][
            "compound"
        ]
        ==
        "HARD"
    )


    assert (
        state[
            "tyres"
        ][
            "1"
        ][
            "tyre_age"
        ]
        ==
        14.0
    )


    assert (
        state[
            "tyres"
        ][
            "4"
        ][
            "compound"
        ]
        ==
        "HARD"
    )


    print(
        "✅ Live tyre data parsed."
    )


    # ========================================================
    # 6
    # WEATHER / TRACK
    # ========================================================

    print(
        "\n[6/8] Parsing live weather and track state..."
    )


    parser.parse_message(
        "WeatherData",
        WEATHER_DATA
    )


    parser.parse_message(
        "TrackStatus",
        TRACK_STATUS
    )


    state = parser.get_state()


    assert (
        state[
            "weather"
        ][
            "air_temperature"
        ]
        ==
        21.4
    )


    assert (
        state[
            "weather"
        ][
            "track_temperature"
        ]
        ==
        31.8
    )


    assert (
        state[
            "track"
        ][
            "status"
        ]
        ==
        "1"
    )


    print(
        "✅ Live weather and track state parsed."
    )


    # ========================================================
    # 7
    # RACE CONTROL
    # ========================================================

    print(
        "\n[7/8] Parsing race control messages..."
    )


    parser.parse_message(
        "RaceControlMessages",
        RACE_CONTROL
    )


    state = parser.get_state()


    assert (
        len(
            state[
                "race_control"
            ]
        )
        ==
        1
    )


    assert (
        state[
            "race_control"
        ][
            0
        ][
            "flag"
        ]
        ==
        "GREEN"
    )


    print(
        "✅ Race control messages parsed."
    )


    # ========================================================
    # 8
    # COMBINED DRIVER STATE
    # ========================================================

    print(
        "\n[8/8] Validating combined live driver state..."
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


    driver = (
        parser.get_driver_by_abbreviation(
            "VER"
        )
    )


    assert (
        driver[
            "driver"
        ][
            "abbreviation"
        ]
        ==
        "VER"
    )


    assert (
        driver[
            "timing"
        ][
            "position"
        ]
        ==
        1
    )


    assert (
        driver[
            "tyre"
        ][
            "compound"
        ]
        ==
        "HARD"
    )


    assert (
        driver[
            "tyre"
        ][
            "tyre_age"
        ]
        ==
        14.0
    )


    print(
        "✅ Combined live driver state validated."
    )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    display_live_data_parser(
        parser
    )


    # ========================================================
    # FINAL VALIDATION
    # ========================================================

    summary = parser.get_summary()


    assert (
        summary[
            "phase"
        ]
        ==
        "6.2"
    )


    assert (
        summary[
            "component"
        ]
        ==
        "live_data_parser"
    )


    assert (
        summary[
            "current_lap"
        ]
        ==
        32
    )


    assert (
        summary[
            "total_laps"
        ]
        ==
        44
    )


    assert (
        summary[
            "driver_count"
        ]
        ==
        2
    )


    assert (
        summary[
            "timing_driver_count"
        ]
        ==
        2
    )


    assert (
        summary[
            "tyre_driver_count"
        ]
        ==
        2
    )


    print(
        "\n" + "=" * 78
    )

    print(
        "✅ PHASE 6.2 LIVE DATA PARSER TEST PASSED"
    )

    print(
        "=" * 78
    )


if __name__ == "__main__":

    main()