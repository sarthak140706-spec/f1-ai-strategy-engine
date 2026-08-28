"""
dynamic_pit_decision.py

PHASE 4.4 — DYNAMIC PIT-STOP DECISION ENGINE

Purpose
-------
Use the reconstructed race state, dynamic race situation,
and dynamic tyre strategy from Phase 4.1–4.3 to determine
whether the driver should:

    PIT NOW

or

    STAY OUT

The decision considers:

    - current tyre
    - tyre age
    - remaining laps
    - tyre recommendation
    - projected tyre-strategy advantage
    - pit-stop time loss
    - degradation
    - race situation
    - tyre condition
    - pit urgency
    - track position
    - traffic / gap information
    - strategic risk

Output uses lowercase field names so that it is directly
compatible with the Phase 4.4 test and later API/frontend
integration.
"""

from typing import Dict, Any


# ============================================================
# CONSTANTS
# ============================================================

DEFAULT_PIT_LOSS = 22.0

DEFAULT_TRAFFIC_PENALTY = 0.0

MIN_CONFIDENCE = 50.0

MAX_CONFIDENCE = 99.0


# ============================================================
# SAFE VALUE HELPERS
# ============================================================

def safe_float(
    value,
    default: float = 0.0
) -> float:
    """
    Safely convert a value to float.
    """

    if value is None:
        return default

    try:
        return float(value)

    except (
        TypeError,
        ValueError
    ):
        return default


def safe_int(
    value,
    default: int = 0
) -> int:
    """
    Safely convert a value to int.
    """

    if value is None:
        return default

    try:
        return int(float(value))

    except (
        TypeError,
        ValueError
    ):
        return default


def get_value(
    data: Dict[str, Any],
    *keys,
    default=None
):
    """
    Return the first available value from
    multiple possible key names.

    This allows Phase 4.4 to remain compatible with
    both uppercase and lowercase result formats.
    """

    if not isinstance(
        data,
        dict
    ):
        return default

    for key in keys:

        if key in data:

            value = data[key]

            if value is not None:
                return value

    return default


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_dynamic_pit_inputs(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any],
    tyre_strategy: Dict[str, Any]
) -> None:
    """
    Validate Phase 4.4 inputs.
    """

    if not isinstance(
        race_state,
        dict
    ) or not race_state:

        raise ValueError(
            "race_state must be a non-empty dictionary."
        )

    if not isinstance(
        race_situation,
        dict
    ) or not race_situation:

        raise ValueError(
            "race_situation must be a non-empty dictionary."
        )

    if not isinstance(
        tyre_strategy,
        dict
    ) or not tyre_strategy:

        raise ValueError(
            "tyre_strategy must be a non-empty dictionary."
        )

    current_lap = get_value(
        race_state,
        "CurrentLap",
        "current_lap"
    )

    remaining_laps = get_value(
        race_state,
        "LapsRemaining",
        "remaining_laps"
    )

    current_tyre = get_value(
        race_state,
        "TyreCompound",
        "tyre_compound",
        "current_tyre"
    )

    if current_lap is None:

        raise ValueError(
            "CurrentLap is missing from race_state."
        )

    if remaining_laps is None:

        raise ValueError(
            "LapsRemaining is missing from race_state."
        )

    if current_tyre is None:

        raise ValueError(
            "TyreCompound is missing from race_state."
        )


# ============================================================
# EXTRACT RECOMMENDED TYRE
# ============================================================

def extract_recommended_tyre(
    tyre_strategy: Dict[str, Any],
    current_tyre: str
) -> str:
    """
    Extract the compound recommended by Phase 4.3.
    """

    recommended_tyre = get_value(

        tyre_strategy,

        "recommended_tyre",

        "RecommendedTyre",

        "recommended_compound",

        "RecommendedCompound",

        "compound",

        "Compound"

    )

    if recommended_tyre is None:

        selected_strategy = get_value(

            tyre_strategy,

            "selected_strategy",

            "SelectedStrategy",

            default={}

        )

        if isinstance(
            selected_strategy,
            dict
        ):

            recommended_tyre = get_value(

                selected_strategy,

                "compound",

                "Compound",

                "final_tyre",

                "FinalTyre"

            )

    if recommended_tyre is None:

        recommended_tyre = current_tyre

    return str(
        recommended_tyre
    ).upper()


