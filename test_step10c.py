from src.data_loader import load_session
from src.race_state import build_race_state
from src.strategy.decision_engine import get_decision_from_race_state


# ============================================================
# STEP 10C - MULTI-DRIVER VALIDATION
# ============================================================

SEASON = 2025

GRAND_PRIX = "British Grand Prix"

SESSION_TYPE = "R"

DRIVERS = [
    "VER",
    "HAM",
    "LEC",
    "ALO"
]


# ============================================================
# HEADER
# ============================================================

print("=" * 80)

print("V5 STEP 10C - MULTI-DRIVER STRATEGY VALIDATION")

print("=" * 80)

print(f"Season: {SEASON}")

print(f"Grand Prix: {GRAND_PRIX}")

print(f"Session: {SESSION_TYPE}")

print(f"Drivers: {', '.join(DRIVERS)}")

print("=" * 80)


# ============================================================
# LOAD SESSION ONCE
# ============================================================

print("\n[1/3] Loading FastF1 session...")

session = load_session(
    SEASON,
    GRAND_PRIX,
    SESSION_TYPE
)

if session is None:
    raise RuntimeError(
        "Failed to load FastF1 session."
    )

print("FastF1 session loaded successfully.")


# ============================================================
# TEST EACH DRIVER
# ============================================================

print("\n[2/3] Testing strategy engine for all drivers...")

results = []

for driver in DRIVERS:

    print("\n" + "-" * 80)

    print(f"Testing driver: {driver}")

    print("-" * 80)

    try:

        # ----------------------------------------------------
        # BUILD RACE STATE
        # ----------------------------------------------------

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

        result = get_decision_from_race_state(
            race_state
        )

        if not result:

            raise RuntimeError(
                "Decision engine returned empty result."
            )


        # ----------------------------------------------------
        # STORE RESULT
        # ----------------------------------------------------

        results.append({

            "driver":
                driver,

            "position":
                result.get("position"),

            "tyre":
                result.get("tyre_compound"),

            "current_lap":
                result.get("current_lap"),

            "laps_remaining":
                result.get("laps_remaining"),

            "pit_probability":
                result.get("pit_probability"),

            "simulator_recommendation":
                result.get(
                    "simulator_recommendation"
                ),

            "final_decision":
                result.get(
                    "final_decision"
                ),

            "confidence":
                result.get(
                    "confidence"
                ),

            "race_context":
                result.get(
                    "race_situation"
                )

        })


        print(
            "Status: PASS"
        )

        print(
            f"Position: "
            f"{result.get('position')}"
        )

        print(
            f"Tyre: "
            f"{result.get('tyre_compound')}"
        )

        print(
            f"Pit Probability: "
            f"{result.get('pit_probability')}%"
        )

        print(
            f"Simulator: "
            f"{result.get('simulator_recommendation')}"
        )

        print(
            f"Final Decision: "
            f"{result.get('final_decision')}"
        )

        print(
            f"Confidence: "
            f"{result.get('confidence')}"
        )

        print(
            f"Race Situation: "
            f"{result.get('race_situation')}"
        )


    except Exception as e:

        print(
            "Status: FAIL"
        )

        print(
            f"Error: {e}"
        )


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")

print("=" * 80)

print("[3/3] MULTI-DRIVER VALIDATION SUMMARY")

print("=" * 80)


for result in results:

    print(

        f"{result['driver']:>5} | "

        f"Position: "
        f"{str(result['position']):>3} | "

        f"Pit Probability: "
        f"{result['pit_probability']:.4f}% | "

        f"Simulator: "
        f"{result['simulator_recommendation']:<10} | "

        f"Final: "
        f"{result['final_decision']:<10} | "

        f"Confidence: "
        f"{result['confidence']}"

    )


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 80)

if len(results) == len(DRIVERS):

    print(
        "✅ STEP 10C - MULTI-DRIVER VALIDATION PASSED"
    )

else:

    print(
        "❌ STEP 10C - VALIDATION FAILED"
    )

    print(
        f"Successful drivers: "
        f"{len(results)}/{len(DRIVERS)}"
    )

print("=" * 80)