"""
Live Strategy Simulator

Sprint 7 - Step 5
F1 AI Strategist V5

Combines

• Live Race State
• Event Detector
• Strategy Engine

into a continuous strategy simulator.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any

import pandas as pd
import fastf1

from .live_race_state import (
    LiveRaceState
)

from .live_event_detector import (
    LiveEventDetector,
    RaceEvent
)

from .strategy_decision_engine import (
    StrategyDecisionEngine,
    StrategyDecision
)


# ==========================================================
# SIMULATION SNAPSHOT
# ==========================================================

@dataclass
class SimulationSnapshot:

    timestamp: datetime

    lap_number: int

    strategies: Dict[
        str,
        StrategyDecision
    ]

    events: List[
        RaceEvent
    ]


# ==========================================================
# LIVE STRATEGY SIMULATOR
# ==========================================================

class LiveStrategySimulator:

    """
    Main real-time simulator.

    Every update performs

    Race State
          ↓
    Event Detection
          ↓
    Strategy Engine
          ↓
    Snapshot Storage
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

        self.state_builder = LiveRaceState(
            session
        )

        self.event_detector = (
            LiveEventDetector()
        )

        self.strategy_engine = (
            StrategyDecisionEngine()
        )

        self.snapshots: List[
            SimulationSnapshot
        ] = []

        self.previous_state = {}

        self.current_state = {}

        self.current_events = []

        self.current_strategies = {}

    # ------------------------------------------------------
    # INITIALIZE
    # ------------------------------------------------------

    def initialize(self):

        """
        Build first race snapshot.
        """

        self.current_state = (
            self.state_builder.update()
        )

        self.previous_state = dict(
            self.current_state
        )

        self.current_events = []

        self.current_strategies = (
            self.strategy_engine.evaluate(

                self.current_state,

                []

            )

        )

        snapshot = SimulationSnapshot(

            timestamp=datetime.now(),

            lap_number=self._current_lap(),

            strategies=self.current_strategies,

            events=[]

        )

        self.snapshots.append(
            snapshot
        )
        # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------

    def update(self):

        """
        Refresh simulator state.
        """

        self.previous_state = dict(
            self.current_state
        )

        self.current_state = (
            self.state_builder.update()
        )

        self.current_events = (
            self.event_detector.detect_events(

                self.previous_state,

                self.current_state

            )
        )

        self.current_strategies = (
            self.strategy_engine.evaluate(

                self.current_state,

                self.current_events

            )
        )

        snapshot = SimulationSnapshot(

            timestamp=datetime.now(),

            lap_number=self._current_lap(),

            strategies=dict(
                self.current_strategies
            ),

            events=list(
                self.current_events
            )

        )

        self.snapshots.append(
            snapshot
        )

        return snapshot

    # ------------------------------------------------------
    # CURRENT LAP
    # ------------------------------------------------------

    def _current_lap(
        self
    ) -> int:

        laps = []

        for state in self.current_state.values():

            if state.lap_number is not None:

                laps.append(
                    state.lap_number
                )

        if not laps:

            return 0

        return max(laps)

    # ------------------------------------------------------
    # GETTERS
    # ------------------------------------------------------

    def get_current_state(self):

        return self.current_state

    def get_current_events(self):

        return self.current_events

    def get_current_strategies(self):

        return self.current_strategies

    def get_snapshots(self):

        return self.snapshots

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    def summary(
        self
    ) -> Dict[str, Any]:

        actions = {}

        for decision in self.current_strategies.values():

            actions[
                decision.action
            ] = actions.get(

                decision.action,

                0

            ) + 1

        return {

            "lap":

                self._current_lap(),

            "drivers":

                len(
                    self.current_state
                ),

            "events":

                len(
                    self.current_events
                ),

            "snapshots":

                len(
                    self.snapshots
                ),

            "actions":

                actions

        }

    # ------------------------------------------------------
    # DATAFRAME
    # ------------------------------------------------------

    def to_dataframe(
        self
    ) -> pd.DataFrame:

        rows = []

        for decision in self.current_strategies.values():

            rows.append(

                asdict(
                    decision
                )

            )

        return pd.DataFrame(
            rows
        )

# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    print(
        "=" * 100
    )

    print(
        "V5 SPRINT 7 - STEP 5"
    )

    print(
        "LIVE STRATEGY SIMULATOR"
    )

    print(
        "=" * 100
    )

    # ------------------------------------------------------
    # LOAD SESSION
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # CREATE SIMULATOR
    # ------------------------------------------------------

    print(
        "\nCreating strategy simulator..."
    )

    simulator = LiveStrategySimulator(

        session

    )

    # ------------------------------------------------------
    # INITIALIZE
    # ------------------------------------------------------

    print(
        "\nInitializing simulator..."
    )

    simulator.initialize()

    print(
        "Simulator initialized successfully."
    )

    # ------------------------------------------------------
    # FIRST SNAPSHOT
    # ------------------------------------------------------

    print(
        "\nFirst Snapshot"
    )

    print(
        "-" * 40
    )

    summary = simulator.summary()

    print(
        f"Lap       : "
        f"{summary['lap']}"
    )

    print(
        f"Drivers   : "
        f"{summary['drivers']}"
    )

    print(
        f"Events    : "
        f"{summary['events']}"
    )

    print(
        f"Snapshots : "
        f"{summary['snapshots']}"
    )

    print(
        f"Actions   : "
        f"{summary['actions']}"
    )

    # ------------------------------------------------------
    # SIMULATE UPDATE
    # ------------------------------------------------------

    print(
        "\nRunning simulator update..."
    )

    snapshot = simulator.update()

    print(
        "Simulator update completed."
    )

    # ------------------------------------------------------
    # UPDATED SNAPSHOT
    # ------------------------------------------------------

    print(
        "\nUpdated Snapshot"
    )

    print(
        "-" * 40
    )

    summary = simulator.summary()

    print(
        f"Lap       : "
        f"{summary['lap']}"
    )

    print(
        f"Drivers   : "
        f"{summary['drivers']}"
    )

    print(
        f"Events    : "
        f"{summary['events']}"
    )

    print(
        f"Snapshots : "
        f"{summary['snapshots']}"
    )

    print(
        f"Actions   : "
        f"{summary['actions']}"
    )

    # ------------------------------------------------------
    # STRATEGY OUTPUT
    # ------------------------------------------------------

    print(
        "\nCurrent Strategies"
    )

    print(
        "-" * 120
    )

    print(

        f"{'Driver':<8}"

        f"{'Action':<18}"

        f"{'Confidence':<12}"

        f"{'Tyre':<10}"

        f"{'Pace':<10}"

        f"{'Traffic':<10}"

        f"{'Risk':<10}"

    )

    print(
        "-" * 120
    )

    for decision in sorted(

        simulator.get_current_strategies().values(),

        key=lambda x:
        x.driver

    ):

        print(

            f"{decision.driver:<8}"

            f"{decision.action:<18}"

            f"{decision.confidence:<12.1f}"

            f"{decision.tyre_score:<10.1f}"

            f"{decision.pace_score:<10.1f}"

            f"{decision.traffic_score:<10.1f}"

            f"{decision.risk_score:<10.1f}"

        )

    # ------------------------------------------------------
    # EVENTS
    # ------------------------------------------------------

    print(
        "\nDetected Events"
    )

    print(
        "-" * 40
    )

    events = simulator.get_current_events()

    if events:

        for event in events:

            print(
                event
            )

    else:

        print(
            "No race events detected."
        )

    # ------------------------------------------------------
    # DATAFRAME TEST
    # ------------------------------------------------------

    print(
        "\nStrategy DataFrame"
    )

    print(
        "-" * 40
    )

    dataframe = simulator.to_dataframe()

    print(
        dataframe.to_string(
            index=False
        )
    )

    # ------------------------------------------------------
    # FINAL TEST
    # ------------------------------------------------------

    print(
        "\n"

        + "=" * 100
    )

    print(
        "STEP 7.5 LIVE STRATEGY SIMULATOR TEST PASSED"
    )

    print(
        "=" * 100
    )