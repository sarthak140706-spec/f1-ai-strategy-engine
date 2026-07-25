import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# V5 IMPORTS
# ============================================================

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

from src.strategy.decision_engine import (
    get_strategy_decision
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title=
        "F1 AI Strategy Engineer",

    page_icon=
        "🏎️",

    layout=
        "wide"

)


# ============================================================
# TITLE
# ============================================================

st.title(
    "🏎️ F1 AI Strategy Engineer"
)

st.caption(
    "V5 — Dynamic FastF1 Race Strategy Engine"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "🏁 Race Selection"
)


# ============================================================
# SEASON
# ============================================================

season = st.sidebar.number_input(

    "Season",

    min_value=2018,

    max_value=2026,

    value=2025,

    step=1

)


# ============================================================
# LOAD RACE SCHEDULE
# ============================================================

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

        "Unable to load F1 race schedule: "

        f"{e}"

    )

    st.stop()


if not races:

    st.warning(

        "No races found for the selected season."

    )

    st.stop()


# ============================================================
# GRAND PRIX
# ============================================================

grand_prix = st.sidebar.selectbox(

    "Grand Prix",

    races

)


# ============================================================
# SESSION
# ============================================================

session_type = st.sidebar.selectbox(

    "Session",

    [

        "R",

        "Q",

        "FP1",

        "FP2",

        "FP3",

        "S"

    ],

    format_func=lambda x: {

        "R": "Race",

        "Q": "Qualifying",

        "FP1": "Free Practice 1",

        "FP2": "Free Practice 2",

        "FP3": "Free Practice 3",

        "S": "Sprint"

    }.get(

        x,

        x

    )

)


# ============================================================
# LOAD DRIVERS
# ============================================================

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


# ============================================================
# DRIVER SELECTOR
# ============================================================

driver = st.sidebar.selectbox(

    "Driver",

    drivers

)


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.sidebar.button(

    "🏁 Analyze Strategy",

    type="primary"

)


# ============================================================
# MAIN ANALYSIS
# ============================================================

