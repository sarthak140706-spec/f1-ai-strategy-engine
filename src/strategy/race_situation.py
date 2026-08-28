"""
race_situation.py

PHASE 3.2
RACE SITUATION ANALYSIS

Purpose:
--------
Convert the current race state into a structured
strategic interpretation.

This module does NOT:
- choose a tyre
- decide whether to pit
- simulate strategies
- score strategies
- generate the final AI recommendation

Those responsibilities belong to later Phase 3 modules.

Pipeline:

    Race State
        ↓
    Race Situation Analysis
        ↓
    Strategic Situation
        ↓
    Threats / Opportunities / Urgency
"""


from typing import Dict, Any, Optional


# ============================================================
# SAFE NUMERIC CONVERSION
# ============================================================

def _to_float(
    value: Any,
    default: Optional[float] = None
) -> Optional[float]:

    try:

        if value is None:
            return default

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


def _to_int(
    value: Any,
    default: Optional[int] = None
) -> Optional[int]:

    try:

        if value is None:
            return default

        return int(value)

    except (
        TypeError,
        ValueError
    ):

        return default


# ============================================================
# POSITION ANALYSIS
# ============================================================

def analyze_position(
    position: Optional[int]
) -> str:

    if position is None:
        return "UNKNOWN"

    if position <= 3:
        return "PODIUM"

    if position <= 10:
        return "POINTS"

    return "OUTSIDE_POINTS"


# ============================================================
# TYRE ANALYSIS
# ============================================================

def analyze_tyre_status(
    tyre_compound: Optional[str],
    tyre_life: Optional[float]
) -> str:

    if not tyre_compound:
        return "UNKNOWN"

    tyre = str(
        tyre_compound
    ).upper()

    if tyre_life is None:
        return "UNKNOWN"

    # --------------------------------------------------------
    # General tyre-life interpretation
    # --------------------------------------------------------

    if tyre_life < 8:

        return "FRESH"

    if tyre_life < 18:

        return "HEALTHY"

    if tyre_life < 28:

        return "AGING"

    return "HIGH_AGE"


# ============================================================
# PACE ANALYSIS
# ============================================================

def analyze_pace(
    recent_pace: Optional[float],
    average_pace: Optional[float]
) -> str:

    if (
        recent_pace is None
        or average_pace is None
        or average_pace <= 0
    ):

        return "UNKNOWN"

    pace_difference = (
        recent_pace - average_pace
    )

    # Lower lap time = faster pace

    if pace_difference <= -0.5:

        return "IMPROVING"

    if pace_difference >= 0.5:

        return "DECLINING"

    return "STABLE"


# ============================================================
# TRAFFIC ANALYSIS
# ============================================================

def analyze_traffic(
    gap_ahead: Optional[float],
    gap_behind: Optional[float]
) -> str:

    if (
        gap_ahead is None
        and gap_behind is None
    ):

        return "UNKNOWN"

    # --------------------------------------------------------
    # Strong pressure from behind
    # --------------------------------------------------------

    if (
        gap_behind is not None
        and gap_behind <= 2.0
    ):

        return "HIGH_REAR_PRESSURE"

    # --------------------------------------------------------
    # Close car ahead = attack opportunity
    # --------------------------------------------------------

    if (
        gap_ahead is not None
        and gap_ahead <= 2.0
    ):

        return "CLOSE_CAR_AHEAD"

    # --------------------------------------------------------
    # Comfortable gaps
    # --------------------------------------------------------

    if (
        gap_behind is not None
        and gap_behind >= 8.0
    ):

        return "LOW_REAR_THREAT"

    return "MODERATE_TRAFFIC"


# ============================================================
# ATTACK / DEFENCE ANALYSIS
# ============================================================

def analyze_race_fight(
    gap_ahead: Optional[float],
    gap_behind: Optional[float]
) -> str:

    if (
        gap_ahead is not None
        and gap_ahead <= 2.0
    ):

        if (
            gap_behind is not None
            and gap_behind <= 3.0
        ):

            return "ACTIVE_BATTLE"

        return "ATTACKING"

    if (
        gap_behind is not None
        and gap_behind <= 2.0
    ):

        return "DEFENDING"

    if (
        gap_behind is not None
        and gap_behind >= 8.0
    ):

        return "SECURE_POSITION"

    return "NEUTRAL"


