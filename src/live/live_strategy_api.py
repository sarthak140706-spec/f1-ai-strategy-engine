"""
Live Strategy API

Sprint 7 - Step 7
F1 AI Strategist V5

Provides a clean interface between the live strategy
orchestrator and the application/dashboard layer.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd

from .live_strategy_orchestrator import (
    LiveStrategyOrchestrator
)


# ============================================================
# LIVE STRATEGY API
# ============================================================

class LiveStrategyAPI:

    """
    Application-facing interface for the live strategy system.

    This class hides the internal implementation of:

        LiveRaceState
        LiveEventDetector
        StrategyDecisionEngine
        LiveStrategySimulator
        LiveStrategyOrchestrator

    The dashboard or frontend can interact with this
    class without directly accessing internal modules.
    """

    def __init__(
        self,
        orchestrator: LiveStrategyOrchestrator
    ) -> None:

        if orchestrator is None:

            raise ValueError(
                "orchestrator cannot be None."
            )

        self.orchestrator = orchestrator

    # --------------------------------------------------------
    # INITIALIZE
    # --------------------------------------------------------

    def initialize(
        self
    ) -> Dict[str, Any]:

        """
        Initialize the complete live strategy pipeline.

        Returns a structured snapshot of the initial state.
        """

        strategies = (

            self.orchestrator.initialize()

        )

        return self.get_snapshot()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(
        self
    ) -> Dict[str, Any]:

        """
        Run one complete live strategy update cycle.

        Returns the latest strategy snapshot.
        """

        self.orchestrator.update()

        return self.get_snapshot()

    
    # --------------------------------------------------------
    # GET SNAPSHOT
    # --------------------------------------------------------

    def get_snapshot(
        self
    ) -> Dict[str, Any]:

        """
        Return the latest complete strategy snapshot.
        """

        history = (

            self.orchestrator.get_history()

        )

        if not history:

            return {

                "status": "not_initialized",

                "lap": None,

                "drivers": 0,

                "events": 0,

                "strategies": 0,

                "actions": {},

                "timestamp": None

            }

        snapshot = history[-1]

        return {

            "status": "active",

            "lap": snapshot.lap_number,

            "drivers": snapshot.drivers,

            "events": snapshot.events,

            "strategies": snapshot.strategies,

            "actions": snapshot.actions,

            "timestamp":
                snapshot.timestamp

        }

    # --------------------------------------------------------
    # GET DRIVER STRATEGY
    # --------------------------------------------------------

    def get_driver_strategy(
        self,
        driver: str
    ) -> Optional[Dict[str, Any]]:

        """
        Return the latest strategy for one driver.
        """

        if driver is None:

            return None

        strategies = (

            self.orchestrator.get_strategies()

        )

        strategy = strategies.get(

            str(driver).upper()

        )

        if strategy is None:

            return None

        return {

            "driver":
                strategy.driver,

            "action":
                strategy.action,

            "confidence":
                strategy.confidence,

            "reason":
                strategy.reason,

            "tyre_score":
                strategy.tyre_score,

            "pace_score":
                strategy.pace_score,

            "traffic_score":
                strategy.traffic_score,

            "risk_score":
                strategy.risk_score,

            "timestamp":
                strategy.timestamp

        }

    # --------------------------------------------------------
    # GET ALL STRATEGIES
    # --------------------------------------------------------

    def get_all_strategies(
        self
    ) -> List[Dict[str, Any]]:

        """
        Return strategies for all drivers.
        """

        strategies = (

            self.orchestrator.get_strategies()

        )

        return [

            {

                "driver":
                    strategy.driver,

                "action":
                    strategy.action,

                "confidence":
                    strategy.confidence,

                "reason":
                    strategy.reason,

                "tyre_score":
                    strategy.tyre_score,

                "pace_score":
                    strategy.pace_score,

                "traffic_score":
                    strategy.traffic_score,

                "risk_score":
                    strategy.risk_score,

                "timestamp":
                    strategy.timestamp

            }

            for strategy in strategies.values()

        ]

    # --------------------------------------------------------
    # STRATEGIES DATAFRAME
    # --------------------------------------------------------

    def get_strategies_dataframe(
        self
    ) -> pd.DataFrame:

        """
        Return the latest strategy data
        as a pandas DataFrame.
        """

        return (

            self.orchestrator.strategies_to_dataframe()

        )

    # --------------------------------------------------------
    # GET EVENTS
    # --------------------------------------------------------

    def get_events(
        self
    ) -> List[Dict[str, Any]]:

        """
        Return all detected race events.
        """

        events = (

            self.orchestrator.get_events()

        )

        return [

            {

                "event_type":
                    event.event_type,

                "driver":
                    event.driver,

                "lap":
                    event.lap,

                "description":
                    event.description,

                "severity":
                    event.severity,

                "timestamp":
                    event.timestamp

            }

            for event in events

        ]

    # --------------------------------------------------------
    # GET EVENT SUMMARY
    # --------------------------------------------------------

    def get_event_summary(
        self
    ) -> Dict[str, Any]:

        """
        Return a summary of detected race events.
        """

        return (

            self.orchestrator.event_summary()

        )

    # --------------------------------------------------------
    # GET STRATEGY SUMMARY
    # --------------------------------------------------------

    def get_strategy_summary(
        self
    ) -> Dict[str, Any]:

        """
        Return a summary of current strategies.
        """

        return (

            self.orchestrator.strategy_summary()

        )
        # --------------------------------------------------------
    # GET RACE STATE
    # --------------------------------------------------------

    def get_race_state(
        self
    ) -> List[Dict[str, Any]]:

        """
        Return the latest race state
        for all available drivers.
        """

        states = (

            self.orchestrator.get_race_state()

        )

        return [

            {

                "driver":
                    state.driver,

                "position":
                    state.position,

                "lap_number":
                    state.lap_number,

                "tyre_compound":
                    state.tyre_compound,

                "tyre_age":
                    state.tyre_age,

                "last_lap_time":
                    state.last_lap_time,

                "best_lap_time":
                    state.best_lap_time,

                "average_last_5":
                    state.average_last_5,

                "average_last_10":
                    state.average_last_10,

                "gap_to_leader":
                    state.gap_to_leader,

                "interval_ahead":
                    state.interval_ahead,

                "interval_behind":
                    state.interval_behind,

                "pit_stops":
                    state.pit_stops,

                "in_pit":
                    state.in_pit,

                "retired":
                    state.retired,

                "track_status":
                    state.track_status,

                "weather":
                    state.weather,

                "timestamp":
                    state.timestamp

            }

            for state in states

        ]

    # --------------------------------------------------------
    # GET WEATHER
    # --------------------------------------------------------

    def get_weather(
        self
    ) -> Dict[str, Any]:

        """
        Return the latest weather information.
        """

        race_state = (

            self.get_race_state()

        )

        if not race_state:

            return {}

        return race_state[0].get(

            "weather",

            {}

        )

    # --------------------------------------------------------
    # GET TRACK STATUS
    # --------------------------------------------------------

    def get_track_status(
        self
    ) -> Optional[str]:

        """
        Return the latest track status.
        """

        race_state = (

            self.get_race_state()

        )

        if not race_state:

            return None

        return race_state[0].get(

            "track_status"

        )

    # --------------------------------------------------------
    # GET CURRENT LAP
    # --------------------------------------------------------

    def get_current_lap(
        self
    ) -> Optional[int]:

        """
        Return the latest available race lap.
        """

        snapshot = (

            self.get_snapshot()

        )

        return snapshot.get(

            "lap"

        )

    # --------------------------------------------------------
    # GET DRIVER COUNT
    # --------------------------------------------------------

    def get_driver_count(
        self
    ) -> int:

        """
        Return the number of drivers
        currently available in the race state.
        """

        snapshot = (

            self.get_snapshot()

        )

        return snapshot.get(

            "drivers",

            0

        )

    # --------------------------------------------------------
    # GET EVENT COUNT
    # --------------------------------------------------------

    def get_event_count(
        self
    ) -> int:

        """
        Return the number of detected race events.
        """

        snapshot = (

            self.get_snapshot()

        )

        return snapshot.get(

            "events",

            0

        )

    # --------------------------------------------------------
    # GET STRATEGY COUNT
    # --------------------------------------------------------

    def get_strategy_count(
        self
    ) -> int:

        """
        Return the number of generated strategies.
        """

        snapshot = (

            self.get_snapshot()

        )

        return snapshot.get(

            "strategies",

            0

        )

    # --------------------------------------------------------
    # GET ACTION COUNTS
    # --------------------------------------------------------

    def get_action_counts(
        self
    ) -> Dict[str, int]:

        """
        Return the count of each recommended
        strategy action.
        """

        snapshot = (

            self.get_snapshot()

        )

        return snapshot.get(

            "actions",

            {}

        )

    # --------------------------------------------------------
    # GET COMPLETE API RESPONSE
    # --------------------------------------------------------

    def get_full_response(
        self
    ) -> Dict[str, Any]:

        """
        Return a complete structured response
        suitable for a dashboard or frontend.
        """

        return {

            "snapshot":
                self.get_snapshot(),

            "race_state":
                self.get_race_state(),

            "strategies":
                self.get_all_strategies(),

            "events":
                self.get_events(),

            "event_summary":
                self.get_event_summary(),

            "strategy_summary":
                self.get_strategy_summary(),

            "weather":
                self.get_weather(),

            "track_status":
                self.get_track_status()

        }

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    import fastf1

    print("=" * 100)
    print("V5 SPRINT 7 - STEP 7")
    print("LIVE STRATEGY API")
    print("=" * 100)

    print("\nLoading session...")

    session = fastf1.get_session(
        2025,
        "British Grand Prix",
        "R"
    )

    session.load()

    print("Session loaded successfully.")

    # --------------------------------------------------------
    # CREATE API
    # --------------------------------------------------------

    print("\nCreating Live Strategy Orchestrator...")

    orchestrator = LiveStrategyOrchestrator(
        session
    )

    print("\nCreating Live Strategy API...")

    api = LiveStrategyAPI(
        orchestrator
    )

    # --------------------------------------------------------
    # INITIALIZE
    # --------------------------------------------------------

    print("\nInitializing API...")

    initial_snapshot = api.initialize()

    print("API initialized successfully.")

    print("\nInitial Snapshot")
    print("-" * 40)

    print(
        f"Lap       : "
        f"{api.get_current_lap()}"
    )

    print(
        f"Drivers   : "
        f"{api.get_driver_count()}"
    )

    print(
        f"Events    : "
        f"{api.get_event_count()}"
    )

    print(
        f"Strategies: "
        f"{api.get_strategy_count()}"
    )

    print(
        f"Actions   : "
        f"{api.get_action_counts()}"
    )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    print("\nRunning API update...")

    updated_snapshot = api.update()

    print("API update completed.")

    print("\nUpdated Snapshot")
    print("-" * 40)

    print(
        f"Lap       : "
        f"{api.get_current_lap()}"
    )

    print(
        f"Drivers   : "
        f"{api.get_driver_count()}"
    )

    print(
        f"Events    : "
        f"{api.get_event_count()}"
    )

    print(
        f"Strategies: "
        f"{api.get_strategy_count()}"
    )

    print(
        f"Actions   : "
        f"{api.get_action_counts()}"
    )

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    print("\nWeather")
    print("-" * 40)

    weather = api.get_weather()

    if weather:

        for key, value in weather.items():

            print(
                f"{key:<20}: {value}"
            )

    else:

        print(
            "No weather data available."
        )

    # --------------------------------------------------------
    # TRACK STATUS
    # --------------------------------------------------------

    print("\nTrack Status")
    print("-" * 40)

    print(
        api.get_track_status()
    )

    # --------------------------------------------------------
    # EVENT SUMMARY
    # --------------------------------------------------------

    print("\nEvent Summary")
    print("-" * 40)

    event_summary = (

        api.get_event_summary()

    )

    print(
        f"Total Events : "
        f"{event_summary.get('total_events', 0)}"
    )

    print(
        f"Event Types  : "
        f"{event_summary.get('event_types', [])}"
    )

    # --------------------------------------------------------
    # STRATEGY SUMMARY
    # --------------------------------------------------------

    print("\nStrategy Summary")
    print("-" * 40)

    strategy_summary = (

        api.get_strategy_summary()

    )

    print(
        f"Drivers : "
        f"{strategy_summary.get('drivers', 0)}"
    )

    print(
        f"Actions : "
        f"{strategy_summary.get('actions', {})}"
    )

    # --------------------------------------------------------
    # DRIVER STRATEGY TEST
    # --------------------------------------------------------

    print("\nDriver Strategy Test")
    print("-" * 40)

    driver_strategy = (

        api.get_driver_strategy(
            "VER"
        )

    )

    if driver_strategy:

        print(
            f"Driver     : "
            f"{driver_strategy.get('driver')}"
        )

        print(
            f"Action     : "
            f"{driver_strategy.get('action')}"
        )

        print(
            f"Confidence : "
            f"{driver_strategy.get('confidence')}"
        )

        print(
            f"Reason     : "
            f"{driver_strategy.get('reason')}"
        )

    else:

        print(
            "No strategy found for VER."
        )

    # --------------------------------------------------------
    # FULL RESPONSE TEST
    # --------------------------------------------------------

    print("\nFull API Response Test")
    print("-" * 40)

    full_response = (

        api.get_full_response()

    )

    print(
        f"Response Keys: "
        f"{list(full_response.keys())}"
    )

    # --------------------------------------------------------
    # FINAL TEST
    # --------------------------------------------------------

    print(
        "\n" + "=" * 100
    )

    print(
        "STEP 7.7 LIVE STRATEGY API TEST PASSED"
    )

    print(
        "=" * 100
    )