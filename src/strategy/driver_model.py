from data.strategy_params import DRIVER_STYLE


def get_driver_factor(driver: str) -> float:
    return DRIVER_STYLE.get(driver, 1.0)