# ============================================================
# PIT URGENCY
# ============================================================

def analyze_pit_urgency(
    laps_remaining: Optional[int],
    tyre_status: str,
    gap_behind: Optional[float]
) -> str:

    urgency_score = 0

    # --------------------------------------------------------
    # Tyre age
    # --------------------------------------------------------

    if tyre_status == "HIGH_AGE":

        urgency_score += 3

    elif tyre_status == "AGING":

        urgency_score += 2

    elif tyre_status == "HEALTHY":

        urgency_score += 1

    # --------------------------------------------------------
    # Remaining race distance
    # --------------------------------------------------------

    if laps_remaining is not None:

        if laps_remaining <= 10:

            urgency_score += 2

        elif laps_remaining <= 20:

            urgency_score += 1

    # --------------------------------------------------------
    # Traffic protection
    # --------------------------------------------------------

    if (
        gap_behind is not None
        and gap_behind <= 2.0
    ):

        urgency_score += 1

    # --------------------------------------------------------
    # Final classification
    # --------------------------------------------------------

    if urgency_score >= 5:

        return "HIGH"

    if urgency_score >= 3:

        return "MEDIUM"

    return "LOW"


# ============================================================
# STRATEGIC OPPORTUNITY
# ============================================================

def identify_opportunity(
    gap_ahead: Optional[float],
    gap_behind: Optional[float],
    tyre_status: str
) -> str:

    if (
        gap_ahead is not None
        and gap_ahead <= 2.0
        and tyre_status in (
            "AGING",
            "HIGH_AGE"
        )
    ):

        return "UNDERCUT"

    if (
        gap_ahead is not None
        and gap_ahead <= 2.0
    ):

        return "ATTACK_CAR_AHEAD"

    if (
        gap_behind is not None
        and gap_behind >= 8.0
    ):

        return "SAFE_PIT_WINDOW"

    return "NONE"


# ============================================================
# STRATEGIC THREAT
# ============================================================

def identify_threat(
    gap_ahead: Optional[float],
    gap_behind: Optional[float],
    tyre_status: str,
    pace_status: str
) -> str:

    if tyre_status == "HIGH_AGE":

        return "TYRE_DEGRADATION"

    if (
        gap_behind is not None
        and gap_behind <= 2.0
    ):

        return "REAR_PRESSURE"

    if pace_status == "DECLINING":

        return "PACE_DROP"

    if (
        gap_ahead is not None
        and gap_ahead <= 2.0
    ):

        return "CAR_AHEAD"

    return "NONE"


# ============================================================
# STRATEGIC SUMMARY
# ============================================================