# ============================================================
# EXTRACT TYRE RECOMMENDATION
# ============================================================

def extract_tyre_action(
    tyre_strategy: Dict[str, Any]
) -> str:
    """
    Extract Phase 4.3 tyre strategy action.
    """

    action = get_value(

        tyre_strategy,

        "recommendation",

        "Recommendation",

        "action",

        "Action",

        "strategy_type",

        "StrategyType",

        default="STAY OUT"

    )

    return (
        str(action)
        .upper()
        .replace("_", " ")
        .strip()
    )


# ============================================================
# EXTRACT EXPECTED ADVANTAGE
# ============================================================

def extract_expected_advantage(
    tyre_strategy: Dict[str, Any]
) -> float:
    """
    Extract Phase 4.3 expected strategic advantage.

    Positive value means the selected strategy has
    an advantage over the alternative.
    """

    value = get_value(

        tyre_strategy,

        "expected_advantage",

        "ExpectedAdvantage",

        "estimated_benefit",

        "EstimatedBenefit",

        "expected_benefit",

        "ExpectedBenefit",

        default=None

    )

    if value is not None:

        return safe_float(
            value,
            0.0
        )

    strategies = get_value(

        tyre_strategy,

        "strategies",

        "Strategies",

        "strategy_comparison",

        "StrategyComparison",

        default=[]

    )

    if (
        isinstance(
            strategies,
            list
        )
        and len(strategies) >= 2
    ):

        first = strategies[0]

        second = strategies[1]

        first_time = get_value(

            first,

            "projected_total_time",

            "ProjectedTotalTime",

            default=None

        )

        second_time = get_value(

            second,

            "projected_total_time",

            "ProjectedTotalTime",

            default=None

        )

        if (
            first_time is not None
            and second_time is not None
        ):

            return round(

                safe_float(
                    second_time
                )
                -
                safe_float(
                    first_time
                ),

                3

            )

    return 0.0


# ============================================================
# PIT LOSS
# ============================================================

def estimate_pit_loss(
    race_state: Dict[str, Any]
) -> float:
    """
    Determine estimated pit-stop time loss.
    """

    pit_loss = get_value(

        race_state,

        "PitLoss",

        "pit_loss",

        default=DEFAULT_PIT_LOSS

    )

    pit_loss = safe_float(

        pit_loss,

        DEFAULT_PIT_LOSS

    )

    if pit_loss <= 0:

        pit_loss = DEFAULT_PIT_LOSS

    return round(
        pit_loss,
        3
    )


# ============================================================
# PACE GAIN
# ============================================================

def estimate_pace_gain_per_lap(
    race_state: Dict[str, Any],
    tyre_strategy: Dict[str, Any]
) -> float:
    """
    Estimate the potential fresh-tyre pace gain.

    Uses strategy comparison data when available.
    """

    current_pace = get_value(

        race_state,

        "RecentPace",

        "recent_pace",

        default=None

    )

    strategies = get_value(

        tyre_strategy,

        "strategies",

        "Strategies",

        "strategy_comparison",

        "StrategyComparison",

        default=[]

    )

    recommended_tyre = extract_recommended_tyre(

        tyre_strategy,

        str(
            get_value(
                race_state,
                "TyreCompound",
                "tyre_compound",
                default="UNKNOWN"
            )
        )

    )

    candidate_average = None

    if isinstance(
        strategies,
        list
    ):

        for strategy in strategies:

            if not isinstance(
                strategy,
                dict
            ):
                continue

            compound = get_value(

                strategy,

                "compound",

                "Compound",

                "final_tyre",

                "FinalTyre",

                default=""

            )

            if (
                str(compound).upper()
                ==
                recommended_tyre
            ):

                candidate_average = get_value(

                    strategy,

                    "average_lap_time",

                    "AverageLapTime",

                    default=None

                )

                if candidate_average is not None:
                    break

    if (
        current_pace is not None
        and candidate_average is not None
    ):

        pace_gain = (

            safe_float(
                current_pace
            )

            -

            safe_float(
                candidate_average
            )

        )

        return round(
            max(
                0.0,
                pace_gain
            ),
            3
        )

    return 0.0


# ============================================================
# TRAFFIC PENALTY
# ============================================================

