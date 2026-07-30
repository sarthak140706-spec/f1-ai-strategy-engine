"""
undercut_overcut.py

Sprint 5 - Step 6

Evaluates undercut and overcut opportunities
using race gaps, tyre advantage, degradation,
traffic risk and pit window conditions.
"""

from typing import Dict, List


# ============================================================
# UNDERCUT / OVERCUT ANALYSIS
# ============================================================

def analyse_undercut_overcut(
    race_state: dict
) -> Dict:
    """
    Analyse undercut and overcut opportunities.

    Parameters
    ----------
    race_state : dict
        Current race situation.

    Returns
    -------
    dict
        Undercut / Overcut analysis.
    """


    # --------------------------------------------------------
    # BASIC RACE DATA
    # --------------------------------------------------------

    gap_ahead = race_state.get(
        "GapAhead",
        999.0
    )

    gap_behind = race_state.get(
        "GapBehind",
        999.0
    )


    remaining_laps = race_state.get(
        "RemainingLaps",
        0
    )


    # --------------------------------------------------------
    # TYRE DATA
    # --------------------------------------------------------

    current_tyre_age = race_state.get(
        "CurrentTyreAge",
        0
    )

    opponent_tyre_age = race_state.get(
        "OpponentTyreAge",
        0
    )


    tyre_deg_rate = race_state.get(
        "TyreDegRate",
        0.05
    )


    fresh_tyre_bonus = race_state.get(
        "FreshTyreBonus",
        1.0
    )


    # --------------------------------------------------------
    # PIT / TRAFFIC DATA
    # --------------------------------------------------------

    pit_loss = race_state.get(
        "PitLoss",
        20
    )


    traffic_risk = race_state.get(
        "TrafficRisk",
        "Low"
    )


    # --------------------------------------------------------
    # INITIAL SCORES
    # --------------------------------------------------------

    undercut_score = 0

    overcut_score = 0


    undercut_reasons: List[str] = []

    overcut_reasons: List[str] = []


    # ========================================================
    # UNDERCUT ANALYSIS
    # ========================================================


    # Gap to car ahead

    if gap_ahead <= 2:

        undercut_score += 30

        undercut_reasons.append(
            "Close gap to car ahead"
        )

    elif gap_ahead <= 4:

        undercut_score += 15

        undercut_reasons.append(
            "Potential target within range"
        )


    # Opponent older tyres

    if opponent_tyre_age > current_tyre_age:

        undercut_score += 20

        undercut_reasons.append(
            "Opponent tyres are older"
        )


    # Fresh tyre advantage

    if fresh_tyre_bonus >= 1.5:

        undercut_score += 15

        undercut_reasons.append(
            "Strong fresh tyre advantage"
        )


    # Remaining laps

    if remaining_laps >= 15:

        undercut_score += 10

        undercut_reasons.append(
            "Enough laps to recover pit loss"
        )


    # Traffic penalty

    if traffic_risk == "High":

        undercut_score -= 20

        undercut_reasons.append(
            "High traffic after pit stop"
        )


    # Pit loss penalty

    if pit_loss > 25:

        undercut_score -= 10

        undercut_reasons.append(
            "High pit lane loss"
        )



    # ========================================================
    # OVERCUT ANALYSIS
    # ========================================================


    # Gap behind

    if gap_behind >= 5:

        overcut_score += 30

        overcut_reasons.append(
            "Large gap behind"
        )

    elif gap_behind >= 3:

        overcut_score += 15

        overcut_reasons.append(
            "Safe gap behind"
        )


    # Tyre still alive

    if current_tyre_age < opponent_tyre_age:

        overcut_score += 15

        overcut_reasons.append(
            "Current tyres still competitive"
        )


    # Traffic benefit

    if traffic_risk == "High":

        overcut_score += 20

        overcut_reasons.append(
            "Avoiding traffic after pit"
        )


    # Degeneration check

    if tyre_deg_rate < 0.08:

        overcut_score += 10

        overcut_reasons.append(
            "Low tyre degradation"
        )


    # ========================================================
    # NORMALIZE SCORES
    # ========================================================

    undercut_score = max(
        0,
        min(
            100,
            undercut_score
        )
    )


    overcut_score = max(
        0,
        min(
            100,
            overcut_score
        )
    )


    # ========================================================
    # FINAL DECISION
    # ========================================================


    if undercut_score > overcut_score:

        action = "UNDERCUT"

        recommendation = (
            "Pit early to gain track position."
        )

        reasons = undercut_reasons


    elif overcut_score > undercut_score:

        action = "OVERCUT"

        recommendation = (
            "Stay out and extend the current stint."
        )

        reasons = overcut_reasons


    else:

        action = "NEUTRAL"

        recommendation = (
            "Maintain current strategy."
        )

        reasons = [
            "No clear undercut or overcut advantage"
        ]



    return {


        "UndercutScore":
            undercut_score,


        "OvercutScore":
            overcut_score,


        "RecommendedAction":
            action,


        "Recommendation":
            recommendation,


        "Reason":
            reasons

    }



# ============================================================
# DISPLAY
# ============================================================

def display_undercut_overcut(
    result: Dict
) -> None:


    print("\n" + "=" * 60)

    print(
        "UNDERCUT / OVERCUT ANALYSIS"
    )

    print("=" * 60)


    print(
        f"Undercut Score     : {result['UndercutScore']}/100"
    )


    print(
        f"Overcut Score      : {result['OvercutScore']}/100"
    )


    print(
        f"Recommended Action : {result['RecommendedAction']}"
    )


    print(
        f"Recommendation     : {result['Recommendation']}"
    )


    print("\nReasons:")

    for reason in result["Reason"]:

        print(
            f"- {reason}"
        )


    print("=" * 60)



# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":


    sample_state = {


        "GapAhead": 1.8,

        "GapBehind": 5.7,


        "CurrentTyreAge": 22,

        "OpponentTyreAge": 35,


        "TyreDegRate": 0.06,


        "FreshTyreBonus": 1.8,


        "PitLoss": 20,


        "TrafficRisk": "Low",


        "RemainingLaps": 25

    }


    result = analyse_undercut_overcut(

        sample_state

    )


    display_undercut_overcut(

        result

    )