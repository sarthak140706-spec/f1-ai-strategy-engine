"""
traffic_model.py

Sprint 5 - Step 5

Analyses nearby cars to estimate whether a pit stop
would release the driver into traffic.
"""

from typing import Dict


# ============================================================
# GET TRAFFIC INFORMATION
# ============================================================

def get_traffic_data(
    session,
    driver: str
) -> Dict:
    """
    Estimate nearby traffic around a driver.
    """

    try:

        laps = session.laps

        latest = laps.pick_drivers(driver)

        if latest.empty:

            raise ValueError

        latest = latest.iloc[-1]

        position = int(latest["Position"])

        total_cars = int(
            laps["Driver"].nunique()
        )

        cars_ahead = max(
            0,
            position - 1
        )

        cars_behind = max(
            0,
            total_cars - position
        )

        return {

            "Position":
                position,

            "CarsAhead":
                cars_ahead,

            "CarsBehind":
                cars_behind,

            "TrafficDensity":
                cars_ahead + cars_behind

        }

    except Exception:

        return {

            "Position": None,

            "CarsAhead": None,

            "CarsBehind": None,

            "TrafficDensity": None

        }


# ============================================================
# EVALUATE TRAFFIC
# ============================================================

def evaluate_traffic(
    traffic: Dict
) -> Dict:
    """
    Convert traffic information into a
    strategic traffic risk.
    """

    density = traffic.get(
        "TrafficDensity"
    )

    if density is None:

        risk = "UNKNOWN"

    elif density >= 18:

        risk = "HIGH"

    elif density >= 10:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    traffic["TrafficRisk"] = risk

    return traffic


# ============================================================
# DISPLAY
# ============================================================

def display_traffic(
    traffic: Dict
) -> None:

    print("\n" + "=" * 60)
    print("TRAFFIC INFORMATION")
    print("=" * 60)

    for key, value in traffic.items():

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

    traffic = get_traffic_data(

        session,

        "VER"

    )

    traffic = evaluate_traffic(

        traffic

    )

    display_traffic(

        traffic

    )