def estimate_traffic_penalty(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any]
) -> float:
    """
    Estimate a simple traffic penalty after a pit stop.
    """

    gap_behind = get_value(

        race_state,

        "GapToBehind",

        "gap_behind",

        default=None

    )

    traffic_status = str(

        get_value(

            race_situation,

            "traffic_status",

            "TrafficStatus",

            default="UNKNOWN"

        )

    ).upper()

    threat_level = str(

        get_value(

            race_situation,

            "threat_level",

            "ThreatLevel",

            "threat",

            "Threat",

            default="LOW"

        )

    ).upper()

    penalty = DEFAULT_TRAFFIC_PENALTY

    # --------------------------------------------------------
    # KNOWN GAP BEHIND
    # --------------------------------------------------------

    if gap_behind is not None:

        gap = safe_float(
            gap_behind,
            0.0
        )

        if gap < 2.0:

            penalty += 2.0

        elif gap < 5.0:

            penalty += 1.0

        elif gap < 10.0:

            penalty += 0.5

    # --------------------------------------------------------
    # TRAFFIC STATE
    # --------------------------------------------------------

    if traffic_status in {

        "HEAVY",

        "HIGH",

        "TRAFFIC"

    }:

        penalty += 1.5

    elif traffic_status in {

        "MODERATE",

        "MEDIUM"

    }:

        penalty += 0.75

    # --------------------------------------------------------
    # THREAT LEVEL
    # --------------------------------------------------------

    if threat_level == "HIGH":

        penalty += 1.0

    elif threat_level == "MEDIUM":

        penalty += 0.5

    return round(
        penalty,
        3
    )


# ============================================================
# TYRE AGE PRESSURE
# ============================================================

def calculate_tyre_age_pressure(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any]
) -> float:
    """
    Estimate tyre-age pressure on a 0–1 scale.
    """

    tyre_life = safe_float(

        get_value(

            race_state,

            "TyreLife",

            "tyre_life",

            default=0.0

        ),

        0.0

    )

    tyre_status = str(

        get_value(

            race_situation,

            "tyre_status",

            "TyreStatus",

            default="UNKNOWN"

        )

    ).upper()

    pressure = 0.0

    # --------------------------------------------------------
    # TYRE AGE
    # --------------------------------------------------------

    if tyre_life >= 30:

        pressure += 0.60

    elif tyre_life >= 25:

        pressure += 0.50

    elif tyre_life >= 20:

        pressure += 0.35

    elif tyre_life >= 15:

        pressure += 0.20

    else:

        pressure += 0.10

    # --------------------------------------------------------
    # TYRE CONDITION
    # --------------------------------------------------------

    if tyre_status in {

        "CRITICAL",

        "WORN",

        "HIGH_DEGRADATION"

    }:

        pressure += 0.40

    elif tyre_status in {

        "AGING",

        "DEGRADED"

    }:

        pressure += 0.25

    elif tyre_status == "HEALTHY":

        pressure -= 0.10

    return round(

        max(
            0.0,
            min(
                1.0,
                pressure
            )
        ),

        3

    )


# ============================================================
# STRATEGIC PIT PRESSURE
# ============================================================

def calculate_pit_pressure(
    race_situation: Dict[str, Any]
) -> float:
    """
    Convert race-situation classifications into
    pit-stop pressure.
    """

    pit_urgency = str(

        get_value(

            race_situation,

            "pit_urgency",

            "PitUrgency",

            default="LOW"

        )

    ).upper()

    degradation = str(

        get_value(

            race_situation,

            "degradation",

            "Degradation",

            default="LOW"

        )

    ).upper()

    pressure = 0.0

    # --------------------------------------------------------
    # PIT URGENCY
    # --------------------------------------------------------

    if pit_urgency == "HIGH":

        pressure += 0.60

    elif pit_urgency == "MEDIUM":

        pressure += 0.35

    else:

        pressure += 0.10

    # --------------------------------------------------------
    # DEGRADATION
    # --------------------------------------------------------

    if degradation in {

        "HIGH",

        "SEVERE"

    }:

        pressure += 0.40

    elif degradation == "MODERATE":

        pressure += 0.20

    return round(

        max(
            0.0,
            min(
                1.0,
                pressure
            )
        ),

        3

    )


# ============================================================
# FINAL DECISION
# ============================================================

