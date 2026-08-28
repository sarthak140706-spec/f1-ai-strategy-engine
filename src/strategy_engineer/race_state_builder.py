"""
F1 AI STRATEGIST
PHASE 7.1 — MANUAL RACE-STATE BUILDER

Purpose
-------
Convert user-supplied Formula One race information into a
clean, validated race-state representation that can later be
passed into the existing F1 AI strategy pipeline.

Phase 7.1 is responsible for:

1. Accepting manual race-situation inputs.
2. Validating race information.
3. Normalising driver, circuit and tyre information.
4. Calculating derived race-state features.
5. Building a consistent strategy-engine race state.

IMPORTANT
---------
Phase 7.1 does NOT:

- execute the AI strategy engine
- recommend a pit stop
- recommend a tyre
- simulate strategies
- calculate strategy scores
- expose Flask API routes
- communicate with the frontend

Those responsibilities belong to later Phase 7 steps.
"""


from __future__ import annotations

from typing import Any, Dict, Optional


# ============================================================
# PHASE INFORMATION
# ============================================================

PHASE = "7.1"

COMPONENT = "manual_race_state_builder"

SOURCE = "MANUAL"


# ============================================================
# SUPPORTED TYRE COMPOUNDS
# ============================================================

SUPPORTED_TYRE_COMPOUNDS = {

    "SOFT",
    "MEDIUM",
    "HARD",
    "INTERMEDIATE",
    "WET",

}


# ============================================================
# TYRE ALIASES
# ============================================================

TYRE_ALIASES = {

    "S":
        "SOFT",

    "SOFT":
        "SOFT",

    "M":
        "MEDIUM",

    "MEDIUM":
        "MEDIUM",

    "H":
        "HARD",

    "HARD":
        "HARD",

    "I":
        "INTERMEDIATE",

    "INTER":
        "INTERMEDIATE",

    "INTERMEDIATE":
        "INTERMEDIATE",

    "W":
        "WET",

    "WET":
        "WET",

    "FULL WET":
        "WET",

    "FULL_WET":
        "WET",

}


# ============================================================
# TRACK STATUS
# ============================================================

SUPPORTED_TRACK_STATUSES = {

    "GREEN",
    "YELLOW",
    "SAFETY_CAR",
    "VSC",
    "RED_FLAG",

}


# ============================================================
# TRACK STATUS ALIASES
# ============================================================

TRACK_STATUS_ALIASES = {

    "GREEN":
        "GREEN",

    "CLEAR":
        "GREEN",

    "ALL CLEAR":
        "GREEN",

    "ALL_CLEAR":
        "GREEN",

    "YELLOW":
        "YELLOW",

    "YELLOW FLAG":
        "YELLOW",

    "YELLOW_FLAG":
        "YELLOW",

    "SC":
        "SAFETY_CAR",

    "SAFETY CAR":
        "SAFETY_CAR",

    "SAFETY_CAR":
        "SAFETY_CAR",

    "VSC":
        "VSC",

    "VIRTUAL SAFETY CAR":
        "VSC",

    "VIRTUAL_SAFETY_CAR":
        "VSC",

    "RED":
        "RED_FLAG",

    "RED FLAG":
        "RED_FLAG",

    "RED_FLAG":
        "RED_FLAG",

}


# ============================================================
# WEATHER CONDITIONS
# ============================================================

SUPPORTED_WEATHER_CONDITIONS = {

    "DRY",
    "DAMP",
    "WET",

}


# ============================================================
# WEATHER ALIASES
# ============================================================

WEATHER_ALIASES = {

    "DRY":
        "DRY",

    "CLEAR":
        "DRY",

    "DAMP":
        "DAMP",

    "LIGHT RAIN":
        "DAMP",

    "LIGHT_RAIN":
        "DAMP",

    "WET":
        "WET",

    "RAIN":
        "WET",

    "HEAVY RAIN":
        "WET",

    "HEAVY_RAIN":
        "WET",

}


# ============================================================
# EXCEPTION
# ============================================================

class RaceStateValidationError(ValueError):

    """
    Raised when a manually supplied race situation contains
    invalid or impossible values.
    """

    pass


# ============================================================
# GENERIC NORMALISATION
# ============================================================

def _normalise_text(
    value: Any
) -> str:

    """
    Convert a value into a clean uppercase string.
    """

    if value is None:

        return ""

    return (
        str(value)
        .strip()
        .upper()
    )


