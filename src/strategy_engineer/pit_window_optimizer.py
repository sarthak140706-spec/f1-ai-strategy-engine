"""
F1 AI STRATEGIST
PHASE 7.4 — PIT WINDOW OPTIMIZER

Purpose
-------
Estimate the most suitable upcoming pit-stop window from a
manual race state and the verified Phase 7 strategy output.

Pipeline
--------

7.1 Manual Race-State Builder
        ↓
7.2 AI Strategy Engineer Service
        ↓
7.3 Strategy Alternatives Engine
        ↓
7.4 Pit Window Optimizer
        ↓
Recommended Pit Lap
Pit Window
Recommended Tyre
Pit-Lap Ranking

IMPORTANT
---------
Phase 7.4 does not replace the existing Phase 4 simulation or
Phase 7.3 strategy ranking.

The optimizer evaluates WHEN a pit stop should occur while
respecting the strategy context produced by the existing
strategy engine.
"""


from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.strategy_engineer.strategy_alternatives_engine import (
    run_strategy_alternatives_engine,
)


# ============================================================
# CONSTANTS
# ============================================================

PHASE = "7.4"

COMPONENT = "pit_window_optimizer"

SUPPORTED_TYRES = {
    "SOFT",
    "MEDIUM",
    "HARD",
    "INTERMEDIATE",
    "WET",
}


# ============================================================
# SAFE CONVERSION
# ============================================================

def _safe_float(
    value: Any,
    default: float = 0.0
) -> float:

    try:

        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):

        return default


def _safe_int(
    value: Any,
    default: int = 0
) -> int:

    try:

        if value is None:
            return default

        return int(value)

    except (TypeError, ValueError):

        return default


# ============================================================
# NORMALISE TEXT
# ============================================================

def _normalise_text(
    value: Any
) -> str:

    if value is None:
        return ""

    return str(value).strip().upper()


# ============================================================
# EXTRACT RACE STATE
# ============================================================

