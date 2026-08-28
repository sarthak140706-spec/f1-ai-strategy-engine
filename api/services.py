import fastf1
import pandas as pd

from src.data_loader import load_session
from src.race_state import build_race_state

from src.strategy.race_situation import (
    analyze_race_situation
)

from src.strategy.tyre_strategy import (
    generate_tyre_strategy
)

from src.strategy.pit_decision import (
    evaluate_pit_decision
)

from src.strategy.strategy_simulation import (
    run_strategy_simulation
)

from src.strategy.strategy_scoring import (
    run_strategy_scoring
)

from src.strategy.ai_recommendation import (
    generate_ai_recommendation
)
from src.api.dynamic_strategy_api import (
    get_dynamic_strategy
)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def _safe_int(value):
    """
    Convert a value to int safely.
    Returns None when conversion is not possible.
    """

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

    except Exception:
        pass

    try:
        return int(value)

    except (
        ValueError,
        TypeError
    ):
        return None


def _safe_float(value):
    """
    Convert a value to float safely.
    Returns None when conversion is not possible.
    """

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

    except Exception:
        pass

    try:
        return float(value)

    except (
        ValueError,
        TypeError
    ):
        return None


def _safe_string(value, default=""):
    """
    Convert a value to string safely.
    """

    if value is None:
        return default

    try:

        if pd.isna(value):
            return default

    except Exception:
        pass

    return str(value)


def _lap_time_to_seconds(value):
    """
    Convert a FastF1 lap-time value to seconds.
    """

    if value is None:
        return None

    try:

        if pd.isna(value):
            return None

    except Exception:
        pass

    try:

        return float(
            value.total_seconds()
        )

    except AttributeError:

        return None

    except (
        ValueError,
        TypeError
    ):

        return None


def _get_event_information(
    session,
    grand_prix
):
    """
    Extract common event information from a FastF1 session.
    """

    return {

        "name": _safe_string(
            session.event.get(
                "EventName",
                grand_prix
            ),
            grand_prix
        ),

        "country": _safe_string(
            session.event.get(
                "Country",
                ""
            )
        ),

        "location": _safe_string(
            session.event.get(
                "Location",
                ""
            )
        ),

        "date": _safe_string(
            session.event.get(
                "EventDate",
                ""
            )
        )

    }


# ==========================================================
# HEALTH
# ==========================================================

def health():

    return {

        "status": "healthy",

        "service":
            "F1 AI Strategist API"

    }


# ==========================================================
# AVAILABLE RACES
# ==========================================================

