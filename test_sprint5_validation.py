"""
Sprint 5 Final Validation Test

Validates complete race awareness pipeline.
"""


from src.data_loader import (
    load_session
)

from src.race_state import (
    build_race_state
)

from src.strategy.decision_engine import (
    get_decision_from_race_state
)



# ============================================================
# CONFIGURATION
# ============================================================

SEASON = 2025

GRAND_PRIX = (
    "British Grand Prix"
)

SESSION_TYPE = "R"

DRIVER = "VER"



# ============================================================
# VALIDATION
# ============================================================


def run_sprint5_validation():


    print(
        "=" * 70
    )

    print(
        "V5 SPRINT 5 FINAL VALIDATION TEST"
    )

    print(
        "=" * 70
    )


    # --------------------------------------------------------
    # Load Session
    # --------------------------------------------------------

    print(
        "\n[1/5] Loading FastF1 session..."
    )


    session = load_session(

        SEASON,

        GRAND_PRIX,

        SESSION_TYPE

    )


    assert session is not None


    print(
        "✓ Session loaded"
    )


    # --------------------------------------------------------
    # Build Race State
    # --------------------------------------------------------

    print(
        "\n[2/5] Building race state..."
    )


    race_state = build_race_state(

        session,

        DRIVER

    )


    assert isinstance(
        race_state,
        dict
    )


    print(
        "✓ Race state generated"
    )


    # --------------------------------------------------------
    # Run AI Strategy
    # --------------------------------------------------------

    print(
        "\n[3/5] Running AI strategy engine..."
    )


    result = get_decision_from_race_state(

        race_state

    )


    assert isinstance(
        result,
        dict
    )


    print(
        "✓ Strategy generated"
    )


    # --------------------------------------------------------
    # Validate Sprint 5 Modules
    # --------------------------------------------------------

    print(
        "\n[4/5] Checking Sprint 5 outputs..."
    )


    required_outputs = [

        "race_context_score",

        "race_situation",

        "context_confidence",

        "undercut_overcut",

        "ai_explanation"

    ]


    for field in required_outputs:


        assert field in result, (

            f"Missing output: {field}"

        )


        print(
            f"✓ {field}"
        )


    # --------------------------------------------------------
    # Final Check
    # --------------------------------------------------------

    print(
        "\n[5/5] Final validation..."
    )


    assert result[
        "final_decision"
    ] in [

        "PIT NOW",

        "STAY OUT"

    ]


    assert result[
        "confidence"
    ] in [

        "HIGH",

        "MEDIUM",

        "LOW"

    ]


    print(
        "✓ Decision output valid"
    )


    print(
        "\n"
        + "=" * 70
    )

    print(
        "🏁 SPRINT 5 VALIDATION PASSED"
    )

    print(
        "Sprint 5 is ready for freeze."
    )

    print(
        "=" * 70
    )



# ============================================================
# RUN
# ============================================================


if __name__ == "__main__":

    run_sprint5_validation()