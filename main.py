from src.build_dataset import (
    build_dataset
)

from src.feature_engineering import (
    prepare_model_data
)

from src.train_model import (
    train_model
)

from src.degradation_model import (
    train_degradation_model
)


def main():

    print(
        "\n======================================"
    )

    print(
        "🚀 F1 AI STRATEGY ENGINE"
    )

    print(
        "   V5 FOUNDATION PIPELINE"
    )

    print(
        "======================================\n"
    )

    # ------------------------------------------
    # STEP 1
    # BUILD DATASET
    # ------------------------------------------

    print(
        "📊 Building dataset..."
    )

    dataset = build_dataset(

        seasons=[

            2022,

            2023,

            2024,

            2025

        ]

    )

    print(
        "\n✅ Dataset created!"
    )

    print(
        "Shape:",
        dataset.shape
    )

    # ------------------------------------------
    # STEP 2
    # PREPARE MODEL DATA
    # ------------------------------------------

    print(
        "\n🧠 Preparing model data..."
    )

    model_data = (

        prepare_model_data(
            dataset
        )

    )

    print(
        "✅ Model data ready!"
    )

    print(
        "Shape:",
        model_data.shape
    )

    # ------------------------------------------
    # STEP 3
    # TRAIN PIT MODEL
    # ------------------------------------------

    print(
        "\n🏁 Training pit strategy model..."
    )

    train_model(
        model_data
    )

    # ------------------------------------------
    # STEP 4
    # TRAIN DEGRADATION MODEL
    # ------------------------------------------

    print(
        "\n🛞 Training degradation model..."
    )

    train_degradation_model(
        dataset
    )

    # ------------------------------------------
    # COMPLETE
    # ------------------------------------------

    print(
        "\n======================================"
    )

    print(
        "✅ V5 FOUNDATION TRAINING COMPLETE"
    )

    print(
        "======================================\n"
    )


if __name__ == "__main__":

    main()