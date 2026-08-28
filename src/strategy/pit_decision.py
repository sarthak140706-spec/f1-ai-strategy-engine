"""
pit_decision.py

PHASE 3.4 — PIT-STOP DECISION ENGINE

Purpose
-------
Convert race situation + tyre strategy + pit-stop analytics
into a strategic PIT NOW / STAY OUT decision.

This module does NOT perform pit-stop data collection.

It uses:
    Phase 2.4.4 -> Pit-stop analytics
    Phase 3.2   -> Race situation analysis
    Phase 3.3   -> Tyre strategy decision engine

Output:
    PIT NOW
    or
    STAY OUT

The engine also provides:
    - recommended compound
    - expected pit loss
    - estimated pace gain/loss
    - estimated strategic benefit
    - confidence
    - reasoning
"""


from typing import Dict, Any, Optional


# ============================================================
# DEFAULT PIT-STOP PARAMETERS
# ============================================================

DEFAULT_PIT_LOSS = 22.0


# ============================================================
# INPUT VALIDATION
# ============================================================

def _validate_inputs(
    current_lap: int,
    remaining_laps: int,
    tyre_age: float,
    recent_pace: float,
    pit_loss: float
) -> None:

    if current_lap < 0:
        raise ValueError(
            "current_lap cannot be negative."
        )

    if remaining_laps < 0:
        raise ValueError(
            "remaining_laps cannot be negative."
        )

    if tyre_age < 0:
        raise ValueError(
            "tyre_age cannot be negative."
        )

    if recent_pace <= 0:
        raise ValueError(
            "recent_pace must be greater than zero."
        )

    if pit_loss < 0:
        raise ValueError(
            "pit_loss cannot be negative."
        )


# ============================================================
# ESTIMATE TYRE PACE GAIN
# ============================================================

def estimate_pace_gain(
    current_tyre: str,
    recommended_tyre: str,
    tyre_age: float,
    degradation_rate: float = 0.0
) -> float:
    """
    Estimate expected lap-time improvement after changing tyres.

    This is intentionally conservative.

    The value represents seconds gained per lap.
    """

    current_tyre = (
        current_tyre or ""
    ).upper()

    recommended_tyre = (
        recommended_tyre or ""
    ).upper()

    # --------------------------------------------------------
    # BASE COMPOUND ADVANTAGE
    # --------------------------------------------------------

    compound_gain = {

        ("HARD", "SOFT"): 1.10,

        ("HARD", "MEDIUM"): 0.80,

        ("MEDIUM", "SOFT"): 0.65,

        ("MEDIUM", "HARD"): -0.25,

        ("SOFT", "MEDIUM"): -0.20,

        ("SOFT", "HARD"): -0.40,

    }

    gain = compound_gain.get(

        (
            current_tyre,
            recommended_tyre
        ),

        0.0

    )

    # --------------------------------------------------------
    # TYRE AGE EFFECT
    # --------------------------------------------------------

    if tyre_age >= 20:

        gain += 0.45

    elif tyre_age >= 15:

        gain += 0.25

    elif tyre_age >= 10:

        gain += 0.10

    # --------------------------------------------------------
    # DEGRADATION EFFECT
    # --------------------------------------------------------

    if degradation_rate > 0:

        gain += min(

            degradation_rate * 0.5,

            0.50

        )

    return round(

        max(gain, -1.0),

        3

    )


# ============================================================
# ESTIMATE PIT BENEFIT
# ============================================================

def estimate_pit_benefit(
    pit_loss: float,
    pace_gain_per_lap: float,
    remaining_laps: int
) -> float:
    """
    Estimate net time benefit of pitting.

    Positive value:
        PIT is beneficial.

    Negative value:
        STAY OUT is beneficial.

    Formula:

        Total Pace Gain
        -
        Pit Stop Loss
    """

    total_pace_gain = (

        pace_gain_per_lap
        * remaining_laps

    )

    benefit = (

        total_pace_gain
        - pit_loss

    )

    return round(

        benefit,

        3

    )


# ============================================================
# TRAFFIC ADJUSTMENT
# ============================================================

def calculate_traffic_penalty(
    gap_ahead: Optional[float],
    gap_behind: Optional[float],
    position: Optional[int]
) -> float:
    """
    Estimate the strategic penalty caused by traffic.

    Returns seconds of estimated additional loss.
    """

    penalty = 0.0

    # --------------------------------------------------------
    # CAR AHEAD
    # --------------------------------------------------------

    if gap_ahead is not None:

        if gap_ahead <= 1.0:

            penalty += 0.8

        elif gap_ahead <= 2.0:

            penalty += 0.4

    # --------------------------------------------------------
    # CAR BEHIND
    # --------------------------------------------------------

    if gap_behind is not None:

        if gap_behind <= 2.0:

            penalty += 0.8

        elif gap_behind <= 5.0:

            penalty += 0.3

    # --------------------------------------------------------
    # TRACK POSITION
    # --------------------------------------------------------

    if position is not None:

        if position <= 3:

            penalty += 0.2

    return round(

        penalty,

        3

    )


