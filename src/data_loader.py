import os
import fastf1
import pandas as pd


# --------------------------------------------------
# FASTF1 CACHE
# --------------------------------------------------

CACHE_DIR = os.getenv(
    "FASTF1_CACHE_DIR",
    ".fastf1_cache"
)

os.makedirs(
    CACHE_DIR,
    exist_ok=True
)

fastf1.Cache.enable_cache(
    CACHE_DIR
)


# --------------------------------------------------
# LOAD SESSION
# --------------------------------------------------

def load_session(
    season: int,
    grand_prix: str,
    session_type: str = "R"
):
    """
    Load a FastF1 session.

    Parameters
    ----------
    season : int
        F1 season year.

    grand_prix : str
        Grand Prix name.

    session_type : str
        Session identifier:
        R   = Race
        Q   = Qualifying
        FP1 = Free Practice 1
        FP2 = Free Practice 2
        FP3 = Free Practice 3
        SQ  = Sprint Qualifying
        S   = Sprint

    Returns
    -------
    FastF1 Session or None
    """

    try:

        session = fastf1.get_session(
            season,
            grand_prix,
            session_type
        )

        session.load()

        return session

    except Exception as e:

        print(
            f"❌ Failed to load session: "
            f"{season} - {grand_prix} - {session_type}"
        )

        print(
            f"Error: {e}"
        )

        return None


# --------------------------------------------------
# LOAD RACE / SESSION DATA
# --------------------------------------------------

def load_race_data(
    season: int,
    grand_prix: str,
    session_type: str = "R"
) -> pd.DataFrame:

    """
    Load lap-level data for a selected F1 session.

    Returns
    -------
    pandas.DataFrame
        Lap-level session data.
    """

    session = load_session(
        season,
        grand_prix,
        session_type
    )

    if session is None:

        return pd.DataFrame()

    return session.laps.copy()


# --------------------------------------------------
# GET RACE SCHEDULE
# --------------------------------------------------

def get_race_schedule(
    season: int
) -> pd.DataFrame:

    """
    Return the F1 event schedule for a season.

    Returns
    -------
    pandas.DataFrame
        F1 event schedule.
    """

    try:

        schedule = fastf1.get_event_schedule(
            season
        )

        return schedule.copy()

    except Exception as e:

        print(
            f"❌ Failed to load "
            f"{season} F1 schedule."
        )

        print(
            f"Error: {e}"
        )

        return pd.DataFrame()


# --------------------------------------------------
# GET AVAILABLE RACES
# --------------------------------------------------

def get_available_races(
    season: int
):

    """
    Return a list of available Grand Prix names
    for a selected F1 season.

    Returns
    -------
    list
        List of Grand Prix event names.
    """

    schedule = get_race_schedule(
        season
    )

    if schedule.empty:

        return []

    if "EventName" not in schedule.columns:

        return []

    races = (
        schedule["EventName"]
        .dropna()
        .unique()
        .tolist()
    )

    return races


# --------------------------------------------------
# GET AVAILABLE DRIVERS
# --------------------------------------------------

def get_available_drivers(
    season: int,
    grand_prix: str,
    session_type: str = "R"
):

    """
    Dynamically return drivers participating
    in the selected session.

    No hardcoded driver list is required.

    Returns
    -------
    list
        List of driver abbreviations.
    """

    session = load_session(
        season,
        grand_prix,
        session_type
    )

    if session is None:

        return []

    if session.laps.empty:

        return []

    if "Driver" not in session.laps.columns:

        return []

    drivers = (
        session.laps["Driver"]
        .dropna()
        .unique()
        .tolist()
    )

    return sorted(
        drivers
    )


# --------------------------------------------------
# GET SESSION DATA FOR DRIVER
# --------------------------------------------------

def get_driver_laps(
    season: int,
    grand_prix: str,
    driver: str,
    session_type: str = "R"
) -> pd.DataFrame:

    """
    Return lap data for one selected driver.

    Returns
    -------
    pandas.DataFrame
        Lap data for the selected driver.
    """

    laps = load_race_data(
        season,
        grand_prix,
        session_type
    )

    if laps.empty:

        return pd.DataFrame()

    if "Driver" not in laps.columns:

        return pd.DataFrame()

    driver_laps = laps[
        laps["Driver"] == driver
    ].copy()

    return driver_laps