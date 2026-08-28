from flask import Blueprint

from api.services import (
    health,
    get_available_races,
    get_race_session,
    get_session_data,
    get_race_results,
    get_driver_performance,
    get_lap_time_analytics,
    get_tyre_strategy,
    get_pit_stop_analytics,
    get_race_pace_analytics,
    get_ai_strategy,
    get_dynamic_strategy_service
)


api = Blueprint(

    "api",

    __name__

)


# ==========================================================
# HEALTH
# ==========================================================

@api.route(

    "/health",

    methods=["GET"]

)

def health_route():

    return health()


# ==========================================================
# RACES
# ==========================================================

@api.route(

    "/races/<int:season>",

    methods=["GET"]

)

def races(

    season

):

    return get_available_races(

        season

    )


# ==========================================================
# RACE INFO
# ==========================================================

@api.route(

    "/race/<int:season>/<grand_prix>",

    methods=["GET"]

)

def race(

    season,

    grand_prix

):

    session = get_race_session(

        season,

        grand_prix.replace(

            "_",

            " "

        )

    )


    return {

        "event":
            session.event["EventName"],

        "country":
            session.event["Country"],

        "location":
            session.event["Location"],

        "laps":
            session.total_laps

    }


# ==========================================================
# PHASE 2.3.1
# HISTORICAL RACE RESULTS
# ==========================================================

@api.route(

    "/race/<int:season>/<grand_prix>/results",

    methods=["GET"]

)

def race_results(

    season,

    grand_prix

):

    return get_race_results(

        season,

        grand_prix.replace(

            "_",

            " "

        )

    )


# ==========================================================
# PHASE 2.3.3 / 2.3.4
# SESSION DATA
# ==========================================================

@api.route(

    "/session/<int:season>/<grand_prix>/<session_type>",

    methods=["GET"]

)

def session_data(

    season,

    grand_prix,

    session_type

):

    return get_session_data(

        season,

        grand_prix.replace(

            "_",

            " "

        ),

        session_type

    )


# ==========================================================
# PHASE 2.4.1
# DRIVER PERFORMANCE ANALYTICS
# ==========================================================

@api.route(

    "/analytics/driver-performance/<int:season>/<grand_prix>",

    methods=["GET"]

)

def driver_performance(

    season,

    grand_prix

):

    return get_driver_performance(

        season,

        grand_prix.replace(

            "_",

            " "

        )

    )


# ==========================================================
# PHASE 2.4.2
# LAP-TIME ANALYTICS
# ==========================================================

@api.route(

    "/analytics/lap-times/<int:season>/<grand_prix>",

    methods=["GET"]

)

def lap_time_analytics(

    season,

    grand_prix

):

    return get_lap_time_analytics(

        season,

        grand_prix.replace(

            "_",

            " "

        )

    )


# ==========================================================
# PHASE 2.4.3
# TYRE STRATEGY ANALYTICS
# ==========================================================

@api.route(

    "/race/<int:season>/<grand_prix>/tyre-strategy",

    methods=["GET"]

)

def tyre_strategy(

    season,

    grand_prix

):

    return get_tyre_strategy(

        season,

        grand_prix.replace(

            "_",

            " "

        )

    )


# ==========================================================
# PHASE 2.4.4
# PIT STOP ANALYTICS
# ==========================================================

@api.route(

    "/race/<int:season>/<grand_prix>/pit-stops",

    methods=["GET"]

)

def pit_stop_analytics(

    season,

    grand_prix

):

    return get_pit_stop_analytics(

        season,

        grand_prix.replace(

            "_",

            " "

        )

    )


# ==========================================================
# PHASE 2.4.5
# RACE PACE / PERFORMANCE TREND ANALYTICS
# ==========================================================

@api.route(

    "/race/<int:season>/<grand_prix>/race-pace",

    methods=["GET"]

)

def race_pace(

    season,

    grand_prix

):

    return get_race_pace_analytics(

        season,

        grand_prix.replace(

            "_",

            " "

        )

    )

# ==========================================================
# PHASE 3.8
# AI STRATEGY ENGINE
# ==========================================================

@api.route(
    "/strategy/<int:season>/<grand_prix>/<driver>",
    methods=["GET"]
)
def ai_strategy(
    season,
    grand_prix,
    driver
):

    return get_ai_strategy(
        season,
        grand_prix.replace(
            "_",
            " "
        ),
        driver
    )

# ==========================================================
# PHASE 5.3
# DYNAMIC STRATEGY API ROUTE
# ==========================================================

@api.route(
    "/dynamic-strategy/"
    "<int:season>/"
    "<grand_prix>/"
    "<driver>/"
    "<int:lap>",
    methods=["GET"]
)
def dynamic_strategy(
    season,
    grand_prix,
    driver,
    lap
):

    return get_dynamic_strategy_service(
        season=season,
        grand_prix=grand_prix,
        driver=driver,
        lap=lap
    )