# ============================================================
# SAFE INTEGER
# ============================================================

def _to_int(
    value: Any,
    field_name: str
) -> int:

    """
    Convert a supplied value to an integer.
    """

    if isinstance(
        value,
        bool
    ):

        raise RaceStateValidationError(

            f"{field_name} must be an integer."

        )

    try:

        numeric_value = float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        raise RaceStateValidationError(

            f"{field_name} must be an integer."

        )


    if not numeric_value.is_integer():

        raise RaceStateValidationError(

            f"{field_name} must be an integer."

        )


    return int(
        numeric_value
    )


# ============================================================
# SAFE FLOAT
# ============================================================

def _to_float(
    value: Any,
    field_name: str
) -> float:

    """
    Convert a supplied value to float.
    """

    if isinstance(
        value,
        bool
    ):

        raise RaceStateValidationError(

            f"{field_name} must be numeric."

        )

    try:

        return float(
            value
        )

    except (
        TypeError,
        ValueError
    ):

        raise RaceStateValidationError(

            f"{field_name} must be numeric."

        )


# ============================================================
# OPTIONAL FLOAT
# ============================================================

def _optional_float(
    value: Any,
    field_name: str
) -> Optional[float]:

    """
    Convert optional numeric input to float.
    """

    if value is None:

        return None


    if isinstance(
        value,
        str
    ):

        cleaned = value.strip()

        if cleaned == "":

            return None


    return _to_float(

        value,

        field_name

    )


# ============================================================
# BOOLEAN NORMALISATION
# ============================================================

def _to_bool(
    value: Any,
    field_name: str
) -> bool:

    """
    Convert common boolean representations into bool.
    """

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
            .upper()
        )


        if cleaned in {

            "TRUE",
            "YES",
            "Y",
            "1",
            "ON",

        }:

            return True


        if cleaned in {

            "FALSE",
            "NO",
            "N",
            "0",
            "OFF",

        }:

            return False


    raise RaceStateValidationError(

        f"{field_name} must be true or false."

    )


# ============================================================
# DRIVER NORMALISATION
# ============================================================

def normalise_driver(
    driver: Any
) -> str:

    """
    Normalise driver identifier.

    Phase 7 intentionally does not restrict the user to a
    hard-coded list of four drivers.

    The driver may be supplied as an abbreviation such as:

        VER
        NOR
        LEC
        HAM

    or another valid textual identifier.
    """

    driver = _normalise_text(
        driver
    )


    if not driver:

        raise RaceStateValidationError(

            "Driver is required."

        )


    if len(driver) > 50:

        raise RaceStateValidationError(

            "Driver identifier is too long."

        )


    return driver


# ============================================================
# CIRCUIT NORMALISATION
# ============================================================

def normalise_circuit(
    circuit: Any
) -> str:

    """
    Validate and normalise circuit information.

    Circuits are deliberately not restricted to four tracks.
    """

    if circuit is None:

        raise RaceStateValidationError(

            "Circuit is required."

        )


    circuit = (
        str(circuit)
        .strip()
    )


    if not circuit:

        raise RaceStateValidationError(

            "Circuit is required."

        )


    if len(circuit) > 100:

        raise RaceStateValidationError(

            "Circuit name is too long."

        )


    return circuit


# ============================================================
# TYRE NORMALISATION
# ============================================================

def normalise_tyre(
    tyre: Any
) -> str:

    """
    Convert tyre input into one of the official strategy
    compound categories used by Phase 7.
    """

    tyre = _normalise_text(
        tyre
    )


    tyre = TYRE_ALIASES.get(

        tyre,

        tyre

    )


    if tyre not in SUPPORTED_TYRE_COMPOUNDS:

        supported = ", ".join(

            sorted(
                SUPPORTED_TYRE_COMPOUNDS
            )

        )


        raise RaceStateValidationError(

            f"Unsupported tyre compound: {tyre or 'EMPTY'}. "
            f"Supported compounds: {supported}."

        )


    return tyre


# ============================================================
# TRACK STATUS NORMALISATION
# ============================================================

