"""
Live Strategy Orchestrator

Sprint 7 - Step 6
F1 AI Strategist V5

Main orchestration layer that connects:

    Live Race State
            ↓
    Live Event Detector
            ↓
    Strategy Decision Engine
            ↓
    Live Strategy Simulator

This module provides a single interface for
running the complete live strategy pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any

import pandas as pd
import fastf1

from .live_race_state import (
    LiveRaceState,
    DriverRaceState
)

from .live_event_detector import (
    LiveEventDetector,
    RaceEvent
)

from .strategy_decision_engine import (
    StrategyDecisionEngine,
    StrategyDecision
)

from .live_strategy_simulator import (
    LiveStrategySimulator,
)


# ==========================================================
# ORCHESTRATOR SNAPSHOT
# ==========================================================

@dataclass
class OrchestratorSnapshot:

    timestamp: datetime

    lap_number: int

    drivers: int

    events: int

    strategies: int

    actions: Dict[str, int]


# ==========================================================
# LIVE STRATEGY ORCHESTRATOR
# ==========================================================

class LiveStrategyOrchestrator:

    """
    Main controller for the complete live
    F1 strategy pipeline.
    """

    def __init__(

        self,

        session

    ):

        if session is None:

            raise ValueError(
                "session cannot be None."
            )

        self.session = session

        # --------------------------------------------------
        # CORE COMPONENTS
        # --------------------------------------------------

        self.race_state = LiveRaceState(

            session

        )

        self.event_detector = (
            LiveEventDetector()
        )

        self.strategy_engine = (
            StrategyDecisionEngine()
        )

        self.simulator = (
            LiveStrategySimulator(

                session

            )
        )

        # --------------------------------------------------
        # CURRENT DATA
        # --------------------------------------------------

        self.current_state: Dict[
            str,
            DriverRaceState
        ] = {}

        self.current_events: List[
            RaceEvent
        ] = []

        self.current_strategies: Dict[
            str,
            StrategyDecision
        ] = {}

        # --------------------------------------------------
        # HISTORY
        # --------------------------------------------------

        self.history: List[
            OrchestratorSnapshot
        ] = []

        self.initialized = False

    # ------------------------------------------------------
    # INITIALIZE
    # ------------------------------------------------------

    def initialize(self):

        """
        Initialize the complete strategy pipeline.
        """

        print(
            "Initializing Live Strategy Orchestrator..."
        )

        # Build initial race state

        self.current_state = (
            self.race_state.update()
        )

        # No previous snapshot exists yet

        self.current_events = []

        # Generate initial strategies

        self.current_strategies = (

            self.strategy_engine.evaluate(

                self.current_state,

                self.current_events

            )

        )

        self.initialized = True

        self._record_snapshot()

        return self.current_strategies

        # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------

    def update(self):

        """
        Run one complete live strategy update cycle.

        Pipeline:

            1. Refresh race state
            2. Detect race events
            3. Generate strategy decisions
            4. Record snapshot
        """

        if not self.initialized:

            self.initialize()

        # --------------------------------------------------
        # SAVE PREVIOUS STATE
        # --------------------------------------------------

        previous_state = (

            self.current_state.copy()

        )

        # --------------------------------------------------
        # REFRESH RACE STATE
        # --------------------------------------------------

        self.current_state = (

            self.race_state.update()

        )

        # --------------------------------------------------
        # DETECT EVENTS
        # --------------------------------------------------

        try:

            events = (

                self.event_detector.detect_events(

                    previous_state,

                    self.current_state

                )

            )

            if events is None:

                events = []

            self.current_events = events

        except Exception as e:

            print(

                f"Event detection failed: {e}"

            )

            self.current_events = []

        # --------------------------------------------------
        # GENERATE STRATEGY DECISIONS
        # --------------------------------------------------

        self.current_strategies = (

            self.strategy_engine.evaluate(

                self.current_state,

                self.current_events

            )

        )

        # --------------------------------------------------
        # RECORD SNAPSHOT
        # --------------------------------------------------

        self._record_snapshot()

        return self.current_strategies

    # --------------------------------------------------------
    # GET STRATEGIES
    # --------------------------------------------------------
        
    def get_strategies(
            self
    ):
        return self.current_strategies
    # ========================================================
    # GET RACE STATE
    # ========================================================

    def get_race_state(
        self
    ) -> List[DriverRaceState]:

        """
        Return the latest race state
        for all available drivers.
        """

        return list(

            self.current_race_state.values()

        )

    # --------------------------------------------------------
    # GET EVENTS
    # --------------------------------------------------------

    def get_events(
        self
    ) -> List[RaceEvent]:

        """
        Return all currently detected race events.
        """

        return (

            self.event_detector.get_events()

        )
    # ------------------------------------------------------
    # RECORD SNAPSHOT
    # ------------------------------------------------------

    def _record_snapshot(self):

        """
        Store a summary of the current
        orchestration cycle.
        """

        lap_numbers = [

            state.lap_number

            for state

            in self.current_state.values()

            if state.lap_number is not None

        ]

        current_lap = (

            max(lap_numbers)

            if lap_numbers

            else 0

        )

        action_counts = {}

        for decision in (

            self.current_strategies.values()

        ):

            action = decision.action

            action_counts[action] = (

                action_counts.get(

                    action,

                    0

                )

                + 1

            )

        snapshot = OrchestratorSnapshot(

            timestamp=datetime.now(),

            lap_number=current_lap,

            drivers=len(

                self.current_state

            ),

            events=len(

                self.current_events

            ),

            strategies=len(

                self.current_strategies

            ),

            actions=action_counts

        )

        self.history.append(

            snapshot

        )

    # ------------------------------------------------------
    # GET CURRENT STATE
    # ------------------------------------------------------

    def get_current_state(

        self

    ) -> Dict[str, DriverRaceState]:

        return self.current_state

    # ------------------------------------------------------
    # GET CURRENT EVENTS
    # ------------------------------------------------------

    def get_current_events(

        self

    ) -> List[RaceEvent]:

        return self.current_events

    # ------------------------------------------------------
    # GET CURRENT STRATEGIES
    # ------------------------------------------------------

    def get_current_strategies(

        self

    ) -> Dict[

        str,

        StrategyDecision

    ]:

        return self.current_strategies

    # ------------------------------------------------------
    # GET HISTORY
    # ------------------------------------------------------

    def get_history(

        self

    ) -> List[OrchestratorSnapshot]:

        return self.history

    # ------------------------------------------------------
    # STRATEGY DATAFRAME
    # ------------------------------------------------------

    def strategies_to_dataframe(

        self

    ) -> pd.DataFrame:

        if not self.current_strategies:

            return pd.DataFrame()

        rows = []

        for decision in (

            self.current_strategies.values()

        ):

            rows.append(

                asdict(

                    decision

                )

            )

        return pd.DataFrame(

            rows

        )

    # ------------------------------------------------------
    # EVENT SUMMARY
    # ------------------------------------------------------

    def event_summary(

        self

    ) -> Dict[str, Any]:

        if not self.current_events:

            return {

                "total_events": 0,

                "event_types": []

            }

        event_types = []

        for event in (

            self.current_events

        ):

            event_type = (

                event.event_type

            )

            if event_type not in event_types:

                event_types.append(

                    event_type

                )

        return {

            "total_events": len(

                self.current_events

            ),

            "event_types": event_types

        }

    # ------------------------------------------------------
    # STRATEGY SUMMARY
    # ------------------------------------------------------

    def strategy_summary(

        self

    ) -> Dict[str, Any]:

        action_counts = {}

        for decision in (

            self.current_strategies.values()

        ):

            action = decision.action

            action_counts[action] = (

                action_counts.get(

                    action,

                    0

                )

                + 1

            )

        return {

            "drivers": len(

                self.current_strategies

            ),

            "actions": action_counts

        }
    # --------------------------------------------------------
    # GET RACE STATE
    # --------------------------------------------------------

    def get_race_state(
        self
    ):
        """
        Return the latest race state
        for all available drivers.
        """

        return list(
            self.race_state.driver_states.values()
        )

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 100)
    print("V5 SPRINT 7 - STEP 6")
    print("LIVE STRATEGY ORCHESTRATOR")
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
    # CREATE ORCHESTRATOR
    # --------------------------------------------------------

    print(
        "\nCreating Live Strategy Orchestrator..."
    )

    orchestrator = LiveStrategyOrchestrator(
        session
    )

    # --------------------------------------------------------
    # INITIALIZE
    # --------------------------------------------------------

    print(
        "\nInitializing strategy pipeline..."
    )

    strategies = orchestrator.initialize()

    print(
        "Strategy pipeline initialized successfully."
    )

    # --------------------------------------------------------
    # FIRST SNAPSHOT
    # --------------------------------------------------------

    print("\nInitial Snapshot")
    print("-" * 40)

    history = orchestrator.get_history()

    if history:

        snapshot = history[-1]

        print(
            f"Lap       : {snapshot.lap_number}"
        )

        print(
            f"Drivers   : {snapshot.drivers}"
        )

        print(
            f"Events    : {snapshot.events}"
        )

        print(
            f"Strategies: {snapshot.strategies}"
        )

        print(
            f"Actions   : {snapshot.actions}"
        )

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    print(
        "\nRunning orchestrator update..."
    )

    orchestrator.update()

    print(
        "Orchestrator update completed."
    )

    # --------------------------------------------------------
    # UPDATED SNAPSHOT
    # --------------------------------------------------------

    print("\nUpdated Snapshot")
    print("-" * 40)

    history = orchestrator.get_history()

    if history:

        snapshot = history[-1]

        print(
            f"Lap       : {snapshot.lap_number}"
        )

        print(
            f"Drivers   : {snapshot.drivers}"
        )

        print(
            f"Events    : {snapshot.events}"
        )

        print(
            f"Strategies: {snapshot.strategies}"
        )

        print(
            f"Actions   : {snapshot.actions}"
        )

    # --------------------------------------------------------
    # EVENT SUMMARY
    # --------------------------------------------------------

    print("\nEvent Summary")
    print("-" * 40)

    event_summary = (

        orchestrator.event_summary()

    )

    print(
        f"Total Events : "
        f"{event_summary['total_events']}"
    )

    print(
        f"Event Types  : "
        f"{event_summary['event_types']}"
    )

    # --------------------------------------------------------
    # STRATEGY SUMMARY
    # --------------------------------------------------------

    print("\nStrategy Summary")
    print("-" * 40)

    strategy_summary = (

        orchestrator.strategy_summary()

    )

    print(
        f"Drivers : "
        f"{strategy_summary['drivers']}"
    )

    print(
        f"Actions : "
        f"{strategy_summary['actions']}"
    )

    # --------------------------------------------------------
    # STRATEGY DATAFRAME
    # --------------------------------------------------------

    print("\nStrategy DataFrame")
    print("-" * 40)

    dataframe = (

        orchestrator.strategies_to_dataframe()

    )

    if not dataframe.empty:

        print(

            dataframe[
                [
                    "driver",
                    "action",
                    "confidence",
                    "reason"
                ]
            ].to_string(

                index=False

            )

        )

    else:

        print(
            "No strategy data available."
        )

    # --------------------------------------------------------
    # FINAL TEST
    # --------------------------------------------------------

    print(
        "\n" + "=" * 100
    )

    print(
        "STEP 7.6 LIVE STRATEGY ORCHESTRATOR "
        "TEST PASSED"
    )

    print(
        "=" * 100
    )