if analyze:

    # ========================================================
    # LOAD DRIVER DATA
    # ========================================================

    with st.spinner(

        "Loading FastF1 race data..."

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

                "Unable to load driver data: "

                f"{e}"

            )

            st.stop()


    # ========================================================
    # PREPROCESS
    # ========================================================

    try:

        driver_laps = preprocess_data(

            driver_laps

        )

        driver_laps = detect_pit_stops(

            driver_laps

        )

        driver_laps = create_race_features(

            driver_laps

        )

    except Exception as e:

        st.error(

            "Race data processing failed: "

            f"{e}"

        )

        st.stop()


    # ========================================================
    # VALIDATE DATA
    # ========================================================

    if driver_laps.empty:

        st.error(

            "No valid lap data available."

        )

        st.stop()


    # ========================================================
    # CURRENT RACE STATE
    # ========================================================

    latest = (

        driver_laps

        .sort_values(

            "LapNumber"

        )

        .iloc[-1]

    )


    # ========================================================
    # MODEL FEATURES
    # ========================================================

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


    # ========================================================
    # CHECK FEATURES
    # ========================================================

    missing_features = [

        feature

        for feature in model_features

        if feature
        not in latest.index

    ]


    if missing_features:

        st.error(

            "Missing required ML features: "

            + ", ".join(

                missing_features

            )

        )

        st.stop()


    # ========================================================
    # BUILD MODEL INPUT
    # ========================================================

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


    # ========================================================
    # EXTRACT STRATEGY INPUTS
    # ========================================================

    # --------------------------------------------------------
    # TRACK
    # --------------------------------------------------------

    track = (

        latest.get(

            "Circuit",

            grand_prix

        )

    )


    # --------------------------------------------------------
    # TYRE COMPOUND
    # --------------------------------------------------------

    tyre_compound = (

        latest.get(

            "TyreCompound",

            latest.get(

                "Compound",

                "MEDIUM"

            )

        )

    )


    # --------------------------------------------------------
    # PREDICTED LAP TIME
    # --------------------------------------------------------

    predicted_lap_time = (

        latest[
            "AvgPaceLast5"
        ]

    )


    # --------------------------------------------------------
    # LAPS REMAINING
    # --------------------------------------------------------

    laps_remaining = int(

        latest[
            "LapsRemaining"
        ]

    )


    # ========================================================
    # RUN V5 DECISION ENGINE
    # ========================================================

    with st.spinner(

        "AI Strategy Engine is analyzing the race..."

    ):

        try:

            strategy_result = (

                get_strategy_decision(

                    track=track,

                    driver=driver,

                    tyre_compound=tyre_compound,

                    predicted_lap_time=(

                        predicted_lap_time

                    ),

                    laps_remaining=(

                        laps_remaining

                    ),

                    model_data=model_input

                )

            )

        except Exception as e:

            st.error(

                "Strategy analysis failed: "

                f"{e}"

            )

            st.stop()


    # ========================================================
    # TOP METRICS
    # ========================================================

    st.subheader(

        "🏎️ Current Race Overview"

    )


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

        f"{strategy_result['pit_probability']}%"

    )


    st.divider()


    # ========================================================
    # FINAL AI DECISION
    # ========================================================

    st.subheader(

        "🧠 AI Strategy Decision"

    )


    final_decision = (

        strategy_result[
            "final_decision"
        ]

    )


    confidence = (

        strategy_result[
            "confidence"
        ]

    )


    if final_decision == "PIT NOW":

        st.error(

            f"🔴 FINAL RECOMMENDATION: "

            f"{final_decision}"

        )

    else:

        st.success(

            f"🟢 FINAL RECOMMENDATION: "

            f"{final_decision}"

        )


    # ========================================================
    # DECISION METRICS
    # ========================================================

    decision_col1, decision_col2, decision_col3 = (

        st.columns(3)

    )


    decision_col1.metric(

        "Pit Probability",

        f"{strategy_result['pit_probability']}%"

    )


    decision_col2.metric(

        "Simulator",

        strategy_result[

            "simulator_recommendation"

        ]

    )


    decision_col3.metric(

        "Confidence",

        confidence

    )


    # ========================================================
    # AI REASON
    # ========================================================

    st.info(

        "💡 "

        + strategy_result[
            "reason"
        ]

    )


    # ========================================================
    # SIMULATION COMPARISON
    # ========================================================

    st.subheader(

        "⚖️ Strategy Simulation"

    )


    sim_col1, sim_col2, sim_col3 = (

        st.columns(3)

    )


    sim_col1.metric(

        "Stay Out Time",

        f"{strategy_result['stay_out_time']} sec"

    )


    sim_col2.metric(

        "Pit Now Time",

        f"{strategy_result['pit_now_time']} sec"

    )


    sim_col3.metric(

        "Strategy Delta",

        f"{strategy_result['delta']} sec"

    )


    # ========================================================
    # CURRENT RACE STATE
    # ========================================================

    st.subheader(

        "📊 Current Race State"

    )


    race_state_df = pd.DataFrame({

        "Metric": [

            "Season",

            "Grand Prix",

            "Session",

            "Driver",

            "Track",

            "Lap",

            "Position",

            "Tyre Compound",

            "Tyre Life",

            "Laps Remaining",

            "Average Pace (Last 5)",

            "Degradation Rate",

            "Pit Stops"

        ],

        "Value": [

            season,

            grand_prix,

            session_type,

            driver,

            track,

            latest[
                "LapNumber"
            ],

            latest[
                "Position"
            ],

            tyre_compound,

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


    # ========================================================
    # ML FEATURE TABLE
    # ========================================================

    with st.expander(

        "🔍 View ML Model Features"

    ):

        st.dataframe(

            model_input,

            use_container_width=True,

            hide_index=True

        )


    # ========================================================
    # LAP TIME GRAPH
    # ========================================================

    st.subheader(

        "⏱️ Lap Time Progression"

    )


    fig = px.line(

        driver_laps,

        x="LapNumber",

        y="LapTimeSeconds",

        title=(

            f"{driver} Lap Time Progression"

        )

    )


    st.plotly_chart(

        fig,

        use_container_width=True

    )


    # ========================================================
    # PACE GRAPH
    # ========================================================

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


# ============================================================
# DEFAULT LANDING MESSAGE
# ============================================================

else:

    st.info(

        "👈 Select a season, Grand Prix, session, "

        "and driver from the sidebar, then click "

        "**Analyze Strategy**."

    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(

    "F1 AI Strategy Engineer — "

    "V5 Dynamic FastF1 Strategy Engine"

)