def normalise_track_status(
    track_status: Any
) -> str:

    """
    Normalise track status.
    """

    if track_status is None:

        return "GREEN"


    track_status = _normalise_text(
        track_status
    )


    track_status = TRACK_STATUS_ALIASES.get(

        track_status,

        track_status

    )


    if (
        track_status
        not in
        SUPPORTED_TRACK_STATUSES
    ):

        raise RaceStateValidationError(

            f"Unsupported track status: {track_status}."

        )


    return track_status


# ============================================================
# WEATHER NORMALISATION
# ============================================================

def normalise_weather(
    weather: Any
) -> str:

    """
    Normalise weather condition.
    """

    if weather is None:

        return "DRY"


    weather = _normalise_text(
        weather
    )


    weather = WEATHER_ALIASES.get(

        weather,

        weather

    )


    if (
        weather
        not in
        SUPPORTED_WEATHER_CONDITIONS
    ):

        raise RaceStateValidationError(

            f"Unsupported weather condition: {weather}."

        )


    return weather


# ============================================================
# RACE PROGRESS
# ============================================================

def calculate_race_progress(
    current_lap: int,
    total_laps: int
) -> float:

    """
    Calculate race progress as a value between 0 and 1.
    """

    if total_laps <= 0:

        return 0.0


    return round(

        current_lap
        /
        total_laps,

        4

    )


# ============================================================
# TYRE CONDITION
# ============================================================

def determine_tyre_condition(
    tyre_age: float,
    compound: str
) -> str:

    """
    Provide a simple descriptive tyre-condition classification.

    This is NOT the Phase 7 strategy recommendation.

    It is only race-state metadata.
    """

    thresholds = {

        "SOFT": (
            8.0,
            15.0
        ),

        "MEDIUM": (
            15.0,
            25.0
        ),

        "HARD": (
            22.0,
            35.0
        ),

        "INTERMEDIATE": (
            15.0,
            25.0
        ),

        "WET": (
            20.0,
            35.0
        ),

    }


    warning_age, critical_age = thresholds[
        compound
    ]


    if tyre_age >= critical_age:

        return "CRITICAL"


    if tyre_age >= warning_age:

        return "WORN"


    return "HEALTHY"


# ============================================================
# RACE PHASE
# ============================================================

def determine_race_phase(
    race_progress: float
) -> str:

    """
    Determine the broad stage of the race.
    """

    if race_progress < 0.25:

        return "EARLY"


    if race_progress < 0.70:

        return "MIDDLE"


    return "LATE"


# ============================================================
# VALIDATE MANUAL INPUT
# ============================================================

