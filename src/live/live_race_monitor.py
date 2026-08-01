import time
from datetime import datetime
from typing import Any, Dict, Optional

import fastf1


# ============================================================
# V5 SPRINT 7 - LIVE RACE MONITOR
# STEP 1: LIVE / NEAR-REAL-TIME MONITORING FOUNDATION
# ============================================================


class LiveRaceMonitor:
    """
    V5 Sprint 7 live / near-real-time race monitoring foundation.

    Responsibilities:
        1. Connect to a FastF1 session.
        2. Track the current monitoring state.
        3. Maintain the latest race snapshot.
        4. Detect changes in race information.
        5. Provide a clean interface for future
           live strategy decision updates.

    Note:
        FastF1 is primarily designed for accessing session data
        rather than providing a guaranteed live timing stream.
        Therefore, this class provides the monitoring architecture
        required for near-real-time strategy processing.
    """

    # --------------------------------------------------------
    # INITIALIZATION
    # --------------------------------------------------------

    def __init__(
        self,
        season: int,
        grand_prix: str,
        session_type: str = "R"
    ):
        """
        Initialize the live race monitor.

        Parameters
        ----------
        season : int
            F1 season year.

        grand_prix : str
            Grand Prix name.

        session_type : str
            Session identifier.
            Default: R (Race)
        """

        self.season = season
        self.grand_prix = grand_prix
        self.session_type = session_type

        self.session = None

        self.is_connected = False
        self.is_monitoring = False

        self.last_snapshot = None
        self.previous_snapshot = None

        self.last_update_time = None

    # --------------------------------------------------------
    # LOAD SESSION
    # --------------------------------------------------------

    def connect(self):
        """
        Load the FastF1 session.

        Returns
        -------
        FastF1 Session

        Raises
        ------
        RuntimeError
            If the session cannot be loaded.
        """

        try:

            print(
                "\nConnecting to FastF1 session..."
            )

            self.session = fastf1.get_session(
                self.season,
                self.grand_prix,
                self.session_type
            )

            self.session.load()

            self.is_connected = True

            self.last_update_time = (
                datetime.now()
            )

            print(
                "FastF1 session connected successfully."
            )

            return self.session

        except Exception as e:

            self.is_connected = False

            raise RuntimeError(
                "Failed to connect to FastF1 session: "
                f"{e}"
            ) from e

    # --------------------------------------------------------
    # VALIDATE CONNECTION
    # --------------------------------------------------------

    def _validate_connection(self):
        """
        Ensure that the monitor is connected
        to a FastF1 session.
        """

        if not self.is_connected:

            raise RuntimeError(
                "Live race monitor is not connected. "
                "Call connect() first."
            )

        if self.session is None:

            raise RuntimeError(
                "FastF1 session is unavailable."
            )

    # --------------------------------------------------------
    # GET CURRENT SESSION STATUS
    # --------------------------------------------------------

    def get_session_status(self) -> Dict[str, Any]:
        """
        Get the current session status.

        Returns
        -------
        dict
            Current monitoring status.
        """

        self._validate_connection()

        return {

            "season":
                self.season,

            "grand_prix":
                self.grand_prix,

            "session_type":
                self.session_type,

            "connected":
                self.is_connected,

            "monitoring":
                self.is_monitoring,

            "last_update":
                self.last_update_time

        }

    # --------------------------------------------------------
    # BUILD RACE SNAPSHOT
    # --------------------------------------------------------

    def build_snapshot(self) -> Dict[str, Any]:
        """
        Build a snapshot of the currently available
        session data.

        The snapshot is intentionally lightweight.
        Detailed driver-level race state will be integrated
        in later Sprint 7 steps.
        """

        self._validate_connection()

        snapshot = {

            "timestamp":
                datetime.now(),

            "season":
                self.season,

            "grand_prix":
                self.grand_prix,

            "session_type":
                self.session_type,

            "session_name":
                getattr(
                    self.session,
                    "name",
                    None
                ),

            "session_status":
                getattr(
                    self.session,
                    "status",
                    None
                ),

            "total_laps":
                getattr(
                    self.session,
                    "total_laps",
                    None
                )

        }

        return snapshot

    # --------------------------------------------------------
    # UPDATE SNAPSHOT
    # --------------------------------------------------------

    def update_snapshot(self) -> Dict[str, Any]:
        """
        Update the latest race snapshot.

        Returns
        -------
        dict
            Updated snapshot.
        """

        self._validate_connection()

        new_snapshot = (
            self.build_snapshot()
        )

        self.previous_snapshot = (
            self.last_snapshot
        )

        self.last_snapshot = (
            new_snapshot
        )

        self.last_update_time = (
            datetime.now()
        )

        return new_snapshot

    # --------------------------------------------------------
    # DETECT CHANGES
    # --------------------------------------------------------

    def detect_changes(
        self,
        current_snapshot: Optional[
            Dict[str, Any]
        ] = None
    ) -> Dict[str, Any]:
        """
        Detect changes between the previous
        and current snapshots.

        Returns
        -------
        dict
            Change information.
        """

        if current_snapshot is None:

            current_snapshot = (
                self.last_snapshot
            )

        if current_snapshot is None:

            return {

                "changed":
                    False,

                "changes":
                    {}

            }

        if self.previous_snapshot is None:

            return {

                "changed":
                    False,

                "changes":
                    {}

            }

        changes = {}

        for key in current_snapshot:

            if key == "timestamp":

                continue

            previous_value = (
                self.previous_snapshot.get(
                    key
                )
            )

            current_value = (
                current_snapshot.get(
                    key
                )
            )

            if (
                previous_value
                != current_value
            ):

                changes[key] = {

                    "previous":
                        previous_value,

                    "current":
                        current_value

                }

        return {

            "changed":
                bool(changes),

            "changes":
                changes

        }

    # --------------------------------------------------------
    # START MONITORING
    # --------------------------------------------------------

    def start_monitoring(
        self,
        interval: int = 30,
        iterations: int = 1
    ):
        """
        Start the near-real-time monitoring loop.

        Parameters
        ----------
        interval : int
            Number of seconds between monitoring cycles.

        iterations : int
            Number of monitoring cycles.

        Returns
        -------
        list
            List of collected snapshots.
        """

        self._validate_connection()

        if interval <= 0:

            raise ValueError(
                "interval must be greater than zero."
            )

        if iterations <= 0:

            raise ValueError(
                "iterations must be greater than zero."
            )

        self.is_monitoring = True

        snapshots = []

        try:

            for iteration in range(
                iterations
            ):

                print(
                    f"\nMonitoring cycle "
                    f"{iteration + 1}/"
                    f"{iterations}"
                )

                snapshot = (
                    self.update_snapshot()
                )

                snapshots.append(
                    snapshot
                )

                print(
                    "Snapshot updated successfully."
                )

                print(
                    f"Timestamp: "
                    f"{snapshot['timestamp']}"
                )

                if (
                    iteration
                    <
                    iterations - 1
                ):

                    time.sleep(
                        interval
                    )

        finally:

            self.is_monitoring = False

        return snapshots

    # --------------------------------------------------------
    # STOP MONITORING
    # --------------------------------------------------------

    def stop_monitoring(self):
        """
        Stop the monitoring loop.
        """

        self.is_monitoring = False

        print(
            "Live race monitoring stopped."
        )


