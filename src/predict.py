import joblib


import os
import joblib

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "pit_strategy_model.pkl"
)

pit_model = joblib.load(MODEL_PATH)


FEATURES = [
    "LapNumber",
    "TyreLife",
    "Position",
    "LapsRemaining",
    "RaceProgress",
    "AvgPaceLast3",
    "AvgPaceLast5",
    "AvgPaceLast10",
    "DegradationRate",
    "CurrentStintLength",
    "PitStopsCompleted"
]


def predict_pit_probability(data):

    X = data[FEATURES]

    probability = pit_model.predict_proba(X)[0][1]

    return round(probability * 100, 2)