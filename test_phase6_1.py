"""
F1 AI STRATEGIST
PHASE 6.1 — LIVE TIMING CLIENT TEST
"""


import os

import time


from src.live.live_timing_client import (

    F1LiveTimingClient,

    LIVE_TIMING_TOPICS,

    create_live_timing_client,

    display_live_timing_status

)


# ============================================================
# TEST CONFIGURATION
# ============================================================

OUTPUT_FILE = (
    "data/live/f1_live_timing.txt"
)


# Keep this short for the structural test.
TEST_TIMEOUT = 10


# ============================================================
# PHASE 6.1 TEST
# ============================================================

def main():

    print(
        "\n" + "=" * 78
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "PHASE 6.1 — LIVE TIMING CLIENT TEST"
    )

    print(
        "=" * 78
    )


    # ========================================================
    # STEP 1
    # CREATE LIVE DIRECTORY
    # ========================================================

    print(
        "\n[1/5] Preparing live timing directory..."
    )


    os.makedirs(

        os.path.dirname(
            OUTPUT_FILE
        ),

        exist_ok=True

    )


    assert os.path.isdir(
        "data/live"
    )


    print(
        "✅ Live timing directory ready."
    )


    # ========================================================
    # STEP 2
    # CREATE CLIENT
    # ========================================================

    print(
        "\n[2/5] Creating live timing client..."
    )


    client = create_live_timing_client(

        output_file=OUTPUT_FILE,

        timeout=TEST_TIMEOUT,

        no_auth=False

    )


    assert isinstance(

        client,

        F1LiveTimingClient

    )


    print(
        "✅ Live timing client created."
    )


    # ========================================================
    # STEP 3
    # VALIDATE FASTF1 LIVE SUPPORT
    # ========================================================

    print(
        "\n[3/5] Validating FastF1 live timing support..."
    )


    client.validate_environment()


    status = client.get_status()


    assert (
        status[
            "fastf1_live_available"
        ]
        is True
    )


    print(
        "✅ FastF1 live timing support available."
    )


    # ========================================================
    # STEP 4
    # VALIDATE LIVE TOPICS
    # ========================================================

    print(
        "\n[4/5] Validating live timing topics..."
    )


    required_topics = {

        "DriverList",

        "TimingData",

        "TimingAppData",

        "WeatherData",

        "TrackStatus",

        "RaceControlMessages",

        "LapCount"

    }


    available_topics = set(

        LIVE_TIMING_TOPICS

    )


    missing_topics = (

        required_topics
        -
        available_topics

    )


    assert not missing_topics, (

        "Missing required live timing topics: "
        f"{missing_topics}"

    )


    print(
        "✅ Required live timing topics configured."
    )


    # ========================================================
    # STEP 5
    # VALIDATE CLIENT STATUS CONTRACT
    # ========================================================

    print(
        "\n[5/5] Validating live timing client status..."
    )


    status = client.get_status()


    required_status_fields = {

        "phase",

        "component",

        "fastf1_live_available",

        "connected",

        "running",

        "thread_alive",

        "message_count",

        "last_message_time",

        "connection_error",

        "output_file",

        "authentication_disabled",

        "topics"

    }


    missing_fields = (

        required_status_fields
        -
        set(
            status.keys()
        )

    )


    assert not missing_fields, (

        "Missing status fields: "
        f"{missing_fields}"

    )


    assert (
        status["phase"]
        ==
        "6.1"
    )


    assert (
        status["component"]
        ==
        "live_timing_client"
    )


    assert isinstance(

        status["topics"],

        list

    )


    print(
        "✅ Live timing client status contract validated."
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    display_live_timing_status(
        client
    )


    # ========================================================
    # SUCCESS
    # ========================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "✅ PHASE 6.1 LIVE TIMING CLIENT STRUCTURAL TEST PASSED"
    )

    print(
        "=" * 78
    )


    print(
        "\nNOTE:"
    )

    print(
        "This test validates the Phase 6.1 live timing "
        "infrastructure."
    )

    print(
        "Actual timing messages can only be verified when "
        "the F1 live timing stream is available and "
        "authentication/network access succeeds."
    )


if __name__ == "__main__":

    main()