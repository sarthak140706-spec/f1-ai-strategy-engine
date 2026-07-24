import pandas as pd

from src.predict import (
    predict_pit_probability
)

from src.simulator import (
    simulate_strategy
)


# --------------------------------------------------
# SAMPLE RACE STATE
# --------------------------------------------------

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


# --------------------------------------------------
# PIT PROBABILITY
# --------------------------------------------------

probability = (

    predict_pit_probability(
        sample
    )

)


# --------------------------------------------------
# STRATEGY SIMULATION
# --------------------------------------------------

race_state = (
    sample.iloc[0]
)


result = simulate_strategy(

    current_lap=
        race_state[
            "LapNumber"
        ],

    tyre_life=
        race_state[
            "TyreLife"
        ],

    predicted_lap_time=
        race_state[
            "AvgPaceLast5"
        ],

    laps_remaining=
        race_state[
            "LapsRemaining"
        ],

    tyre_compound=
        "MEDIUM"

)


# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print(
    "\nPit Probability:",
    probability,
    "%"
)


print(
    "\nStrategy Simulation:"
)


for key, value in result.items():

    print(
        f"{key}: {value}"
    )