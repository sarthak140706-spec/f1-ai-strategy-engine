"""
context_score.py

Sprint 5 - Step 7

Combines race situation factors into a single
Race Context Score for strategy decisions.
"""

from typing import Dict, List


# ============================================================
# RACE CONTEXT SCORING
# ============================================================

def calculate_race_context_score(
    race_context: dict
) -> Dict:
    """
    Calculate overall race situation score.

    Parameters
    ----------
    race_context : dict
        Contains outputs from race awareness modules.

    Returns
    -------
    dict
        Race context evaluation.
    """


    score = 50

    reasons: List[str] = []


    # ========================================================
    # SAFETY CAR IMPACT
    # ========================================================

    safety_car = race_context.get(
        "SafetyCar",
        False
    )

    vsc = race_context.get(
        "VSC",
        False
    )


    if safety_car:

        score += 20

        reasons.append(
            "Safety Car creates strategic opportunity"
        )


    elif vsc:

        score += 10

        reasons.append(
            "Virtual Safety Car may reduce pit loss"
        )


    # ========================================================
    # WEATHER IMPACT
    # ========================================================

    weather_factor = race_context.get(
        "WeatherFactor",
        0
    )


    if weather_factor >= 0.7:

        score += 15

        reasons.append(
            "Weather conditions favour strategic change"
        )


    elif weather_factor >= 0.4:

        score += 5

        reasons.append(
            "Weather may influence strategy"
        )


    # ========================================================
    # TRAFFIC ANALYSIS
    # ========================================================

    traffic_risk = race_context.get(
        "TrafficRisk",
        "Low"
    )


    if traffic_risk == "Low":

        score += 10

        reasons.append(
            "Low traffic risk after pit stop"
        )


    elif traffic_risk == "Medium":

        score -= 5

        reasons.append(
            "Moderate traffic risk"
        )


    elif traffic_risk == "High":

        score -= 15

        reasons.append(
            "High traffic risk after pit stop"
        )


    # ========================================================
    # GAP ANALYSIS
    # ========================================================

    gap_ahead = race_context.get(
        "GapAhead",
        999
    )

    gap_behind = race_context.get(
        "GapBehind",
        999
    )


    if gap_ahead <= 2:

        score += 10

        reasons.append(
            "Car ahead is within attack range"
        )


    if gap_behind >= 5:

        score += 5

        reasons.append(
            "Safe gap behind allows strategic flexibility"
        )


    # ========================================================
    # UNDERCUT / OVERCUT SCORE
    # ========================================================

    undercut_score = race_context.get(
        "UndercutScore",
        0
    )


    overcut_score = race_context.get(
        "OvercutScore",
        0
    )


    strategy_score = max(
        undercut_score,
        overcut_score
    )


    if strategy_score >= 75:

        score += 15

        reasons.append(
            "Strong strategic opportunity detected"
        )


    elif strategy_score >= 50:

        score += 8

        reasons.append(
            "Moderate strategic opportunity"
        )


    # ========================================================
    # NORMALIZE SCORE
    # ========================================================

    score = max(
        0,
        min(
            100,
            score
        )
    )


    # ========================================================
    # CLASSIFY SITUATION
    # ========================================================

    if score >= 80:

        situation = (
            "HIGHLY_FAVOURABLE"
        )

        confidence = "HIGH"


    elif score >= 60:

        situation = (
            "FAVOURABLE"
        )

        confidence = "MEDIUM"


    elif score >= 40:

        situation = (
            "NEUTRAL"
        )

        confidence = "MEDIUM"


    else:

        situation = (
            "UNFAVOURABLE"
        )

        confidence = "LOW"



    return {

        "RaceContextScore":
            score,


        "Situation":
            situation,


        "Confidence":
            confidence,


        "Reasons":
            reasons

    }



# ============================================================
# DISPLAY
# ============================================================

def display_context_score(
    result: Dict
) -> None:


    print("\n" + "=" * 60)

    print(
        "RACE CONTEXT SCORE"
    )

    print("=" * 60)


    print(
        f"Score      : {result['RaceContextScore']}/100"
    )


    print(
        f"Situation  : {result['Situation']}"
    )


    print(
        f"Confidence : {result['Confidence']}"
    )


    print("\nReasons:")


    for reason in result["Reasons"]:

        print(
            f"- {reason}"
        )


    print("=" * 60)



# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":


    sample_context = {


        "SafetyCar": False,

        "VSC": False,


        "WeatherFactor": 0.5,


        "TrafficRisk": "Low",


        "GapAhead": 1.8,

        "GapBehind": 6.0,


        "UndercutScore": 75,

        "OvercutScore": 55

    }


    result = calculate_race_context_score(

        sample_context

    )


    display_context_score(

        result

    )