# ============================================================
# PIT DECISION ENGINE
# ============================================================

def evaluate_pit_decision(
    current_lap: int,
    remaining_laps: int,
    current_tyre: str,
    tyre_age: float,
    recent_pace: float,
    position: Optional[int] = None,
    gap_ahead: Optional[float] = None,
    gap_behind: Optional[float] = None,
    pit_loss: float = DEFAULT_PIT_LOSS,
    recommended_tyre: Optional[str] = None,
    degradation_rate: float = 0.0,
    race_situation: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Evaluate whether the driver should PIT NOW or STAY OUT.
    """

    _validate_inputs(

        current_lap=current_lap,

        remaining_laps=remaining_laps,

        tyre_age=tyre_age,

        recent_pace=recent_pace,

        pit_loss=pit_loss

    )

    current_tyre = (

        current_tyre or "UNKNOWN"

    ).upper()

    if recommended_tyre is None:

        recommended_tyre = current_tyre

    recommended_tyre = (

        recommended_tyre or current_tyre

    ).upper()

    # ========================================================
    # RACE FINISHED / VERY FEW LAPS
    # ========================================================

    if remaining_laps <= 1:

        return {

            "action": "STAY_OUT",

            "recommended_tyre":
                current_tyre,

            "pit_loss":
                pit_loss,

            "pace_gain_per_lap":
                0.0,

            "estimated_benefit":
                -pit_loss,

            "traffic_penalty":
                0.0,

            "confidence":
                99.0,

            "decision":
                "STAY OUT",

            "reason":
                "There are too few laps remaining to recover "
                "the pit-stop time loss."

        }

    # ========================================================
    # PACE GAIN
    # ========================================================

    pace_gain = estimate_pace_gain(

        current_tyre=current_tyre,

        recommended_tyre=recommended_tyre,

        tyre_age=tyre_age,

        degradation_rate=degradation_rate

    )

    # ========================================================
    # TRAFFIC
    # ========================================================

    traffic_penalty = calculate_traffic_penalty(

        gap_ahead=gap_ahead,

        gap_behind=gap_behind,

        position=position

    )

    # ========================================================
    # RAW PIT BENEFIT
    # ========================================================

    raw_benefit = estimate_pit_benefit(

        pit_loss=pit_loss,

        pace_gain_per_lap=pace_gain,

        remaining_laps=remaining_laps

    )

    adjusted_benefit = (

        raw_benefit
        - traffic_penalty

    )

    # ========================================================
    # TYRE AGE PRESSURE
    # ========================================================

    tyre_age_pressure = 0.0

    if tyre_age >= 25:

        tyre_age_pressure = 2.0

    elif tyre_age >= 20:

        tyre_age_pressure = 1.0

    elif tyre_age >= 15:

        tyre_age_pressure = 0.5

    adjusted_benefit += tyre_age_pressure

    # ========================================================
    # RACE SITUATION INPUT
    # ========================================================

    situation_name = ""

    if race_situation:

        situation_name = str(

            race_situation.get(

                "race_situation",

                ""

            )

        ).upper()

        pit_urgency = str(

            race_situation.get(

                "pit_urgency",

                ""

            )

        ).upper()

        if pit_urgency == "HIGH":

            adjusted_benefit += 1.0

        elif pit_urgency == "MEDIUM":

            adjusted_benefit += 0.5

    # ========================================================
    # FINAL DECISION
    # ========================================================

    if adjusted_benefit > 0:

        action = "PIT_NOW"

        decision = "PIT NOW"

    else:

        action = "STAY_OUT"

        decision = "STAY OUT"

    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = 50.0

    confidence += min(

        abs(adjusted_benefit) * 2.5,

        40.0

    )

    if tyre_age >= 20:

        confidence += 5.0

    confidence = min(

        confidence,

        99.0

    )

    confidence = round(

        confidence,

        1

    )

    # ========================================================
    # REASONING
    # ========================================================

    if action == "PIT_NOW":

        reason = (

            f"Pitting is projected to recover the "
            f"{pit_loss:.1f}s pit-stop loss through an "
            f"estimated {pace_gain:.2f}s/lap pace improvement. "
            f"The adjusted strategic benefit is "
            f"{adjusted_benefit:.2f}s."
        )

    else:

        reason = (

            f"Staying out is currently more efficient because "
            f"the estimated tyre pace benefit does not justify "
            f"the {pit_loss:.1f}s pit-stop loss. "
            f"Adjusted pit benefit is "
            f"{adjusted_benefit:.2f}s."
        )

    return {

        "action":
            action,

        "decision":
            decision,

        "recommended_tyre":
            recommended_tyre,

        "current_tyre":
            current_tyre,

        "current_lap":
            current_lap,

        "remaining_laps":
            remaining_laps,

        "tyre_age":
            tyre_age,

        "pit_loss":
            round(
                pit_loss,
                3
            ),

        "pace_gain_per_lap":
            pace_gain,

        "estimated_benefit":
            adjusted_benefit,

        "raw_benefit":
            raw_benefit,

        "traffic_penalty":
            traffic_penalty,

        "tyre_age_pressure":
            tyre_age_pressure,

        "confidence":
            confidence,

        "race_situation":
            situation_name,

        "reason":
            reason

    }


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_pit_decision(
    result: Dict[str, Any]
) -> None:
    """
    Display the pit-stop decision.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "PIT-STOP DECISION ENGINE"
    )

    print(
        "=" * 60
    )

    print(
        f"\nDecision: "
        f"{result.get('decision')}"
    )

    print(
        f"Recommended Tyre: "
        f"{result.get('recommended_tyre')}"
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
        f"Remaining Laps: "
        f"{result.get('remaining_laps')}"
    )

    print(
        f"Pit Loss: "
        f"{result.get('pit_loss'):.2f}s"
    )

    print(
        f"Expected Pace Gain: "
        f"{result.get('pace_gain_per_lap'):.3f}s/lap"
    )

    print(
        f"Estimated Strategic Benefit: "
        f"{result.get('estimated_benefit'):.3f}s"
    )

    print(
        f"Traffic Penalty: "
        f"{result.get('traffic_penalty'):.3f}s"
    )

    print(
        f"Confidence: "
        f"{result.get('confidence'):.1f}%"
    )

    print(
        f"\nReason:"
    )

    print(
        result.get(
            "reason"
        )
    )

    print(
        "=" * 60
    )


