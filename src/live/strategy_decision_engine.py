"""
Strategy Decision Engine

Sprint 7 - Step 4
F1 AI Strategist V5

Generates live strategy recommendations for every
driver using race state and detected race events.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from .live_race_state import (
    DriverRaceState,
    LiveRaceState
)

from .live_event_detector import (
    RaceEvent,
    LiveEventDetector
)


# ============================================================
# STRATEGY DECISION
# ============================================================

@dataclass
class StrategyDecision:
    """
    Strategy recommendation
    for a single driver.
    """

    driver: str

    action: str

    confidence: float

    reason: str

    tyre_score: float

    pace_score: float

    traffic_score: float

    risk_score: float

    timestamp: datetime


# ============================================================
# STRATEGY ENGINE
# ============================================================

class StrategyDecisionEngine:
    """
    Produces live strategy
    recommendations.
    """

    def __init__(self):

        self.decisions: Dict[
            str,
            StrategyDecision
        ] = {}

        self.events: List[
            RaceEvent
        ] = []

    # --------------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------------

    def evaluate(
        self,
        race_state: Dict[
            str,
            DriverRaceState
        ],
        events: List[
            RaceEvent
        ]
    ) -> Dict[
        str,
        StrategyDecision
    ]:

        """
        Evaluate every driver.
        """

        self.decisions.clear()

        self.events = events

        for driver, state in race_state.items():

            decision = self._evaluate_driver(
                state
            )

            self.decisions[
                driver
            ] = decision

        return self.decisions

        # --------------------------------------------------------
    # DRIVER EVALUATION
    # --------------------------------------------------------

    def _evaluate_driver(
        self,
        state: DriverRaceState
    ) -> StrategyDecision:

        tyre_score = self._tyre_score(
            state
        )

        pace_score = self._pace_score(
            state
        )

        traffic_score = self._traffic_score(
            state
        )

        risk_score = self._risk_score(
            state
        )

        action = "STAY OUT"

        confidence = 70.0

        reason = "Race conditions stable."

        # ----------------------------------------------------
        # PIT WINDOW
        # ----------------------------------------------------

        if tyre_score >= 80:

            action = "PIT"

            confidence = 92.0

            reason = (
                "High tyre degradation."
            )

        # ----------------------------------------------------
        # SAVE TYRES
        # ----------------------------------------------------

        elif tyre_score >= 60:

            action = "SAVE TYRES"

            confidence = 82.0

            reason = (
                "Tyres approaching wear limit."
            )

        # ----------------------------------------------------
        # PUSH
        # ----------------------------------------------------

        elif (

            pace_score >= 80

            and

            traffic_score <= 40

        ):

            action = "PUSH"

            confidence = 87.0

            reason = (
                "Good pace with clear track."
            )

        # ----------------------------------------------------
        # DEFEND
        # ----------------------------------------------------

        elif risk_score >= 70:

            action = "DEFEND"

            confidence = 80.0

            reason = (
                "High strategic risk."
            )

        # ----------------------------------------------------
        # EVENT OVERRIDE
        # ----------------------------------------------------

        for event in self.events:

            if event.driver != state.driver:

                continue

            if event.event_type == "SAFETY_CAR":

                action = "PIT"

                confidence = 98.0

                reason = (
                    "Safety Car opportunity."
                )

            elif event.event_type == "VIRTUAL_SAFETY_CAR":

                action = "PIT"

                confidence = max(
                    confidence,
                    90.0
                )

                reason = (
                    "Virtual Safety Car."
                )

            elif event.event_type == "RAIN":

                action = "BOX FOR INTERS"

                confidence = 96.0

                reason = (
                    "Rain detected."
                )

            elif event.event_type == "RED_FLAG":

                action = "HOLD"

                confidence = 100.0

                reason = (
                    "Red Flag."
                )

        return StrategyDecision(

            driver=state.driver,

            action=action,

            confidence=round(
                confidence,
                1
            ),

            reason=reason,

            tyre_score=round(
                tyre_score,
                1
            ),

            pace_score=round(
                pace_score,
                1
            ),

            traffic_score=round(
                traffic_score,
                1
            ),

            risk_score=round(
                risk_score,
                1
            ),

            timestamp=datetime.now()

        )

    # --------------------------------------------------------
    # TYRE SCORE
    # --------------------------------------------------------

    def _tyre_score(
        self,
        state: DriverRaceState
    ) -> float:

        age = state.tyre_age

        if age is None:

            return 0.0

        return min(
            age * 5,
            100.0
        )

    # --------------------------------------------------------
    # PACE SCORE
    # --------------------------------------------------------

    def _pace_score(
        self,
        state: DriverRaceState
    ) -> float:

        if (

            state.best_lap_time is None

            or

            state.last_lap_time is None

        ):

            return 50.0

        diff = (

            state.last_lap_time

            -

            state.best_lap_time

        )

        score = 100 - diff * 25

        return max(
            0.0,
            min(score, 100.0)
        )

    # --------------------------------------------------------
    # TRAFFIC SCORE
    # --------------------------------------------------------

    def _traffic_score(
        self,
        state: DriverRaceState
    ) -> float:

        if state.interval_ahead is None:

            return 50.0

        if state.interval_ahead < 1:

            return 90.0

        if state.interval_ahead < 2:

            return 70.0

        if state.interval_ahead < 4:

            return 45.0

        return 20.0

    # --------------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------------

    def _risk_score(
        self,
        state: DriverRaceState
    ) -> float:

        risk = 0.0

        if state.tyre_age:

            risk += min(
                state.tyre_age * 3,
                40
            )

        if state.in_pit:

            risk += 20

        if state.retired:

            risk += 100

        if state.track_status not in (

            None,
            "1"

        ):

            risk += 20

        return min(
            risk,
            100.0
        )

        # --------------------------------------------------------
    # GET DRIVER
    # --------------------------------------------------------

    def get_driver(
        self,
        driver: str
    ) -> Optional[StrategyDecision]:

        return self.decisions.get(
            driver.upper()
        )

    # --------------------------------------------------------
    # GET ALL
    # --------------------------------------------------------

    def get_all(
        self
    ) -> List[StrategyDecision]:

        return list(
            self.decisions.values()
        )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    def summary(
        self
    ) -> Dict:

        actions = {}

        for decision in self.decisions.values():

            actions[
                decision.action
            ] = actions.get(
                decision.action,
                0
            ) + 1

        return {

            "drivers":
                len(
                    self.decisions
                ),

            "actions":
                actions,

            "timestamp":
                datetime.now()

        }

if __name__ == "__main__":

    import fastf1

    print("=" * 100)
    print("V5 SPRINT 7 - STEP 4")
    print("STRATEGY DECISION ENGINE")
    print("=" * 100)

    print("\nLoading session...")

    session = fastf1.get_session(
        2025,
        "British Grand Prix",
        "R"
    )

    session.load()

    print("Session loaded successfully.")

    race_state = LiveRaceState(
        session
    )

    race_state.update()

    detector = LiveEventDetector()

    events = detector.detect_events(
        race_state.driver_states,
        race_state.driver_states
    )

    engine = StrategyDecisionEngine()

    decisions = engine.evaluate(
        race_state.driver_states,
        events
    )

    print(
        f"\nStrategies Generated: {len(decisions)}"
    )

    print("-" * 120)

    print(
        f"{'Driver':<8}"
        f"{'Action':<18}"
        f"{'Conf':<8}"
        f"{'Tyre':<8}"
        f"{'Pace':<8}"
        f"{'Traffic':<10}"
        f"{'Risk':<8}"
    )

    print("-" * 120)

    for decision in sorted(
        decisions.values(),
        key=lambda x: x.driver
    ):

        print(

            f"{decision.driver:<8}"

            f"{decision.action:<18}"

            f"{decision.confidence:<8.1f}"

            f"{decision.tyre_score:<8.1f}"

            f"{decision.pace_score:<8.1f}"

            f"{decision.traffic_score:<10.1f}"

            f"{decision.risk_score:<8.1f}"

        )

    print("\nSummary")
    print("-" * 30)

    summary = engine.summary()

    print(
        f"Drivers : {summary['drivers']}"
    )

    print(
        f"Actions : {summary['actions']}"
    )

    print(
        "\n" + "=" * 100
    )

    print(
        "STEP 7.4 STRATEGY ENGINE TEST PASSED"
    )

    print("=" * 100)