def get_available_races(
    season: int
):

    try:

        schedule = (
            fastf1.get_event_schedule(
                season
            )
        )

        races = []

        for _, event in schedule.iterrows():

            event_name = event.get(
                "EventName"
            )

            if pd.isna(event_name):

                continue

            races.append({

                "round":
                    _safe_int(
                        event.get(
                            "RoundNumber"
                        )
                    ),

                "event_name":
                    _safe_string(
                        event_name
                    ),

                "country":
                    _safe_string(
                        event.get(
                            "Country"
                        )
                    ),

                "location":
                    _safe_string(
                        event.get(
                            "Location"
                        )
                    ),

                "date":
                    _safe_string(
                        event.get(
                            "EventDate"
                        )
                    )

            })

        return {

            "season":
                season,

            "count":
                len(races),

            "races":
                races

        }

    except Exception as error:

        print(
            "Race schedule error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# RACE SESSION
# ==========================================================

def get_race_session(
    season: int,
    grand_prix: str,
    session_type: str = "R"
):

    return load_session(

        season,

        grand_prix,

        session_type

    )


# ==========================================================
# RACE RESULTS
# PHASE 2.3.1
# ==========================================================

def get_race_results(
    season: int,
    grand_prix: str
):

    try:

        print(
            "--------------------------------------------"
        )

        print(
            f"Loading race results: "
            f"{season} - {grand_prix}"
        )

        print(
            "--------------------------------------------"
        )

        # --------------------------------------------------
        # LOAD RACE
        # --------------------------------------------------

        session = get_race_session(

            season,

            grand_prix,

            "R"

        )

        if session is None:

            return {

                "error":
                    "Race session could not be loaded."

            }, 500

        # --------------------------------------------------
        # LOAD FASTF1 SESSION
        # --------------------------------------------------

        session.load()

        # --------------------------------------------------
        # EVENT INFORMATION
        # --------------------------------------------------

        event = _get_event_information(

            session,

            grand_prix

        )

        # --------------------------------------------------
        # DRIVER RESULTS
        # --------------------------------------------------

        drivers = []

        results = session.results

        if (
            results is not None
            and not results.empty
        ):

            for _, row in results.iterrows():

                drivers.append({

                    "position":
                        _safe_int(
                            row.get(
                                "Position"
                            )
                        ),

                    "driver_number":
                        _safe_string(
                            row.get(
                                "DriverNumber"
                            )
                        ),

                    "abbreviation":
                        _safe_string(
                            row.get(
                                "Abbreviation"
                            )
                        ),

                    "full_name":
                        _safe_string(
                            row.get(
                                "FullName"
                            )
                        ),

                    "team":
                        _safe_string(
                            row.get(
                                "TeamName"
                            )
                        ),

                    "laps":
                        _safe_int(
                            row.get(
                                "Laps"
                            )
                        ),

                    "points":
                        _safe_float(
                            row.get(
                                "Points"
                            )
                        )

                })

        # --------------------------------------------------
        # SORT RESULTS
        # --------------------------------------------------

        drivers.sort(

            key=lambda driver:

                driver["position"]

                if driver["position"] is not None

                else 999

        )

        # --------------------------------------------------
        # TOTAL LAPS
        # --------------------------------------------------

        total_laps = _safe_int(
            getattr(
                session,
                "total_laps",
                None
            )
        )

        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        response = {

            "season":
                season,

            "session":
                "Race",

            "event":
                event,

            "total_laps":
                total_laps,

            "drivers":
                drivers,

            "driver_count":
                len(drivers)

        }

        print(
            f"Race results loaded successfully: "
            f"{len(drivers)} drivers"
        )

        return response

    except Exception as error:

        print(
            "Race results error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# DRIVER PERFORMANCE ANALYTICS
# PHASE 2.4.1
# ==========================================================

def get_driver_performance(
    season: int,
    grand_prix: str
):

    try:

        print(
            "--------------------------------------------"
        )

        print(
            f"Loading driver performance: "
            f"{season} - {grand_prix}"
        )

        print(
            "--------------------------------------------"
        )

        session = get_race_session(

            season,

            grand_prix,

            "R"

        )

        if session is None:

            return {

                "error":
                    "Race session could not be loaded."

            }, 500

        session.load()

        event = _get_event_information(

            session,

            grand_prix

        )

        performance = []

        results = session.results

        if (
            results is not None
            and not results.empty
        ):

            for _, row in results.iterrows():

                performance.append({

                    "driver_number":
                        _safe_string(
                            row.get(
                                "DriverNumber"
                            )
                        ),

                    "abbreviation":
                        _safe_string(
                            row.get(
                                "Abbreviation"
                            )
                        ),

                    "full_name":
                        _safe_string(
                            row.get(
                                "FullName"
                            )
                        ),

                    "team":
                        _safe_string(
                            row.get(
                                "TeamName"
                            )
                        ),

                    "position":
                        _safe_int(
                            row.get(
                                "Position"
                            )
                        ),

                    "laps":
                        _safe_int(
                            row.get(
                                "Laps"
                            )
                        ),

                    "points":
                        _safe_float(
                            row.get(
                                "Points"
                            )
                        )

                })

        # --------------------------------------------------
        # SORT
        # --------------------------------------------------

        performance.sort(

            key=lambda driver:

                driver["position"]

                if driver["position"] is not None

                else 999

        )

        # --------------------------------------------------
        # SUMMARY
        # --------------------------------------------------

        valid_positions = [

            driver["position"]

            for driver in performance

            if driver["position"] is not None

        ]

        valid_points = [

            driver["points"]

            for driver in performance

            if driver["points"] is not None

        ]

        average_position = None

        if valid_positions:

            average_position = round(

                sum(valid_positions)
                /
                len(valid_positions),

                2

            )

        total_points = round(

            sum(valid_points),

            2

        ) if valid_points else 0

        response = {

            "season":
                season,

            "session":
                "Race",

            "event":
                event,

            "driver_count":
                len(performance),

            "average_position":
                average_position,

            "total_points":
                total_points,

            "drivers":
                performance

        }

        print(
            f"Driver performance loaded: "
            f"{len(performance)} drivers"
        )

        return response

    except Exception as error:

        print(
            "Driver performance error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# LAP-TIME ANALYTICS
# PHASE 2.4.2
# ==========================================================

def get_lap_time_analytics(
    season: int,
    grand_prix: str
):

    try:

        print(
            "--------------------------------------------"
        )

        print(
            f"Loading lap-time analytics: "
            f"{season} - {grand_prix}"
        )

        print(
            "--------------------------------------------"
        )

        session = get_race_session(

            season,

            grand_prix,

            "R"

        )

        if session is None:

            return {

                "error":
                    "Race session could not be loaded."

            }, 500

        session.load()

        event = _get_event_information(

            session,

            grand_prix

        )

        # --------------------------------------------------
        # CHECK LAP DATA
        # --------------------------------------------------

        if (
            session.laps is None
            or session.laps.empty
        ):

            return {

                "season":
                    season,

                "session":
                    "Race",

                "event":
                    event,

                "total_lap_records":
                    0,

                "valid_lap_records":
                    0,

                "invalid_lap_records":
                    0,

                "fastest_lap":
                    None,

                "average_lap_time":
                    None,

                "driver_count":
                    0,

                "drivers":
                    []

            }

        # --------------------------------------------------
        # KEEP AVAILABLE COLUMNS
        # --------------------------------------------------

        required_columns = [

            "Driver",

            "LapNumber",

            "LapTime"

        ]

        available_columns = [

            column

            for column in required_columns

            if column in session.laps.columns

        ]

        laps = session.laps[
            available_columns
        ].copy()

        total_lap_records = len(laps)

        if "LapTime" not in laps.columns:

            return {

                "season":
                    season,

                "session":
                    "Race",

                "event":
                    event,

                "total_lap_records":
                    total_lap_records,

                "valid_lap_records":
                    0,

                "invalid_lap_records":
                    total_lap_records,

                "fastest_lap":
                    None,

                "average_lap_time":
                    None,

                "driver_count":
                    0,

                "drivers":
                    []

            }

        # --------------------------------------------------
        # CONVERT LAP TIME
        # --------------------------------------------------

        laps["LapTimeSeconds"] = (

            laps["LapTime"].apply(
                _lap_time_to_seconds
            )

        )

        valid_laps = laps[
            laps["LapTimeSeconds"].notna()
        ].copy()

        invalid_laps = laps[
            laps["LapTimeSeconds"].isna()
        ].copy()

        valid_lap_records = len(
            valid_laps
        )

        invalid_lap_records = len(
            invalid_laps
        )

        # --------------------------------------------------
        # OVERALL STATISTICS
        # --------------------------------------------------

        fastest_lap = None
        average_lap_time = None

        if not valid_laps.empty:

            fastest_row = valid_laps.loc[

                valid_laps[
                    "LapTimeSeconds"
                ].idxmin()

            ]

            fastest_lap = {

                "driver":
                    _safe_string(
                        fastest_row.get(
                            "Driver"
                        )
                    ),

                "lap":
                    _safe_int(
                        fastest_row.get(
                            "LapNumber"
                        )
                    ),

                "lap_time_seconds":
                    round(
                        float(
                            fastest_row[
                                "LapTimeSeconds"
                            ]
                        ),
                        3
                    )

            }

            average_lap_time = round(

                float(
                    valid_laps[
                        "LapTimeSeconds"
                    ].mean()
                ),

                3

            )

        # --------------------------------------------------
        # DRIVER-WISE ANALYTICS
        # --------------------------------------------------

        drivers = []

        if (
            not valid_laps.empty
            and "Driver" in valid_laps.columns
        ):

            grouped = valid_laps.groupby(
                "Driver"
            )

            for driver, driver_data in grouped:

                fastest_driver_lap = (
                    driver_data[
                        "LapTimeSeconds"
                    ].min()
                )

                average_driver_lap = (
                    driver_data[
                        "LapTimeSeconds"
                    ].mean()
                )

                fastest_driver_row = (
                    driver_data.loc[
                        driver_data[
                            "LapTimeSeconds"
                        ].idxmin()
                    ]
                )

                drivers.append({

                    "driver":
                        _safe_string(
                            driver
                        ),

                    "lap_count":
                        len(driver_data),

                    "fastest_lap":
                        _safe_int(
                            fastest_driver_row.get(
                                "LapNumber"
                            )
                        ),

                    "fastest_lap_time_seconds":
                        round(
                            float(
                                fastest_driver_lap
                            ),
                            3
                        ),

                    "average_lap_time_seconds":
                        round(
                            float(
                                average_driver_lap
                            ),
                            3
                        )

                })

        drivers.sort(

            key=lambda driver:

                driver[
                    "fastest_lap_time_seconds"
                ]

        )

        response = {

            "season":
                season,

            "session":
                "Race",

            "event":
                event,

            "total_lap_records":
                total_lap_records,

            "valid_lap_records":
                valid_lap_records,

            "invalid_lap_records":
                invalid_lap_records,

            "fastest_lap":
                fastest_lap,

            "average_lap_time":
                average_lap_time,

            "driver_count":
                len(drivers),

            "drivers":
                drivers

        }

        print(
            f"Lap-time analytics loaded: "
            f"{valid_lap_records} valid laps"
        )

        print(
            f"Drivers analyzed: "
            f"{len(drivers)}"
        )

        return response

    except Exception as error:

        print(
            "Lap-time analytics error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# TYRE STRATEGY ANALYTICS
# PHASE 2.4.3
# ==========================================================

def get_tyre_strategy(
    season: int,
    grand_prix: str
):

    try:

        print(
            "--------------------------------------------"
        )

        print(
            f"Loading tyre strategy analytics: "
            f"{season} - {grand_prix}"
        )

        print(
            "--------------------------------------------"
        )

        session = get_race_session(

            season,

            grand_prix,

            "R"

        )

        if session is None:

            return {

                "error":
                    "Race session could not be loaded."

            }, 500

        session.load()

        event = _get_event_information(

            session,

            grand_prix

        )

        # --------------------------------------------------
        # CHECK LAP DATA
        # --------------------------------------------------

        if (
            session.laps is None
            or session.laps.empty
        ):

            return {

                "season":
                    season,

                "session":
                    "Race",

                "event":
                    event,

                "driver_count":
                    0,

                "stint_count":
                    0,

                "drivers":
                    [],

                "stints":
                    [],

                "compound_summary":
                    []

            }

        # --------------------------------------------------
        # REQUIRED DATA
        # --------------------------------------------------

        required_columns = [

            "Driver",

            "LapNumber",

            "Compound",

            "TyreLife",

            "Stint",

            "LapTime"

        ]

        available_columns = [

            column

            for column in required_columns

            if column in session.laps.columns

        ]

        laps = session.laps[
            available_columns
        ].copy()

        # --------------------------------------------------
        # CLEAN DRIVER
        # --------------------------------------------------

        if "Driver" in laps.columns:

            laps = laps[
                laps["Driver"].notna()
            ].copy()

        # --------------------------------------------------
        # CLEAN COMPOUND
        # --------------------------------------------------

        if "Compound" in laps.columns:

            laps = laps[
                laps["Compound"].notna()
            ].copy()

            laps["Compound"] = (

                laps["Compound"]
                .astype(str)
                .str.upper()
                .str.strip()

            )

            laps = laps[
                laps["Compound"] != ""
            ].copy()

        # --------------------------------------------------
        # LAP TIME
        # --------------------------------------------------

        if "LapTime" in laps.columns:

            laps["LapTimeSeconds"] = (

                laps["LapTime"].apply(
                    _lap_time_to_seconds
                )

            )

        else:

            laps["LapTimeSeconds"] = None

        # --------------------------------------------------
        # STINT DATA
        # --------------------------------------------------

        stints = []

        if (
            "Driver" in laps.columns
            and "Stint" in laps.columns
        ):

            grouped = laps.groupby(

                [
                    "Driver",
                    "Stint"
                ],

                dropna=True

            )

            for (
                driver,
                stint_number
            ), stint_data in grouped:

                if pd.isna(
                    stint_number
                ):

                    continue

                # ------------------------------------------
                # COMPOUND
                # ------------------------------------------

                compound = None

                if "Compound" in stint_data.columns:

                    compounds = (

                        stint_data[
                            "Compound"
                        ]
                        .dropna()
                        .astype(str)
                        .tolist()

                    )

                    if compounds:

                        compound = compounds[0]

                if compound is None:

                    continue

                # ------------------------------------------
                # LAP NUMBERS
                # ------------------------------------------

                valid_laps = []

                if "LapNumber" in stint_data.columns:

                    for value in stint_data[
                        "LapNumber"
                    ]:

                        converted = _safe_int(
                            value
                        )

                        if converted is not None:

                            valid_laps.append(
                                converted
                            )

                # ------------------------------------------
                # TYRE LIFE
                # ------------------------------------------

                tyre_life_values = []

                if "TyreLife" in stint_data.columns:

                    for value in stint_data[
                        "TyreLife"
                    ]:

                        converted = _safe_float(
                            value
                        )

                        if converted is not None:

                            tyre_life_values.append(
                                converted
                            )

                # ------------------------------------------
                # LAP TIMES
                # ------------------------------------------

                lap_times = []

                if (
                    "LapTimeSeconds"
                    in stint_data.columns
                ):

                    lap_times = (

                        stint_data[
                            "LapTimeSeconds"
                        ]
                        .dropna()
                        .astype(float)
                        .tolist()

                    )

                # ------------------------------------------
                # STINT RECORD
                # ------------------------------------------

                stints.append({

                    "driver":
                        _safe_string(
                            driver
                        ),

                    "stint":
                        _safe_int(
                            stint_number
                        ),

                    "compound":
                        compound,

                    "lap_count":
                        len(stint_data),

                    "start_lap":
                        min(valid_laps)
                        if valid_laps
                        else None,

                    "end_lap":
                        max(valid_laps)
                        if valid_laps
                        else None,

                    "tyre_life_start":
                        round(
                            min(
                                tyre_life_values
                            ),
                            2
                        )
                        if tyre_life_values
                        else None,

                    "tyre_life_end":
                        round(
                            max(
                                tyre_life_values
                            ),
                            2
                        )
                        if tyre_life_values
                        else None,

                    "average_lap_time_seconds":
                        round(
                            sum(lap_times)
                            /
                            len(lap_times),
                            3
                        )
                        if lap_times
                        else None

                })

        # --------------------------------------------------
        # SORT STINTS
        # --------------------------------------------------

        stints.sort(

            key=lambda item: (

                item["driver"],

                item["stint"]

                if item["stint"] is not None
                else 999

            )

        )

        # --------------------------------------------------
        # DRIVER SUMMARY
        # --------------------------------------------------

        driver_summary = []

        driver_names = sorted(

            set(

                stint["driver"]

                for stint in stints

            )

        )

        for driver in driver_names:

            driver_stints = [

                stint

                for stint in stints

                if stint["driver"] == driver

            ]

            compounds = [

                stint["compound"]

                for stint in driver_stints

                if stint["compound"] is not None

            ]

            driver_summary.append({

                "driver":
                    driver,

                "stint_count":
                    len(driver_stints),

                "compounds":
                    compounds,

                "strategy":
                    " → ".join(
                        compounds
                    ),

                "total_laps":
                    sum(
                        stint["lap_count"]
                        for stint in driver_stints
                    ),

                "stints":
                    driver_stints

            })

        # --------------------------------------------------
        # COMPOUND SUMMARY
        # --------------------------------------------------

        compound_summary = []

        if "Compound" in laps.columns:

            grouped_compounds = laps.groupby(
                "Compound"
            )

            for (
                compound,
                compound_data
            ) in grouped_compounds:

                valid_times = []

                if (
                    "LapTimeSeconds"
                    in compound_data.columns
                ):

                    valid_times = (

                        compound_data[
                            "LapTimeSeconds"
                        ]
                        .dropna()
                        .astype(float)
                        .tolist()

                    )

                compound_summary.append({

                    "compound":
                        _safe_string(
                            compound
                        ),

                    "lap_count":
                        len(
                            compound_data
                        ),

                    "driver_count":
                        compound_data[
                            "Driver"
                        ].nunique()
                        if "Driver"
                        in compound_data.columns
                        else 0,

                    "average_lap_time_seconds":
                        round(
                            sum(valid_times)
                            /
                            len(valid_times),
                            3
                        )
                        if valid_times
                        else None

                })

        compound_summary.sort(

            key=lambda item:
                item["lap_count"],

            reverse=True

        )

        compounds_used = [

            item["compound"]

            for item in compound_summary

        ]

        response = {

            "season":
                season,

            "session":
                "Race",

            "event":
                event,

            "driver_count":
                len(driver_summary),

            "stint_count":
                len(stints),

            "compounds_used":
                compounds_used,

            "compound_count":
                len(compounds_used),

            "compound_summary":
                compound_summary,

            "drivers":
                driver_summary,

            "stints":
                stints

        }

        print(
            f"Tyre strategy loaded: "
            f"{len(stints)} stints"
        )

        print(
            f"Drivers analyzed: "
            f"{len(driver_summary)}"
        )

        print(
            f"Compounds detected: "
            f"{compounds_used}"
        )

        return response

    except Exception as error:

        print(
            "Tyre strategy error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# PIT STOP ANALYTICS
# PHASE 2.4.4
# ==========================================================

def get_pit_stop_analytics(
    season: int,
    grand_prix: str
):

    try:

        print(
            "--------------------------------------------"
        )

        print(
            f"Loading pit-stop analytics: "
            f"{season} - {grand_prix}"
        )

        print(
            "--------------------------------------------"
        )

        session = get_race_session(

            season,

            grand_prix,

            "R"

        )

        if session is None:

            return {

                "error":
                    "Race session could not be loaded."

            }, 500

        session.load()

        event = _get_event_information(

            session,

            grand_prix

        )

        laps = session.laps

        if (
            laps is None
            or laps.empty
        ):

            return {

                "season":
                    season,

                "session":
                    "Race",

                "event":
                    event,

                "pit_stop_count":
                    0,

                "valid_duration_count":
                    0,

                "driver_count":
                    0,

                "average_pit_stop_duration":
                    None,

                "fastest_pit_stop":
                    None,

                "drivers":
                    [],

                "pit_stops":
                    []

            }

        # --------------------------------------------------
        # CHECK PIT-IN COLUMN
        # --------------------------------------------------

        if "PitInTime" not in laps.columns:

            return {

                "season":
                    season,

                "session":
                    "Race",

                "event":
                    event,

                "pit_stop_count":
                    0,

                "valid_duration_count":
                    0,

                "driver_count":
                    0,

                "average_pit_stop_duration":
                    None,

                "fastest_pit_stop":
                    None,

                "drivers":
                    [],

                "pit_stops":
                    []

            }

        required_columns = [

            "Driver",

            "LapNumber",

            "PitInTime",

            "PitOutTime",

            "LapTime"

        ]

        available_columns = [

            column

            for column in required_columns

            if column in laps.columns

        ]

        pit_data = laps[
            available_columns
        ].copy()

        pit_data = pit_data[
            pit_data["PitInTime"].notna()
        ].copy()

        # --------------------------------------------------
        # PIT STOP RECORDS
        # --------------------------------------------------

        pit_stops = []

        for _, row in pit_data.iterrows():

            driver = _safe_string(
                row.get(
                    "Driver"
                )
            )

            lap_number = _safe_int(
                row.get(
                    "LapNumber"
                )
            )

            pit_in_time = row.get(
                "PitInTime"
            )

            pit_out_time = row.get(
                "PitOutTime"
            )

            duration = None

            if (
                pd.notna(pit_in_time)
                and pd.notna(pit_out_time)
            ):

                try:

                    duration = (

                        pit_out_time
                        -
                        pit_in_time

                    ).total_seconds()

                except Exception:

                    duration = None

            pit_stops.append({

                "driver":
                    driver,

                "lap":
                    lap_number,

                "pit_in_time":

                    str(
                        pit_in_time
                    )
                    if pd.notna(
                        pit_in_time
                    )
                    else None,

                "pit_out_time":

                    str(
                        pit_out_time
                    )
                    if pd.notna(
                        pit_out_time
                    )
                    else None,

                "duration_seconds":

                    round(
                        float(duration),
                        3
                    )
                    if duration is not None
                    else None

            })

        # --------------------------------------------------
        # VALID STOPS
        # --------------------------------------------------

        valid_stops = [

            stop

            for stop in pit_stops

            if stop[
                "duration_seconds"
            ] is not None

        ]

        # --------------------------------------------------
        # FASTEST
        # --------------------------------------------------

        fastest_pit_stop = None

        if valid_stops:

            fastest_pit_stop = min(

                valid_stops,

                key=lambda stop:
                    stop[
                        "duration_seconds"
                    ]

            )

        # --------------------------------------------------
        # AVERAGE
        # --------------------------------------------------

        average_pit_stop_duration = None

        if valid_stops:

            average_pit_stop_duration = round(

                sum(

                    stop[
                        "duration_seconds"
                    ]

                    for stop in valid_stops

                )
                /
                len(valid_stops),

                3

            )

        # --------------------------------------------------
        # DRIVER ANALYTICS
        # --------------------------------------------------

        drivers = []

        driver_names = sorted(

            set(

                stop["driver"]

                for stop in pit_stops

                if stop["driver"]

            )

        )

        for driver in driver_names:

            driver_stops = [

                stop

                for stop in pit_stops

                if stop["driver"] == driver

            ]

            driver_valid_stops = [

                stop

                for stop in driver_stops

                if stop[
                    "duration_seconds"
                ] is not None

            ]

            driver_average = None

            if driver_valid_stops:

                driver_average = round(

                    sum(

                        stop[
                            "duration_seconds"
                        ]

                        for stop
                        in driver_valid_stops

                    )
                    /
                    len(
                        driver_valid_stops
                    ),

                    3

                )

            driver_fastest = None

            if driver_valid_stops:

                driver_fastest = min(

                    driver_valid_stops,

                    key=lambda stop:
                        stop[
                            "duration_seconds"
                        ]

                )

            drivers.append({

                "driver":
                    driver,

                "pit_stop_count":
                    len(driver_stops),

                "average_pit_stop_duration":
                    driver_average,

                "fastest_pit_stop":
                    driver_fastest

            })

        drivers.sort(

            key=lambda driver:
                driver[
                    "pit_stop_count"
                ],

            reverse=True

        )

        response = {

            "season":
                season,

            "session":
                "Race",

            "event":
                event,

            "pit_stop_count":
                len(pit_stops),

            "valid_duration_count":
                len(valid_stops),

            "driver_count":
                len(drivers),

            "average_pit_stop_duration":
                average_pit_stop_duration,

            "fastest_pit_stop":
                fastest_pit_stop,

            "drivers":
                drivers,

            "pit_stops":
                pit_stops

        }

        print(
            f"Pit-stop analytics loaded: "
            f"{len(pit_stops)} pit stops"
        )

        print(
            f"Drivers analyzed: "
            f"{len(drivers)}"
        )

        return response

    except Exception as error:

        print(
            "Pit-stop analytics error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# RACE PACE / PERFORMANCE TREND ANALYTICS
# PHASE 2.4.5
# ==========================================================

def get_race_pace_analytics(
    season: int,
    grand_prix: str
):

    try:

        print(
            "--------------------------------------------"
        )

        print(
            f"Loading race pace analytics: "
            f"{season} - {grand_prix}"
        )

        print(
            "--------------------------------------------"
        )

        session = get_race_session(

            season,

            grand_prix,

            "R"

        )

        if session is None:

            return {

                "error":
                    "Race session could not be loaded."

            }, 500

        session.load()

        event = _get_event_information(

            session,

            grand_prix

        )

        if (
            session.laps is None
            or session.laps.empty
        ):

            return {

                "season":
                    season,

                "session":
                    "Race",

                "event":
                    event,

                "driver_count":
                    0,

                "drivers":
                    [],

                "total_lap_records":
                    0,

                "valid_lap_records":
                    0

            }

        required_columns = [

            "Driver",

            "LapNumber",

            "LapTime"

        ]

        missing_columns = [

            column

            for column in required_columns

            if column not in session.laps.columns

        ]

        if missing_columns:

            return {

                "error":
                    "Required lap columns missing.",

                "missing_columns":
                    missing_columns

            }, 500

        laps = session.laps[
            required_columns
        ].copy()

        total_lap_records = len(laps)

        laps[
            "LapTimeSeconds"
        ] = laps[
            "LapTime"
        ].apply(
            _lap_time_to_seconds
        )

        laps = laps[
            laps[
                "LapTimeSeconds"
            ].notna()
        ].copy()

        laps = laps[
            laps[
                "LapNumber"
            ].notna()
        ].copy()

        laps[
            "LapNumber"
        ] = laps[
            "LapNumber"
        ].astype(int)

        valid_lap_records = len(laps)

        # --------------------------------------------------
        # DRIVER ANALYTICS
        # --------------------------------------------------

        drivers = []

        grouped = laps.groupby(
            "Driver"
        )

        for driver, driver_data in grouped:

            driver_data = (

                driver_data
                .sort_values(
                    "LapNumber"
                )
                .copy()

            )

            if driver_data.empty:

                continue

            average_pace = float(

                driver_data[
                    "LapTimeSeconds"
                ].mean()

            )

            fastest_pace = float(

                driver_data[
                    "LapTimeSeconds"
                ].min()

            )

            slowest_pace = float(

                driver_data[
                    "LapTimeSeconds"
                ].max()

            )

            first_lap_row = (
                driver_data.iloc[0]
            )

            last_lap_row = (
                driver_data.iloc[-1]
            )

            first_lap_number = int(
                first_lap_row[
                    "LapNumber"
                ]
            )

            first_lap_time = float(
                first_lap_row[
                    "LapTimeSeconds"
                ]
            )

            last_lap_number = int(
                last_lap_row[
                    "LapNumber"
                ]
            )

            last_lap_time = float(
                last_lap_row[
                    "LapTimeSeconds"
                ]
            )

            pace_change = (

                last_lap_time
                -
                first_lap_time

            )

            lap_history = []

            for _, row in driver_data.iterrows():

                lap_history.append({

                    "lap":
                        int(
                            row[
                                "LapNumber"
                            ]
                        ),

                    "lap_time_seconds":
                        round(
                            float(
                                row[
                                    "LapTimeSeconds"
                                ]
                            ),
                            3
                        )

                })

            drivers.append({

                "driver":
                    _safe_string(
                        driver
                    ),

                "lap_count":
                    len(driver_data),

                "average_pace_seconds":
                    round(
                        average_pace,
                        3
                    ),

                "fastest_lap_seconds":
                    round(
                        fastest_pace,
                        3
                    ),

                "slowest_lap_seconds":
                    round(
                        slowest_pace,
                        3
                    ),

                "first_lap":
                    first_lap_number,

                "first_lap_time_seconds":
                    round(
                        first_lap_time,
                        3
                    ),

                "last_lap":
                    last_lap_number,

                "last_lap_time_seconds":
                    round(
                        last_lap_time,
                        3
                    ),

                "pace_change_seconds":
                    round(
                        pace_change,
                        3
                    ),

                "lap_history":
                    lap_history

            })

        # --------------------------------------------------
        # SORT BY AVERAGE PACE
        # --------------------------------------------------

        drivers.sort(

            key=lambda driver:
                driver[
                    "average_pace_seconds"
                ]

        )

        # --------------------------------------------------
        # OVERALL PACE
        # --------------------------------------------------

        overall_average_pace = None

        if not laps.empty:

            overall_average_pace = round(

                float(
                    laps[
                        "LapTimeSeconds"
                    ].mean()
                ),

                3

            )

        # --------------------------------------------------
        # FASTEST DRIVER
        # --------------------------------------------------

        fastest_driver = None

        if drivers:

            fastest_driver = {

                "driver":
                    drivers[0][
                        "driver"
                    ],

                "average_pace_seconds":
                    drivers[0][
                        "average_pace_seconds"
                    ]

            }

        response = {

            "season":
                season,

            "session":
                "Race",

            "event":
                event,

            "total_lap_records":
                total_lap_records,

            "valid_lap_records":
                valid_lap_records,

            "driver_count":
                len(drivers),

            "overall_average_pace":
                overall_average_pace,

            "fastest_driver":
                fastest_driver,

            "drivers":
                drivers

        }

        print(
            f"Race pace analytics loaded: "
            f"{len(drivers)} drivers"
        )

        print(
            f"Valid lap records: "
            f"{valid_lap_records}"
        )

        if fastest_driver:

            print(
                "Fastest average race pace:",
                fastest_driver
            )

        return response

    except Exception as error:

        print(
            "Race pace analytics error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# SESSION DATA
# ==========================================================

def get_session_data(
    season: int,
    grand_prix: str,
    session_type: str = "R"
):

    try:

        session = get_race_session(

            season,

            grand_prix,

            session_type

        )

        if session is None:

            return {

                "error":
                    "Race session could not be loaded."

            }, 500

        session.load()

        # --------------------------------------------------
        # EVENT
        # --------------------------------------------------

        event = _get_event_information(

            session,

            grand_prix

        )

        # --------------------------------------------------
        # DRIVERS
        # --------------------------------------------------

        drivers = []

        if (
            session.results is not None
            and not session.results.empty
        ):

            for _, row in session.results.iterrows():

                drivers.append({

                    "driver_number":
                        _safe_string(
                            row.get(
                                "DriverNumber"
                            )
                        ),

                    "abbreviation":
                        _safe_string(
                            row.get(
                                "Abbreviation"
                            )
                        ),

                    "full_name":
                        _safe_string(
                            row.get(
                                "FullName"
                            )
                        ),

                    "team":
                        _safe_string(
                            row.get(
                                "TeamName"
                            )
                        ),

                    "position":
                        _safe_int(
                            row.get(
                                "Position"
                            )
                        )

                })

        # --------------------------------------------------
        # LAP DATA
        # --------------------------------------------------

        laps = []

        if (
            session.laps is not None
            and not session.laps.empty
        ):

            required_columns = [

                "Driver",

                "LapNumber",

                "LapTime",

                "Compound",

                "TyreLife",

                "Stint"

            ]

            available_columns = [

                column

                for column in required_columns

                if column in session.laps.columns

            ]

            lap_data = session.laps[
                available_columns
            ].copy()

            # Keep response manageable

            lap_data = lap_data.head(
                500
            )

            for _, row in lap_data.iterrows():

                lap_number = _safe_int(
                    row.get(
                        "LapNumber"
                    )
                )

                tyre_life = _safe_float(
                    row.get(
                        "TyreLife"
                    )
                )

                stint = _safe_int(
                    row.get(
                        "Stint"
                    )
                )

                lap_time = row.get(
                    "LapTime"
                )

                compound = row.get(
                    "Compound"
                )

                laps.append({

                    "driver":
                        _safe_string(
                            row.get(
                                "Driver"
                            )
                        ),

                    "lap":
                        lap_number,

                    "lap_time":

                        str(
                            lap_time
                        )
                        if pd.notna(
                            lap_time
                        )
                        else None,

                    "compound":

                        _safe_string(
                            compound
                        )
                        if pd.notna(
                            compound
                        )
                        else None,

                    "tyre_life":
                        tyre_life,

                    "stint":
                        stint

                })

        # --------------------------------------------------
        # TOTAL LAPS
        # --------------------------------------------------

        total_laps = _safe_int(

            getattr(
                session,
                "total_laps",
                None
            )

        )

        return {

            "season":
                season,

            "session":
                session_type,

            "event":
                event,

            "total_laps":
                total_laps,

            "drivers":
                drivers,

            "driver_count":
                len(drivers),

            "laps":
                laps,

            "lap_count":
                len(laps)

        }

    except Exception as error:

        print(
            "Session data error:",
            error
        )

        return {

            "error":
                str(error)

        }, 500


# ==========================================================
# PHASE 3.8
# AI STRATEGY API SERVICE
# ==========================================================

def get_ai_strategy(
    season: int,
    grand_prix: str,
    driver: str,
    session_type: str = "R"
):
    """
    Generate the complete Phase 3 AI strategy result.

    Pipeline:

        FastF1 Session
              ↓
        Race State
              ↓
        Race Situation
              ↓
        Tyre Strategy
              ↓
        Pit Decision
              ↓
        Strategy Simulation
              ↓
        Strategy Scoring
              ↓
        AI Recommendation
    """

    # ======================================================
    # INPUT VALIDATION
    # ======================================================

    if not isinstance(
        season,
        int
    ):

        raise TypeError(
            "season must be an integer."
        )

    if (
        not isinstance(
            grand_prix,
            str
        )
        or not grand_prix.strip()
    ):

        raise ValueError(
            "grand_prix must be a valid "
            "non-empty string."
        )

    if (
        not isinstance(
            driver,
            str
        )
        or not driver.strip()
    ):

        raise ValueError(
            "driver must be a valid "
            "non-empty driver abbreviation."
        )

    driver = driver.upper().strip()

    # ======================================================
    # STEP 1
    # LOAD SESSION
    # ======================================================

    session = load_session(

        season=season,

        grand_prix=grand_prix,

        session_type=session_type

    )

    if session is None:

        raise RuntimeError(
            "Unable to load FastF1 session."
        )

    # ======================================================
    # STEP 2
    # BUILD RACE STATE
    # ======================================================

    race_state = build_race_state(

        session=session,

        driver=driver

    )

    if not race_state:

        raise RuntimeError(
            "Race state generation returned empty data."
        )

    # ======================================================
    # STEP 3
    # RACE SITUATION
    # ======================================================

    race_situation = (
        analyze_race_situation(
            race_state
        )
    )

    if not race_situation:

        raise RuntimeError(
            "Race situation analysis returned empty data."
        )

    # ======================================================
    # STEP 4
    # EXTRACT STRATEGY INPUTS
    # ======================================================

    current_lap = race_state.get(
        "CurrentLap"
    )

    current_tyre = race_state.get(
        "TyreCompound"
    )

    tyre_age = race_state.get(
        "TyreLife"
    )

    remaining_laps = race_state.get(
        "LapsRemaining"
    )

    base_lap_time = race_state.get(
        "RecentPace"
    )

    position = race_state.get(
        "Position"
    )

    gap_ahead = race_state.get(
        "GapToAhead"
    )

    gap_behind = race_state.get(
        "GapToBehind"
    )

    degradation_rate = race_state.get(
        "DegradationRate"
    )

    pit_loss = race_state.get(
        "PitLoss"
    )

    # ======================================================
    # DEFAULT VALUES
    # ======================================================

    if pit_loss is None:

        pit_loss = 22.0

    if degradation_rate is None:

        degradation_rate = 0.0

    # ======================================================
    # HISTORICAL RACE HANDLING
    # ======================================================

    historical_snapshot = False

    if (
        remaining_laps is None
        or remaining_laps <= 0
    ):

        historical_snapshot = True

        current_lap = 35

        remaining_laps = 22

        current_tyre = "HARD"

        tyre_age = 22

        position = 4

        gap_ahead = 1.8

        gap_behind = 12.4

        base_lap_time = 96.2

        degradation_rate = 0.735

        pit_loss = 22.0

    # ======================================================
    # REQUIRED VALUE VALIDATION
    # ======================================================

    if current_lap is None:

        raise ValueError(
            "CurrentLap is unavailable."
        )

    if current_tyre is None:

        raise ValueError(
            "TyreCompound is unavailable."
        )

    if tyre_age is None:

        raise ValueError(
            "TyreLife is unavailable."
        )

    if remaining_laps is None:

        raise ValueError(
            "LapsRemaining is unavailable."
        )

    if base_lap_time is None:

        raise ValueError(
            "RecentPace is unavailable."
        )

    if remaining_laps <= 0:

        raise ValueError(
            "Strategy engine requires "
            "remaining_laps greater than zero."
        )

    # ======================================================
    # STEP 5
    # TYRE STRATEGY
    # ======================================================

    tyre_decision = generate_tyre_strategy(

        base_lap_time=float(
            base_lap_time
        ),

        current_tyre=str(
            current_tyre
        ),

        tyre_age=int(
            tyre_age
        ),

        remaining_laps=int(
            remaining_laps
        ),

        pit_loss=float(
            pit_loss
        )

    )

    if not tyre_decision:

        raise RuntimeError(
            "Tyre strategy generation failed."
        )

    recommended_tyre = (
        tyre_decision.get(
            "Compound"
        )
    )

    # ======================================================
    # STEP 6
    # PIT DECISION
    # ======================================================

    pit_decision = evaluate_pit_decision(

        current_lap=int(
            current_lap
        ),

        remaining_laps=int(
            remaining_laps
        ),

        current_tyre=str(
            current_tyre
        ),

        tyre_age=float(
            tyre_age
        ),

        recent_pace=float(
            base_lap_time
        ),

        position=(
            int(position)
            if position is not None
            else None
        ),

        gap_ahead=(
            float(gap_ahead)
            if gap_ahead is not None
            else None
        ),

        gap_behind=(
            float(gap_behind)
            if gap_behind is not None
            else None
        ),

        pit_loss=float(
            pit_loss
        ),

        recommended_tyre=
            recommended_tyre,

        degradation_rate=float(
            degradation_rate
        ),

        race_situation=
            race_situation

    )

    if not pit_decision:

        raise RuntimeError(
            "Pit-stop decision generation failed."
        )

    # ======================================================
    # STEP 7
    # STRATEGY SIMULATION
    # ======================================================

    simulation_result = (
        run_strategy_simulation(

            base_lap_time=float(
                base_lap_time
            ),

            current_tyre=str(
                current_tyre
            ),

            tyre_age=int(
                tyre_age
            ),

            remaining_laps=int(
                remaining_laps
            ),

            pit_loss=float(
                pit_loss
            )

        )
    )

    if not simulation_result:

        raise RuntimeError(
            "Strategy simulation returned empty data."
        )

    # ======================================================
    # STEP 8
    # STRATEGY SCORING
    # ======================================================

    strategies = (
        simulation_result.get(
            "strategies",
            []
        )
    )

    if not strategies:

        raise RuntimeError(
            "No simulated strategies were generated."
        )

    scoring_result = (
        run_strategy_scoring(
            strategies
        )
    )

    if not scoring_result:

        raise RuntimeError(
            "Strategy scoring returned empty data."
        )

    # ======================================================
    # STEP 9
    # AI RECOMMENDATION
    # ======================================================

    recommendation = (
        generate_ai_recommendation(

            scoring_result=
                scoring_result,

            race_situation=
                race_situation,

            tyre_decision=
                tyre_decision,

            pit_decision=
                pit_decision

        )
    )

    if not recommendation:

        raise RuntimeError(
            "AI recommendation generation failed."
        )

    # ======================================================
    # COMPLETE RESPONSE
    # ======================================================

    return {

        # --------------------------------------------------
        # REQUEST
        # --------------------------------------------------

        "season":
            season,

        "grand_prix":
            grand_prix,

        "driver":
            driver,

        "session_type":
            session_type,

        # --------------------------------------------------
        # STRATEGY MODE
        # --------------------------------------------------

        "strategy_mode":

            (
                "HISTORICAL_TEST_SNAPSHOT"

                if historical_snapshot

                else "LIVE_RACE_STATE"

            ),

        # --------------------------------------------------
        # RACE STATE
        # --------------------------------------------------

        "race_state":
            race_state,

        # --------------------------------------------------
        # STRATEGIC INPUTS
        # --------------------------------------------------

        "strategy_inputs": {

            "current_lap":
                int(current_lap),

            "remaining_laps":
                int(remaining_laps),

            "current_tyre":
                str(current_tyre),

            "tyre_age":
                int(tyre_age),

            "base_lap_time":
                float(base_lap_time),

            "position":

                (
                    int(position)
                    if position is not None
                    else None
                ),

            "gap_ahead":

                (
                    float(gap_ahead)
                    if gap_ahead is not None
                    else None
                ),

            "gap_behind":

                (
                    float(gap_behind)
                    if gap_behind is not None
                    else None
                ),

            "pit_loss":
                float(pit_loss),

            "degradation_rate":
                float(degradation_rate)

        },

        # --------------------------------------------------
        # RACE SITUATION
        # --------------------------------------------------

        "race_situation":
            race_situation,

        # --------------------------------------------------
        # TYRE STRATEGY
        # --------------------------------------------------

        "tyre_strategy":
            tyre_decision,

        # --------------------------------------------------
        # PIT DECISION
        # --------------------------------------------------

        "pit_decision":
            pit_decision,

        # --------------------------------------------------
        # STRATEGY SIMULATION
        # --------------------------------------------------

        "strategy_simulation":
            simulation_result,

        # --------------------------------------------------
        # STRATEGY SCORING
        # --------------------------------------------------

        "strategy_scoring":
            scoring_result,

        # --------------------------------------------------
        # AI RECOMMENDATION
        # --------------------------------------------------

        "ai_recommendation":
            recommendation

    }

# ============================================================
# PHASE 5.3
# DYNAMIC STRATEGY FLASK SERVICE
# ============================================================

def get_dynamic_strategy_service(
    season: int,
    grand_prix: str,
    driver: str,
    lap: int
):
    """
    Flask service wrapper for the Phase 5.2
    Dynamic Strategy API.

    Pipeline
    --------
    Flask Route
        ↓
    Phase 5.3 Service
        ↓
    Phase 5.2 Dynamic Strategy API
        ↓
    Phase 5.1 Unified Service
        ↓
    Phase 4 Dynamic Strategy Engine
    """

    # ========================================================
    # INPUT NORMALIZATION
    # ========================================================

    grand_prix = (
        str(grand_prix)
        .replace("_", " ")
        .strip()
    )

    driver = (
        str(driver)
        .strip()
        .upper()
    )


    # ========================================================
    # EXECUTE PHASE 5.2
    # ========================================================

    try:

        result = get_dynamic_strategy(
            season=season,
            grand_prix=grand_prix,
            driver=driver,
            lap=lap
        )


        if not result:

            return {
                "status": "ERROR",
                "phase": "5.3",
                "error":
                    "Dynamic strategy engine returned no data."
            }, 500


        return result


    except ValueError as error:

        return {
            "status": "ERROR",
            "phase": "5.3",
            "error": str(error)
        }, 400


    except Exception as error:

        print(
            "Dynamic strategy service error:",
            error
        )

        return {
            "status": "ERROR",
            "phase": "5.3",
            "error": str(error)
        }, 500