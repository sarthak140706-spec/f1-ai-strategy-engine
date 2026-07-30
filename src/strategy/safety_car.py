"""
safety_car.py

Sprint 5

Detects Safety Car (SC), Virtual Safety Car (VSC),
and adjusts candidate strategies accordingly.
"""

from typing import Dict, List


# ============================================================
# SAFETY CAR DETECTION
# ============================================================

def detect_safety_car(session) -> Dict:
    """
    Detect the current race neutralisation status.
    """

    status = "GREEN"

    try:

        track_status = session.track_status

        if track_status is None or track_status.empty:

            return {
                "TrackStatus": "GREEN",
                "SafetyCar": False,
                "VirtualSafetyCar": False
            }

        latest = str(
            track_status.iloc[-1]["Status"]
        )

        if latest == "4":

            status = "SAFETY CAR"

        elif latest == "6":

            status = "VIRTUAL SAFETY CAR"

    except Exception:

        status = "GREEN"

    return {

        "TrackStatus": status,

        "SafetyCar":
            status == "SAFETY CAR",

        "VirtualSafetyCar":
            status == "VIRTUAL SAFETY CAR"

    }


# ============================================================
# APPLY SAFETY CAR TO STRATEGIES
# ============================================================

def apply_safety_car_to_strategies(
    strategies: List[dict],
    session
) -> List[dict]:
    """
    Modify strategy scores depending on the
    current race neutralisation.

    Rules
    -----
    GREEN
        No change.

    VSC
        Small bonus to early pit stops.

    SAFETY CAR
        Large bonus to early pit stops.
    """

    safety_info = detect_safety_car(
        session
    )

    updated = []

    for strategy in strategies:

        strategy = strategy.copy()

        score = strategy.get(
            "StrategyScore",
            0
        )

        pit_lap = strategy.get(
            "pit_lap",
            0
        )

        # -----------------------------------------
        # GREEN FLAG
        # -----------------------------------------

        if safety_info["TrackStatus"] == "GREEN":

            strategy["SafetyCarAdjustment"] = 0

            strategy["SafetyCarRecommendation"] = (
                "Normal racing conditions."
            )

        # -----------------------------------------
        # VIRTUAL SAFETY CAR
        # -----------------------------------------

        elif safety_info["VirtualSafetyCar"]:

            bonus = 5

            if pit_lap <= 5:

                bonus += 2

            score += bonus

            strategy["SafetyCarAdjustment"] = bonus

            strategy["SafetyCarRecommendation"] = (
                "Consider pitting under VSC."
            )

        # -----------------------------------------
        # SAFETY CAR
        # -----------------------------------------

        elif safety_info["SafetyCar"]:

            bonus = 10

            if pit_lap <= 5:

                bonus += 5

            score += bonus

            strategy["SafetyCarAdjustment"] = bonus

            strategy["SafetyCarRecommendation"] = (
                "Strong opportunity to pit under Safety Car."
            )

        strategy["TrackStatus"] = safety_info[
            "TrackStatus"
        ]

        strategy["StrategyScore"] = round(
            score,
            2
        )

        updated.append(
            strategy
        )

    return updated


# ============================================================
# DISPLAY
# ============================================================

def display_safety_car(
    info: Dict
) -> None:

    print("\n" + "=" * 60)
    print("SAFETY CAR STATUS")
    print("=" * 60)

    print(
        f"Track Status : {info['TrackStatus']}"
    )

    print(
        f"Safety Car  : {info['SafetyCar']}"
    )

    print(
        f"VSC          : {info['VirtualSafetyCar']}"
    )

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

    result = detect_safety_car(
        session
    )

    display_safety_car(
        result
    )

    sample = [

        {
            "pit_lap": 3,
            "StrategyScore": 82.5
        },

        {
            "pit_lap": 12,
            "StrategyScore": 78.1
        }

    ]

    updated = apply_safety_car_to_strategies(

        sample,

        session

    )

    print("\nUPDATED STRATEGIES")
    print("=" * 60)

    for strategy in updated:

        print(strategy)