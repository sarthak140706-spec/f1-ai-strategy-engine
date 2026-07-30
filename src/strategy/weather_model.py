"""
weather_model.py

Sprint 5 - Step 4

Extracts live weather information from a FastF1
session and converts it into a structured format
for the strategy engine.
"""

from typing import Dict


# ============================================================
# WEATHER INFORMATION
# ============================================================

def get_weather(session) -> Dict:
    """
    Extract the latest weather information from
    the FastF1 session.
    """

    try:

        weather = session.weather_data

        if weather is None or weather.empty:

            raise ValueError

        latest = weather.iloc[-1]

        return {

            "AirTemperature":
                round(float(latest["AirTemp"]), 1),

            "TrackTemperature":
                round(float(latest["TrackTemp"]), 1),

            "Humidity":
                round(float(latest["Humidity"]), 1),

            "Pressure":
                round(float(latest["Pressure"]), 1),

            "WindSpeed":
                round(float(latest["WindSpeed"]), 1),

            "Rainfall":
                bool(latest["Rainfall"])

        }

    except Exception:

        return {

            "AirTemperature": None,

            "TrackTemperature": None,

            "Humidity": None,

            "Pressure": None,

            "WindSpeed": None,

            "Rainfall": False

        }


# ============================================================
# WEATHER RISK
# ============================================================

def evaluate_weather_risk(
    weather: Dict
) -> Dict:
    """
    Evaluate the strategic impact of
    the current weather.
    """

    rainfall = weather["Rainfall"]

    track_temp = weather["TrackTemperature"]

    risk = "LOW"

    if rainfall:

        risk = "HIGH"

    elif (
        track_temp is not None
        and track_temp >= 45
    ):

        risk = "MEDIUM"

    weather["WeatherRisk"] = risk

    return weather


# ============================================================
# DISPLAY
# ============================================================

def display_weather(
    weather: Dict
) -> None:

    print("\n" + "=" * 60)
    print("WEATHER INFORMATION")
    print("=" * 60)

    for key, value in weather.items():

        print(f"{key}: {value}")

    print("=" * 60)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from src.data_loader import load_session

    session = load_session(

        2025,

        "British Grand Prix",

        "R"

    )

    weather = get_weather(

        session

    )

    weather = evaluate_weather_risk(

        weather

    )

    display_weather(

        weather

    )