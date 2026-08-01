"""
V5 SPRINT 6 - STEP 4
DRIVER STRATEGY COMPARISON & STRATEGIC OPPORTUNITIES

This module compares strategy recommendations across the full grid
and identifies strategic opportunities such as:

- Drivers with high pit probability
- Drivers with low pit probability
- Potential undercut opportunities
- Potential overcut opportunities
- Drivers with strategic conflicts
- Drivers with high-confidence decisions
- Drivers with low-confidence decisions

The module is designed to work with the full-grid analysis output
generated in Sprint 6 Step 3.
"""

from typing import Dict, List, Any, Optional


# ============================================================
# CONSTANTS
# ============================================================

PIT_NOW = "PIT NOW"
STAY_OUT = "STAY OUT"
DATA_UNAVAILABLE = "DATA UNAVAILABLE"

HIGH = "HIGH"
MEDIUM = "MEDIUM"
LOW = "LOW"


# ============================================================
# SAFE FLOAT CONVERSION
# ============================================================

def _safe_float(
    value: Any
) -> Optional[float]:
    """
    Safely convert a value to float.

    Returns
    -------
    float or None
        Converted value if valid.
        Otherwise None.
    """

    if value is None:
        return None

    try:

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return None


# ============================================================
# NORMALIZE DRIVER RESULT
# ============================================================