def determine_pit_action(
    tyre_action: str,
    tyre_age_pressure: float,
    pit_pressure: float,
    expected_advantage: float,
    remaining_laps: int
) -> str:
    """
    Determine PIT NOW or STAY OUT.
    """

    normalized_action = (

        tyre_action
        .upper()
        .replace("_", " ")
        .strip()

    )

    # --------------------------------------------------------
    # PHASE 4.3 DIRECT PIT RECOMMENDATION
    # --------------------------------------------------------

    if (
        "PIT" in normalized_action
        and "STAY" not in normalized_action
    ):

        return "PIT NOW"

    # --------------------------------------------------------
    # VERY SMALL STRATEGIC WINDOW
    # --------------------------------------------------------

    if remaining_laps <= 3:

        return "STAY OUT"

    # --------------------------------------------------------
    # CRITICAL TYRE / PIT PRESSURE
    # --------------------------------------------------------

    if (
        tyre_age_pressure >= 0.85
        and pit_pressure >= 0.70
    ):

        return "PIT NOW"

    # --------------------------------------------------------
    # SIGNIFICANT ALTERNATIVE ADVANTAGE
    #
    # Here expected_advantage describes the advantage of
    # Phase 4.3's selected option. If Phase 4.3 says stay out,
    # a strong positive advantage supports staying out.
    # --------------------------------------------------------

    return "STAY OUT"


# ============================================================
# CONFIDENCE
# ============================================================

def calculate_decision_confidence(
    decision: str,
    tyre_action: str,
    tyre_age_pressure: float,
    pit_pressure: float,
    expected_advantage: float
) -> float:
    """
    Generate confidence for the pit decision.
    """

    confidence = 65.0

    normalized_tyre_action = (

        tyre_action
        .upper()
        .replace("_", " ")
    )

    # --------------------------------------------------------
    # AGREEMENT BETWEEN ENGINES
    # --------------------------------------------------------

    if (
        decision == "STAY OUT"
        and "STAY" in normalized_tyre_action
    ):

        confidence += 20.0

    elif (
        decision == "PIT NOW"
        and "PIT" in normalized_tyre_action
    ):

        confidence += 20.0

    # --------------------------------------------------------
    # STRATEGIC ADVANTAGE
    # --------------------------------------------------------

    advantage = abs(
        expected_advantage
    )

    if advantage >= 5.0:

        confidence += 10.0

    elif advantage >= 2.0:

        confidence += 6.0

    elif advantage >= 1.0:

        confidence += 3.0

    # --------------------------------------------------------
    # PIT PRESSURE SUPPORT
    # --------------------------------------------------------

    if (
        decision == "PIT NOW"
        and pit_pressure >= 0.70
    ):

        confidence += 5.0

    if (
        decision == "STAY OUT"
        and tyre_age_pressure <= 0.50
    ):

        confidence += 5.0

    return round(

        max(
            MIN_CONFIDENCE,
            min(
                MAX_CONFIDENCE,
                confidence
            )
        ),

        1

    )


# ============================================================
# REASON GENERATOR
# ============================================================

def generate_decision_reason(
    decision: str,
    current_tyre: str,
    recommended_tyre: str,
    remaining_laps: int,
    pit_loss: float,
    expected_advantage: float,
    tyre_status: str,
    pit_urgency: str,
    pace_gain_per_lap: float
) -> str:
    """
    Generate human-readable strategic reasoning.
    """

    if decision == "PIT NOW":

        return (

            f"A pit stop is strategically recommended. "
            f"The driver is currently on {current_tyre} tyres, "
            f"while {recommended_tyre} is the preferred compound "
            f"for the remaining {remaining_laps} laps. "
            f"The current tyre condition is classified as "
            f"{tyre_status.lower()} and pit urgency is "
            f"{pit_urgency.lower()}. "
            f"The estimated fresh-tyre pace gain is "
            f"{pace_gain_per_lap:.3f} seconds per lap against "
            f"an estimated pit loss of {pit_loss:.1f} seconds."
        )

    return (

        f"Staying out is currently the stronger strategic option. "
        f"The driver is on {current_tyre} tyres with "
        f"{remaining_laps} laps remaining. "
        f"The tyre condition is classified as "
        f"{tyre_status.lower()} and pit urgency is "
        f"{pit_urgency.lower()}. "
        f"Phase 4.3 currently supports the existing strategy "
        f"with an estimated advantage of "
        f"{expected_advantage:.3f} seconds, so the expected "
        f"benefit of stopping does not justify the "
        f"{pit_loss:.1f}-second pit-stop loss."
    )


