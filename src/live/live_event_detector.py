"""
Live Event Detector

Sprint 7 - Step 6
F1 AI Strategist V5

This module detects important events during a live F1 race.

Pipeline position:

FastF1 Session
        ↓
Live Race State
        ↓
Live Event Detector
        ↓
Strategy Decision Engine
        ↓
Live Strategy Simulator
        ↓
Final Strategy Output

IMPORTANT:
This module is intentionally independent.

It MUST NOT import:
    - strategy_decision_engine
    - live_strategy_simulator
    - live_strategy_orchestrator

This prevents circular imports.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ============================================================
# RACE EVENT
# ============================================================

@dataclass
class RaceEvent:
    """
    Represents one detected race event.
    """

    event_type: str

    driver: Optional[str] = None

    lap_number: Optional[int] = None

    description: str = ""

    severity: str = "INFO"

    previous_value: Any = None

    current_value: Any = None

    timestamp: datetime = field(
        default_factory=datetime.now
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------------
    # CONVERT TO DICTIONARY
    # --------------------------------------------------------

    def to_dict(
        self
    ) -> Dict[str, Any]:

        return {

            "event_type":
                self.event_type,

            "driver":
                self.driver,

            "lap_number":
                self.lap_number,

            "description":
                self.description,

            "severity":
                self.severity,

            "previous_value":
                self.previous_value,

            "current_value":
                self.current_value,

            "timestamp":
                self.timestamp,

            "metadata":
                self.metadata

        }


# ============================================================
# LIVE EVENT DETECTOR
# ============================================================

class LiveEventDetector:
    """
    Detects important changes between two consecutive
    live race-state snapshots.

    The detector does not depend on the strategy engine
    or simulator.

    Input:

        previous_state:
            Dict[str, DriverRaceState]

        current_state:
            Dict[str, DriverRaceState]

    Output:

        List[RaceEvent]
    """

    # --------------------------------------------------------
    # EVENT TYPES
    # --------------------------------------------------------

    EVENT_PIT_ENTRY = (
        "PIT_ENTRY"
    )

    EVENT_PIT_EXIT = (
        "PIT_EXIT"
    )

    EVENT_POSITION_CHANGE = (
        "POSITION_CHANGE"
    )

    EVENT_RETIREMENT = (
        "RETIREMENT"
    )

    EVENT_TYRE_CHANGE = (
        "TYRE_CHANGE"
    )

    EVENT_PACE_CHANGE = (
        "PACE_CHANGE"
    )

    EVENT_TRACK_STATUS_CHANGE = (
        "TRACK_STATUS_CHANGE"
    )

    EVENT_WEATHER_CHANGE = (
        "WEATHER_CHANGE"
    )

    EVENT_LAP_CHANGE = (
        "LAP_CHANGE"
    )

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        pace_change_threshold: float = 5.0
    ):

        self.pace_change_threshold = (

            float(
                pace_change_threshold
            )

        )

        # Events generated during
        # the latest detection cycle.

        self.current_events: List[
            RaceEvent
        ] = []

        # Complete event history.

        self.event_history: List[
            RaceEvent
        ] = []

        self.previous_state: Dict[
            str,
            Any
        ] = {}

        self.current_state: Dict[
            str,
            Any
        ] = {}

    # ========================================================
    # DETECT EVENTS
    # ========================================================

    def detect_events(
        self,
        previous_state: Dict[str, Any],
        current_state: Dict[str, Any]
    ) -> List[RaceEvent]:

        """
        Compare two race-state snapshots and detect
        all relevant changes.

        Returns only events detected during this update.
        """

        if previous_state is None:

            previous_state = {}

        if current_state is None:

            current_state = {}

        self.previous_state = (

            previous_state

        )

        self.current_state = (

            current_state

        )

        # Reset events for current update.

        self.current_events = []

        # ----------------------------------------------------
        # DRIVER-LEVEL EVENTS
        # ----------------------------------------------------

        all_drivers = set(

            previous_state.keys()

        ).union(

            current_state.keys()

        )

        for driver in sorted(
            all_drivers
        ):

            previous = (

                previous_state.get(
                    driver
                )

            )

            current = (

                current_state.get(
                    driver
                )

            )

            # A driver appearing for the first time
            # does not automatically generate an event.

            if previous is None:

                continue

            if current is None:

                continue

            # ------------------------------------------------
            # PIT ENTRY
            # ------------------------------------------------

            self._detect_pit_entry(

                driver,

                previous,

                current

            )

            # ------------------------------------------------
            # PIT EXIT
            # ------------------------------------------------

            self._detect_pit_exit(

                driver,

                previous,

                current

            )

            # ------------------------------------------------
            # POSITION CHANGE
            # ------------------------------------------------

            self._detect_position_change(

                driver,

                previous,

                current

            )

            # ------------------------------------------------
            # RETIREMENT
            # ------------------------------------------------

            self._detect_retirement(

                driver,

                previous,

                current

            )

            # ------------------------------------------------
            # TYRE CHANGE
            # ------------------------------------------------

            self._detect_tyre_change(

                driver,

                previous,

                current

            )

            # ------------------------------------------------
            # PACE CHANGE
            # ------------------------------------------------

            self._detect_pace_change(

                driver,

                previous,

                current

            )

            # ------------------------------------------------
            # TRACK STATUS
            # ------------------------------------------------

            self._detect_track_status_change(

                driver,

                previous,

                current

            )

            # ------------------------------------------------
            # WEATHER
            # ------------------------------------------------

            self._detect_weather_change(

                driver,

                previous,

                current

            )

        # ----------------------------------------------------
        # LAP CHANGE
        # ----------------------------------------------------

        self._detect_lap_change(

            previous_state,

            current_state

        )

        # ----------------------------------------------------
        # SAVE EVENTS TO HISTORY
        # ----------------------------------------------------

        self.event_history.extend(

            self.current_events

        )

        return list(

            self.current_events

        )

    # ========================================================
    # PIT ENTRY
    # ========================================================

    def _detect_pit_entry(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_in_pit = self._get_value(

            previous,

            "in_pit",

            False

        )

        current_in_pit = self._get_value(

            current,

            "in_pit",

            False

        )

        if (

            not previous_in_pit

            and current_in_pit

        ):

            self._add_event(

                event_type=(
                    self.EVENT_PIT_ENTRY
                ),

                driver=driver,

                state=current,

                description=(
                    f"{driver} entered the pit lane."
                ),

                severity="INFO",

                previous_value=False,

                current_value=True

            )

    # ========================================================
    # PIT EXIT
    # ========================================================

    def _detect_pit_exit(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_in_pit = self._get_value(

            previous,

            "in_pit",

            False

        )

        current_in_pit = self._get_value(

            current,

            "in_pit",

            False

        )

        if (

            previous_in_pit

            and not current_in_pit

        ):

            self._add_event(

                event_type=(
                    self.EVENT_PIT_EXIT
                ),

                driver=driver,

                state=current,

                description=(
                    f"{driver} exited the pit lane."
                ),

                severity="INFO",

                previous_value=True,

                current_value=False

            )

    # ========================================================
    # POSITION CHANGE
    # ========================================================

    def _detect_position_change(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_position = self._get_value(

            previous,

            "position",

            None

        )

        current_position = self._get_value(

            current,

            "position",

            None

        )

        if (

            previous_position is None

            or current_position is None

        ):

            return

        if (

            previous_position

            == current_position

        ):

            return

        position_change = (

            previous_position

            - current_position

        )

        if position_change > 0:

            description = (

                f"{driver} gained "
                f"{abs(position_change)} "
                f"position(s)."

            )

            severity = "POSITIVE"

        else:

            description = (

                f"{driver} lost "
                f"{abs(position_change)} "
                f"position(s)."

            )

            severity = "WARNING"

        self._add_event(

            event_type=(
                self.EVENT_POSITION_CHANGE
            ),

            driver=driver,

            state=current,

            description=description,

            severity=severity,

            previous_value=(
                previous_position
            ),

            current_value=(
                current_position
            ),

            metadata={

                "positions_gained":
                    max(
                        position_change,
                        0
                    ),

                "positions_lost":
                    max(
                        -position_change,
                        0
                    )

            }

        )

    # ========================================================
    # RETIREMENT
    # ========================================================

    def _detect_retirement(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_retired = self._get_value(

            previous,

            "retired",

            False

        )

        current_retired = self._get_value(

            current,

            "retired",

            False

        )

        if (

            not previous_retired

            and current_retired

        ):

            self._add_event(

                event_type=(
                    self.EVENT_RETIREMENT
                ),

                driver=driver,

                state=current,

                description=(
                    f"{driver} has retired from the race."
                ),

                severity="CRITICAL",

                previous_value=False,

                current_value=True

            )

    # ========================================================
    # TYRE CHANGE
    # ========================================================

    def _detect_tyre_change(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_tyre = self._get_value(

            previous,

            "tyre_compound",

            None

        )

        current_tyre = self._get_value(

            current,

            "tyre_compound",

            None

        )

        if (

            previous_tyre is None

            or current_tyre is None

        ):

            return

        if (

            str(
                previous_tyre
            ).upper()

            ==

            str(
                current_tyre
            ).upper()

        ):

            return

        self._add_event(

            event_type=(
                self.EVENT_TYRE_CHANGE
            ),

            driver=driver,

            state=current,

            description=(

                f"{driver} changed tyres "
                f"from {previous_tyre} "
                f"to {current_tyre}."

            ),

            severity="INFO",

            previous_value=(
                previous_tyre
            ),

            current_value=(
                current_tyre
            ),

            metadata={

                "old_compound":
                    previous_tyre,

                "new_compound":
                    current_tyre

            }

        )

    # ========================================================
    # PACE CHANGE
    # ========================================================

    def _detect_pace_change(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_pace = self._get_pace(

            previous

        )

        current_pace = self._get_pace(

            current

        )

        if (

            previous_pace is None

            or current_pace is None

        ):

            return

        difference = (

            current_pace

            - previous_pace

        )

        if (

            abs(
                difference
            )

            <

            self.pace_change_threshold

        ):

            return

        if difference < 0:

            description = (

                f"{driver} pace improved "
                f"significantly."

            )

            severity = "POSITIVE"

        else:

            description = (

                f"{driver} pace dropped "
                f"significantly."

            )

            severity = "WARNING"

        self._add_event(

            event_type=(
                self.EVENT_PACE_CHANGE
            ),

            driver=driver,

            state=current,

            description=description,

            severity=severity,

            previous_value=(
                previous_pace
            ),

            current_value=(
                current_pace
            ),

            metadata={

                "pace_difference":
                    difference,

                "absolute_change":
                    abs(
                        difference
                    )

            }

        )

    # ========================================================
    # TRACK STATUS CHANGE
    # ========================================================

    def _detect_track_status_change(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_status = self._get_value(

            previous,

            "track_status",

            None

        )

        current_status = self._get_value(

            current,

            "track_status",

            None

        )

        if (

            previous_status is None

            or current_status is None

        ):

            return

        if (

            str(
                previous_status
            )

            ==

            str(
                current_status
            )

        ):

            return

        self._add_event(

            event_type=(
                self.EVENT_TRACK_STATUS_CHANGE
            ),

            driver=driver,

            state=current,

            description=(

                f"Track status changed "
                f"from {previous_status} "
                f"to {current_status}."

            ),

            severity="IMPORTANT",

            previous_value=(
                previous_status
            ),

            current_value=(
                current_status
            )

        )

    # ========================================================
    # WEATHER CHANGE
    # ========================================================

    def _detect_weather_change(
        self,
        driver: str,
        previous: Any,
        current: Any
    ) -> None:

        previous_weather = self._get_value(

            previous,

            "weather",

            None

        )

        current_weather = self._get_value(

            current,

            "weather",

            None

        )

        if not isinstance(
            previous_weather,
            dict
        ):

            return

        if not isinstance(
            current_weather,
            dict
        ):

            return

        changed_fields = {}

        all_keys = set(

            previous_weather.keys()

        ).union(

            current_weather.keys()

        )

        for key in all_keys:

            old_value = (

                previous_weather.get(
                    key
                )

            )

            new_value = (

                current_weather.get(
                    key
                )

            )

            if old_value != new_value:

                changed_fields[key] = {

                    "previous":
                        old_value,

                    "current":
                        new_value

                }

        if not changed_fields:

            return

        self._add_event(

            event_type=(
                self.EVENT_WEATHER_CHANGE
            ),

            driver=driver,

            state=current,

            description=(

                "Weather conditions changed."

            ),

            severity="IMPORTANT",

            previous_value=(
                previous_weather
            ),

            current_value=(
                current_weather
            ),

            metadata={

                "changed_fields":
                    changed_fields

            }

        )

    # ========================================================
    # LAP CHANGE
    # ========================================================

    def _detect_lap_change(
        self,
        previous_state: Dict[str, Any],
        current_state: Dict[str, Any]
    ) -> None:

        previous_laps = []

        current_laps = []

        for state in previous_state.values():

            lap = self._get_value(

                state,

                "lap_number",

                None

            )

            if lap is not None:

                previous_laps.append(

                    lap

                )

        for state in current_state.values():

            lap = self._get_value(

                state,

                "lap_number",

                None

            )

            if lap is not None:

                current_laps.append(

                    lap

                )

        if not current_laps:

            return

        current_lap = max(

            current_laps

        )

        previous_lap = (

            max(
                previous_laps
            )

            if previous_laps

            else None

        )

        if (

            previous_lap is None

            or current_lap
            == previous_lap

        ):

            return

        self._add_event(

            event_type=(
                self.EVENT_LAP_CHANGE
            ),

            driver=None,

            state=None,

            description=(

                f"Race advanced from "
                f"lap {previous_lap} "
                f"to lap {current_lap}."

            ),

            severity="INFO",

            previous_value=(
                previous_lap
            ),

            current_value=(
                current_lap
            )

        )

    # ========================================================
    # ADD EVENT
    # ========================================================

    def _add_event(
        self,
        event_type: str,
        driver: Optional[str],
        state: Any,
        description: str,
        severity: str = "INFO",
        previous_value: Any = None,
        current_value: Any = None,
        metadata: Optional[
            Dict[str, Any]
        ] = None
    ) -> None:

        lap_number = None

        if state is not None:

            lap_number = self._get_value(

                state,

                "lap_number",

                None

            )

        event = RaceEvent(

            event_type=event_type,

            driver=driver,

            lap_number=lap_number,

            description=description,

            severity=severity,

            previous_value=previous_value,

            current_value=current_value,

            metadata=(
                metadata
                if metadata is not None
                else {}
            )

        )

        self.current_events.append(

            event

        )

    # ========================================================
    # GET EVENTS
    # ========================================================

    def get_events(
        self
    ) -> List[RaceEvent]:

        """
        Return events detected during
        the latest update cycle.
        """

        return list(

            self.current_events

        )

    # ========================================================
    # GET EVENT HISTORY
    # ========================================================

    def get_event_history(
        self
    ) -> List[RaceEvent]:

        """
        Return all events detected
        since detector initialization.
        """

        return list(

            self.event_history

        )

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(
        self
    ) -> Dict[str, Any]:

        """
        Return a summary of events detected
        during the latest update cycle.
        """

        event_types = [

            event.event_type

            for event

            in self.current_events

        ]

        unique_types = list(

            dict.fromkeys(

                event_types

            )

        )

        severity_counts = {}

        for event in self.current_events:

            severity = event.severity

            severity_counts[severity] = (

                severity_counts.get(

                    severity,

                    0

                )

                + 1

            )

        return {

            "total_events":
                len(
                    self.current_events
                ),

            "unique_types":
                unique_types,

            "severity_counts":
                severity_counts

        }

    # ========================================================
    # CLEAR CURRENT EVENTS
    # ========================================================

    def clear_events(
        self
    ) -> None:

        """
        Clear only the latest event list.

        Event history is preserved.
        """

        self.current_events = []

    # ========================================================
    # RESET
    # ========================================================

    def reset(
        self
    ) -> None:

        """
        Completely reset the event detector.
        """

        self.current_events = []

        self.event_history = []

        self.previous_state = {}

        self.current_state = {}

    # ========================================================
    # HELPER: GET VALUE
    # ========================================================

    @staticmethod
    def _get_value(
        state: Any,
        attribute: str,
        default: Any = None
    ) -> Any:

        """
        Safely read an attribute from either:

        - dataclass/object
        - dictionary
        """

        if state is None:

            return default

        if isinstance(
            state,
            dict
        ):

            return state.get(

                attribute,

                default

            )

        return getattr(

            state,

            attribute,

            default

        )

    # ========================================================
    # HELPER: GET PACE
    # ========================================================

    def _get_pace(
        self,
        state: Any
    ) -> Optional[float]:

        """
        Extract the most useful available pace metric.

        Priority:

        1. average_last_5
        2. average_last_10
        3. last_lap_time

        Returns None when no valid numeric value exists.
        """

        candidates = [

            "average_last_5",

            "average_last_10",

            "last_lap_time"

        ]

        for attribute in candidates:

            value = self._get_value(

                state,

                attribute,

                None

            )

            numeric_value = (

                self._to_float(
                    value
                )

            )

            if numeric_value is not None:

                return numeric_value

        return None

    # ========================================================
    # HELPER: SAFE FLOAT
    # ========================================================

    @staticmethod
    def _to_float(
        value: Any
    ) -> Optional[float]:

        """
        Safely convert a value to float.

        Handles:

        - int
        - float
        - numeric strings
        - pandas/numpy numeric values
        """

        if value is None:

            return None

        if isinstance(
            value,
            bool
        ):

            return None

        try:

            numeric_value = float(

                value

            )

            return numeric_value

        except (

            TypeError,

            ValueError

        ):

            return None


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 100
    )

    print(
        "V5 SPRINT 7 - STEP 6"
    )

    print(
        "LIVE EVENT DETECTOR TEST"
    )

    print(
        "=" * 100
    )

    # --------------------------------------------------------
    # MOCK PREVIOUS STATE
    # --------------------------------------------------------

    previous_state = {

        "VER": {

            "driver":
                "VER",

            "position":
                1,

            "lap_number":
                52,

            "tyre_compound":
                "MEDIUM",

            "tyre_age":
                18,

            "last_lap_time":
                90.0,

            "average_last_5":
                90.0,

            "average_last_10":
                90.0,

            "in_pit":
                False,

            "retired":
                False,

            "track_status":
                "1",

            "weather": {

                "air_temp":
                    19.6,

                "track_temp":
                    24.3,

                "rainfall":
                    False

            }

        },

        "HAM": {

            "driver":
                "HAM",

            "position":
                3,

            "lap_number":
                52,

            "tyre_compound":
                "MEDIUM",

            "tyre_age":
                20,

            "last_lap_time":
                92.0,

            "average_last_5":
                92.0,

            "average_last_10":
                92.0,

            "in_pit":
                False,

            "retired":
                False,

            "track_status":
                "1",

            "weather": {

                "air_temp":
                    19.6,

                "track_temp":
                    24.3,

                "rainfall":
                    False

            }

        }

    }

    # --------------------------------------------------------
    # MOCK CURRENT STATE
    # --------------------------------------------------------

    current_state = {

        "VER": {

            "driver":
                "VER",

            "position":
                2,

            "lap_number":
                53,

            "tyre_compound":
                "SOFT",

            "tyre_age":
                1,

            "last_lap_time":
                88.0,

            "average_last_5":
                88.0,

            "average_last_10":
                89.0,

            "in_pit":
                False,

            "retired":
                False,

            "track_status":
                "2",

            "weather": {

                "air_temp":
                    19.8,

                "track_temp":
                    24.5,

                "rainfall":
                    True

            }

        },

        "HAM": {

            "driver":
                "HAM",

            "position":
                3,

            "lap_number":
                53,

            "tyre_compound":
                "MEDIUM",

            "tyre_age":
                21,

            "last_lap_time":
                98.0,

            "average_last_5":
                98.0,

            "average_last_10":
                95.0,

            "in_pit":
                True,

            "retired":
                False,

            "track_status":
                "2",

            "weather": {

                "air_temp":
                    19.8,

                "track_temp":
                    24.5,

                "rainfall":
                    True

            }

        }

    }

    # --------------------------------------------------------
    # CREATE DETECTOR
    # --------------------------------------------------------

    detector = LiveEventDetector(

        pace_change_threshold=5.0

    )

    print(
        "\nDetecting race events..."
    )

    events = detector.detect_events(

        previous_state,

        current_state

    )

    print(
        f"\nDetected Events: "
        f"{len(events)}"
    )

    print(
        "-" * 100
    )

    for event in events:

        print(

            f"{event.event_type:<25}"

            f"{str(event.driver):<10}"

            f"{event.severity:<12}"

            f"{event.description}"

        )

    print(
        "\nEvent Summary"
    )

    print(
        "-" * 40
    )

    summary = detector.summary()

    print(

        f"Total Events : "
        f"{summary['total_events']}"

    )

    print(

        f"Event Types  : "
        f"{summary['unique_types']}"

    )

    print(

        f"Severities   : "
        f"{summary['severity_counts']}"

    )

    # --------------------------------------------------------
    # ASSERTIONS
    # --------------------------------------------------------

    assert len(events) > 0

    assert any(

        event.event_type

        ==

        LiveEventDetector.EVENT_POSITION_CHANGE

        for event in events

    )

    assert any(

        event.event_type

        ==

        LiveEventDetector.EVENT_TYRE_CHANGE

        for event in events

    )

    assert any(

        event.event_type

        ==

        LiveEventDetector.EVENT_PIT_ENTRY

        for event in events

    )

    assert any(

        event.event_type

        ==

        LiveEventDetector.EVENT_PACE_CHANGE

        for event in events

    )

    assert any(

        event.event_type

        ==

        LiveEventDetector.EVENT_TRACK_STATUS_CHANGE

        for event in events

    )

    assert any(

        event.event_type

        ==

        LiveEventDetector.EVENT_WEATHER_CHANGE

        for event in events

    )

    assert any(

        event.event_type

        ==

        LiveEventDetector.EVENT_LAP_CHANGE

        for event in events

    )

    print(
        "\n"
        + "=" * 100
    )

    print(
        "LIVE EVENT DETECTOR TEST PASSED"
    )

    print(
        "=" * 100
    )