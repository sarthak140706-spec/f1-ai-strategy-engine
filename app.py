import streamlit as st
import pandas as pd
import plotly.express as px

from src.predict import predict_pit_probability
from src.strategy.decision_engine import get_strategy_decision


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="F1 AI Strategy Engineer",
    layout="wide"
)

st.title("🏎️ F1 AI Strategy Engineer Dashboard (V4)")


# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Race Inputs")

lap = st.sidebar.slider("Lap Number", 1, 70, 25)
tyre_life = st.sidebar.slider("Tyre Life", 1, 50, 15)
position = st.sidebar.slider("Position", 1, 20, 3)
laps_remaining = st.sidebar.slider("Laps Remaining", 1, 70, 20)

driver = st.sidebar.selectbox(
    "Driver",
    ["Verstappen", "Hamilton", "Leclerc", "Alonso"]
)

track = st.sidebar.selectbox(
    "Track",
    ["Monaco", "Monza", "Silverstone", "Bahrain"]
)

tyre = st.sidebar.selectbox(
    "Tyre Compound",
    ["Soft", "Medium", "Hard"]
)


# -----------------------------
# ML INPUT DATA
# -----------------------------
data = pd.DataFrame([{
    "LapNumber": lap,
    "TyreLife": tyre_life,
    "Position": position,
    "LapsRemaining": laps_remaining,
    "RaceProgress": lap / 70,
    "AvgPaceLast3": 92.2,
    "AvgPaceLast5": 92.4,
    "AvgPaceLast10": 92.6,
    "DegradationRate": 0.35,
    "CurrentStintLength": tyre_life,
    "PitStopsCompleted": 1
}])


# -----------------------------
# RUN BUTTON
# -----------------------------
if st.button("🏁 Analyze Strategy"):

    # =============================
    # ML PREDICTION
    # =============================
    pit_prob = predict_pit_probability(data)

    # =============================
    # STRATEGY ENGINE
    # =============================
    strategy = get_strategy_decision(
        track=track,
        driver=driver,
        tyre_compound=tyre,
        predicted_lap_time=92.4,
        laps_remaining=laps_remaining
    )

    decision = strategy["recommendation"]
    confidence = strategy["confidence"]
    delta = strategy["delta"]

    # =============================
    # TOP METRICS
    # =============================
    col1, col2, col3 = st.columns(3)

    col1.metric("Pit Probability", f"{pit_prob} %")
    col2.metric("Decision", decision)
    col3.metric("Confidence", confidence)

    st.divider()

    # =============================
    # DECISION PANEL (NO RAW JSON)
    # =============================
    st.subheader("🧠 Race Engineer Decision Panel")

    if "PIT" in decision:
        st.error(f"🔴 DECISION: {decision}")
    else:
        st.success(f"🟢 DECISION: {decision}")

    st.info(f"📊 Confidence Level: {confidence}")

    if delta > 0:
        st.warning(f"⏱ Pit Advantage: +{delta:.2f} sec")
    else:
        st.warning(f"⏱ Stay Advantage: +{abs(delta):.2f} sec")

    st.divider()

    # =============================
    # BAR CHART (TIME COMPARISON)
    # =============================
    st.subheader("⏱ Strategy Time Comparison")

    chart_df = pd.DataFrame({
        "Strategy": ["Stay Out", "Pit Now"],
        "Time": [
            strategy["stay_out_time"],
            strategy["pit_now_time"]
        ]
    })

    fig = px.bar(
        chart_df,
        x="Strategy",
        y="Time",
        text="Time",
        color="Strategy"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =============================
    # PIE CHART (DECISION SPLIT)
    # =============================
    st.subheader("📊 Strategy Breakdown")

    pie_df = pd.DataFrame({
        "Type": ["Advantage", "Risk"],
        "Value": [
            max(delta, 0),
            abs(min(delta, 0))
        ]
    })

    fig2 = px.pie(
        pie_df,
        names="Type",
        values="Value",
        hole=0.4
    )

    st.plotly_chart(fig2, use_container_width=True)

    # =============================
    # STATUS SECTION
    # =============================
    st.subheader("🏎️ Race Engineer Status")

    if confidence == "HIGH":
        st.success("🟢 Strong Strategy Confidence")
    elif confidence == "MEDIUM":
        st.warning("🟡 Medium Confidence Strategy")
    else:
        st.error("🔴 Low Confidence - Risky Decision")

    st.caption("F1 AI Strategy Engine - V4 Data Driven Simulation")