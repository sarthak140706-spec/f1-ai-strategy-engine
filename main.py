from src.build_dataset import build_dataset
from src.feature_engineering import prepare_model_data
from src.train_model import train_model


def main():

    print("\n======================================")
    print("🚀 F1 AI STRATEGIST - V4 PIPELINE")
    print("======================================\n")

    # -----------------------------
    # STEP 1: BUILD DATASET
    # -----------------------------
    print("📊 Building dataset from FastF1...")

    dataset = build_dataset(season=2025)

    print("✅ Dataset created!")
    print("Shape:", dataset.shape)

    # -----------------------------
    # STEP 2: PREPARE MODEL DATA
    # -----------------------------
    print("\n🧠 Preparing model data...")

    model_data = prepare_model_data(dataset)

    print("✅ Model data ready!")
    print("Shape:", model_data.shape)

    # -----------------------------
    # STEP 3: TRAIN MODEL
    # -----------------------------
    print("\n🏁 Training XGBoost model...")

    model = train_model(model_data)

    print("\n✅ MODEL TRAINING COMPLETED!")
    print("📦 Model saved to: models/pit_strategy_model.pkl")

    print("\n======================================")
    print("🏎️ V4 PIPELINE FINISHED SUCCESSFULLY")
    print("======================================\n")


if __name__ == "__main__":
    main()