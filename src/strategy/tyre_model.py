from data.strategy_params import TYRE_DEGRADATION


def get_degradation_rate(tyre_compound: str) -> float:
    return TYRE_DEGRADATION.get(tyre_compound, 0.06)