# ============================================================
# SPRINT 7 STEP 1 TEST
# ============================================================

if __name__ == "__main__":

    print(
        "=" * 90
    )

    print(
        "V5 SPRINT 7 - STEP 1"
    )

    print(
        "LIVE / NEAR-REAL-TIME RACE MONITORING FOUNDATION"
    )

    print(
        "=" * 90
    )

    # --------------------------------------------------------
    # TEST CONFIGURATION
    # --------------------------------------------------------

    SEASON = 2025

    GRAND_PRIX = (
        "British Grand Prix"
    )

    SESSION_TYPE = "R"

    # --------------------------------------------------------
    # CREATE MONITOR
    # --------------------------------------------------------

    print(
        "\n[1/5] Creating live race monitor..."
    )

    monitor = LiveRaceMonitor(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        session_type=SESSION_TYPE

    )

    print(
        "Monitor created successfully."
    )

    # --------------------------------------------------------
    # CONNECT
    # --------------------------------------------------------

    print(
        "\n[2/5] Connecting to FastF1 session..."
    )

    monitor.connect()

    print(
        "Connection successful."
    )

    # --------------------------------------------------------
    # SESSION STATUS
    # --------------------------------------------------------

    print(
        "\n[3/5] Checking session status..."
    )

    status = (
        monitor.get_session_status()
    )

    print(
        f"Season: "
        f"{status['season']}"
    )

    print(
        f"Grand Prix: "
        f"{status['grand_prix']}"
    )

    print(
        f"Session: "
        f"{status['session_type']}"
    )

    print(
        f"Connected: "
        f"{status['connected']}"
    )

    # --------------------------------------------------------
    # BUILD INITIAL SNAPSHOT
    # --------------------------------------------------------

    print(
        "\n[4/5] Building initial race snapshot..."
    )

    snapshot = (
        monitor.update_snapshot()
    )

    print(
        "Snapshot created successfully."
    )

    print(
        f"Session Name: "
        f"{snapshot['session_name']}"
    )

    print(
        f"Session Status: "
        f"{snapshot['session_status']}"
    )

    print(
        f"Total Laps: "
        f"{snapshot['total_laps']}"
    )

    # --------------------------------------------------------
    # VERIFY MONITORING
    # --------------------------------------------------------

    print(
        "\n[5/5] Verifying monitoring state..."
    )

    print(
        f"Connected: "
        f"{monitor.is_connected}"
    )

    print(
        f"Monitoring: "
        f"{monitor.is_monitoring}"
    )

    print(
        "=" * 90
    )

    print(
        "\n✅ SPRINT 7 STEP 1 "
        "LIVE MONITORING FOUNDATION TEST PASSED"
    )

    print(
        "=" * 90
    )