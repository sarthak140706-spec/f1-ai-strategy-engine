import joblib


pit_model = joblib.load(
    "models/pit_strategy_model.pkl"
)


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