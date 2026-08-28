# ============================================================
# IMPORTS
# ============================================================

# ------------------------------------------------------------
# Standard Library Imports
# ------------------------------------------------------------

import logging
import warnings
from datetime import datetime
from typing import Any, Dict, List, Optional

# ------------------------------------------------------------
# Third-Party Imports
# ------------------------------------------------------------

import fastf1
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# ------------------------------------------------------------
# Project Module Imports
# ------------------------------------------------------------

import src.data_loader as data_loader
import src.preprocessing as preprocessing
import src.feature_engineering as feature_engineering
import src.predict as predict

import src.strategy.decision_engine as decision_engine
import src.strategy.simulator as simulator

import src.live.live_strategy_api as live_strategy_api
import src.visualization as visualization

# ------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# General Configuration
# ------------------------------------------------------------

warnings.filterwarnings("ignore")

# ------------------------------------------------------------
# FastF1 Cache Initialization
# ------------------------------------------------------------

try:
    fastf1.Cache.enable_cache(".fastf1_cache")
    logger.info("FastF1 cache initialized successfully.")
except Exception as e:
    logger.warning(f"Unable to initialize FastF1 cache: {e}")

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="F1 AI Strategy Engineer V5",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a Bug": None,
        "About": """
        # F1 AI Strategy Engineer V5

        A professional Formula 1 strategy analysis platform built using:

        - Streamlit
        - FastF1
        - Plotly
        - Pandas
        - Artificial Intelligence

        Features:
        • Historical Race Strategy Analysis
        • Live Race Strategy Dashboard
        • AI Strategy Recommendations
        • Interactive Visualizations
        • Race Reports
        """
    }
)

# ------------------------------------------------------------
# Application Metadata
# ------------------------------------------------------------

APP_NAME = "F1 AI Strategy Engineer V5"
APP_VERSION = "Version 5.0"

CURRENT_YEAR = datetime.now().year
BUILD_DATE = datetime.now().strftime("%d %B %Y")

# ------------------------------------------------------------
# Display Configuration
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# GLOBAL CONSTANTS
# ============================================================

# ------------------------------------------------------------
# Application Information
# ------------------------------------------------------------

APP_TITLE = "F1 AI Strategy Engineer V5"
APP_SUBTITLE = "AI-Powered Formula 1 Race Strategy Analysis & Live Decision Support"

# ------------------------------------------------------------
# Strategy Modes
# ------------------------------------------------------------

HISTORICAL_MODE = "Historical Strategy"
LIVE_MODE = "Live Strategy"

APPLICATION_MODES = [
    HISTORICAL_MODE,
    LIVE_MODE
]

# ------------------------------------------------------------
# Formula 1 Seasons
# ------------------------------------------------------------

CURRENT_SEASON = datetime.now().year

AVAILABLE_SEASONS = list(range(2018, CURRENT_SEASON + 1))

# ------------------------------------------------------------
# Formula 1 Session Types
# ------------------------------------------------------------

SESSION_TYPES = [
    "Practice 1",
    "Practice 2",
    "Practice 3",
    "Sprint Shootout",
    "Sprint",
    "Qualifying",
    "Race"
]

SESSION_CODES = {
    "Practice 1": "FP1",
    "Practice 2": "FP2",
    "Practice 3": "FP3",
    "Sprint Shootout": "SS",
    "Sprint": "S",
    "Qualifying": "Q",
    "Race": "R"
}

# ------------------------------------------------------------
# Dashboard Refresh Settings
# ------------------------------------------------------------

DEFAULT_REFRESH_INTERVAL = 30          # seconds
MIN_REFRESH_INTERVAL = 5
MAX_REFRESH_INTERVAL = 120

# ------------------------------------------------------------
# Visualization Defaults
# ------------------------------------------------------------

DEFAULT_PLOT_HEIGHT = 500
DEFAULT_TABLE_HEIGHT = 450

PLOTLY_TEMPLATE = "plotly_dark"

