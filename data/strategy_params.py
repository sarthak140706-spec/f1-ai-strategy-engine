# data/strategy_params.py

"""
Fallback strategy parameters.

These values are used only when dynamic race data is unavailable.
V5 will gradually replace these static defaults with
data-driven estimates derived from FastF1 and race simulations.
"""

# --------------------------------------------------
# DEFAULT PIT LOSS
# --------------------------------------------------

DEFAULT_PIT_LOSS = 22.0


# --------------------------------------------------
# DEFAULT TYRE DEGRADATION
# --------------------------------------------------

DEFAULT_TYRE_DEGRADATION = {
    "SOFT": 0.10,
    "MEDIUM": 0.06,
    "HARD": 0.03,
    "INTERMEDIATE": 0.08,
    "WET": 0.12
}


# --------------------------------------------------
# DEFAULT FRESH TYRE ADVANTAGE
# --------------------------------------------------

DEFAULT_FRESH_TYRE_BONUS = {
    "SOFT": 1.2,
    "MEDIUM": 0.9,
    "HARD": 0.6,
    "INTERMEDIATE": 1.0,
    "WET": 1.0
}


# --------------------------------------------------
# DEFAULT DRIVER PERFORMANCE FACTOR
# --------------------------------------------------

DEFAULT_DRIVER_FACTOR = 1.0