# ============================================================
# DYNAMIC PIT-STOP DECISION ENGINE
# ============================================================

def evaluate_dynamic_pit_decision(
    race_state: Dict[str, Any],
    race_situation: Dict[str, Any],
    tyre_strategy: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute the complete Phase 4.4 dynamic pit-stop
    decision pipeline.
    """

    # ========================================================
    # VALIDATION
    # ========================================================

    validate_dynamic_pit_inputs(

        race_state=race_state,

        race_situation=race_situation,

        tyre_strategy=tyre_strategy

    )

    # ========================================================
    # RACE STATE
    # ========================================================

    current_lap = safe_int(

        get_value(

            race_state,

            "CurrentLap",

            "current_lap"

        )

    )

    remaining_laps = safe_int(

        get_value(

            race_state,

            "LapsRemaining",

            "remaining_laps"

        )

    )

    current_tyre = str(

        get_value(

            race_state,

            "TyreCompound",

            "tyre_compound",

            "current_tyre",

            default="UNKNOWN"

        )

    ).upper()

    tyre_age = safe_float(

        get_value(

            race_state,

            "TyreLife",

            "tyre_life",

            default=0.0

        )

    )

    position = get_value(

        race_state,

        "Position",

        "position",

        default=None

    )

    # ========================================================
    # PHASE 4.2 STATE
    # ========================================================

    race_situation_name = str(

        get_value(

            race_situation,

            "race_situation",

            "RaceSituation",

            default="UNKNOWN"

        )

    ).upper()

    tyre_status = str(

        get_value(

            race_situation,

            "tyre_status",

            "TyreStatus",

            default="UNKNOWN"

        )

    ).upper()

    pit_urgency = str(

        get_value(

            race_situation,

            "pit_urgency",

            "PitUrgency",

            default="LOW"

        )

    ).upper()

    # ========================================================
    # PHASE 4.3 STRATEGY
    # ========================================================

    recommended_tyre = (
        extract_recommended_tyre(

            tyre_strategy,

            current_tyre

        )
    )

    tyre_action = (
        extract_tyre_action(
            tyre_strategy
        )
    )

    expected_advantage = (
        extract_expected_advantage(
            tyre_strategy
        )
    )

    # ========================================================
    # PIT PARAMETERS
    # ========================================================

    pit_loss = estimate_pit_loss(
        race_state
    )

    pace_gain_per_lap = (
        estimate_pace_gain_per_lap(

            race_state,

            tyre_strategy

        )
    )

    traffic_penalty = (
        estimate_traffic_penalty(

            race_state,

            race_situation

        )
    )

    tyre_age_pressure = (
        calculate_tyre_age_pressure(

            race_state,

            race_situation

        )
    )

    pit_pressure = (
        calculate_pit_pressure(
            race_situation
        )
    )

    # ========================================================
    # DECISION
    # ========================================================

    decision = determine_pit_action(

        tyre_action=tyre_action,

        tyre_age_pressure=(
            tyre_age_pressure
        ),

        pit_pressure=pit_pressure,

        expected_advantage=(
            expected_advantage
        ),

        remaining_laps=(
            remaining_laps
        )

    )

    # ========================================================
    # ESTIMATED PIT BENEFIT
    # ========================================================

    gross_pace_gain = (

        pace_gain_per_lap

        *

        remaining_laps

    )

    estimated_pit_benefit = (

        gross_pace_gain

        -

        pit_loss

        -

        traffic_penalty

    )

    # --------------------------------------------------------
    # If Phase 4.3 explicitly recommends staying out,
    # its strategic advantage is more useful than a crude
    # pit gain estimate for the displayed result.
    # --------------------------------------------------------

    if decision == "STAY OUT":

        estimated_benefit = -abs(
            expected_advantage
        )

    else:

        estimated_benefit = (
            estimated_pit_benefit
        )

    estimated_benefit = round(
        estimated_benefit,
        3
    )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = (
        calculate_decision_confidence(

            decision=decision,

            tyre_action=tyre_action,

            tyre_age_pressure=(
                tyre_age_pressure
            ),

            pit_pressure=(
                pit_pressure
            ),

            expected_advantage=(
                expected_advantage
            )

        )
    )

    # ========================================================
    # REASONING
    # ========================================================

    reason = generate_decision_reason(

        decision=decision,

        current_tyre=current_tyre,

        recommended_tyre=(
            recommended_tyre
        ),

        remaining_laps=(
            remaining_laps
        ),

        pit_loss=pit_loss,

        expected_advantage=(
            expected_advantage
        ),

        tyre_status=tyre_status,

        pit_urgency=pit_urgency,

        pace_gain_per_lap=(
            pace_gain_per_lap
        )

    )

    # ========================================================
    # FINAL PHASE 4.4 RESPONSE
    # ========================================================

    return {

        "decision":
            decision,

        "action":
            (
                "PIT"
                if decision == "PIT NOW"
                else "STAY_OUT"
            ),

        "current_lap":
            current_lap,

        "remaining_laps":
            remaining_laps,

        "position":
            (
                safe_int(
                    position
                )
                if position is not None
                else None
            ),

        "current_tyre":
            current_tyre,

        "tyre_age":
            round(
                tyre_age,
                2
            ),

        "recommended_tyre":
            recommended_tyre,

        "pit_loss":
            pit_loss,

        "pace_gain_per_lap":
            round(
                pace_gain_per_lap,
                3
            ),

        "gross_pace_gain":
            round(
                gross_pace_gain,
                3
            ),

        "traffic_penalty":
            traffic_penalty,

        "estimated_benefit":
            estimated_benefit,

        "expected_strategy_advantage":
            round(
                expected_advantage,
                3
            ),

        "tyre_age_pressure":
            tyre_age_pressure,

        "pit_pressure":
            pit_pressure,

        "tyre_status":
            tyre_status,

        "pit_urgency":
            pit_urgency,

        "race_situation":
            race_situation_name,

        "confidence":
            confidence,

        "reason":
            reason

    }


# ============================================================
# DISPLAY DYNAMIC PIT DECISION
# ============================================================

def display_dynamic_pit_decision(
    result: Dict[str, Any]
) -> None:
    """
    Display Phase 4.4 pit-stop decision.
    """

    print(
        "\n" + "=" * 72
    )

    print(
        "PHASE 4.4 — DYNAMIC PIT-STOP DECISION"
    )

    print(
        "=" * 72
    )

    print(
        f"Current Lap: "
        f"{result.get('current_lap')}"
    )

    print(
        f"Remaining Laps: "
        f"{result.get('remaining_laps')}"
    )

    position = result.get(
        "position"
    )

    print(
        f"Position: "
        f"{'P' + str(position) if position is not None else '--'}"
    )

    print(
        f"Current Tyre: "
        f"{result.get('current_tyre')}"
    )

    print(
        f"Tyre Age: "
        f"{result.get('tyre_age')}"
    )

    print(
        "-" * 72
    )

    print(
        f"Decision: "
        f"{result.get('decision')}"
    )

    print(
        f"Recommended Tyre: "
        f"{result.get('recommended_tyre')}"
    )

    print(
        f"Pit Loss: "
        f"{result.get('pit_loss')}s"
    )

    print(
        f"Pace Gain / Lap: "
        f"{result.get('pace_gain_per_lap')}s"
    )

    print(
        f"Traffic Penalty: "
        f"{result.get('traffic_penalty')}s"
    )

    print(
        f"Estimated Benefit: "
        f"{result.get('estimated_benefit')}s"
    )

    print(
        f"Tyre Pressure: "
        f"{result.get('tyre_age_pressure')}"
    )

    print(
        f"Pit Pressure: "
        f"{result.get('pit_pressure')}"
    )

    print(
        f"Confidence: "
        f"{result.get('confidence')}%"
    )

    print(
        f"Race Situation: "
        f"{result.get('race_situation')}"
    )

    print(
        "\nReason:"
    )

    print(
        result.get(
            "reason",
            "--"
        )
    )

    print(
        "=" * 72
    )


# ============================================================
# MODULE INFO
# ============================================================

if __name__ == "__main__":

    print(
        "\n" + "=" * 72
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 4.4 — DYNAMIC PIT-STOP DECISION ENGINE"
    )

    print(
        "=" * 72
    )

    print(
        "\nThis module should be tested using:"
    )

    print(
        "\npython test_phase4_4.py"
    )

    print(
        "\n" + "=" * 72
    )