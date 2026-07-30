import os
import json
import pandas as pd
import fastf1

from src.data_loader import load_race_data

from src.preprocessing import preprocess_data

from src.feature_engineering import (
    detect_pit_stops,
    create_race_features,
    create_target
)


# --------------------------------------------------
# PATHS
# --------------------------------------------------

DATASET_PATH = (
    "data/processed/f1_strategy_dataset.csv"
)

CHECKPOINT_PATH = (
    "data/processed/processed_races.json"
)


# --------------------------------------------------
# CHECKPOINT HELPERS
# --------------------------------------------------

def load_processed_races():

    if os.path.exists(CHECKPOINT_PATH):

        with open(
            CHECKPOINT_PATH,
            "r"
        ) as file:

            return json.load(file)

    return []


def save_processed_races(
    races
):

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    with open(
        CHECKPOINT_PATH,
        "w"
    ) as file:

        json.dump(
            races,
            file,
            indent=4
        )


# --------------------------------------------------
# DATASET BUILDER
# --------------------------------------------------

def build_dataset(
    seasons=None
):

    if seasons is None:

        seasons = [
            2022,
            2023,
            2024,
            2025
        ]


    os.makedirs(
        "data/processed",
        exist_ok=True
    )


    processed_races = load_processed_races()


    all_races = []


    # Load previous checkpoint

    if os.path.exists(DATASET_PATH):

        print(
            "📂 Existing dataset found. Loading..."
        )

        existing = pd.read_csv(
            DATASET_PATH
        )

        all_races.append(
            existing
        )


    for season in seasons:


        print(
            f"\n🏎️ Processing season: {season}"
        )


        schedule = (
            fastf1
            .get_event_schedule(
                season
            )
        )


        for race in schedule[
            "EventName"
        ]:


            race_id = (
                f"{season}-{race}"
            )


            if race_id in processed_races:

                print(
                    f"⏭️ Skipping cached race: {race_id}"
                )

                continue


            try:


                print(
                    f"Processing {season} - {race}"
                )


                df = load_race_data(
                    season,
                    race
                )


                df = preprocess_data(
                    df
                )


                df = detect_pit_stops(
                    df
                )


                df = create_race_features(
                    df
                )


                df = create_target(
                    df
                )


                df["Season"] = season

                df["Race"] = race


                all_races.append(
                    df
                )


                # -----------------------------
                # SAVE CHECKPOINT
                # -----------------------------

                dataset = pd.concat(
                    all_races,
                    ignore_index=True
                )


                dataset.to_csv(
                    DATASET_PATH,
                    index=False
                )


                processed_races.append(
                    race_id
                )


                save_processed_races(
                    processed_races
                )


                print(
                    "💾 Checkpoint saved"
                )


            except Exception as e:


                print(
                    f"Skipped {season} - {race}: {e}"
                )


    if not all_races:

        raise ValueError(
            "No race data was successfully loaded."
        )


    dataset = pd.concat(
        all_races,
        ignore_index=True
    )


    print(
        "\n✅ Dataset built successfully."
    )


    print(
        "Shape:",
        dataset.shape
    )


    return dataset