import os
import joblib
import pandas as pd


MODEL_PATH = (
    "models/pit_strategy_model.pkl"
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

def load_model():

    if not os.path.exists(
        MODEL_PATH
    ):

        raise FileNotFoundError(

            f"Model not found at "
            f"{MODEL_PATH}. "

            "Run the training pipeline first."

        )

    return joblib.load(
        MODEL_PATH
    )


# --------------------------------------------------
# PREDICT PIT PROBABILITY
# --------------------------------------------------

def predict_pit_probability(
    data: pd.DataFrame
):

    model = load_model()

    probability = (

        model.predict_proba(
            data
        )[0][1]

    )

    return round(
        probability * 100,
        2
    )


# --------------------------------------------------
# PREDICT PIT DECISION
# --------------------------------------------------

def predict_pit_decision(
    data: pd.DataFrame,
    threshold: float = 50.0
):

    probability = (
        predict_pit_probability(
            data
        )
    )

    if probability >= threshold:

        decision = "PIT"

    else:

        decision = "STAY"

    return {

        "pit_probability":
            probability,

        "decision":
            decision

    }