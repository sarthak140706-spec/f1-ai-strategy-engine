from data.strategy_params import (
    DEFAULT_TYRE_DEGRADATION
)


# ============================================================
# GET TYRE DEGRADATION RATE
# ============================================================

def get_degradation_rate(
    tyre_compound: str
) -> float:
    """
    Return the fallback tyre degradation rate.

    Parameters
    ----------
    tyre_compound : str
        Tyre compound name.

    Returns
    -------
    float
        Degradation rate in seconds per lap.
    """

    if tyre_compound is None:

        raise ValueError(
            "tyre_compound cannot be None."
        )

    compound = (
        str(tyre_compound)
        .strip()
        .upper()
    )

    # --------------------------------------------------------
    # NORMALIZE COMPOUND NAMES
    # --------------------------------------------------------

    compound_aliases = {

        "S": "SOFT",

        "SOFT": "SOFT",

        "M": "MEDIUM",

        "MEDIUM": "MEDIUM",

        "H": "HARD",

        "HARD": "HARD",

        "I": "INTERMEDIATE",

        "INTERMEDIATE": "INTERMEDIATE",

        "W": "WET",

        "WET": "WET"

    }

    normalized_compound = (
        compound_aliases.get(
            compound,
            compound
        )
    )

    # --------------------------------------------------------
    # GET DEGRADATION
    # --------------------------------------------------------

    degradation = (
        DEFAULT_TYRE_DEGRADATION.get(
            normalized_compound
        )
    )

    # --------------------------------------------------------
    # UNKNOWN COMPOUND
    # --------------------------------------------------------

    if degradation is None:

        degradation = 0.0

    return float(
        degradation
    )