# ------------------------------------------------------------
# Driver Table Defaults
# ------------------------------------------------------------

DEFAULT_DRIVER_COLUMNS = [
    "Driver",
    "Position",
    "Lap",
    "Compound",
    "Tyre Life",
    "Gap",
    "Pit Stops",
    "Strategy"
]

# ------------------------------------------------------------
# Export Options
# ------------------------------------------------------------

EXPORT_FORMATS = [
    "CSV",
    "Excel"
]

# ------------------------------------------------------------
# Theme Colors
# ------------------------------------------------------------

PRIMARY_COLOR = "#E10600"        # Formula 1 Red
SECONDARY_COLOR = "#1F1F1F"
SUCCESS_COLOR = "#00C853"
WARNING_COLOR = "#FFC107"
ERROR_COLOR = "#D32F2F"
INFO_COLOR = "#2196F3"

# ------------------------------------------------------------
# Status Labels
# ------------------------------------------------------------

STATUS_READY = "Ready"
STATUS_LOADING = "Loading..."
STATUS_CONNECTED = "Connected"
STATUS_DISCONNECTED = "Disconnected"

# ------------------------------------------------------------
# Metric Labels
# ------------------------------------------------------------

METRIC_POSITION = "Position"
METRIC_LAP = "Current Lap"
METRIC_COMPOUND = "Tyre Compound"
METRIC_STINT = "Current Stint"
METRIC_GAP = "Gap to Leader"
METRIC_PITS = "Pit Stops"

# ------------------------------------------------------------
# Default Empty DataFrame
# ------------------------------------------------------------

EMPTY_DATAFRAME = pd.DataFrame()

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

# ------------------------------------------------------------
# Historical Strategy State
# ------------------------------------------------------------

DEFAULT_SESSION_STATE = {
    # Application
    "current_mode": HISTORICAL_MODE,

    # Historical Inputs
    "selected_season": AVAILABLE_SEASONS[-1],
    "selected_grand_prix": None,
    "selected_session": "Race",
    "selected_driver": None,

    # Historical Data
    "race_data": EMPTY_DATAFRAME.copy(),
    "processed_data": EMPTY_DATAFRAME.copy(),
    "feature_data": EMPTY_DATAFRAME.copy(),
    "prediction_result": None,

    # Historical Visualizations
    "lap_time_figure": None,
    "tyre_strategy_figure": None,
    "position_figure": None,
    "pit_stop_figure": None,
    "strategy_timeline_figure": None,
    "driver_comparison_figure": None,

    # Reports
    "report_generated": False,
    "report_data": None,

    # --------------------------------------------------------
    # Live Strategy State
    # --------------------------------------------------------

    "live_connected": False,
    "live_session": None,
    "live_race_state": None,
    "live_strategy": None,
    "live_weather": None,
    "live_events": [],
    "live_driver_table": EMPTY_DATAFRAME.copy(),
    "live_recommendations": [],

    # --------------------------------------------------------
    # Dashboard Settings
    # --------------------------------------------------------

    "refresh_interval": DEFAULT_REFRESH_INTERVAL,
    "auto_refresh": False,

    # --------------------------------------------------------
    # Application Status
    # --------------------------------------------------------

    "status": STATUS_READY,
    "last_updated": None,
}

# ------------------------------------------------------------
# Initialize Session State
# ------------------------------------------------------------

for key, value in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------------------------------------------------
# Update Last Refresh Timestamp
# ------------------------------------------------------------

if st.session_state.last_updated is None:
    st.session_state.last_updated = datetime.now()

# ============================================================
# CUSTOM CSS
# ============================================================