def normalize_driver_result(
    result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Normalize a single driver's strategy result.

    Parameters
    ----------
    result : dict
        Full-grid strategy result for one driver.

    Returns
    -------
    dict
        Normalized driver strategy information.
    """

    if not isinstance(
        result,
        dict
    ):

        raise TypeError(
            "Driver result must be a dictionary."
        )

    driver = result.get(
        "driver"
    )

    position = result.get(
        "position"
    )

    tyre = result.get(
        "tyre_compound"
    )

    tyre_age = result.get(
        "tyre_life"
    )

    pit_probability = _safe_float(
        result.get(
            "pit_probability"
        )
    )

    simulator_recommendation = result.get(
        "simulator_recommendation"
    )

    final_decision = result.get(
        "final_decision"
    )

    confidence = result.get(
        "confidence"
    )

    return {

        "driver":
            driver,

        "position":
            position,

        "tyre_compound":
            tyre,

        "tyre_life":
            tyre_age,

        "pit_probability":
            pit_probability,

        "simulator_recommendation":
            simulator_recommendation,

        "final_decision":
            final_decision,

        "confidence":
            confidence

    }


# ============================================================
# CLASSIFY STRATEGY GROUP
# ============================================================

def classify_strategy_group(
    result: Dict[str, Any]
) -> str:
    """
    Classify a driver into a strategic group.

    Groups:

    PIT
    STAY_OUT
    DATA_UNAVAILABLE
    OTHER
    """

    if not isinstance(
        result,
        dict
    ):

        return DATA_UNAVAILABLE

    final_decision = result.get(
        "final_decision"
    )

    if final_decision == PIT_NOW:

        return PIT_NOW

    if final_decision == STAY_OUT:

        return STAY_OUT

    if final_decision == DATA_UNAVAILABLE:

        return DATA_UNAVAILABLE

    return "OTHER"


# ============================================================
# GET STRATEGY GROUPS
# ============================================================

def get_strategy_groups(
    driver_results: List[Dict[str, Any]]
) -> Dict[str, List[str]]:
    """
    Group drivers according to their final strategy decisions.

    Parameters
    ----------
    driver_results : list of dict
        Full-grid strategy results.

    Returns
    -------
    dict
        Strategic driver groups.
    """

    if not isinstance(
        driver_results,
        list
    ):

        raise TypeError(
            "driver_results must be a list."
        )

    pit_drivers = []

    stay_out_drivers = []

    unavailable_drivers = []

    other_drivers = []

    for result in driver_results:

        normalized = normalize_driver_result(
            result
        )

        driver = normalized.get(
            "driver"
        )

        group = classify_strategy_group(
            normalized
        )

        if not driver:

            continue

        if group == PIT_NOW:

            pit_drivers.append(
                driver
            )

        elif group == STAY_OUT:

            stay_out_drivers.append(
                driver
            )

        elif group == DATA_UNAVAILABLE:

            unavailable_drivers.append(
                driver
            )

        else:

            other_drivers.append(
                driver
            )

    return {

        "pit_drivers":
            pit_drivers,

        "stay_out_drivers":
            stay_out_drivers,

        "data_unavailable_drivers":
            unavailable_drivers,

        "other_drivers":
            other_drivers

    }


# ============================================================
# HIGH-CONFIDENCE DECISIONS
# ============================================================

def get_high_confidence_drivers(
    driver_results: List[Dict[str, Any]]
) -> List[str]:
    """
    Return drivers with HIGH confidence decisions.
    """

    high_confidence = []

    for result in driver_results:

        normalized = normalize_driver_result(
            result
        )

        driver = normalized.get(
            "driver"
        )

        confidence = normalized.get(
            "confidence"
        )

        final_decision = normalized.get(
            "final_decision"
        )

        if (

            driver

            and

            confidence == HIGH

            and

            final_decision
            in {
                PIT_NOW,
                STAY_OUT
            }

        ):

            high_confidence.append(
                driver
            )

    return high_confidence


# ============================================================
# LOW-CONFIDENCE DECISIONS
# ============================================================

def get_low_confidence_drivers(
    driver_results: List[Dict[str, Any]]
) -> List[str]:
    """
    Return drivers with LOW confidence decisions.
    """

    low_confidence = []

    for result in driver_results:

        normalized = normalize_driver_result(
            result
        )

        driver = normalized.get(
            "driver"
        )

        confidence = normalized.get(
            "confidence"
        )

        if (

            driver

            and

            confidence == LOW

        ):

            low_confidence.append(
                driver
            )

    return low_confidence


# ============================================================
# PIT PROBABILITY RANKING
# ============================================================

def rank_by_pit_probability(
    driver_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Rank successfully analyzed drivers by pit probability.

    Drivers without valid pit probability are excluded.
    """

    ranked = []

    for result in driver_results:

        normalized = normalize_driver_result(
            result
        )

        probability = normalized.get(
            "pit_probability"
        )

        if probability is None:

            continue

        if normalized.get(
            "final_decision"
        ) == DATA_UNAVAILABLE:

            continue

        ranked.append(
            normalized
        )

    ranked.sort(

        key=lambda item:
            item[
                "pit_probability"
            ],

        reverse=True

    )

    return ranked


# ============================================================
# IDENTIFY PIT OPPORTUNITIES
# ============================================================

def identify_pit_opportunities(
    driver_results: List[Dict[str, Any]],
    threshold: float = 0.20
) -> List[Dict[str, Any]]:
    """
    Identify drivers with elevated pit probability.

    Parameters
    ----------
    driver_results : list of dict
        Full-grid strategy results.

    threshold : float
        Pit probability threshold.

    Returns
    -------
    list of dict
        Drivers above the threshold.
    """

    if threshold < 0:

        raise ValueError(
            "threshold cannot be negative."
        )

    opportunities = []

    ranked = rank_by_pit_probability(
        driver_results
    )

    for result in ranked:

        probability = result[
            "pit_probability"
        ]

        if probability >= threshold:

            opportunities.append(
                {

                    "driver":
                        result[
                            "driver"
                        ],

                    "position":
                        result[
                            "position"
                        ],

                    "pit_probability":
                        probability,

                    "tyre_compound":
                        result[
                            "tyre_compound"
                        ],

                    "tyre_life":
                        result[
                            "tyre_life"
                        ],

                    "confidence":
                        result[
                            "confidence"
                        ]

                }
            )

    return opportunities


# ============================================================
# IDENTIFY STRATEGIC CONFLICTS
# ============================================================

def identify_strategy_conflicts(
    driver_results: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Identify drivers where ML prediction and simulator
    recommendation disagree.

    These drivers may require additional strategic analysis.
    """

    conflicts = []

    for result in driver_results:

        normalized = normalize_driver_result(
            result
        )

        driver = normalized.get(
            "driver"
        )

        ml_recommendation = result.get(
            "ml_recommendation"
        )

        simulator_recommendation = normalized.get(
            "simulator_recommendation"
        )

        final_decision = normalized.get(
            "final_decision"
        )

        if not driver:

            continue

        if final_decision == DATA_UNAVAILABLE:

            continue

        if (

            ml_recommendation
            and

            simulator_recommendation

            and

            ml_recommendation
            != simulator_recommendation

        ):

            conflicts.append(
                {

                    "driver":
                        driver,

                    "ml_recommendation":
                        ml_recommendation,

                    "simulator_recommendation":
                        simulator_recommendation,

                    "final_decision":
                        final_decision,

                    "confidence":
                        normalized[
                            "confidence"
                        ]

                }
            )

    return conflicts


# ============================================================
# IDENTIFY UNDERCUT / OVERCUT OPPORTUNITIES
# ============================================================

def identify_undercut_overcut_opportunities(
    driver_results: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Analyze strategy outputs for undercut and overcut
    opportunities.

    This function uses the optional 'undercut_overcut'
    field generated by the Sprint 5 decision engine.

    Drivers without this information are safely ignored.
    """

    undercut_opportunities = []

    overcut_opportunities = []

    for result in driver_results:

        normalized = normalize_driver_result(
            result
        )

        driver = normalized.get(
            "driver"
        )

        if not driver:

            continue

        if normalized.get(
            "final_decision"
        ) == DATA_UNAVAILABLE:

            continue

        strategy_data = result.get(
            "undercut_overcut"
        )

        if not isinstance(
            strategy_data,
            dict
        ):

            continue

        undercut_score = _safe_float(
            strategy_data.get(
                "UndercutScore"
            )
        )

        overcut_score = _safe_float(
            strategy_data.get(
                "OvercutScore"
            )
        )

        if undercut_score is not None:

            undercut_opportunities.append(
                {

                    "driver":
                        driver,

                    "position":
                        normalized[
                            "position"
                        ],

                    "score":
                        undercut_score,

                    "tyre_compound":
                        normalized[
                            "tyre_compound"
                        ],

                    "tyre_life":
                        normalized[
                            "tyre_life"
                        ]

                }
            )

        if overcut_score is not None:

            overcut_opportunities.append(
                {

                    "driver":
                        driver,

                    "position":
                        normalized[
                            "position"
                        ],

                    "score":
                        overcut_score,

                    "tyre_compound":
                        normalized[
                            "tyre_compound"
                        ],

                    "tyre_life":
                        normalized[
                            "tyre_life"
                        ]

                }
            )

    undercut_opportunities.sort(

        key=lambda item:
            item[
                "score"
            ],

        reverse=True

    )

    overcut_opportunities.sort(

        key=lambda item:
            item[
                "score"
            ],

        reverse=True

    )

    return {

        "undercut_opportunities":
            undercut_opportunities,

        "overcut_opportunities":
            overcut_opportunities

    }


# ============================================================
# BUILD GRID STRATEGY COMPARISON
# ============================================================

def build_grid_strategy_comparison(
    driver_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Build a complete strategic comparison across the grid.

    Parameters
    ----------
    driver_results : list of dict
        Full-grid strategy results.

    Returns
    -------
    dict
        Complete grid-level strategic analysis.
    """

    if not isinstance(
        driver_results,
        list
    ):

        raise TypeError(
            "driver_results must be a list."
        )

    normalized_results = []

    for result in driver_results:

        try:

            normalized_results.append(
                normalize_driver_result(
                    result
                )
            )

        except Exception:

            continue

    strategy_groups = get_strategy_groups(
        driver_results
    )

    high_confidence = get_high_confidence_drivers(
        driver_results
    )

    low_confidence = get_low_confidence_drivers(
        driver_results
    )

    ranked_drivers = rank_by_pit_probability(
        driver_results
    )

    pit_opportunities = identify_pit_opportunities(
        driver_results
    )

    conflicts = identify_strategy_conflicts(
        driver_results
    )

    undercut_overcut = (
        identify_undercut_overcut_opportunities(
            driver_results
        )
    )

    return {

        "total_drivers":
            len(
                driver_results
            ),

        "successful_drivers":
            len(
                [
                    result

                    for result
                    in normalized_results

                    if result.get(
                        "final_decision"
                    )
                    in {
                        PIT_NOW,
                        STAY_OUT
                    }
                ]
            ),

        "data_unavailable_drivers":
            len(
                strategy_groups[
                    "data_unavailable_drivers"
                ]
            ),

        "strategy_groups":
            strategy_groups,

        "high_confidence_drivers":
            high_confidence,

        "low_confidence_drivers":
            low_confidence,

        "pit_probability_ranking":
            ranked_drivers,

        "pit_opportunities":
            pit_opportunities,

        "strategy_conflicts":
            conflicts,

        "undercut_opportunities":
            undercut_overcut[
                "undercut_opportunities"
            ],

        "overcut_opportunities":
            undercut_overcut[
                "overcut_opportunities"
            ],

        "driver_results":
            normalized_results

    }


# ============================================================
# PRINT GRID STRATEGY COMPARISON
# ============================================================

def print_grid_strategy_comparison(
    comparison: Dict[str, Any]
) -> None:
    """
    Print a readable grid-level strategy comparison.
    """

    if not isinstance(
        comparison,
        dict
    ):

        raise TypeError(
            "comparison must be a dictionary."
        )

    print(
        "\n"
        + "=" * 100
    )

    print(
        "GRID STRATEGY COMPARISON & STRATEGIC OPPORTUNITIES"
    )

    print(
        "=" * 100
    )

    print(
        f"Total Drivers: "
        f"{comparison.get('total_drivers', 0)}"
    )

    print(
        f"Successful Analyses: "
        f"{comparison.get('successful_drivers', 0)}"
    )

    print(
        f"Data Unavailable: "
        f"{comparison.get('data_unavailable_drivers', 0)}"
    )

    # --------------------------------------------------------
    # STRATEGY GROUPS
    # --------------------------------------------------------

    groups = comparison.get(
        "strategy_groups",
        {}
    )

    print(
        "\n"
        + "-" * 100
    )

    print(
        "STRATEGY GROUPS"
    )

    print(
        "-" * 100
    )

    print(
        "PIT NOW:"
    )

    print(

        ", ".join(
            groups.get(
                "pit_drivers",
                []
            )
        )

        or

        "None"

    )

    print(
        "\nSTAY OUT:"
    )

    print(

        ", ".join(
            groups.get(
                "stay_out_drivers",
                []
            )
        )

        or

        "None"

    )

    print(
        "\nDATA UNAVAILABLE:"
    )

    print(

        ", ".join(
            groups.get(
                "data_unavailable_drivers",
                []
            )
        )

        or

        "None"

    )

    # --------------------------------------------------------
    # HIGH CONFIDENCE
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 100
    )

    print(
        "HIGH-CONFIDENCE DECISIONS"
    )

    print(
        "-" * 100
    )

    print(

        ", ".join(
            comparison.get(
                "high_confidence_drivers",
                []
            )
        )

        or

        "None"

    )

    # --------------------------------------------------------
    # LOW CONFIDENCE
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 100
    )

    print(
        "LOW-CONFIDENCE DECISIONS"
    )

    print(
        "-" * 100
    )

    print(

        ", ".join(
            comparison.get(
                "low_confidence_drivers",
                []
            )
        )

        or

        "None"

    )

    # --------------------------------------------------------
    # PIT OPPORTUNITIES
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 100
    )

    print(
        "PIT OPPORTUNITIES"
    )

    print(
        "-" * 100
    )

    pit_opportunities = comparison.get(
        "pit_opportunities",
        []
    )

    if not pit_opportunities:

        print(
            "No elevated pit-probability opportunities detected."
        )

    else:

        for opportunity in pit_opportunities:

            print(

                f"{opportunity['driver']} | "

                f"Pit Probability: "
                f"{opportunity['pit_probability']:.4f}% | "

                f"Tyre: "
                f"{opportunity['tyre_compound']} | "

                f"Tyre Age: "
                f"{opportunity['tyre_life']}"

            )

    # --------------------------------------------------------
    # STRATEGY CONFLICTS
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 100
    )

    print(
        "ML / SIMULATOR STRATEGY CONFLICTS"
    )

    print(
        "-" * 100
    )

    conflicts = comparison.get(
        "strategy_conflicts",
        []
    )

    if not conflicts:

        print(
            "No strategy conflicts detected."
        )

    else:

        for conflict in conflicts:

            print(

                f"{conflict['driver']} | "

                f"ML: "
                f"{conflict['ml_recommendation']} | "

                f"Simulator: "
                f"{conflict['simulator_recommendation']} | "

                f"Final: "
                f"{conflict['final_decision']} | "

                f"Confidence: "
                f"{conflict['confidence']}"

            )

    # --------------------------------------------------------
    # UNDERCUT OPPORTUNITIES
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 100
    )

    print(
        "UNDERCUT OPPORTUNITIES"
    )

    print(
        "-" * 100
    )

    undercuts = comparison.get(
        "undercut_opportunities",
        []
    )

    if not undercuts:

        print(
            "No undercut opportunity data available."
        )

    else:

        for item in undercuts:

            print(

                f"{item['driver']} | "

                f"Score: "
                f"{item['score']}"

            )

    # --------------------------------------------------------
    # OVERCUT OPPORTUNITIES
    # --------------------------------------------------------

    print(
        "\n"
        + "-" * 100
    )

    print(
        "OVERCUT OPPORTUNITIES"
    )

    print(
        "-" * 100
    )

    overcuts = comparison.get(
        "overcut_opportunities",
        []
    )

    if not overcuts:

        print(
            "No overcut opportunity data available."
        )

    else:

        for item in overcuts:

            print(

                f"{item['driver']} | "

                f"Score: "
                f"{item['score']}"

            )

    print(
        "\n"
        + "=" * 100
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 100
    )

    print(
        "V5 SPRINT 6 - STEP 4"
    )

    print(
        "DRIVER STRATEGY COMPARISON & STRATEGIC OPPORTUNITIES"
    )

    print(
        "=" * 100
    )

    # --------------------------------------------------------
    # SAMPLE DATA
    # --------------------------------------------------------

    sample_results = [

        {

            "driver":
                "VER",

            "position":
                1,

            "tyre_compound":
                "MEDIUM",

            "tyre_life":
                10,

            "pit_probability":
                0.35,

            "ml_recommendation":
                "PIT NOW",

            "simulator_recommendation":
                "PIT NOW",

            "final_decision":
                "PIT NOW",

            "confidence":
                "HIGH"

        },

        {

            "driver":
                "NOR",

            "position":
                2,

            "tyre_compound":
                "MEDIUM",

            "tyre_life":
                8,

            "pit_probability":
                0.12,

            "ml_recommendation":
                "STAY OUT",

            "simulator_recommendation":
                "STAY OUT",

            "final_decision":
                "STAY OUT",

            "confidence":
                "HIGH"

        },

        {

            "driver":
                "LEC",

            "position":
                3,

            "tyre_compound":
                "SOFT",

            "tyre_life":
                14,

            "pit_probability":
                0.28,

            "ml_recommendation":
                "PIT NOW",

            "simulator_recommendation":
                "STAY OUT",

            "final_decision":
                "STAY OUT",

            "confidence":
                "LOW"

        },

        {

            "driver":
                "ANT",

            "position":
                16,

            "tyre_compound":
                "INTERMEDIATE",

            "tyre_life":
                3,

            "pit_probability":
                None,

            "ml_recommendation":
                None,

            "simulator_recommendation":
                DATA_UNAVAILABLE,

            "final_decision":
                DATA_UNAVAILABLE,

            "confidence":
                None

        }

    ]

    comparison = build_grid_strategy_comparison(
        sample_results
    )

    print_grid_strategy_comparison(
        comparison
    )

    print(
        "\n"
        "STEP 6.4 TEST COMPLETED"
    )