def generate_summary(
    race_state: Dict[str, Any],
    situation: str,
    tyre_status: str,
    pace_status: str,
    traffic_status: str,
    opportunity: str,
    threat: str
) -> str:

    driver = race_state.get(
        "Driver",
        "Driver"
    )

    position = race_state.get(
        "Position"
    )

    tyre = race_state.get(
        "TyreCompound",
        "UNKNOWN"
    )

    tyre_life = race_state.get(
        "TyreLife"
    )

    gap_ahead = race_state.get(
        "GapAhead"
    )

    gap_behind = race_state.get(
        "GapBehind"
    )

    parts = []

    # --------------------------------------------------------
    # Position
    # --------------------------------------------------------

    if position is not None:

        parts.append(
            f"{driver} is currently running "
            f"P{position}"
        )

    # --------------------------------------------------------
    # Tyre
    # --------------------------------------------------------

    if tyre_life is not None:

        parts.append(
            f"on {tyre} tyres with "
            f"{tyre_life:.0f} laps of tyre life"
        )

    # --------------------------------------------------------
    # Traffic
    # --------------------------------------------------------

    if (
        gap_ahead is not None
        and gap_behind is not None
    ):

        parts.append(
            f"{gap_ahead:.1f}s ahead and "
            f"{gap_behind:.1f}s behind"
        )

    # --------------------------------------------------------
    # Interpretation
    # --------------------------------------------------------

    if situation == "ATTACKING":

        parts.append(
            "The driver is close enough to "
            "attack the car ahead."
        )

    elif situation == "DEFENDING":

        parts.append(
            "The driver is under pressure "
            "from the car behind."
        )

    elif situation == "ACTIVE_BATTLE":

        parts.append(
            "The driver is involved in an "
            "active battle both ahead and behind."
        )

    elif situation == "SECURE_POSITION":

        parts.append(
            "The current track position is "
            "relatively secure."
        )

    # --------------------------------------------------------
    # Tyre degradation
    # --------------------------------------------------------

    if tyre_status == "HIGH_AGE":

        parts.append(
            "Tyre age indicates significant "
            "degradation risk."
        )

    elif tyre_status == "AGING":

        parts.append(
            "The current tyres are entering "
            "an aging phase."
        )

    # --------------------------------------------------------
    # Pace
    # --------------------------------------------------------

    if pace_status == "IMPROVING":

        parts.append(
            "Recent pace is improving."
        )

    elif pace_status == "DECLINING":

        parts.append(
            "Recent pace is declining."
        )

    # --------------------------------------------------------
    # Opportunity
    # --------------------------------------------------------

    if opportunity == "UNDERCUT":

        parts.append(
            "An undercut opportunity may exist."
        )

    elif opportunity == "SAFE_PIT_WINDOW":

        parts.append(
            "The gap behind provides a "
            "potentially safe pit window."
        )

    # --------------------------------------------------------
    # Threat
    # --------------------------------------------------------

    if threat == "TYRE_DEGRADATION":

        parts.append(
            "The primary strategic threat "
            "is tyre degradation."
        )

    elif threat == "REAR_PRESSURE":

        parts.append(
            "The primary strategic threat "
            "is pressure from behind."
        )

    elif threat == "PACE_DROP":

        parts.append(
            "The primary strategic threat "
            "is declining race pace."
        )

    return " ".join(parts)


# ============================================================
# MAIN RACE SITUATION ANALYSIS
# ============================================================