def extract_race_state(
    alternatives_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract the Phase 7.1 race state from the nested
    Phase 7.2 result.
    """

    phase_7_2 = alternatives_result.get(
        "phase_7_2_result",
        {}
    )

    if not isinstance(phase_7_2, dict):
        return {}


    # --------------------------------------------------------
    # Most likely Phase 7.2 keys
    # --------------------------------------------------------

    for key in (
        "race_state",
        "manual_race_state",
        "state",
        "phase_7_1_state",
    ):

        state = phase_7_2.get(key)

        if isinstance(state, dict) and state:
            return state


    # --------------------------------------------------------
    # Compatibility fallback
    # --------------------------------------------------------

    return phase_7_2


# ============================================================
# SELECT PIT STRATEGY
# ============================================================

def select_best_pit_strategy(
    alternatives: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Return the highest-ranked actual PIT strategy.

    STAY OUT is deliberately excluded because Phase 7.4
    answers the question:

        "If we pit, when should we pit and which tyre
         should we use?"
    """

    pit_strategies = []

    for alternative in alternatives:

        strategy = _normalise_text(
            alternative.get("strategy")
        )

        if strategy == "PIT":

            pit_strategies.append(
                alternative
            )


    if not pit_strategies:
        return None


    pit_strategies.sort(

        key=lambda item: (

            item.get(
                "comparison_rank",
                999
            ),

            -_safe_float(
                item.get("dynamic_score"),
                -1_000_000.0
            ),

        )

    )


    return pit_strategies[0]


# ============================================================
# DETERMINE RECOMMENDED TYRE
# ============================================================

def determine_recommended_tyre(
    alternatives_result: Dict[str, Any],
    best_pit_strategy: Optional[Dict[str, Any]]
) -> Optional[str]:
    """
    Determine the tyre that should be used for the optimized
    pit window.
    """

    if best_pit_strategy:

        tyre = _normalise_text(
            best_pit_strategy.get(
                "final_tyre"
            )
        )

        if tyre in SUPPORTED_TYRES:
            return tyre


    ai_tyre = _normalise_text(
        alternatives_result.get(
            "ai_recommended_tyre"
        )
    )

    if ai_tyre in SUPPORTED_TYRES:
        return ai_tyre


    return None


# ============================================================
# DETERMINE TYRE LIFE
# ============================================================

def get_current_tyre_age(
    race_state: Dict[str, Any]
) -> float:

    for key in (
        "TyreAge",
        "TyreLife",
        "tyre_age",
        "tyre_life",
        "current_tyre_age",
    ):

        if key in race_state:

            return _safe_float(
                race_state.get(key),
                0.0
            )


    return 0.0


# ============================================================
# DETERMINE DEGRADATION
# ============================================================

def get_degradation_rate(
    race_state: Dict[str, Any]
) -> float:

    for key in (
        "DegradationRate",
        "degradation_rate",
        "degradation",
    ):

        if key in race_state:

            return max(
                0.0,
                _safe_float(
                    race_state.get(key),
                    0.0
                )
            )


    return 0.0


# ============================================================
# GAP VALUES
# ============================================================

def get_gap_ahead(
    race_state: Dict[str, Any]
) -> Optional[float]:

    for key in (
        "GapAhead",
        "gap_ahead",
        "IntervalToAhead",
        "interval_to_ahead",
    ):

        value = race_state.get(key)

        if value is not None:

            return _safe_float(value)


    return None


def get_gap_behind(
    race_state: Dict[str, Any]
) -> Optional[float]:

    for key in (
        "GapBehind",
        "gap_behind",
        "IntervalToBehind",
        "interval_to_behind",
    ):

        value = race_state.get(key)

        if value is not None:

            return _safe_float(value)


    return None


# ============================================================
# TRACK STATE
# ============================================================

def get_track_status(
    race_state: Dict[str, Any]
) -> str:

    for key in (
        "TrackStatus",
        "track_status",
    ):

        value = race_state.get(key)

        if value is not None:
            return _normalise_text(value)


    return "GREEN"


def get_boolean(
    race_state: Dict[str, Any],
    *keys: str
) -> bool:

    for key in keys:

        if key in race_state:

            return bool(
                race_state.get(key)
            )


    return False


# ============================================================
# PIT URGENCY
# ============================================================

def calculate_pit_urgency(
    tyre_age: float,
    degradation_rate: float,
    pit_decision: str,
    race_situation: str
) -> float:
    """
    Estimate urgency on a 0–100 scale.

    This is not the final strategy score. It is only used
    inside Phase 7.4 to determine how quickly the optimal
    pit window should begin.
    """

    score = 25.0


    # --------------------------------------------------------
    # TYRE AGE
    # --------------------------------------------------------

    score += min(
        tyre_age * 1.6,
        35.0
    )


    # --------------------------------------------------------
    # DEGRADATION
    # --------------------------------------------------------

    score += min(
        degradation_rate * 180.0,
        25.0
    )


    # --------------------------------------------------------
    # EXISTING PIT DECISION
    # --------------------------------------------------------

    decision = _normalise_text(
        pit_decision
    )


    if "PIT NOW" in decision:

        score += 20.0

    elif "PIT" in decision:

        score += 10.0


    # --------------------------------------------------------
    # RACE SITUATION
    # --------------------------------------------------------

    situation = _normalise_text(
        race_situation
    )


    if situation in {
        "SAFETY_CAR",
        "VSC",
        "VIRTUAL_SAFETY_CAR",
    }:

        score += 15.0


    return round(
        max(
            0.0,
            min(
                100.0,
                score
            )
        ),
        2
    )


# ============================================================
# BUILD CANDIDATE PIT LAPS
# ============================================================

def build_candidate_pit_laps(
    current_lap: int,
    total_laps: int,
    urgency: float,
    maximum_window: int = 6
) -> List[int]:
    """
    Build the upcoming laps that should be evaluated.

    Higher urgency produces a shorter and earlier window.
    """

    if current_lap >= total_laps:

        return []


    # --------------------------------------------------------
    # HIGH URGENCY
    # --------------------------------------------------------

    if urgency >= 80:

        offset = 0
        window_size = 3


    # --------------------------------------------------------
    # MEDIUM-HIGH
    # --------------------------------------------------------

    elif urgency >= 60:

        offset = 1
        window_size = 4


    # --------------------------------------------------------
    # MEDIUM
    # --------------------------------------------------------

    elif urgency >= 40:

        offset = 2
        window_size = 5


    # --------------------------------------------------------
    # LOW
    # --------------------------------------------------------

    else:

        offset = 3
        window_size = maximum_window


    first_lap = current_lap + offset

    # Pit cannot happen before current lap.
    first_lap = max(
        current_lap,
        first_lap
    )


    # Do not generate a pit candidate after the final lap.
    last_possible_lap = total_laps - 1


    last_lap = min(
        first_lap + window_size - 1,
        last_possible_lap
    )


    if first_lap > last_lap:
        return []


    return list(
        range(
            first_lap,
            last_lap + 1
        )
    )


# ============================================================
# CALCULATE CANDIDATE SCORE
# ============================================================

def calculate_pit_lap_score(
    pit_lap: int,
    current_lap: int,
    total_laps: int,
    tyre_age: float,
    degradation_rate: float,
    urgency: float,
    gap_ahead: Optional[float],
    gap_behind: Optional[float],
    safety_car: bool,
    virtual_safety_car: bool,
    track_status: str
) -> Dict[str, Any]:
    """
    Score a candidate pit lap.

    The optimizer combines:

    - tyre degradation pressure
    - tyre age
    - urgency
    - remaining-race usefulness
    - traffic/gap context
    - SC/VSC opportunity
    - delay penalty
    """

    laps_until_pit = max(
        0,
        pit_lap - current_lap
    )


    laps_after_pit = max(
        0,
        total_laps - pit_lap
    )


    projected_tyre_age = (
        tyre_age
        +
        laps_until_pit
    )


    # ========================================================
    # TYRE PRESSURE SCORE
    # ========================================================

    tyre_pressure = min(

        100.0,

        (
            projected_tyre_age * 2.0
        )
        +
        (
            degradation_rate * 250.0
        )

    )


    # ========================================================
    # URGENCY SCORE
    # ========================================================

    urgency_score = urgency


    # ========================================================
    # REMAINING RACE VALUE
    # ========================================================

    if total_laps > 0:

        remaining_value = (

            laps_after_pit
            /
            total_laps

        ) * 100.0

    else:

        remaining_value = 0.0


    # ========================================================
    # TRAFFIC SCORE
    # ========================================================

    traffic_score = 50.0


    if gap_behind is not None:

        if gap_behind >= 3.0:

            traffic_score += 12.0

        elif gap_behind >= 1.5:

            traffic_score += 5.0

        elif gap_behind < 1.0:

            traffic_score -= 8.0


    if gap_ahead is not None:

        if gap_ahead <= 1.0:

            traffic_score += 5.0

        elif gap_ahead >= 5.0:

            traffic_score -= 3.0


    traffic_score = max(
        0.0,
        min(
            100.0,
            traffic_score
        )
    )


    # ========================================================
    # SC / VSC OPPORTUNITY
    # ========================================================

    neutralisation_bonus = 0.0


    if safety_car:

        neutralisation_bonus = 30.0


    elif virtual_safety_car:

        neutralisation_bonus = 22.0


    elif track_status in {

        "SAFETY CAR",
        "SAFETY_CAR",
        "SC",

    }:

        neutralisation_bonus = 30.0


    elif track_status in {

        "VSC",
        "VIRTUAL SAFETY CAR",
        "VIRTUAL_SAFETY_CAR",

    }:

        neutralisation_bonus = 22.0


    # Neutralisation is most valuable immediately.
    if (
        neutralisation_bonus > 0
        and laps_until_pit > 0
    ):

        neutralisation_bonus = max(

            0.0,

            neutralisation_bonus
            -
            (
                laps_until_pit * 10.0
            )

        )


    # ========================================================
    # DELAY PENALTY
    # ========================================================

    delay_penalty = (

        laps_until_pit
        *
        (
            4.0
            +
            degradation_rate * 30.0
        )

    )


    # High urgency makes delaying more expensive.
    delay_penalty += (

        laps_until_pit
        *
        (
            urgency / 100.0
        )
        *
        4.0

    )


    # ========================================================
    # FINAL SCORE
    # ========================================================

    score = (

        tyre_pressure * 0.28

        +

        urgency_score * 0.27

        +

        remaining_value * 0.15

        +

        traffic_score * 0.10

        +

        neutralisation_bonus

        -

        delay_penalty

    )


    score = round(
        score,
        2
    )


    return {

        "pit_lap":
            pit_lap,

        "laps_until_pit":
            laps_until_pit,

        "laps_after_pit":
            laps_after_pit,

        "projected_tyre_age":
            round(
                projected_tyre_age,
                2
            ),

        "tyre_pressure_score":
            round(
                tyre_pressure,
                2
            ),

        "urgency_score":
            round(
                urgency_score,
                2
            ),

        "remaining_race_score":
            round(
                remaining_value,
                2
            ),

        "traffic_score":
            round(
                traffic_score,
                2
            ),

        "neutralisation_bonus":
            round(
                neutralisation_bonus,
                2
            ),

        "delay_penalty":
            round(
                delay_penalty,
                2
            ),

        "pit_window_score":
            score,

    }


# ============================================================
# RANK CANDIDATES
# ============================================================

def rank_pit_candidates(
    candidates: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    ordered = sorted(

        candidates,

        key=lambda candidate: (

            -candidate[
                "pit_window_score"
            ],

            candidate[
                "pit_lap"
            ],

        )

    )


    for rank, candidate in enumerate(
        ordered,
        start=1
    ):

        candidate[
            "rank"
        ] = rank


    return ordered


# ============================================================
# CALCULATE CONFIDENCE
# ============================================================

def calculate_window_confidence(
    ranked_candidates: List[Dict[str, Any]]
) -> float:
    """
    Estimate confidence from the separation between the best
    and second-best pit laps.

    This is an optimizer confidence, not model probability.
    """

    if not ranked_candidates:

        return 0.0


    if len(ranked_candidates) == 1:

        return 90.0


    best_score = ranked_candidates[
        0
    ][
        "pit_window_score"
    ]


    second_score = ranked_candidates[
        1
    ][
        "pit_window_score"
    ]


    separation = max(
        0.0,
        best_score - second_score
    )


    confidence = (

        70.0
        +
        min(
            separation * 3.0,
            25.0
        )

    )


    return round(
        min(
            95.0,
            confidence
        ),
        1
    )


# ============================================================
# BUILD OPTIMAL WINDOW
# ============================================================

def build_optimal_window(
    ranked_candidates: List[Dict[str, Any]],
    recommended_lap: int
) -> Dict[str, Any]:
    """
    Build a practical pit window around the recommended lap.

    Candidate laps whose score remains reasonably close to
    the best candidate are treated as viable.
    """

    if not ranked_candidates:

        return {
            "start_lap": None,
            "recommended_lap": None,
            "end_lap": None,
            "laps": [],
        }


    best_score = ranked_candidates[
        0
    ][
        "pit_window_score"
    ]


    threshold = best_score - 8.0


    viable_laps = sorted([

        candidate[
            "pit_lap"
        ]

        for candidate
        in ranked_candidates

        if candidate[
            "pit_window_score"
        ] >= threshold

    ])


    if not viable_laps:

        viable_laps = [
            recommended_lap
        ]


    # Keep the final window compact.
    nearby_laps = [

        lap

        for lap in viable_laps

        if abs(
            lap - recommended_lap
        ) <= 2

    ]


    if nearby_laps:

        viable_laps = nearby_laps


    return {

        "start_lap":
            min(
                viable_laps
            ),

        "recommended_lap":
            recommended_lap,

        "end_lap":
            max(
                viable_laps
            ),

        "laps":
            viable_laps,

    }


# ============================================================
# BUILD REASON
# ============================================================

def build_optimizer_reason(
    recommended_lap: int,
    current_lap: int,
    tyre_age: float,
    degradation_rate: float,
    urgency: float,
    recommended_tyre: Optional[str],
    safety_car: bool,
    virtual_safety_car: bool
) -> str:

    parts = []


    if recommended_lap == current_lap:

        parts.append(
            "The optimizer recommends pitting immediately"
        )

    else:

        parts.append(
            f"The optimizer recommends targeting lap "
            f"{recommended_lap}"
        )


    parts.append(
        f"with the current tyre age at "
        f"{tyre_age:.1f} laps"
    )


    parts.append(
        f"and degradation at "
        f"{degradation_rate:.3f} s/lap"
    )


    if urgency >= 80:

        parts.append(
            "The pit-stop urgency is very high"
        )

    elif urgency >= 60:

        parts.append(
            "The pit-stop urgency is high"
        )

    elif urgency >= 40:

        parts.append(
            "The pit-stop urgency is moderate"
        )

    else:

        parts.append(
            "The pit-stop urgency is currently low"
        )


    if safety_car:

        parts.append(
            "A Safety Car creates an immediate reduced-cost "
            "pit opportunity"
        )

    elif virtual_safety_car:

        parts.append(
            "A Virtual Safety Car improves the value of an "
            "immediate pit stop"
        )


    if recommended_tyre:

        parts.append(
            f"The strongest available pit alternative uses "
            f"the {recommended_tyre} compound"
        )


    return ". ".join(
        parts
    ) + "."


# ============================================================
# BUILD PIT WINDOW FROM 7.3 RESULT
# ============================================================

def build_pit_window(
    alternatives_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build Phase 7.4 output from an existing Phase 7.3 result.
    """

    if not isinstance(
        alternatives_result,
        dict
    ):

        raise TypeError(
            "alternatives_result must be a dictionary."
        )


    if alternatives_result.get(
        "phase"
    ) != "7.3":

        raise ValueError(
            "Phase 7.4 requires a Phase 7.3 alternatives result."
        )


    alternatives = alternatives_result.get(
        "alternatives",
        []
    )


    if not alternatives:

        raise RuntimeError(
            "Phase 7.3 returned no strategy alternatives."
        )


    # ========================================================
    # RACE INFORMATION
    # ========================================================

    current_lap = _safe_int(
        alternatives_result.get(
            "current_lap"
        )
    )


    total_laps = _safe_int(
        alternatives_result.get(
            "total_laps"
        )
    )


    if current_lap <= 0:

        raise ValueError(
            "Current lap must be greater than zero."
        )


    if total_laps <= 0:

        raise ValueError(
            "Total laps must be greater than zero."
        )


    if current_lap > total_laps:

        raise ValueError(
            "Current lap cannot exceed total laps."
        )


    # ========================================================
    # RACE STATE
    # ========================================================

    race_state = extract_race_state(
        alternatives_result
    )


    tyre_age = get_current_tyre_age(
        race_state
    )


    degradation_rate = get_degradation_rate(
        race_state
    )


    gap_ahead = get_gap_ahead(
        race_state
    )


    gap_behind = get_gap_behind(
        race_state
    )


    track_status = get_track_status(
        race_state
    )


    safety_car = get_boolean(
        race_state,
        "SafetyCar",
        "safety_car"
    )


    virtual_safety_car = get_boolean(
        race_state,
        "VirtualSafetyCar",
        "virtual_safety_car",
        "vsc"
    )


    # ========================================================
    # BEST PIT ALTERNATIVE
    # ========================================================

    best_pit_strategy = select_best_pit_strategy(
        alternatives
    )


    recommended_tyre = determine_recommended_tyre(

        alternatives_result=
            alternatives_result,

        best_pit_strategy=
            best_pit_strategy

    )


    # ========================================================
    # URGENCY
    # ========================================================

    urgency = calculate_pit_urgency(

        tyre_age=
            tyre_age,

        degradation_rate=
            degradation_rate,

        pit_decision=
            alternatives_result.get(
                "pit_decision",
                ""
            ),

        race_situation=
            alternatives_result.get(
                "race_situation",
                ""
            )

    )


    # ========================================================
    # CANDIDATE LAPS
    # ========================================================

    candidate_laps = build_candidate_pit_laps(

        current_lap=
            current_lap,

        total_laps=
            total_laps,

        urgency=
            urgency

    )


    if not candidate_laps:

        raise RuntimeError(
            "No valid future pit laps are available."
        )


    candidates = [

        calculate_pit_lap_score(

            pit_lap=
                pit_lap,

            current_lap=
                current_lap,

            total_laps=
                total_laps,

            tyre_age=
                tyre_age,

            degradation_rate=
                degradation_rate,

            urgency=
                urgency,

            gap_ahead=
                gap_ahead,

            gap_behind=
                gap_behind,

            safety_car=
                safety_car,

            virtual_safety_car=
                virtual_safety_car,

            track_status=
                track_status

        )

        for pit_lap
        in candidate_laps

    ]


    # ========================================================
    # RANK
    # ========================================================

    ranked_candidates = rank_pit_candidates(
        candidates
    )


    best_candidate = ranked_candidates[
        0
    ]


    recommended_lap = best_candidate[
        "pit_lap"
    ]


    # ========================================================
    # WINDOW
    # ========================================================

    pit_window = build_optimal_window(

        ranked_candidates=
            ranked_candidates,

        recommended_lap=
            recommended_lap

    )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = calculate_window_confidence(
        ranked_candidates
    )


    # ========================================================
    # REASONING
    # ========================================================

    reason = build_optimizer_reason(

        recommended_lap=
            recommended_lap,

        current_lap=
            current_lap,

        tyre_age=
            tyre_age,

        degradation_rate=
            degradation_rate,

        urgency=
            urgency,

        recommended_tyre=
            recommended_tyre,

        safety_car=
            safety_car,

        virtual_safety_car=
            virtual_safety_car

    )


    # ========================================================
    # RETURN
    # ========================================================

    return {

        "engine":
            COMPONENT,

        "phase":
            PHASE,

        "status":
            "SUCCESS",

        "driver":
            alternatives_result.get(
                "driver"
            ),

        "circuit":
            alternatives_result.get(
                "circuit"
            ),

        "current_lap":
            current_lap,

        "total_laps":
            total_laps,

        "position":
            alternatives_result.get(
                "position"
            ),

        "current_tyre":
            alternatives_result.get(
                "current_tyre"
            ),

        "tyre_age":
            tyre_age,

        "degradation_rate":
            degradation_rate,

        "race_situation":
            alternatives_result.get(
                "race_situation"
            ),

        "pit_decision":
            alternatives_result.get(
                "pit_decision"
            ),

        "ai_recommendation":
            alternatives_result.get(
                "ai_recommendation"
            ),

        "recommended_tyre":
            recommended_tyre,

        "best_pit_strategy":
            best_pit_strategy,

        "pit_urgency":
            urgency,

        "recommended_pit_lap":
            recommended_lap,

        "pit_window":
            pit_window,

        "window_start":
            pit_window[
                "start_lap"
            ],

        "window_end":
            pit_window[
                "end_lap"
            ],

        "window_confidence":
            confidence,

        "candidate_count":
            len(
                ranked_candidates
            ),

        "candidate_laps":
            ranked_candidates,

        "reasoning":
            reason,

        "phase_7_3_result":
            alternatives_result,

    }


# ============================================================
# COMPLETE PHASE 7.4 SERVICE
# ============================================================

def run_pit_window_optimizer(
    race_input: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute:

        7.1
         ↓
        7.2
         ↓
        7.3
         ↓
        7.4
    """

    alternatives_result = (
        run_strategy_alternatives_engine(
            race_input
        )
    )


    return build_pit_window(
        alternatives_result
    )


# ============================================================
# DISPLAY
# ============================================================

def display_pit_window(
    result: Dict[str, Any]
) -> None:

    print(
        "\n" + "=" * 88
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 7.4 — PIT WINDOW OPTIMIZER"
    )

    print(
        "=" * 88
    )


    print(
        f"Driver:               "
        f"{result.get('driver', '--')}"
    )


    print(
        f"Circuit:              "
        f"{result.get('circuit', '--')}"
    )


    print(
        f"Current Lap:          "
        f"{result.get('current_lap', '--')}"
        f"/"
        f"{result.get('total_laps', '--')}"
    )


    position = result.get(
        "position"
    )

    if position is not None:

        print(
            f"Position:             "
            f"P{position}"
        )


    print(
        f"Current Tyre:         "
        f"{result.get('current_tyre', '--')}"
    )


    print(
        f"Tyre Age:             "
        f"{result.get('tyre_age', '--')}"
    )


    print(
        f"Degradation Rate:     "
        f"{result.get('degradation_rate', '--')}"
    )


    print(
        "-" * 88
    )


    print(
        f"Pit Decision:         "
        f"{result.get('pit_decision', '--')}"
    )


    print(
        f"AI Recommendation:    "
        f"{result.get('ai_recommendation', '--')}"
    )


    print(
        f"Recommended Tyre:     "
        f"{result.get('recommended_tyre', '--')}"
    )


    print(
        f"Pit Urgency:          "
        f"{result.get('pit_urgency', '--')}/100"
    )


    print(
        "-" * 88
    )


    print(
        f"RECOMMENDED PIT LAP:  "
        f"{result.get('recommended_pit_lap', '--')}"
    )


    print(
        f"OPTIMAL PIT WINDOW:   "
        f"Lap {result.get('window_start', '--')}"
        f" – "
        f"{result.get('window_end', '--')}"
    )


    print(
        f"Window Confidence:    "
        f"{result.get('window_confidence', '--')}%"
    )


    print(
        "-" * 88
    )


    print(
        f"{'RANK':<8}"
        f"{'PIT LAP':<12}"
        f"{'IN':<10}"
        f"{'TYRE AGE':<14}"
        f"{'SCORE':<12}"
        f"{'DELAY':<12}"
    )


    print(
        "-" * 88
    )


    for candidate in result.get(
        "candidate_laps",
        []
    ):

        print(

            f"{candidate.get('rank', '--'):<8}"
            f"{candidate.get('pit_lap', '--'):<12}"
            f"{candidate.get('laps_until_pit', '--'):<10}"
            f"{candidate.get('projected_tyre_age', '--'):<14}"
            f"{candidate.get('pit_window_score', '--'):<12}"
            f"{candidate.get('delay_penalty', '--'):<12}"

        )


    print(
        "-" * 88
    )


    print(
        "OPTIMIZER REASONING"
    )


    print(
        "-" * 88
    )


    print(
        result.get(
            "reasoning",
            "--"
        )
    )


    print(
        "=" * 88
    )