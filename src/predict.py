import joblib
import pandas as pd

from src.strategy.decision_engine import get_strategy_decision

# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------
MODEL_PATH = "models/pit_strategy_model.pkl"
model = joblib.load(MODEL_PATH)


# -----------------------------
# PREDICT PIT PROBABILITY
# -----------------------------
def predict_pit_probability(data: pd.DataFrame):

    probability = model.predict_proba(data)[0][1]
    return round(probability * 100, 2)


# -----------------------------
# RUN FULL STRATEGY PIPELINE
# -----------------------------
def run_prediction():

    print("\n======================================")
    print("🏎️ F1 AI STRATEGIST - V4 PREDICTOR")
    print("======================================\n")

    # -----------------------------
    # SAMPLE INPUT (replace with live data later)
    # -----------------------------
    race_state = pd.DataFrame([{
        "LapNumber": 28,
        "TyreLife": 18,
        "Position": 2,
        "LapsRemaining": 15,
        "RaceProgress": 0.65,
        "AvgPaceLast3": 92.3,
        "AvgPaceLast5": 92.5,
        "AvgPaceLast10": 92.8,
        "DegradationRate": 0.45,
        "CurrentStintLength": 12,
        "PitStopsCompleted": 1
    }])

    # -----------------------------
    # ML PREDICTION
    # -----------------------------
    pit_prob = predict_pit_probability(race_state)

    print(f"📊 Pit Stop Probability: {pit_prob} %")

    # -----------------------------
    # STRATEGY ENGINE (V4 CORE)
    # -----------------------------
    strategy = get_strategy_decision(
        track="Monaco",
        driver="Verstappen",
        tyre_compound="Soft",
        predicted_lap_time=92.4,
        laps_remaining=15
    )

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    print("\n🧠 Strategy Decision Engine Output:")
    print("--------------------------------------")
    print(f"Stay Out Time : {strategy['stay_out_time']}")
    print(f"Pit Now Time  : {strategy['pit_now_time']}")
    print(f"Delta         : {strategy['delta']}")
    print(f"Decision      : {strategy['recommendation']}")
    print(f"Confidence    : {strategy['confidence']}")
    print("--------------------------------------\n")


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_prediction()