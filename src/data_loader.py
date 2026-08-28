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
# SUPPORTED SESSION TYPES
# --------------------------------------------------

VALID_SESSION_TYPES = {

    "R",
    "Q",
    "FP1",
    "FP2",
    "FP3",
    "SQ",
    "S"

}


# --------------------------------------------------
# VALIDATE GRAND PRIX
# --------------------------------------------------

def validate_grand_prix(
    season: int,
    grand_prix: str
) -> None:
    """
    Validate that the requested Grand Prix
    exists in the specified F1 season.

    The validation accepts:
        - EventName
        - Country
        - Location

    Comparison is case-insensitive.
    """

    try:

        schedule = fastf1.get_event_schedule(
            season
        )

    except Exception as e:

        raise RuntimeError(

            f"Failed to retrieve F1 schedule "
            f"for season {season}: {e}"

        ) from e


    # --------------------------------------------------
    # BUILD VALID GRAND PRIX NAMES
    # --------------------------------------------------

    valid_grands_prix = []

    for _, event in schedule.iterrows():

        # Event name
        if pd.notna(
            event.EventName
        ):

            valid_grands_prix.append(
                str(
                    event.EventName
                ).strip()
            )

        # Country
        if pd.notna(
            event.Country
        ):

            valid_grands_prix.append(
                str(
                    event.Country
                ).strip()
            )

        # Circuit/location
        if pd.notna(
            event.Location
        ):

            valid_grands_prix.append(
                str(
                    event.Location
                ).strip()
            )


    # --------------------------------------------------
    # CASE-INSENSITIVE VALIDATION
    # --------------------------------------------------

    requested_grand_prix = (
        grand_prix.strip().lower()
    )

    valid_grands_prix_lower = [

        gp.lower()

        for gp in valid_grands_prix

    ]


    if (
        requested_grand_prix
        not in valid_grands_prix_lower
    ):

        raise ValueError(

            f"Invalid Grand Prix: "
            f"{grand_prix}. "

            f"Please provide a valid Grand Prix "
            f"name for the {season} season."

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
    Load a FastF1 session with input validation.
    """

    # --------------------------------------------------
    # VALIDATE SEASON
    # --------------------------------------------------

    if not isinstance(
        season,
        int
    ):

        raise TypeError(
            "season must be an integer."
        )


    if season < 1950:

        raise ValueError(

            f"Invalid F1 season: {season}. "

            "Season must be 1950 or later."

        )


    # --------------------------------------------------
    # VALIDATE GRAND PRIX
    # --------------------------------------------------

    if not isinstance(
        grand_prix,
        str
    ):

        raise TypeError(
            "grand_prix must be a string."
        )


    grand_prix = grand_prix.strip()


    if not grand_prix:

        raise ValueError(
            "grand_prix cannot be empty."
        )


    validate_grand_prix(

        season,

        grand_prix

    )


    # --------------------------------------------------
    # VALIDATE SESSION TYPE
    # --------------------------------------------------

    if not isinstance(
        session_type,
        str
    ):

        raise TypeError(
            "session_type must be a string."
        )


    session_type = (
        session_type
        .strip()
        .upper()
    )


    if not session_type:

        raise ValueError(
            "session_type cannot be empty."
        )


    if session_type not in VALID_SESSION_TYPES:

        raise ValueError(

            f"Unsupported session type: "

            f"{session_type}. "

            f"Supported types: "

            f"{sorted(VALID_SESSION_TYPES)}"

        )


    # --------------------------------------------------
    # LOAD FASTF1 SESSION
    # --------------------------------------------------

    try:

        session = fastf1.get_session(

            season,

            grand_prix,

            session_type

        )

        session.load(
            telemetry=False,
            weather=False,
            messages=False
        )

        return session


    except Exception as e:

        raise RuntimeError(

            f"Failed to load F1 session.\n"

            f"Season: {season}\n"

            f"Grand Prix: {grand_prix}\n"

            f"Session: {session_type}\n"

            f"Error: {e}"

        ) from e