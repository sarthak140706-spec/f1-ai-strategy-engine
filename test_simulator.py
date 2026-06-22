import pandas as pd

from src.predict import predict_pit_probability
from src.simulator import simulate_strategy


sample = pd.DataFrame([{
    "LapNumber": 30,
    "TyreLife": 18,
    "Position": 5,
    "LapsRemaining": 27,
    "RaceProgress": 0.53,
    "AvgPaceLast3": 93.2,
    "AvgPaceLast5": 93.4,
    "AvgPaceLast10": 93.7,
    "DegradationRate": 0.4,
    "CurrentStintLength": 18,
    "PitStopsCompleted": 1
}])


probability = predict_pit_probability(sample)

result = simulate_strategy(
    sample.iloc[0]
)

print("\nPit Probability:", probability, "%")

print("\nStrategy Simulation:")

for key, value in result.items():
    print(f"{key}: {value}")