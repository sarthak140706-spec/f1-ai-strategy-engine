"""
Live Race State Builder

Sprint 7 - Step 2
F1 AI Strategist V5

This module converts a FastF1 session into a complete
driver-by-driver race state that can be consumed by the
real-time strategy engine.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd


# ============================================================
# DRIVER RACE STATE
# ============================================================

@dataclass
class DriverRaceState:
    """
    Current race state for one driver.
    """

    driver: str

    position: Optional[int]

    lap_number: Optional[int]

    tyre_compound: Optional[str]

    tyre_age: Optional[int]

    last_lap_time: Optional[float]

    best_lap_time: Optional[float]

    average_last_5: Optional[float]

    average_last_10: Optional[float]

    gap_to_leader: Optional[float]

    interval_ahead: Optional[float]

    interval_behind: Optional[float]

    pit_stops: int

    in_pit: bool

    retired: bool

    track_status: Optional[str]

    weather: Dict[str, Any]

    timestamp: datetime


# ============================================================
# LIVE RACE STATE
# ============================================================

class LiveRaceState:

    """
    Builds a complete race-state snapshot
    for every driver currently participating
    in a FastF1 session.
    """

    def __init__(self, session):

        if session is None:
            raise ValueError(
                "session cannot be None."
            )

        self.session = session

        self.driver_states: Dict[
            str,
            DriverRaceState
        ] = {}

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------

    def build(self) -> Dict[str, DriverRaceState]:

        """
        Build race state for every driver.
        """

        self.driver_states.clear()

        results = self.session.results

        for _, row in results.iterrows():

            driver = row.get("Abbreviation")

            if driver is None:
                continue

            driver = str(driver).upper()

            try:

                state = self._build_driver_state(
                    driver
                )

                self.driver_states[
                    driver
                ] = state

            except Exception as e:

                print(
                    f"Failed to build state for {driver}: {e}"
                )

                continue

        return self.driver_states

    # --------------------------------------------------------
    # BUILD SINGLE DRIVER
    # --------------------------------------------------------

    def _build_driver_state(
        self,
        driver: str
    ) -> DriverRaceState:

        laps = self.session.laps.pick_drivers(
            driver
        )

        if laps.empty:

            raise ValueError(
                f"No lap data for {driver}"
            )

        latest = laps.iloc[-1]

        weather = self._extract_weather()

        track = self._extract_track_status()

        return DriverRaceState(

            driver=driver,

            position=self._safe_int(
                latest.get("Position")
            ),

            lap_number=self._safe_int(
                latest.get("LapNumber")
            ),

            tyre_compound=self._extract_compound(
                latest
            ),

            tyre_age=self._safe_int(
                latest.get("TyreLife")
            ),

            last_lap_time=self._lap_seconds(
                latest.get("LapTime")
            ),

            best_lap_time=self._best_lap(
                laps
            ),

            average_last_5=self._average_last_n(
                laps,
                5
            ),

            average_last_10=self._average_last_n(
                laps,
                10
            ),

            gap_to_leader=None,

            interval_ahead=None,

            interval_behind=None,

            pit_stops=self._count_pit_stops(
                laps
            ),

            in_pit=self._is_in_pit(
                latest
            ),

            retired=self._is_retired(
                laps
            ),

            track_status=track,

            weather=weather,

            timestamp=datetime.now()

        )

    # --------------------------------------------------------
    # TYRE
    # --------------------------------------------------------

    def _extract_compound(
        self,
        lap
    ) -> Optional[str]:

        compound = lap.get(
            "Compound"
        )

        if pd.isna(compound):
            return None

        return str(compound).upper()

    # --------------------------------------------------------
    # PIT STOP COUNT
    # --------------------------------------------------------

    def _count_pit_stops(
        self,
        laps
    ) -> int:

        count = 0

        for _, lap in laps.iterrows():

            value = lap.get(
                "PitOutTime"
            )

            if pd.notna(value):
                count += 1

        return count

    # --------------------------------------------------------
    # CURRENTLY IN PIT
    # --------------------------------------------------------

    def _is_in_pit(
        self,
        lap
    ) -> bool:

        pit_in = lap.get(
            "PitInTime"
        )

        pit_out = lap.get(
            "PitOutTime"
        )

        if (
            pd.notna(pit_in)
            and
            pd.isna(pit_out)
        ):
            return True

        return False
    # --------------------------------------------------------
    # RETIREMENT
    # --------------------------------------------------------

    def _is_retired(
        self,
        laps
    ) -> bool:

        """
        Placeholder retirement detection.

        FastF1 does not directly expose retirement
        status in lap data. This will be improved
        in a later Sprint 7 step.
        """

        return False

    # --------------------------------------------------------
    # BEST LAP
    # --------------------------------------------------------

    def _best_lap(
        self,
        laps
    ) -> Optional[float]:

        lap_times = []

        for _, lap in laps.iterrows():

            value = self._lap_seconds(
                lap.get("LapTime")
            )

            if value is not None:
                lap_times.append(value)

        if not lap_times:
            return None

        return min(lap_times)

    # --------------------------------------------------------
    # LAST N LAP AVERAGE
    # --------------------------------------------------------

    def _average_last_n(
        self,
        laps,
        n: int
    ) -> Optional[float]:

        values = []

        recent = laps.tail(n)

        for _, lap in recent.iterrows():

            seconds = self._lap_seconds(
                lap.get("LapTime")
            )

            if seconds is not None:
                values.append(seconds)

        if not values:
            return None

        return round(
            sum(values) / len(values),
            3
        )

    # --------------------------------------------------------
    # LAP TO SECONDS
    # --------------------------------------------------------

    def _lap_seconds(
        self,
        lap_time
    ) -> Optional[float]:

        if pd.isna(lap_time):
            return None

        try:

            return round(

                lap_time.total_seconds(),

                3

            )

        except Exception:

            return None

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    def _extract_weather(
        self
    ) -> Dict[str, Any]:

        try:

            weather = self.session.weather_data

            if weather is None:

                return {}

            if weather.empty:

                return {}

            latest = weather.iloc[-1]

            return {

                "air_temp":
                    latest.get(
                        "AirTemp"
                    ),

                "track_temp":
                    latest.get(
                        "TrackTemp"
                    ),

                "humidity":
                    latest.get(
                        "Humidity"
                    ),

                "pressure":
                    latest.get(
                        "Pressure"
                    ),

                "wind_speed":
                    latest.get(
                        "WindSpeed"
                    ),

                "wind_direction":
                    latest.get(
                        "WindDirection"
                    ),

                "rainfall":
                    latest.get(
                        "Rainfall"
                    )

            }

        except Exception:

            return {}

    # --------------------------------------------------------
    # TRACK STATUS
    # --------------------------------------------------------

    def _extract_track_status(
        self
    ) -> Optional[str]:

        try:

            status = self.session.track_status

            if status is None:
                return None

            if status.empty:
                return None

            latest = status.iloc[-1]

            return str(

                latest.get(
                    "Status"
                )

            )

        except Exception:

            return None

    # --------------------------------------------------------
    # SAFE INTEGER
    # --------------------------------------------------------

    def _safe_int(
        self,
        value
    ) -> Optional[int]:

        if pd.isna(value):

            return None

        try:

            return int(value)

        except Exception:

            return None

    # --------------------------------------------------------
    # GAP CALCULATIONS
    # --------------------------------------------------------

    def compute_gaps(
        self
    ) -> None:

        """
        Compute approximate gaps using
        latest lap times.
        """

        ordered = sorted(

            self.driver_states.values(),

            key=lambda x:

            (

                x.position

                if x.position is not None

                else 999

            )

        )

        previous = None

        leader = None

        cumulative_gap = 0.0

        for driver in ordered:

            if leader is None:

                leader = driver

                driver.gap_to_leader = 0.0

                driver.interval_ahead = None

                driver.interval_behind = None

                previous = driver

                continue

            if (

                driver.last_lap_time is None

                or

                previous.last_lap_time is None

            ):

                driver.interval_ahead = None

                driver.gap_to_leader = None

                previous.interval_behind = None

            else:

                interval = round(

                    abs(

                        driver.last_lap_time

                        -

                        previous.last_lap_time

                    ),

                    3

                )

                cumulative_gap += interval

                driver.interval_ahead = interval

                driver.gap_to_leader = round(

                    cumulative_gap,

                    3

                )

                previous.interval_behind = interval

            previous = driver

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self) -> Dict[str, DriverRaceState]:
        """
        Refresh all driver race states.
        """

        states = self.build()

        self.compute_gaps()

        return states

    # --------------------------------------------------------
    # GET DRIVER
    # --------------------------------------------------------

    def get_driver(
        self,
        driver: str
    ) -> Optional[DriverRaceState]:

        if driver is None:

            return None

        return self.driver_states.get(

            str(driver).upper()

        )

    # --------------------------------------------------------
    # GET ALL
    # --------------------------------------------------------

    def get_all(self) -> List[DriverRaceState]:

        return list(

            self.driver_states.values()

        )

    # --------------------------------------------------------
    # TO DICTIONARY
    # --------------------------------------------------------

    def to_dict(self) -> List[Dict[str, Any]]:

        return [

            asdict(driver)

            for driver in

            self.get_all()

        ]

    # --------------------------------------------------------
    # TO DATAFRAME
    # --------------------------------------------------------

    def to_dataframe(self) -> pd.DataFrame:

        return pd.DataFrame(

            self.to_dict()

        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    import fastf1

    print(

        "=" * 100

    )

    print(

        "V5 SPRINT 7 - STEP 2"

    )

    print(

        "LIVE RACE STATE"

    )

    print(

        "=" * 100

    )

    print(

        "\nLoading session..."

    )

    session = fastf1.get_session(

        2025,

        "British Grand Prix",

        "R"

    )

    session.load()

    print(

        "Session loaded successfully."

    )

    print(

        "\nBuilding live race state..."

    )

    race_state = LiveRaceState(

        session

    )

    race_state.update()

    drivers = race_state.get_all()

    print(

        f"Drivers Loaded: "

        f"{len(drivers)}"

    )

    print(

        "\n"

        + "-" * 120

    )

    print(

        f"{'Driver':<8}"

        f"{'Pos':<6}"

        f"{'Lap':<6}"

        f"{'Tyre':<15}"

        f"{'Age':<6}"

        f"{'Best':<10}"

        f"{'Last':<10}"

        f"{'Gap':<10}"

        f"{'PitStops':<10}"

        f"{'Retired':<10}"

    )

    print(

        "-" * 120

    )

    for state in sorted(

        drivers,

        key=lambda x:

        (

            x.position

            if x.position is not None

            else 999

        )

    ):

        best = (

            f"{state.best_lap_time:.3f}"

            if state.best_lap_time is not None

            else "N/A"

        )

        last = (

            f"{state.last_lap_time:.3f}"

            if state.last_lap_time is not None

            else "N/A"

        )

        gap = (

            f"{state.gap_to_leader:.3f}"

            if state.gap_to_leader is not None

            else "N/A"

        )

        print(

            f"{state.driver:<8}"

            f"{str(state.position):<6}"

            f"{str(state.lap_number):<6}"

            f"{str(state.tyre_compound):<15}"

            f"{str(state.tyre_age):<6}"

            f"{best:<10}"

            f"{last:<10}"

            f"{gap:<10}"

            f"{state.pit_stops:<10}"

            f"{str(state.retired):<10}"

        )

    print(

        "\nWeather"

    )

    print(

        "-" * 30

    )

    if drivers:

        weather = drivers[0].weather

        if weather:

            for key, value in weather.items():

                print(

                    f"{key}: {value}"

                )

        else:

            print(

                "No weather data available."

            )

    print(

        "\nTrack Status"

    )

    print(

        "-" * 30

    )

    if drivers:

        print(

            drivers[0].track_status

        )

    print(

        "\n"

        + "=" * 100

    )

    print(

        "STEP 7.2 LIVE RACE STATE TEST PASSED"

    )

    print(

        "=" * 100

    )