def validate_manual_race_input(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:

    """
    Validate and normalise manual race information.

    Returns
    -------
    dict
        Clean validated values.
    """

    if not isinstance(
        race_input,
        dict
    ):

        raise RaceStateValidationError(

            "Race input must be a dictionary."

        )


    # ========================================================
    # REQUIRED FIELDS
    # ========================================================

    required_fields = [

        "driver",
        "circuit",
        "current_lap",
        "total_laps",
        "position",
        "current_tyre",
        "tyre_age",

    ]


    missing_fields = [

        field

        for field
        in required_fields

        if (
            field not in race_input
            or
            race_input.get(field) is None
            or
            (
                isinstance(
                    race_input.get(field),
                    str
                )
                and
                not race_input.get(field).strip()
            )
        )

    ]


    if missing_fields:

        raise RaceStateValidationError(

            "Missing required race input(s): "
            +
            ", ".join(
                missing_fields
            )

        )


    # ========================================================
    # NORMALISE BASIC VALUES
    # ========================================================

    driver = normalise_driver(

        race_input.get(
            "driver"
        )

    )


    circuit = normalise_circuit(

        race_input.get(
            "circuit"
        )

    )


    current_lap = _to_int(

        race_input.get(
            "current_lap"
        ),

        "current_lap"

    )


    total_laps = _to_int(

        race_input.get(
            "total_laps"
        ),

        "total_laps"

    )


    position = _to_int(

        race_input.get(
            "position"
        ),

        "position"

    )


    current_tyre = normalise_tyre(

        race_input.get(
            "current_tyre"
        )

    )


    tyre_age = _to_float(

        race_input.get(
            "tyre_age"
        ),

        "tyre_age"

    )


    # ========================================================
    # VALIDATE LAP INFORMATION
    # ========================================================

    if total_laps <= 0:

        raise RaceStateValidationError(

            "total_laps must be greater than 0."

        )


    if current_lap < 0:

        raise RaceStateValidationError(

            "current_lap cannot be negative."

        )


    if current_lap > total_laps:

        raise RaceStateValidationError(

            "current_lap cannot be greater than total_laps."

        )


    # ========================================================
    # VALIDATE POSITION
    # ========================================================

    if not (
        1
        <=
        position
        <=
        20
    ):

        raise RaceStateValidationError(

            "position must be between 1 and 20."

        )


    # ========================================================
    # VALIDATE TYRE AGE
    # ========================================================

    if tyre_age < 0:

        raise RaceStateValidationError(

            "tyre_age cannot be negative."

        )


    if tyre_age > current_lap:

        raise RaceStateValidationError(

            "tyre_age cannot be greater than current_lap."

        )


    # ========================================================
    # OPTIONAL GAPS
    # ========================================================

    gap_ahead = _optional_float(

        race_input.get(
            "gap_ahead"
        ),

        "gap_ahead"

    )


    gap_behind = _optional_float(

        race_input.get(
            "gap_behind"
        ),

        "gap_behind"

    )


    if (
        gap_ahead is not None
        and
        gap_ahead < 0
    ):

        raise RaceStateValidationError(

            "gap_ahead cannot be negative."

        )


    if (
        gap_behind is not None
        and
        gap_behind < 0
    ):

        raise RaceStateValidationError(

            "gap_behind cannot be negative."

        )


    # ========================================================
    # OPTIONAL PACE INFORMATION
    # ========================================================

    recent_pace = _optional_float(

        race_input.get(
            "recent_pace"
        ),

        "recent_pace"

    )


    average_pace = _optional_float(

        race_input.get(
            "average_pace"
        ),

        "average_pace"

    )


    degradation_rate = _optional_float(

        race_input.get(
            "degradation_rate"
        ),

        "degradation_rate"

    )


    if (
        recent_pace is not None
        and
        recent_pace <= 0
    ):

        raise RaceStateValidationError(

            "recent_pace must be greater than 0."

        )


    if (
        average_pace is not None
        and
        average_pace <= 0
    ):

        raise RaceStateValidationError(

            "average_pace must be greater than 0."

        )


    # ========================================================
    # WEATHER
    # ========================================================

    weather = normalise_weather(

        race_input.get(
            "weather",
            "DRY"
        )

    )


    rainfall = _optional_float(

        race_input.get(
            "rainfall",
            0.0
        ),

        "rainfall"

    )


    if rainfall is None:

        rainfall = 0.0


    if rainfall < 0:

        raise RaceStateValidationError(

            "rainfall cannot be negative."

        )


    # ========================================================
    # TRACK STATUS
    # ========================================================

    track_status = normalise_track_status(

        race_input.get(
            "track_status",
            "GREEN"
        )

    )


    # ========================================================
    # SAFETY CAR
    # ========================================================

    safety_car = _to_bool(

        race_input.get(
            "safety_car",
            False
        ),

        "safety_car"

    )


    virtual_safety_car = _to_bool(

        race_input.get(
            "virtual_safety_car",
            False
        ),

        "virtual_safety_car"

    )


    # ========================================================
    # CONSISTENCY
    # ========================================================

    if track_status == "SAFETY_CAR":

        safety_car = True


    if track_status == "VSC":

        virtual_safety_car = True


    if (
        safety_car
        and
        virtual_safety_car
    ):

        raise RaceStateValidationError(

            "Safety Car and Virtual Safety Car "
            "cannot both be active."

        )


    # ========================================================
    # PIT INFORMATION
    # ========================================================

    pit_stops_completed = _to_int(

        race_input.get(
            "pit_stops_completed",
            0
        ),

        "pit_stops_completed"

    )


    if pit_stops_completed < 0:

        raise RaceStateValidationError(

            "pit_stops_completed cannot be negative."

        )


    # ========================================================
    # OPTIONAL DRIVER / TEAM INFORMATION
    # ========================================================

    team = race_input.get(
        "team"
    )


    if team is not None:

        team = (
            str(team)
            .strip()
        )


        if not team:

            team = None


    grand_prix = race_input.get(
        "grand_prix"
    )


    if grand_prix is not None:

        grand_prix = (
            str(grand_prix)
            .strip()
        )


        if not grand_prix:

            grand_prix = None


    # ========================================================
    # RETURN CLEAN INPUT
    # ========================================================

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
            round(
                tyre_age,
                3
            ),

        "gap_ahead":
            (
                round(
                    gap_ahead,
                    3
                )
                if gap_ahead is not None
                else None
            ),

        "gap_behind":
            (
                round(
                    gap_behind,
                    3
                )
                if gap_behind is not None
                else None
            ),

        "recent_pace":
            (
                round(
                    recent_pace,
                    3
                )
                if recent_pace is not None
                else None
            ),

        "average_pace":
            (
                round(
                    average_pace,
                    3
                )
                if average_pace is not None
                else None
            ),

        "degradation_rate":
            (
                round(
                    degradation_rate,
                    4
                )
                if degradation_rate is not None
                else None
            ),

        "weather":
            weather,

        "rainfall":
            round(
                rainfall,
                3
            ),

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
# BUILD MANUAL RACE STATE
# ============================================================

def build_manual_race_state(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:

    """
    Build a standardized Phase 7.1 manual race state.

    This is the main public function for Phase 7.1.
    """

    clean = validate_manual_race_input(
        race_input
    )


    # ========================================================
    # DERIVED FEATURES
    # ========================================================

    current_lap = clean[
        "current_lap"
    ]


    total_laps = clean[
        "total_laps"
    ]


    laps_remaining = max(

        total_laps
        -
        current_lap,

        0

    )


    race_progress = calculate_race_progress(

        current_lap=current_lap,

        total_laps=total_laps

    )


    race_phase = determine_race_phase(
        race_progress
    )


    tyre_condition = determine_tyre_condition(

        tyre_age=clean[
            "tyre_age"
        ],

        compound=clean[
            "current_tyre"
        ]

    )


    # ========================================================
    # WEATHER FLAGS
    # ========================================================

    wet_conditions = (

        clean[
            "weather"
        ]
        in {
            "DAMP",
            "WET",
        }

        or

        clean[
            "rainfall"
        ]
        > 0

    )


    # ========================================================
    # TRACK FLAGS
    # ========================================================

    safety_car = bool(
        clean[
            "safety_car"
        ]
    )


    virtual_safety_car = bool(
        clean[
            "virtual_safety_car"
        ]
    )


    red_flag = (

        clean[
            "track_status"
        ]
        ==
        "RED_FLAG"

    )


    # ========================================================
    # STANDARDIZED RACE STATE
    # ========================================================

    race_state = {

        # ----------------------------------------------------
        # PHASE 7 METADATA
        # ----------------------------------------------------

        "Phase":
            PHASE,

        "Source":
            SOURCE,

        "ManualData":
            True,

        "LiveData":
            False,

        "Component":
            COMPONENT,


        # ----------------------------------------------------
        # DRIVER / EVENT
        # ----------------------------------------------------

        "Driver":
            clean[
                "driver"
            ],

        "Team":
            clean[
                "team"
            ],

        "GrandPrix":
            clean[
                "grand_prix"
            ],

        "Circuit":
            clean[
                "circuit"
            ],


        # ----------------------------------------------------
        # RACE POSITION
        # ----------------------------------------------------

        "CurrentLap":
            current_lap,

        "TotalLaps":
            total_laps,

        "LapsRemaining":
            laps_remaining,

        "RaceProgress":
            race_progress,

        "RacePhase":
            race_phase,

        "Position":
            clean[
                "position"
            ],


        # ----------------------------------------------------
        # GAPS
        # ----------------------------------------------------

        "GapToAhead":
            clean[
                "gap_ahead"
            ],

        "GapAhead":
            clean[
                "gap_ahead"
            ],

        "GapBehind":
            clean[
                "gap_behind"
            ],


        # ----------------------------------------------------
        # TYRES
        # ----------------------------------------------------

        "TyreCompound":
            clean[
                "current_tyre"
            ],

        "CurrentTyre":
            clean[
                "current_tyre"
            ],

        "TyreLife":
            clean[
                "tyre_age"
            ],

        "TyreAge":
            clean[
                "tyre_age"
            ],

        "TyreCondition":
            tyre_condition,


        # ----------------------------------------------------
        # PACE
        # ----------------------------------------------------

        "RecentPace":
            clean[
                "recent_pace"
            ],

        "AveragePace":
            clean[
                "average_pace"
            ],

        "DegradationRate":
            clean[
                "degradation_rate"
            ],


        # ----------------------------------------------------
        # PIT INFORMATION
        # ----------------------------------------------------

        "PitStopsCompleted":
            clean[
                "pit_stops_completed"
            ],

        "InPit":
            False,

        "PitOut":
            False,


        # ----------------------------------------------------
        # TRACK
        # ----------------------------------------------------

        "TrackStatus":
            clean[
                "track_status"
            ],

        "SafetyCar":
            safety_car,

        "VirtualSafetyCar":
            virtual_safety_car,

        "RedFlag":
            red_flag,


        # ----------------------------------------------------
        # WEATHER
        # ----------------------------------------------------

        "Weather":
            clean[
                "weather"
            ],

        "WetConditions":
            wet_conditions,

        "Rainfall":
            clean[
                "rainfall"
            ],


        # ----------------------------------------------------
        # ORIGINAL CLEAN INPUT
        # ----------------------------------------------------

        "ManualInput":
            dict(
                clean
            ),

    }


    return race_state


# ============================================================
# ALIAS FOR STRATEGY ENGINEER
# ============================================================

def create_manual_race_state(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:

    """
    Alias for build_manual_race_state().
    """

    return build_manual_race_state(
        race_input
    )


# ============================================================
# DISPLAY MANUAL RACE STATE
# ============================================================

def display_manual_race_state(
    race_state: Dict[str, Any]
) -> None:

    """
    Display a readable Phase 7.1 race-state summary.
    """

    if not race_state:

        print(
            "No manual race state available."
        )

        return


    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.1 — MANUAL RACE STATE"
    )

    print(
        "=" * 78
    )


    print(
        f"Driver:              "
        f"{race_state.get('Driver', '--')}"
    )


    print(
        f"Team:                "
        f"{race_state.get('Team') or '--'}"
    )


    print(
        f"Grand Prix:          "
        f"{race_state.get('GrandPrix') or '--'}"
    )


    print(
        f"Circuit:             "
        f"{race_state.get('Circuit', '--')}"
    )


    print(
        "-" * 78
    )


    print(
        f"Lap:                 "
        f"{race_state.get('CurrentLap', '--')}"
        f"/"
        f"{race_state.get('TotalLaps', '--')}"
    )


    print(
        f"Laps Remaining:      "
        f"{race_state.get('LapsRemaining', '--')}"
    )


    print(
        f"Race Progress:       "
        f"{round(race_state.get('RaceProgress', 0) * 100, 1)}%"
    )


    print(
        f"Race Phase:          "
        f"{race_state.get('RacePhase', '--')}"
    )


    print(
        f"Position:            "
        f"P{race_state.get('Position', '--')}"
    )


    print(
        "-" * 78
    )


    print(
        f"Current Tyre:        "
        f"{race_state.get('TyreCompound', '--')}"
    )


    print(
        f"Tyre Age:            "
        f"{race_state.get('TyreAge', '--')} laps"
    )


    print(
        f"Tyre Condition:      "
        f"{race_state.get('TyreCondition', '--')}"
    )


    print(
        f"Pit Stops:           "
        f"{race_state.get('PitStopsCompleted', '--')}"
    )


    print(
        "-" * 78
    )


    print(
        f"Gap Ahead:           "
        f"{race_state.get('GapAhead')}"
    )


    print(
        f"Gap Behind:          "
        f"{race_state.get('GapBehind')}"
    )


    print(
        f"Recent Pace:         "
        f"{race_state.get('RecentPace')}"
    )


    print(
        f"Average Pace:        "
        f"{race_state.get('AveragePace')}"
    )


    print(
        f"Degradation Rate:    "
        f"{race_state.get('DegradationRate')}"
    )


    print(
        "-" * 78
    )


    print(
        f"Track Status:        "
        f"{race_state.get('TrackStatus', '--')}"
    )


    print(
        f"Safety Car:          "
        f"{race_state.get('SafetyCar', False)}"
    )


    print(
        f"Virtual Safety Car:  "
        f"{race_state.get('VirtualSafetyCar', False)}"
    )


    print(
        f"Weather:             "
        f"{race_state.get('Weather', '--')}"
    )


    print(
        f"Wet Conditions:      "
        f"{race_state.get('WetConditions', False)}"
    )


    print(
        f"Rainfall:            "
        f"{race_state.get('Rainfall', 0)}"
    )


    print(
        "=" * 78
    )