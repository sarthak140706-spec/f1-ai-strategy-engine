from data.strategy_params import (
    DEFAULT_PIT_LOSS
)


# ============================================================
# GET PIT LOSS
# ============================================================

def get_pit_loss(
    track: str
) -> float:
    """
    Return the pit lane time loss for a track.

    Parameters
    ----------
    track : str
        Circuit name.

    Returns
    -------
    float
        Estimated pit lane time loss in seconds.

    Notes
    -----
    V5 Sprint 1 currently uses a fallback pit loss
    value when dynamic track-specific data is not
    available.

    Future sprints can replace this static fallback
    with track-specific estimates derived from
    historical FastF1 data.
    """

    if track is None:

        raise ValueError(
            "track cannot be None."
        )

    return float(
        DEFAULT_PIT_LOSS
    )