CUSTOM_CSS = """
<style>

/* ============================================================
   GOOGLE FONT
============================================================ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
}

/* ============================================================
   MAIN APP
============================================================ */

.stApp{
    background-color:#0E1117;
    color:white;
}

/* ============================================================
   HEADINGS
============================================================ */

.main-title{
    font-size:42px;
    font-weight:800;
    color:#FFFFFF;
    margin-bottom:0px;
}

.sub-title{
    font-size:18px;
    color:#B0B0B0;
    margin-bottom:30px;
}

.section-title{
    font-size:26px;
    font-weight:700;
    color:white;
    margin-top:20px;
    margin-bottom:15px;
}

/* ============================================================
   CARDS
============================================================ */

.dashboard-card{

    background:#161B22;

    border-radius:18px;

    padding:20px;

    border:1px solid rgba(255,255,255,0.08);

    box-shadow:0px 4px 20px rgba(0,0,0,0.35);

    margin-bottom:18px;
}

/* ============================================================
   METRIC CARD
============================================================ */

.metric-card{

    background:#1B212C;

    border-radius:15px;

    padding:18px;

    text-align:center;

    border-left:5px solid #E10600;
}

.metric-title{

    color:#A0A0A0;

    font-size:15px;

    font-weight:500;
}

.metric-value{

    color:white;

    font-size:30px;

    font-weight:700;
}

/* ============================================================
   SIDEBAR
============================================================ */

section[data-testid="stSidebar"]{

    background:#11161F;
}

section[data-testid="stSidebar"] h1{

    color:white;
}

/* ============================================================
   BUTTONS
============================================================ */

.stButton > button{

    width:100%;

    border-radius:10px;

    border:none;

    background:#E10600;

    color:white;

    font-weight:600;

    transition:0.25s;
}

.stButton > button:hover{

    background:#B60000;

    color:white;
}

/* ============================================================
   SELECTBOX
============================================================ */

div[data-baseweb="select"] > div{

    border-radius:10px;
}

/* ============================================================
   DATAFRAME
============================================================ */

[data-testid="stDataFrame"]{

    border-radius:12px;

    overflow:hidden;
}

/* ============================================================
   SUCCESS
============================================================ */

.success-box{

    background:#133A1B;

    border-left:6px solid #00C853;

    padding:15px;

    border-radius:10px;

    color:white;
}

/* ============================================================
   WARNING
============================================================ */

.warning-box{

    background:#4E3D09;

    border-left:6px solid #FFC107;

    padding:15px;

    border-radius:10px;

    color:white;
}

/* ============================================================
   ERROR
============================================================ */

.error-box{

    background:#4A1616;

    border-left:6px solid #FF5252;

    padding:15px;

    border-radius:10px;

    color:white;
}

/* ============================================================
   INFO
============================================================ */

.info-box{

    background:#10253D;

    border-left:6px solid #2196F3;

    padding:15px;

    border-radius:10px;

    color:white;
}

/* ============================================================
   HORIZONTAL RULE
============================================================ */

hr{

    border:1px solid rgba(255,255,255,0.08);
}

/* ============================================================
   SCROLLBAR
============================================================ */

::-webkit-scrollbar{

    width:10px;
}

::-webkit-scrollbar-track{

    background:#11161F;
}

::-webkit-scrollbar-thumb{

    background:#444;

    border-radius:20px;
}

::-webkit-scrollbar-thumb:hover{

    background:#666;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # Project Title
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div style="text-align:center;">
            <h1 style="color:white; margin-bottom:0;">
                🏎️ {APP_NAME}
            </h1>
            <p style="color:#B0B0B0;">
                {APP_VERSION}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    selected_mode = st.radio(
        "Select Mode",
        APPLICATION_MODES,
        index=APPLICATION_MODES.index(st.session_state.current_mode)
    )

    st.session_state.current_mode = selected_mode

    st.divider()

    # --------------------------------------------------------
    # System Status
    # --------------------------------------------------------

    st.subheader("System Status")

    st.metric(
        label="Application",
        value=st.session_state.status
    )

    st.metric(
        label="Last Updated",
        value=st.session_state.last_updated.strftime("%H:%M:%S")
    )

    st.divider()

    # --------------------------------------------------------
    # About
    # --------------------------------------------------------

    with st.expander("About Project"):

        st.markdown(
            """
            **F1 AI Strategy Engineer V5**

            A professional Formula 1 race strategy platform featuring:

            - Historical race analysis
            - Live race monitoring
            - AI strategy recommendations
            - Interactive dashboards
            - Plotly visualizations
            - FastF1 integration
            """
        )

    st.divider()

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    st.caption("© 2026 F1 AI Strategy Engineer V5")

# ============================================================
# MAIN HEADER
# ============================================================

# ------------------------------------------------------------
# Dynamic Header Content
# ------------------------------------------------------------

if st.session_state.current_mode == HISTORICAL_MODE:

    page_title = "🏁 Historical Strategy Analysis"

    page_description = (
        "Analyze historical Formula 1 race sessions, evaluate driver strategies, "
        "and generate AI-powered race strategy recommendations."
    )

elif st.session_state.current_mode == LIVE_MODE:

    page_title = "🟢 Live Strategy Dashboard"

    page_description = (
        "Monitor live Formula 1 sessions with real-time telemetry, "
        "strategy insights, weather conditions, and AI-driven decisions."
    )

else:

    page_title = APP_TITLE

    page_description = APP_SUBTITLE

# ------------------------------------------------------------
# Main Header
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="dashboard-card">

        <div class="main-title">
            {APP_TITLE}
        </div>

        <div class="sub-title">
            {APP_SUBTITLE}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(f"## {page_title}")

st.write(page_description)

# ------------------------------------------------------------
# Status Bar
# ------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Current Mode",
        value=st.session_state.current_mode
    )

with col2:
    st.metric(
        label="System Status",
        value=st.session_state.status
    )

with col3:
    st.metric(
        label="Last Updated",
        value=st.session_state.last_updated.strftime("%H:%M:%S")
    )

st.divider()

# ============================================================
# HISTORICAL STRATEGY PAGE
# ============================================================

if st.session_state.current_mode == HISTORICAL_MODE:

    # --------------------------------------------------------
    # Historical Strategy Input Panel
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Historical Strategy Configuration</div>',
        unsafe_allow_html=True
    )

    input_col1, input_col2 = st.columns(2)

    with input_col1:

        selected_season = st.selectbox(
            "Season",
            AVAILABLE_SEASONS,
            index=AVAILABLE_SEASONS.index(st.session_state.selected_season),
            key="historical_season_selector"
        )

        st.session_state.selected_season = selected_season

    with input_col2:

        selected_session = st.selectbox(
            "Session",
            SESSION_TYPES,
            index=SESSION_TYPES.index(st.session_state.selected_session),
            key="historical_session_selector"
        )

        st.session_state.selected_session = selected_session

    # --------------------------------------------------------
    # Grand Prix Selection
    # --------------------------------------------------------

    grand_prix_list = []

    try:

        event_schedule = fastf1.get_event_schedule(selected_season)

        grand_prix_list = sorted(event_schedule["EventName"].tolist())

    except Exception as e:

        st.warning(f"Unable to load event schedule: {e}")

    selected_grand_prix = st.selectbox(
        "Grand Prix",
        options=grand_prix_list,
        index=0 if grand_prix_list else None,
        placeholder="Select a Grand Prix",
        key="historical_grand_prix_selector"
    )

    st.session_state.selected_grand_prix = selected_grand_prix

    # --------------------------------------------------------
    # Driver Selection
    # --------------------------------------------------------

    selected_driver = st.text_input(
        "Driver (3-letter FIA Code)",
        value=st.session_state.selected_driver or "",
        placeholder="Example: VER, HAM, LEC",
        key="historical_driver_selector"
    ).strip().upper()

    st.session_state.selected_driver = (
        selected_driver if selected_driver else None
    )

    st.divider()

    # --------------------------------------------------------
    # Load Historical Race Data
    # --------------------------------------------------------

    load_race = st.button(
        "📥 Load Race Data",
        use_container_width=True
    )

    if load_race:
        if not st.session_state.selected_grand_prix:
            st.warning("Please select a Grand Prix first.")
        else:
            try:

                st.session_state.status = STATUS_LOADING

                with st.spinner("Loading FastF1 session..."):

                    session = data_loader.load_session(
                        season=st.session_state.selected_season,
                        grand_prix=st.session_state.selected_grand_prix,
                        session_type=SESSION_CODES[
                            st.session_state.selected_session
                        ]
                    )

                    st.session_state.race_data = session
                    st.session_state.status = STATUS_CONNECTED
                    st.session_state.last_updated = datetime.now()

                st.success("Historical race session loaded successfully.")

            except Exception as e:

                st.session_state.status = STATUS_DISCONNECTED

                st.error(f"Failed to load race data.\n\n{e}")

    # ============================================================
# HISTORICAL STRATEGY PAGE
# ============================================================

if st.session_state.current_mode == HISTORICAL_MODE:

    # --------------------------------------------------------
    # Historical Strategy Input Panel
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Historical Strategy Configuration</div>',
        unsafe_allow_html=True
    )

    input_col1, input_col2 = st.columns(2)

    with input_col1:

        selected_season = st.selectbox(
            "Season",
            AVAILABLE_SEASONS,
            index=AVAILABLE_SEASONS.index(st.session_state.selected_season),
            key="historical_season_selector"
        )

        st.session_state.selected_season = selected_season

    with input_col2:

        selected_session = st.selectbox(
            "Session",
            SESSION_TYPES,
            index=SESSION_TYPES.index(st.session_state.selected_session),
            key="historical_session_selector"
        )

        st.session_state.selected_session = selected_session

    # --------------------------------------------------------
    # Grand Prix Selection
    # --------------------------------------------------------

    grand_prix_list = []

    try:

        event_schedule = fastf1.get_event_schedule(selected_season)

        grand_prix_list = sorted(event_schedule["EventName"].tolist())

    except Exception as e:

        st.warning(f"Unable to load event schedule: {e}")

    selected_grand_prix = st.selectbox(
        "Grand Prix",
        options=grand_prix_list,
        index=0 if grand_prix_list else None,
        placeholder="Select a Grand Prix",
        key="historical_grand_prix_selector"
    )

    st.session_state.selected_grand_prix = selected_grand_prix

    # --------------------------------------------------------
    # Driver Selection
    # --------------------------------------------------------

    selected_driver = st.text_input(
        "Driver (3-letter FIA Code)",
        value=st.session_state.selected_driver or "",
        placeholder="Example: VER, HAM, LEC",
        key="historical_driver_selector"
    ).strip().upper()

    st.session_state.selected_driver = (
        selected_driver if selected_driver else None
    )

    st.divider()

    # --------------------------------------------------------
    # Load Historical Race Data
    # --------------------------------------------------------

    load_race = st.button(
        "📥 Load Race Data",
        use_container_width=True
    )

    if load_race:
        if not st.session_state.selected_grand_prix:
            st.warning("Please select a Grand Prix first.")
        else:
            try:

                st.session_state.status = STATUS_LOADING

                with st.spinner("Loading FastF1 session..."):

                    session = data_loader.load_session(
                        season=st.session_state.selected_season,
                        grand_prix=st.session_state.selected_grand_prix,
                        session_type=SESSION_CODES[
                            st.session_state.selected_session
                        ]
                    )

                    st.session_state.race_data = session
                    st.session_state.status = STATUS_CONNECTED
                    st.session_state.last_updated = datetime.now()

                st.success("Historical race session loaded successfully.")

            except Exception as e:

                st.session_state.status = STATUS_DISCONNECTED

                st.error(f"Failed to load race data.\n\n{e}")

    # --------------------------------------------------------
    # AI Strategy Prediction
    # --------------------------------------------------------

    predict_strategy = st.button(
        "🤖 Generate AI Strategy",
        use_container_width=True
    )

    if predict_strategy:

        if st.session_state.race_data is None:
            st.warning("Please load a race session first.")

        else:

            try:

                st.session_state.status = STATUS_LOADING

                with st.spinner("Running AI strategy engine..."):

                    laps = st.session_state.race_data.laps

                    if st.session_state.selected_driver:

                        laps = laps[
                            laps["Driver"] ==
                            st.session_state.selected_driver
                        ]

                    processed_data = preprocessing.preprocess_data(
                        laps
                    )

                    processed_data = feature_engineering.detect_pit_stops(
                        processed_data
                    )

                    processed_data = feature_engineering.create_race_features(
                        processed_data
                    )

                    processed_data = feature_engineering.create_target(
                        processed_data
                    )

                    model_data = feature_engineering.prepare_model_data(
                        processed_data
                    )

                    if model_data.empty:
                        raise ValueError(
                            "No valid data available for prediction."
                        )

                    feature_columns = [
                        column
                        for column in model_data.columns
                        if column != "PitNextLap"
                    ]

                    prediction_input = model_data[
                        feature_columns
                    ].iloc[[-1]]

                    pit_probability = predict.predict_pit_probability(
                        prediction_input
                    )

                    recommendation = predict.get_ml_recommendation(
                        pit_probability
                    )

                    st.session_state.processed_data = processed_data
                    st.session_state.feature_data = prediction_input

                    st.session_state.prediction_result = {
                        "pit_probability": pit_probability,
                        "recommendation": recommendation
                    }

                    st.session_state.status = STATUS_READY
                    st.session_state.last_updated = datetime.now()

                st.success("AI strategy prediction completed successfully.")

                # ============================================================
                # PERFORMANCE METRICS
                # ============================================================

                if not processed_data.empty:

                    st.divider()

                    st.subheader("📊 Race Summary")

                    latest = processed_data.iloc[-1]

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(
                            "Current Lap",
                            int(latest["LapNumber"])
                        )

                    with col2:
                        st.metric(
                            "Current Position",
                            int(latest["Position"])
                        )

                    with col3:
                        st.metric(
                            "Tyre Life",
                            int(latest["TyreLife"])
                        )

                    with col4:
                        st.metric(
                            "Pit Stops",
                            int(latest["PitStopsCompleted"])
                        )

                # ============================================================
                # LAP TIME CHART
                # ============================================================

                st.divider()

                st.subheader("📈 Lap Time Analysis")

                lap_fig = visualization.plot_lap_times(
                    processed_data
                )

                st.plotly_chart(
                    lap_fig,
                    use_container_width=True
                )

                # ============================================================
                # POSITION CHANGES
                # ============================================================

                st.divider()

                st.subheader("🏁 Position Changes")

                position_fig = visualization.plot_position_changes(
                    processed_data
                )

                st.plotly_chart(
                    position_fig,
                    use_container_width=True
                )

                # ============================================================
                # TYRE DEGRADATION
                # ============================================================

                st.divider()

                st.subheader("📉 Tyre Degradation")

                degradation_fig = visualization.plot_degradation(
                    processed_data
                )

                st.plotly_chart(
                    degradation_fig,
                    use_container_width=True
                )

                # ============================================================
                # CURRENT STINT
                # ============================================================

                st.divider()

                st.subheader("🛞 Current Stint")

                stint_fig = visualization.plot_stints(
                    processed_data
                )

                st.plotly_chart(
                    stint_fig,
                    use_container_width=True
                )

                # ============================================================
                # AVERAGE PACE
                # ============================================================

                st.divider()

                st.subheader("⚡ Average Pace")

                pace_fig = visualization.plot_average_pace(
                    processed_data
                )

                st.plotly_chart(
                    pace_fig,
                    use_container_width=True
                )

                # ============================================================
                # DRIVER STATISTICS
                # ============================================================

                st.divider()

                st.subheader("📋 Driver Statistics")

                summary = (
                    processed_data
                    .groupby("Driver")
                    .agg(
                        AverageLapTime=("LapTimeSeconds", "mean"),
                        BestLap=("LapTimeSeconds", "min"),
                        PitStops=("PitStopsCompleted", "max"),
                        FinalPosition=("Position", "last")
                    )
                    .reset_index()
                )

                st.dataframe(
                    summary,
                    use_container_width=True
                )

                # ============================================================
                # TYRE STRATEGY
                # ============================================================

                st.divider()

                st.subheader("🛞 Tyre Strategy Timeline")

                tyre_fig = visualization.plot_tyre_strategy(
                    processed_data
                )

                st.plotly_chart(
                    tyre_fig,
                    use_container_width=True
                )

                # ============================================================
                # AI STRATEGY RESULT
                # ============================================================

                st.divider()

                st.subheader("🤖 AI Strategy Result")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Pit Probability",
                        f"{pit_probability:.2f}%"
                    )

                with col2:
                    st.metric(
                        "Recommendation",
                        recommendation
                    )

                with col3:
                    st.metric(
                        "Driver",
                        st.session_state.selected_driver or "All Drivers"
                    )

                if recommendation == "PIT NOW":

                    st.success(
                        """
    ### 🟢 PIT NOW

    The AI predicts that stopping this lap is likely to provide the greatest strategic advantage.
    """
                    )

                elif recommendation == "STAY OUT":

                    st.info(
                        """
    ### 🔵 STAY OUT

    Current tyre performance remains acceptable. Continue on track.
    """
                    )

                else:

                    st.warning(
                        """
    ### 🟡 UNCERTAIN

    The AI confidence is moderate. Consider traffic, weather and race conditions before pitting.
    """
                    )

                # ============================================================
                # PROCESSED DATA
                # ============================================================

                st.divider()

                with st.expander("📄 View Processed Race Data"):

                    st.dataframe(
                        processed_data,
                        use_container_width=True
                    )

            except Exception as e:

                st.session_state.status = STATUS_DISCONNECTED

                st.error(f"Prediction failed.\n\n{e}")


# ============================================================
# LIVE STRATEGY PAGE
# ============================================================

elif st.session_state.current_mode == LIVE_MODE:

    st.markdown(
        '<div class="section-title">Live Strategy Dashboard</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Monitor live Formula 1 sessions and receive AI-powered "
        "strategy recommendations in real time."
    )

    st.divider()

    # --------------------------------------------------------
    # LIVE CONFIGURATION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        live_season = st.selectbox(
            "Season",
            AVAILABLE_SEASONS,
            key="live_season_selector"
        )

    with col2:

        live_session = st.selectbox(
            "Session",
            SESSION_TYPES,
            index=SESSION_TYPES.index("Race"),
            key="live_session_selector"
        )

    # --------------------------------------------------------
    # GRAND PRIX SELECTION
    # --------------------------------------------------------

    grand_prix_list = []

    try:

        schedule = fastf1.get_event_schedule(
            live_season
        )

        grand_prix_list = sorted(
            schedule["EventName"].tolist()
        )

    except Exception as e:

        st.error(e)

    live_grand_prix = st.selectbox(
        "Grand Prix",
        grand_prix_list,
        key="live_gp_selector"
    )

    # --------------------------------------------------------
    # LOAD LIVE SESSION
    # --------------------------------------------------------

    load_live = st.button(
        "🟢 Connect Live Session",
        use_container_width=True
    )

    if load_live:

        try:

            with st.spinner(
                "Loading live session..."
            ):

                session = data_loader.load_session(
                    season=live_season,
                    grand_prix=live_grand_prix,
                    session_type=SESSION_CODES[
                        live_session
                    ]
                )

                orchestrator = (
                    live_strategy_api.LiveStrategyOrchestrator(
                        session
                    )
                )

                api = (
                    live_strategy_api.LiveStrategyAPI(
                        orchestrator
                    )
                )

                api.initialize()

                st.session_state.live_api = api
                st.session_state.live_connected = True

            st.success(
                "Connected successfully."
            )

        except Exception as e:

            st.error(e)

    # --------------------------------------------------------
    # LIVE SNAPSHOT
    # --------------------------------------------------------

    if st.session_state.live_connected:

        api = st.session_state.live_api

        # --------------------------------------------------------
        # AUTO REFRESH SETTINGS
        # --------------------------------------------------------

        st.sidebar.subheader("🔄 Live Refresh")

        auto_refresh = st.sidebar.checkbox(
            "Enable Auto Refresh",
            value=st.session_state.auto_refresh,
            key="live_auto_refresh"
        )

        refresh_interval = st.sidebar.slider(
            "Refresh Interval (seconds)",
            min_value=MIN_REFRESH_INTERVAL,
            max_value=MAX_REFRESH_INTERVAL,
            value=st.session_state.refresh_interval,
            key="live_refresh_interval"
        )

        st.session_state.auto_refresh = auto_refresh
        st.session_state.refresh_interval = refresh_interval

        # --------------------------------------------------------
        # UPDATE LIVE DATA
        # --------------------------------------------------------

        snapshot = api.get_snapshot()

        if st.session_state.auto_refresh:

            try:

                api.update()

                snapshot = api.get_snapshot()

                st.session_state.last_updated = datetime.now()

            except Exception as e:

                st.warning(
                    f"Live update failed: {e}"
                )

        st.success("🟢 Live Strategy Engine Connected")

        st.divider()

        st.subheader("📊 Live Race Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Current Lap", snapshot["lap"])

        with col2:
            st.metric("Drivers", snapshot["drivers"])

        with col3:
            st.metric("Events", snapshot["events"])

        with col4:
            st.metric("Strategies", snapshot["strategies"])

        st.caption(
            f"Last Updated: {st.session_state.last_updated.strftime('%H:%M:%S')}"
        )

        refresh = st.button(
            "🔄 Refresh Now",
            use_container_width=True
        )

        if refresh:

            try:

                api.update()

                st.session_state.last_updated = datetime.now()

                st.rerun()

            except Exception as e:

                st.error(e)

        # --------------------------------------------------------
        # LIVE RACE STATE
        # --------------------------------------------------------

        st.divider()

        st.subheader("🏎️ Live Race State")

        race_state = api.get_race_state()

        if race_state:

            race_df = pd.DataFrame(race_state)

            st.dataframe(
                race_df,
                use_container_width=True
            )

        else:

            st.info(
                "No live race state available."
            )

        # --------------------------------------------------------
        # DRIVER STRATEGIES
        # --------------------------------------------------------

        st.divider()

        st.subheader("🤖 AI Driver Strategies")

        strategy_df = api.get_strategies_dataframe()

        if not strategy_df.empty:

            st.dataframe(
                strategy_df,
                use_container_width=True
            )

        else:

            st.info(
                "No strategy recommendations available."
            )

        # --------------------------------------------------------
        # RACE EVENTS
        # --------------------------------------------------------

        st.divider()

        st.subheader("🚨 Live Race Events")

        events = api.get_events()

        if events:

            event_df = pd.DataFrame(events)

            st.dataframe(
                event_df,
                use_container_width=True
            )

        else:

            st.success(
                "No race events detected."
            )

        # --------------------------------------------------------
        # WEATHER
        # --------------------------------------------------------

        st.divider()

        st.subheader("🌦 Weather")

        weather = api.get_weather()

        if weather:

            weather_df = pd.DataFrame([weather])

            st.dataframe(
                weather_df,
                use_container_width=True
            )

        else:

            st.info(
                "Weather information unavailable."
            )

        # --------------------------------------------------------
        # TRACK STATUS
        # --------------------------------------------------------

        st.divider()

        st.subheader("🏁 Track Status")

        track_status = api.get_track_status()

        if track_status:

            st.success(
                f"Current Track Status: {track_status}"
            )

        else:

            st.info(
                "Track status unavailable."
            )

    else:

        st.subheader("📊 Live Race Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Current Lap", "--")

        with col2:
            st.metric("Drivers", "--")

        with col3:
            st.metric("Events", "--")

        with col4:
            st.metric("Strategies", "--")

        st.divider()

        st.subheader("🤖 Live AI Strategy")

        st.info(
            "Waiting for live telemetry..."
        )               