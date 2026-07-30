"""
recommendation_engine.py

Sprint 5 - Step 9

Generates human-readable F1 strategy explanations
from AI strategy decisions and race context.
"""

from typing import Dict


# ============================================================
# DECISION EXPLANATION
# ============================================================

def generate_strategy_explanation(
    decision_result: Dict
) -> str:
    """
    Generate an F1 strategist-style explanation.

    Parameters
    ----------
    decision_result : dict
        Final AI strategy output.

    Returns
    -------
    str
        Human-readable recommendation.
    """


    # --------------------------------------------------------
    # Extract Data
    # --------------------------------------------------------

    final_decision = decision_result.get(
        "final_decision",
        "UNKNOWN"
    )


    confidence = decision_result.get(
        "confidence",
        "UNKNOWN"
    )


    pit_probability = decision_result.get(
        "pit_probability",
        0
    )


    simulator_recommendation = decision_result.get(
        "simulator_recommendation",
        "UNKNOWN"
    )


    delta = decision_result.get(
        "delta",
        0
    )


    race_context_score = decision_result.get(
        "race_context_score",
        0
    )


    race_situation = decision_result.get(
        "race_situation",
        "UNKNOWN"
    )


    undercut_data = decision_result.get(
        "undercut_overcut",
        {}
    )


    recommendation = undercut_data.get(
        "Recommendation",
        "No undercut or overcut information available."
    )


    reasons = undercut_data.get(
        "Reason",
        []
    )


    # --------------------------------------------------------
    # Strategy Decision
    # --------------------------------------------------------

    if final_decision == "PIT NOW":

        action = (
            "The AI recommends pitting now to improve "
            "the expected race outcome."
        )

    elif final_decision == "STAY OUT":

        action = (
            "The AI recommends staying out and extending "
            "the current stint."
        )

    else:

        action = (
            "The AI strategy recommendation is uncertain."
        )


    # --------------------------------------------------------
    # Simulator Explanation
    # --------------------------------------------------------

    if simulator_recommendation == "PIT NOW":

        simulation_reason = (

            f"The strategy simulator predicts that pitting "
            f"provides an advantage of "
            f"{abs(delta):.2f} seconds."

        )

    else:

        simulation_reason = (

            f"The strategy simulator predicts that staying "
            f"out provides an advantage of "
            f"{abs(delta):.2f} seconds."

        )


    # --------------------------------------------------------
    # Context Explanation
    # --------------------------------------------------------

    context_reason = (

        f"Race conditions are evaluated as "
        f"{race_situation} with a context score of "
        f"{race_context_score}/100."

    )


    # --------------------------------------------------------
    # Undercut / Overcut Explanation
    # --------------------------------------------------------

    if reasons:

        opportunity_reason = (

            "Strategic factors considered: "
            +
            ", ".join(reasons)
            +
            "."

        )

    else:

        opportunity_reason = recommendation


    # --------------------------------------------------------
    # Final Explanation
    # --------------------------------------------------------

    explanation = (

        f"FINAL STRATEGY RECOMMENDATION: "
        f"{final_decision}\n\n"

        f"{action}\n\n"

        f"{simulation_reason}\n\n"

        f"{context_reason}\n\n"

        f"{opportunity_reason}\n\n"

        f"ML pit probability was "
        f"{pit_probability:.2f}%. "

        f"Overall strategy confidence is "
        f"{confidence}."

    )


    return explanation



# ============================================================
# DISPLAY FUNCTION
# ============================================================

def display_recommendation(
    explanation: str
) -> None:

    print("\n")
    print("=" * 70)

    print(
        "AI STRATEGY RECOMMENDATION"
    )

    print("=" * 70)

    print(
        explanation
    )

    print("=" * 70)



# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":


    sample_result = {


        "final_decision":
            "STAY OUT",


        "confidence":
            "HIGH",


        "pit_probability":
            0.05,


        "simulator_recommendation":
            "STAY OUT",


        "delta":
            -22.0,


        "race_context_score":
            65,


        "race_situation":
            "FAVOURABLE",


        "undercut_overcut":
        {

            "RecommendedAction":
                "OVERCUT",


            "Recommendation":
                "Stay out and extend the current stint.",


            "Reason":
            [

                "Large gap behind",

                "Low tyre degradation"

            ]

        }

    }


    result = generate_strategy_explanation(
        sample_result
    )


    display_recommendation(
        result
    )