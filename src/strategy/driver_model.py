from data.strategy_params import (
    DEFAULT_DRIVER_FACTOR
)


# ============================================================
# GET DRIVER PERFORMANCE FACTOR
# ============================================================

def get_driver_factor(
    driver: str
) -> float:
    """
    Return the driver performance factor.

    Parameters
    ----------
    driver : str
        Driver abbreviation or driver identifier.

    Returns
    -------
    float
        Driver performance factor.

    Notes
    -----
    V5 Sprint 1 uses a neutral fallback factor
    for all drivers.

    Future versions can replace this with
    driver-specific performance estimates
    derived from historical FastF1 data.
    """

    if driver is None:

        raise ValueError(
            "driver cannot be None."
        )

    return float(
        DEFAULT_DRIVER_FACTOR
    )