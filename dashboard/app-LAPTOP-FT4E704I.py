import os
import sys

# Add project root to Python path
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import plotly.express as px

from src.predict import predict_pit_probability
from src.simulator import simulate_strategy


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="F1 AI Strategist",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ F1 AI Strategist")
st.markdown(
    "AI-powered Formula 1 pit strategy recommendations based on 2025 race data."
)


# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():

    path = os.path.join(
        project_root,
        "data",
        "processed",
        "f1_2025_dataset.csv"
    )

    return pd.read_csv(path)


df = load_data()


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Race Controls")

races = sorted(df["Race"].unique())

selected_race = st.sidebar.selectbox(
    "Select Race",
    races
)

race_data = df[df["Race"] == selected_race]

drivers = sorted(race_data["Driver"].unique())

selected_driver = st.sidebar.selectbox(
    "Select Driver",
    drivers
)

driver_data = race_data[
    race_data["Driver"] == selected_driver
].sort_values("LapNumber")


selected_lap = st.sidebar.slider(
    "Select Lap",
    min_value=int(driver_data["LapNumber"].min()),
    max_value=int(driver_data["LapNumber"].max()),
    value=int(driver_data["LapNumber"].median())
)


lap_data = driver_data[
    driver_data["LapNumber"] == selected_lap
]


# -----------------------------
# PREDICTIONS
# -----------------------------

if not lap_data.empty:

    current_state = lap_data.iloc[[0]]

    probability = predict_pit_probability(current_state)

    simulation = simulate_strategy(
        current_state.iloc[0]
    )

    current_position = int(
        current_state["Position"].iloc[0]
    )

    current_compound = str(
        current_state["Compound"].iloc[0]
    )

    tyre_life = int(
        current_state["TyreLife"].iloc[0]
    )

    # -----------------------------
    # METRICS
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Pit Probability",
        f"{probability:.1f}%"
    )

    col2.metric(
        "Recommendation",
        simulation["recommendation"]
    )

    col3.metric(
        "Estimated Gain",
        f"{simulation['time_gain']:.2f} s"
    )

    col4.metric(
        "Current Position",
        f"P{current_position}"
    )

    st.divider()

    # -----------------------------
    # CURRENT RACE STATE
    # -----------------------------

    st.subheader("Current Race State")

    info1, info2, info3, info4 = st.columns(4)

    info1.info(f"🛞 Compound: **{current_compound}**")
    info2.info(f"⏱️ Tyre Life: **{tyre_life} laps**")
    info3.info(f"🔢 Lap: **{selected_lap}**")
    info4.info(
        f"🏁 Laps Remaining: **{int(current_state['LapsRemaining'].iloc[0])}**"
    )

    st.divider()

    # -----------------------------
    # CHARTS - ROW 1
    # -----------------------------

    chart1, chart2 = st.columns(2)

    with chart1:

        lap_fig = px.line(
            driver_data,
            x="LapNumber",
            y="LapTimeSeconds",
            color="Compound",
            markers=True,
            title="Lap Time Trend"
        )

        lap_fig.update_layout(
            xaxis_title="Lap Number",
            yaxis_title="Lap Time (seconds)"
        )

        st.plotly_chart(
            lap_fig,
            use_container_width=True
        )

    with chart2:

        tyre_fig = px.line(
            driver_data,
            x="LapNumber",
            y="TyreLife",
            color="Compound",
            markers=True,
            title="Tyre Life Progression"
        )

        tyre_fig.update_layout(
            xaxis_title="Lap Number",
            yaxis_title="Tyre Life"
        )

        st.plotly_chart(
            tyre_fig,
            use_container_width=True
        )

    # -----------------------------
    # CHARTS - ROW 2
    # -----------------------------

    chart3, chart4 = st.columns(2)

    with chart3:

        compound_counts = (
            driver_data["Compound"]
            .value_counts()
            .reset_index()
        )

        compound_counts.columns = [
            "Compound",
            "Count"
        ]

        pie_fig = px.pie(
            compound_counts,
            names="Compound",
            values="Count",
            title="Tyre Compound Usage"
        )

        st.plotly_chart(
            pie_fig,
            use_container_width=True
        )

    with chart4:

        pit_laps = driver_data[
            driver_data["PitLap"] == 1
        ]

        if not pit_laps.empty:

            pit_fig = px.scatter(
                pit_laps,
                x="LapNumber",
                y="Position",
                color="Compound",
                size="TyreLife",
                title="Pit Stop Timeline"
            )

            pit_fig.update_layout(
                xaxis_title="Lap Number",
                yaxis_title="Race Position"
            )

            pit_fig.update_yaxes(
                autorange="reversed"
            )

            st.plotly_chart(
                pit_fig,
                use_container_width=True
            )

        else:
            st.info(
                "No pit stops recorded for this driver."
            )

    st.divider()

    # -----------------------------
    # STRATEGY EXPLANATION
    # -----------------------------

    st.subheader("Strategy Analysis")

    if simulation["recommendation"] == "Pit Now":

        st.success(
            f"""
            The model recommends a pit stop on lap {selected_lap}.

            Estimated time benefit: {simulation['time_gain']:.2f} seconds.

            Current tyre life and predicted degradation suggest that fresh tyres
            may provide a performance advantage for the remaining laps.
            """
        )

    else:

        st.info(
            f"""
            The model recommends staying out.

            Estimated pit stop loss outweighs the potential gain from fresh tyres.

            With only {int(current_state['LapsRemaining'].iloc[0])} laps remaining,
            recovering the pit stop time is unlikely.
            """
        )

    st.subheader("Current Lap Data")

    display_columns = [
        "Race",
        "Driver",
        "LapNumber",
        "Position",
        "Compound",
        "TyreLife",
        "CurrentStintLength",
        "AvgPaceLast5",
        "DegradationRate",
        "LapsRemaining"
    ]

    st.dataframe(
        current_state[display_columns],
        use_container_width=True
    )

else:

    st.warning(
        "No data available for the selected lap."
    )