from data.strategy_params import TRACK_PIT_LOSS


def get_pit_loss(track: str) -> float:
    return TRACK_PIT_LOSS.get(track, 21.0)