import plotly.express as px
import pandas as pd


def plot_lap_times(df):

    fig = px.line(
        df,
        x="LapNumber",
        y="LapTimeSeconds",
        color="Driver",
        title="Lap Time Trend"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Lap",
        yaxis_title="Lap Time (s)"
    )

    return fig

# ============================================================
# LAP TIME ANALYSIS
# ============================================================

def plot_lap_times(
    df: pd.DataFrame
):

    figure = px.line(
        df,
        x="LapNumber",
        y="LapTimeSeconds",
        color="Driver",
        title="Lap Time Analysis",
        template="plotly_dark"
    )

    figure.update_layout(
        height=500,
        xaxis_title="Lap",
        yaxis_title="Lap Time (Seconds)"
    )

    return figure


# ============================================================
# TYRE STRATEGY
# ============================================================

def plot_tyre_strategy(
    df: pd.DataFrame
):

    figure = px.scatter(
        df,
        x="LapNumber",
        y="Driver",
        color="Compound",
        symbol="Compound",
        title="Tyre Strategy Timeline",
        template="plotly_dark"
    )

    figure.update_layout(
        height=500,
        xaxis_title="Lap",
        yaxis_title="Driver"
    )

    return figure

def plot_position_changes(df: pd.DataFrame):

    figure = px.line(
        df,
        x="LapNumber",
        y="Position",
        color="Driver",
        title="Driver Position Progress",
        template="plotly_dark"
    )

    figure.update_yaxes(autorange="reversed")

    figure.update_layout(
        height=500,
        xaxis_title="Lap",
        yaxis_title="Position"
    )

    return figure

def plot_position_changes(df: pd.DataFrame):

    figure = px.line(
        df,
        x="LapNumber",
        y="Position",
        color="Driver",
        title="Driver Position Progress",
        template="plotly_dark"
    )

    figure.update_yaxes(autorange="reversed")

    figure.update_layout(
        height=500,
        xaxis_title="Lap",
        yaxis_title="Position"
    )

    return figure

def plot_degradation(df: pd.DataFrame):

    figure = px.line(
        df,
        x="LapNumber",
        y="DegradationRate",
        color="Driver",
        title="Tyre Degradation",
        template="plotly_dark"
    )

    figure.update_layout(
        height=500
    )

    return figure

def plot_stints(df: pd.DataFrame):

    figure = px.bar(
        df,
        x="LapNumber",
        y="CurrentStintLength",
        color="Driver",
        title="Current Stint Length",
        template="plotly_dark"
    )

    figure.update_layout(
        height=500
    )

    return figure

def plot_pit_stops(df: pd.DataFrame):

    pit_df = df[df["PitLap"] == 1]

    figure = px.scatter(
        pit_df,
        x="LapNumber",
        y="Driver",
        color="Driver",
        title="Pit Stop Timeline",
        template="plotly_dark"
    )

    figure.update_layout(
        height=500
    )

    return figure

def plot_average_pace(df: pd.DataFrame):

    figure = px.line(
        df,
        x="LapNumber",
        y="AvgPaceLast5",
        color="Driver",
        title="Average Pace Comparison",
        template="plotly_dark"
    )

    figure.update_layout(
        height=500
    )

    return figure