from src.data_loader import load_session
from src.race_state import build_race_state
from src.strategy.decision_engine import get_decision_from_race_state


# ============================================================
# STEP 10C - MULTI-RACE VALIDATION
# ============================================================

SEASON = 2025

SESSION_TYPE = "R"

TEST_RACES = [

    {
        "grand_prix": "Bahrain Grand Prix",
        "driver": "VER"
    },

    {
        "grand_prix": "Japanese Grand Prix",
        "driver": "VER"
    },

    {
        "grand_prix": "British Grand Prix",
        "driver": "VER"
    },

    {
        "grand_prix": "Belgian Grand Prix",
        "driver": "VER"
    },

    {
        "grand_prix": "Italian Grand Prix",
        "driver": "VER"
    }

]


# ============================================================
# HEADER
# ============================================================

print("=" * 80)

print("V5 STEP 10C - MULTI-RACE STRATEGY VALIDATION")

print("=" * 80)

print(f"Season: {SEASON}")

print(f"Session: {SESSION_TYPE}")

print(
    f"Number of races: "
    f"{len(TEST_RACES)}"
)

print("=" * 80)


# ============================================================
# RESULTS
# ============================================================

results = []


# ============================================================
# TEST EACH RACE
# ============================================================

for index, test_case in enumerate(
    TEST_RACES,
    start=1
):

    grand_prix = test_case[
        "grand_prix"
    ]

    driver = test_case[
        "driver"
    ]


    print("\n")

    print("-" * 80)

    print(
        f"[{index}/{len(TEST_RACES)}] "
        f"Testing {grand_prix} - {driver}"
    )

    print("-" * 80)


    try:

        # ----------------------------------------------------
        # LOAD SESSION
        # ----------------------------------------------------

        print(
            "Loading FastF1 session..."
        )

        session = load_session(

            SEASON,

            grand_prix,

            SESSION_TYPE

        )


        if session is None:

            raise RuntimeError(

                "Failed to load FastF1 session."

            )


        # ----------------------------------------------------
        # BUILD RACE STATE
        # ----------------------------------------------------

        print(
            "Building race state..."
        )

        race_state = build_race_state(

            session,

            driver

        )


        if not race_state:

            raise RuntimeError(

                "Race state generation returned empty data."

            )


        # ----------------------------------------------------
        # RUN DECISION ENGINE
        # ----------------------------------------------------

        print(
            "Running strategy engine..."
        )

        result = get_decision_from_race_state(

            race_state

        )


        if not result:

            raise RuntimeError(

                "Decision engine returned empty result."

            )


        # ----------------------------------------------------
        # EXTRACT VALUES
        # ----------------------------------------------------

        pit_probability = result.get(

            "pit_probability"

        )

        final_decision = result.get(

            "final_decision"

        )

        simulator_recommendation = result.get(

            "simulator_recommendation"

        )

        confidence = result.get(

            "confidence"

        )

        current_lap = result.get(

            "current_lap"

        )

        laps_remaining = result.get(

            "laps_remaining"

        )

        tyre_compound = result.get(

            "tyre_compound"

        )


        # ----------------------------------------------------
        # SAVE RESULT
        # ----------------------------------------------------

        results.append({

            "grand_prix":

                grand_prix,

            "driver":

                driver,

            "current_lap":

                current_lap,

            "laps_remaining":

                laps_remaining,

            "tyre_compound":

                tyre_compound,

            "pit_probability":

                pit_probability,

            "simulator_recommendation":

                simulator_recommendation,

            "final_decision":

                final_decision,

            "confidence":

                confidence

        })


        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------

        print(
            "\nStatus: PASS"
        )

        print(

            f"Current Lap: "
            f"{current_lap}"

        )

        print(

            f"Laps Remaining: "
            f"{laps_remaining}"

        )

        print(

            f"Tyre: "
            f"{tyre_compound}"

        )

        print(

            f"Pit Probability: "
            f"{pit_probability}%"

        )

        print(

            f"Simulator: "
            f"{simulator_recommendation}"

        )

        print(

            f"Final Decision: "
            f"{final_decision}"

        )

        print(

            f"Confidence: "
            f"{confidence}"

        )


    except Exception as e:

        print(
            "\nStatus: FAIL"
        )

        print(
            f"Error: {e}"
        )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")

print("=" * 80)

print(
    "MULTI-RACE VALIDATION SUMMARY"
)

print("=" * 80)


for result in results:

    print(

        f"{result['grand_prix']:<30} | "

        f"Lap: "
        f"{str(result['current_lap']):>3} | "

        f"Remaining: "
        f"{str(result['laps_remaining']):>3} | "

        f"Pit Probability: "
        f"{result['pit_probability']:.4f}% | "

        f"Final: "
        f"{result['final_decision']:<10} | "

        f"Confidence: "
        f"{result['confidence']}"

    )


# ============================================================
# DECISION DIVERSITY
# ============================================================

decisions = [

    result[
        "final_decision"
    ]

    for result in results

]


unique_decisions = set(

    decisions

)


print("\n")

print(
    f"Unique final decisions: "
    f"{unique_decisions}"
)


print(
    f"Number of unique decisions: "
    f"{len(unique_decisions)}"
)


# ============================================================
# VALIDATION
# ============================================================

print("\n")

print("=" * 80)


if len(results) == len(TEST_RACES):

    print(
        "✅ ALL MULTI-RACE TESTS EXECUTED SUCCESSFULLY"
    )

else:

    print(
        "⚠️ SOME MULTI-RACE TESTS FAILED"
    )

    print(

        f"Successful: "
        f"{len(results)}/"
        f"{len(TEST_RACES)}"

    )


print("=" * 80)