# ============================================================
# PHASE 3.4 TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n" + "=" * 60
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 3.4 — PIT-STOP DECISION ENGINE"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # TEST SCENARIO
    # --------------------------------------------------------

    CURRENT_LAP = 35

    REMAINING_LAPS = 22

    CURRENT_TYRE = "HARD"

    TYRE_AGE = 22

    RECENT_PACE = 96.2

    POSITION = 4

    GAP_AHEAD = 1.8

    GAP_BEHIND = 12.4

    PIT_LOSS = 22.0

    RECOMMENDED_TYRE = "MEDIUM"

    DEGRADATION_RATE = 0.08

    RACE_SITUATION = {

        "race_situation":
            "ATTACKING",

        "pit_urgency":
            "LOW",

        "opportunity":
            "UNDERCUT",

        "threat":
            "CAR_AHEAD"

    }

    # --------------------------------------------------------
    # EVALUATE
    # --------------------------------------------------------

    print(
        "\n[1/2] Evaluating pit-stop decision..."
    )

    result = evaluate_pit_decision(

        current_lap=CURRENT_LAP,

        remaining_laps=REMAINING_LAPS,

        current_tyre=CURRENT_TYRE,

        tyre_age=TYRE_AGE,

        recent_pace=RECENT_PACE,

        position=POSITION,

        gap_ahead=GAP_AHEAD,

        gap_behind=GAP_BEHIND,

        pit_loss=PIT_LOSS,

        recommended_tyre=RECOMMENDED_TYRE,

        degradation_rate=DEGRADATION_RATE,

        race_situation=RACE_SITUATION

    )

    print(
        "Pit-stop evaluation completed."
    )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    print(
        "\n[2/2] Generating pit-stop recommendation..."
    )

    display_pit_decision(

        result

    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    required_fields = [

        "action",

        "decision",

        "recommended_tyre",

        "pit_loss",

        "pace_gain_per_lap",

        "estimated_benefit",

        "confidence",

        "reason"

    ]

    missing_fields = [

        field

        for field in required_fields

        if field not in result

    ]

    if missing_fields:

        raise RuntimeError(

            "Missing required fields: "

            + ", ".join(
                missing_fields
            )

        )

    print(
        "\n" + "=" * 60
    )

    print(
        "PHASE 3.4 PIT-STOP DECISION TEST PASSED"
    )

    print(
        "=" * 60
    )