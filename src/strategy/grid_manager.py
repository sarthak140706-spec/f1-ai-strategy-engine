"""
Full-grid driver discovery and management.

Sprint 6 - Step 1
F1 AI Strategist V5
"""

from __future__ import annotations

from typing import Any


def discover_drivers(session: Any) -> list[dict[str, Any]]:
    """
    Dynamically discover all participating drivers
    from a loaded FastF1 session.

    Parameters
    ----------
    session : FastF1 Session
        A loaded FastF1 session object.

    Returns
    -------
    list[dict[str, Any]]
        List containing structured driver information.

    Raises
    ------
    ValueError
        If the session is invalid or no drivers are found.
    """

    if session is None:
        raise ValueError(
            "session cannot be None."
        )

    if not hasattr(session, "results"):
        raise ValueError(
            "Invalid FastF1 session: session.results is unavailable."
        )

    results = session.results

    if results is None or results.empty:
        raise ValueError(
            "No driver results found in the FastF1 session."
        )

    drivers = []

    for _, row in results.iterrows():

        driver = row.get(
            "Abbreviation"
        )

        driver_number = row.get(
            "DriverNumber"
        )

        full_name = row.get(
            "FullName"
        )

        team_name = row.get(
            "TeamName"
        )

        position = row.get(
            "Position"
        )

        # ---------------------------------------------
        # DRIVER VALIDATION
        # ---------------------------------------------

        if driver is None:

            continue

        if str(driver).strip() == "":

            continue

        driver = str(
            driver
        ).strip().upper()

        # ---------------------------------------------
        # DRIVER NUMBER
        # ---------------------------------------------

        if driver_number is not None:

            driver_number = str(
                driver_number
            ).strip()

        # ---------------------------------------------
        # FULL NAME
        # ---------------------------------------------

        if full_name is not None:

            full_name = str(
                full_name
            ).strip()

        # ---------------------------------------------
        # TEAM NAME
        # ---------------------------------------------

        if team_name is not None:

            team_name = str(
                team_name
            ).strip()

        # ---------------------------------------------
        # POSITION
        # ---------------------------------------------

        try:

            if position is not None:

                position = int(
                    position
                )

        except (
            TypeError,
            ValueError
        ):

            position = None

        # ---------------------------------------------
        # CREATE DRIVER RECORD
        # ---------------------------------------------

        driver_record = {

            "driver": driver,

            "driver_number":
                driver_number,

            "name":
                full_name,

            "team":
                team_name,

            "position":
                position

        }

        drivers.append(
            driver_record
        )

    # ---------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------

    unique_drivers = {}

    for driver in drivers:

        abbreviation = driver[
            "driver"
        ]

        unique_drivers[
            abbreviation
        ] = driver

    drivers = list(
        unique_drivers.values()
    )

    # ---------------------------------------------
    # SORT BY RACE POSITION
    # ---------------------------------------------

    drivers.sort(

        key=lambda driver: (

            driver[
                "position"
            ]
            if driver[
                "position"
            ] is not None

            else float(
                "inf"
            )

        )

    )

    # ---------------------------------------------
    # FINAL VALIDATION
    # ---------------------------------------------

    if not drivers:

        raise ValueError(
            "No valid drivers found in the FastF1 session."
        )

    return drivers