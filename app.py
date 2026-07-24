import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_loader import (
    get_race_schedule,
    get_available_drivers,
    get_driver_laps
)

from src.preprocessing import (
    preprocess_data
)

from src.feature_engineering import (
    detect_pit_stops,
    create_race_features
)

from src.predict import (
    predict_pit_probability
)

from src.simulator import (
    simulate_strategy
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(

    page_title=
        "F1 AI Strategy Engineer",

    page_icon=
        "🏎️",

    layout=
        "wide"

)


st.title(
    "🏎️ F1 AI Strategy Engineer"
)

st.caption(
    "V5 Foundation — Dynamic F1 Race Data"
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header(
    "🏁 Race Selection"
)


# --------------------------------------------------
# SEASON
# --------------------------------------------------

season = st.sidebar.number_input(

    "Season",

    min_value=2018,

    max_value=2026,

    value=2025,

    step=1

)


# --------------------------------------------------
# GET SCHEDULE
# --------------------------------------------------

try:

    schedule = get_race_schedule(
        season
    )

    races = (

        schedule[
            "EventName"
        ]

        .dropna()

        .tolist()

    )

except Exception as e:

    st.error(
        f"Unable to load schedule: {e}"
    )

    st.stop()


# --------------------------------------------------
# GRAND PRIX
# --------------------------------------------------

grand_prix = st.sidebar.selectbox(

    "Grand Prix",

    races

)


# --------------------------------------------------
# SESSION
# --------------------------------------------------

session_type = st.sidebar.selectbox(

    "Session",

    [
        "R",
        "Q",
        "FP1",
        "FP2",
        "FP3",
        "S"
    ]

)


# ==================================================
# LOAD DRIVERS
# ==================================================

try:

    drivers = get_available_drivers(

        season,

        grand_prix,

        session_type

    )

except Exception as e:

    st.warning(
        "Unable to load drivers for this session."
    )

    st.caption(
        str(e)
    )

    st.stop()


if not drivers:

    st.warning(
        "No drivers found for this session."
    )

    st.stop()


# --------------------------------------------------
# DRIVER SELECTOR
# --------------------------------------------------

driver = st.sidebar.selectbox(

    "Driver",

    drivers

)


# ==================================================
# LOAD DRIVER DATA
# ==================================================

if st.sidebar.button(
    "🏁 Analyze Strategy"
):

    with st.spinner(
        "Loading F1 session data..."
    ):

        try:

            driver_laps = get_driver_laps(

                season,

                grand_prix,

                driver,

                session_type

            )

        except Exception as e:

            st.error(
                f"Unable to load driver data: {e}"
            )

            st.stop()


    # --------------------------------------------------
    # PREPROCESS
    # --------------------------------------------------

    driver_laps = preprocess_data(
        driver_laps
    )


    driver_laps = detect_pit_stops(
        driver_laps
    )


    driver_laps = create_race_features(
        driver_laps
    )


    if driver_laps.empty:

        st.error(
            "No valid lap data available."
        )

        st.stop()


    # ==================================================
    # CURRENT RACE STATE
    # ==================================================

    latest = (

        driver_laps

        .sort_values(
            "LapNumber"
        )

        .iloc[-1]

    )


    # --------------------------------------------------
    # BUILD MODEL INPUT
    # --------------------------------------------------

    model_features = [

        "LapNumber",

        "TyreLife",

        "Position",

        "LapsRemaining",

        "RaceProgress",

        "AvgPaceLast3",

        "AvgPaceLast5",

        "AvgPaceLast10",

        "DegradationRate",

        "CurrentStintLength",

        "PitStopsCompleted"

    ]


    missing_features = [

        feature

        for feature in model_features

        if feature
        not in latest.index

    ]


    if missing_features:

        st.error(

            "Missing required features: "

            + ", ".join(
                missing_features
            )

        )

        st.stop()


    model_input = pd.DataFrame(

        [[

            latest[
                feature
            ]

            for feature
            in model_features

        ]],

        columns=
            model_features

    )


    # ==================================================
    # ML PREDICTION
    # ==================================================

    try:

        pit_probability = (

            predict_pit_probability(

                model_input

            )

        )

    except Exception as e:

        st.error(

            f"Prediction failed: {e}"

        )

        st.stop()


    # ==================================================
    # TOP METRICS
    # ==================================================

    col1, col2, col3, col4 = (

        st.columns(4)

    )


    col1.metric(

        "Current Lap",

        int(
            latest[
                "LapNumber"
            ]
        )

    )


    col2.metric(

        "Position",

        int(
            latest[
                "Position"
            ]
        )

    )


    col3.metric(

        "Tyre Life",

        int(
            latest[
                "TyreLife"
            ]
        )

    )


    col4.metric(

        "Pit Probability",

        f"{pit_probability}%"

    )


    st.divider()


    # ==================================================
    # RACE ENGINEER PANEL
    # ==================================================

    st.subheader(

        "🧠 Race Engineer Analysis"

    )


    if pit_probability >= 50:

        decision = "PIT"

        st.error(

            f"🔴 RECOMMENDATION: {decision}"

        )

    else:

        decision = "STAY"

        st.success(

            f"🟢 RECOMMENDATION: {decision}"

        )


    st.info(

        f"Pit Probability: "
        f"{pit_probability}%"

    )


    # ==================================================
    # CURRENT RACE DATA
    # ==================================================

    st.subheader(

        "📊 Current Race State"

    )


    race_state_df = pd.DataFrame({

        "Metric": [

            "Driver",

            "Lap",

            "Position",

            "Tyre Life",

            "Laps Remaining",

            "Average Pace (Last 5)",

            "Degradation Rate",

            "Pit Stops"

        ],

        "Value": [

            driver,

            latest[
                "LapNumber"
            ],

            latest[
                "Position"
            ],

            latest[
                "TyreLife"
            ],

            latest[
                "LapsRemaining"
            ],

            round(

                latest[
                    "AvgPaceLast5"
                ],

                3

            ),

            round(

                latest[
                    "DegradationRate"
                ],

                3

            ),

            latest[
                "PitStopsCompleted"
            ]

        ]

    })


    st.dataframe(

        race_state_df,

        use_container_width=True,

        hide_index=True

    )


    # ==================================================
    # LAP TIME GRAPH
    # ==================================================

    st.subheader(

        "⏱️ Lap Time Progression"

    )


    fig = px.line(

        driver_laps,

        x="LapNumber",

        y="LapTimeSeconds",

        title=
            f"{driver} Lap Time Progression"

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


    # ==================================================
    # PACE GRAPH
    # ==================================================

    st.subheader(

        "📈 Pace Analysis"

    )


    pace_df = driver_laps[

        [

            "LapNumber",

            "AvgPaceLast3",

            "AvgPaceLast5",

            "AvgPaceLast10"

        ]

    ]


    fig2 = px.line(

        pace_df,

        x="LapNumber",

        y=[

            "AvgPaceLast3",

            "AvgPaceLast5",

            "AvgPaceLast10"

        ],

        title=
            "Rolling Pace Analysis"

    )


    st.plotly_chart(

        fig2,

        use_container_width=True

    )


    st.caption(

        "F1 AI Strategy Engine — "
        "V5 Foundation"

    )