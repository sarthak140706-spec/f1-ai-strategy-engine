import pandas as pd
import fastf1

from src.data_loader import load_race_data

from src.preprocessing import (
    preprocess_data
)

from src.feature_engineering import (
    detect_pit_stops,
    create_race_features,
    create_target
)


def build_dataset(
    seasons=None
):

    """
    Build a training dataset from
    multiple F1 seasons.

    Example:

    build_dataset(
        seasons=[2022, 2023, 2024, 2025]
    )
    """

    if seasons is None:

        seasons = [
            2022,
            2023,
            2024,
            2025
        ]

    all_races = []

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

                df["Season"] = (
                    season
                )

                df["Race"] = (
                    race
                )

                all_races.append(
                    df
                )

            except Exception as e:

                print(
                    f"Skipped {season} - "
                    f"{race}: {e}"
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