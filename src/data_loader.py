import fastf1
import pandas as pd

fastf1.Cache.enable_cache(r"D:\FastF1Cache")


def load_race_data(
    season: int,
    grand_prix: str,
    session_type: str = "R"
) -> pd.DataFrame:

    session = fastf1.get_session(
        season,
        grand_prix,
        session_type
    )

    session.load()

    return session.laps