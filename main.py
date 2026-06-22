import pandas as pd

from src.build_dataset import build_dataset

from src.feature_engineering import prepare_model_data

from src.train_model import train_model

from src.degradation_model import train_degradation_model


def main():

    build_dataset(2025)

    df = pd.read_csv(
        "data/processed/f1_2025_dataset.csv"
    )

    model_data = prepare_model_data(df)

    train_model(model_data)

    train_degradation_model(df)


if __name__ == "__main__":
    main()