"""
race_context.py

Sprint 5 - Step 2

Builds a unified race context and detects
Safety Car / Virtual Safety Car conditions.
"""

from typing import Dict, Any

from src.strategy.weather import detect_weather

from src.strategy.traffic import analyse_traffic

from src.strategy.gap_analysis import analyse_gaps

from src.strategy.undercut_overcut import analyse_undercut_overcut

# ============================================================
# SAFETY CAR DETECTION
# ============================================================

def detect_safety_car(
    session
) -> dict:
    """
    Detect Safety Car or Virtual Safety Car
    from FastF1 race control messages.
    """

    safety_car = False
    virtual_safety_car = False

    try:

        messages = session.race_control_messages

        if messages is not None and len(messages) > 0:

            latest = messages.iloc[-1]

            text = str(
                latest.get(
                    "Message",
                    ""
                )
            ).upper()

            if "SAFETY CAR" in text:

                if "VIRTUAL" in text:

                    virtual_safety_car = True

                else:

                    safety_car = True

    except Exception:

        pass

    return {

        "SafetyCar":
            safety_car,

        "VirtualSafetyCar":
            virtual_safety_car

    }


# ============================================================
# BUILD RACE CONTEXT
# ============================================================

def build_race_context(
    session,
    race_state: Dict[str, Any]
) -> Dict[str, Any]:

    if not isinstance(
        race_state,
        dict
    ):

        raise TypeError(
            "race_state must be a dictionary."
        )

    sc = detect_safety_car(
        session
    )

    context = {

        "Driver":
            race_state.get("Driver"),

        "Circuit":
            race_state.get("Circuit"),

        "CurrentLap":
            race_state.get("CurrentLap"),

        "Position":
            race_state.get("Position"),

        "TyreCompound":
            race_state.get("TyreCompound"),

        "TyreAge":
            race_state.get("TyreAge"),

        "AveragePace":
            race_state.get("AveragePace"),

        "AvgPaceLast5":
            race_state.get("AvgPaceLast5"),

        "LapsRemaining":
            race_state.get("LapsRemaining"),

        "AirTemp":
            race_state.get("AirTemp"),

        "TrackTemp":
            race_state.get("TrackTemp"),

        "Humidity":
            race_state.get("Humidity"),

        "Rainfall":
            race_state.get("Rainfall"),

        "SafetyCar":
            sc["SafetyCar"],

        "VirtualSafetyCar":
            sc["VirtualSafetyCar"],

        "TrafficAhead":
            None,

        "TrafficBehind":
            None,

        "GapAhead":
            None,

        "GapBehind":
            None,

        "UndercutAvailable":
            False,

        "OvercutAvailable":
            False

    }
    # --------------------------------------------------------
    # UPDATE WITH STEP 5–7 MODULES
    # --------------------------------------------------------
        # --------------------------------------------------------
    # STEP 5 - WEATHER
    # --------------------------------------------------------

    weather = detect_weather(

        session

    )

    # --------------------------------------------------------
    # STEP 6 - TRAFFIC
    # --------------------------------------------------------

    traffic = analyse_traffic(

        session,

        race_state

    )

    # --------------------------------------------------------
    # STEP 7 - GAP ANALYSIS
    # --------------------------------------------------------

    gaps = analyse_gaps(

        session,

        race_state

    )

    # --------------------------------------------------------
    # STEP 7 - UNDERCUT / OVERCUT
    # --------------------------------------------------------

    undercut = analyse_undercut_overcut(

        race_state,

        gaps

    )
    context.update(weather)

    context.update(traffic)

    context.update(gaps)

    context.update(undercut)

    return context


# ============================================================
# DISPLAY
# ============================================================

def display_race_context(
    context: Dict[str, Any]
) -> None:

    print("\n" + "=" * 60)
    print("RACE CONTEXT")
    print("=" * 60)

    for key, value in context.items():

        print(f"{key}: {value}")

    print("=" * 60)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    from src.data_loader import load_session
    from src.race_state import build_race_state

    print("=" * 60)
    print("SPRINT 5 - STEP 2 TEST")
    print("=" * 60)

    session = load_session(

        2025,

        "British Grand Prix",

        "R"

    )

    race_state = build_race_state(

        session,

        "VER"

    )

    context = build_race_context(

        session,

        race_state

    )

    display_race_context(

        context

    )

    print("=" * 60)
    print("STEP 2 COMPLETED")
    print("=" * 60)