def analyze_race_situation(
    race_state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert a structured race state into a strategic state.

    Parameters
    ----------
    race_state : dict
        Current race-state information.

    Returns
    -------
    dict
        Structured strategic interpretation.
    """

    if not isinstance(
        race_state,
        dict
    ):

        raise TypeError(
            "race_state must be a dictionary."
        )

    # ========================================================
    # EXTRACT CURRENT STATE
    # ========================================================

    position = _to_int(
        race_state.get(
            "Position"
        )
    )

    current_lap = _to_int(
        race_state.get(
            "CurrentLap"
        )
    )

    total_laps = _to_int(
        race_state.get(
            "TotalLaps"
        )
    )

    laps_remaining = _to_int(
        race_state.get(
            "LapsRemaining"
        )
    )

    tyre_life = _to_float(
        race_state.get(
            "TyreLife"
        )
    )

    gap_ahead = _to_float(
        race_state.get(
            "GapAhead"
        )
    )

    gap_behind = _to_float(
        race_state.get(
            "GapBehind"
        )
    )

    recent_pace = _to_float(
        race_state.get(
            "RecentPace"
        )
    )

    average_pace = _to_float(
        race_state.get(
            "AveragePace"
        )
    )

    tyre_compound = race_state.get(
        "TyreCompound"
    )

    # ========================================================
    # ANALYZE INDIVIDUAL COMPONENTS
    # ========================================================

    position_status = analyze_position(
        position
    )

    tyre_status = analyze_tyre_status(
        tyre_compound,
        tyre_life
    )

    pace_status = analyze_pace(
        recent_pace,
        average_pace
    )

    traffic_status = analyze_traffic(
        gap_ahead,
        gap_behind
    )

    situation = analyze_race_fight(
        gap_ahead,
        gap_behind
    )

    pit_urgency = analyze_pit_urgency(
        laps_remaining,
        tyre_status,
        gap_behind
    )

    opportunity = identify_opportunity(
        gap_ahead,
        gap_behind,
        tyre_status
    )

    threat = identify_threat(
        gap_ahead,
        gap_behind,
        tyre_status,
        pace_status
    )

    # ========================================================
    # STRATEGIC SUMMARY
    # ========================================================

    summary = generate_summary(

        race_state=race_state,

        situation=situation,

        tyre_status=tyre_status,

        pace_status=pace_status,

        traffic_status=traffic_status,

        opportunity=opportunity,

        threat=threat

    )

    # ========================================================
    # FINAL STRATEGIC STATE
    # ========================================================

    strategic_state = {

        "current_lap":
            current_lap,

        "total_laps":
            total_laps,

        "laps_remaining":
            laps_remaining,

        "position":
            position,

        "position_status":
            position_status,

        "tyre_compound":
            tyre_compound,

        "tyre_life":
            tyre_life,

        "tyre_status":
            tyre_status,

        "recent_pace":
            recent_pace,

        "average_pace":
            average_pace,

        "pace_status":
            pace_status,

        "gap_ahead":
            gap_ahead,

        "gap_behind":
            gap_behind,

        "traffic_status":
            traffic_status,

        "race_situation":
            situation,

        "pit_urgency":
            pit_urgency,

        "opportunity":
            opportunity,

        "threat":
            threat,

        "strategic_summary":
            summary

    }

    return strategic_state


# ============================================================
# DISPLAY STRATEGIC STATE
# ============================================================

def display_race_situation(
    strategic_state: Dict[str, Any]
) -> None:

    print(
        "\n" + "=" * 60
    )

    print(
        "RACE SITUATION ANALYSIS"
    )

    print(
        "=" * 60
    )

    print(
        f"\nLap: "
        f"{strategic_state.get('current_lap')} / "
        f"{strategic_state.get('total_laps')}"
    )

    print(
        f"Position: "
        f"P{strategic_state.get('position')}"
    )

    print(
        f"Position Status: "
        f"{strategic_state.get('position_status')}"
    )

    print(
        f"Tyre: "
        f"{strategic_state.get('tyre_compound')}"
    )

    print(
        f"Tyre Life: "
        f"{strategic_state.get('tyre_life')}"
    )

    print(
        f"Tyre Status: "
        f"{strategic_state.get('tyre_status')}"
    )

    print(
        f"Recent Pace: "
        f"{strategic_state.get('recent_pace')}"
    )

    print(
        f"Average Pace: "
        f"{strategic_state.get('average_pace')}"
    )

    print(
        f"Pace Status: "
        f"{strategic_state.get('pace_status')}"
    )

    print(
        f"Gap Ahead: "
        f"{strategic_state.get('gap_ahead')}"
    )

    print(
        f"Gap Behind: "
        f"{strategic_state.get('gap_behind')}"
    )

    print(
        f"Traffic Status: "
        f"{strategic_state.get('traffic_status')}"
    )

    print(
        f"\nRace Situation: "
        f"{strategic_state.get('race_situation')}"
    )

    print(
        f"Pit Urgency: "
        f"{strategic_state.get('pit_urgency')}"
    )

    print(
        f"Opportunity: "
        f"{strategic_state.get('opportunity')}"
    )

    print(
        f"Threat: "
        f"{strategic_state.get('threat')}"
    )

    print(
        "\nStrategic Summary:"
    )

    print(
        strategic_state.get(
            "strategic_summary"
        )
    )

    print(
        "\n" + "=" * 60
    )


# ============================================================
# PHASE 3.2 TEST
# ============================================================

if __name__ == "__main__":

    test_race_state = {

        "Driver":
            "VER",

        "Position":
            4,

        "CurrentLap":
            35,

        "TotalLaps":
            57,

        "LapsRemaining":
            22,

        "TyreCompound":
            "HARD",

        "TyreLife":
            22,

        "GapAhead":
            1.8,

        "GapBehind":
            12.4,

        "RecentPace":
            96.2,

        "AveragePace":
            96.8

    }

    try:

        result = analyze_race_situation(
            test_race_state
        )

        display_race_situation(
            result
        )

        print(
            "\n✅ PHASE 3.2 RACE SITUATION "
            "ANALYSIS TEST PASSED"
        )

    except Exception as e:

        print(
            "\n❌ PHASE 3.2 TEST FAILED"
        )

        print(
            f"Error: {e}"
        )