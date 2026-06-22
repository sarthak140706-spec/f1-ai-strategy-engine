import pandas as pd
import fastf1

from src.data_loader import load_race_data
from src.preprocessing import (
    clean_data,
    convert_time_features
)
from src.feature_engineering import (
    detect_pit_stops,
    create_race_features,
    create_target
)


def build_dataset(season=2025):

    schedule = fastf1.get_event_schedule(season)

    all_races = []

    for race in schedule["EventName"]:

        try:
            print(f"Processing {race}")

            df = load_race_data(season, race)

            df = clean_data(df)
            df = convert_time_features(df)

            df = detect_pit_stops(df)
            df = create_race_features(df)
            df = create_target(df)

            df["Season"] = season
            df["Race"] = race

            all_races.append(df)

        except Exception as e:
            print(f"Skipped {race}: {e}")

    dataset = pd.concat(
        all_races,
        ignore_index=True
    )

    required_columns = [
        "Driver",
        "Team",
        "LapNumber",
        "Position",
        "Compound",
        "TyreLife",
        "Stint",
        "TrackStatus",
        "LapTimeSeconds",
        "PitLap",
        "PitNextLap",
        "LapsRemaining",
        "RaceProgress",
        "AvgPaceLast3",
        "AvgPaceLast5",
        "AvgPaceLast10",
        "DegradationRate",
        "CurrentStintLength",
        "PitStopsCompleted",
        "Season",
        "Race"
    ]

    dataset = dataset[required_columns]

    dataset.to_csv(
        "data/processed/f1_2025_dataset.csv",
        index=False
    )

    return dataset