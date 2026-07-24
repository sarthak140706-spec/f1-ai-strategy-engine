import joblib

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error
)

from sklearn.model_selection import (
    train_test_split
)


MODEL_PATH = (
    "models/degradation_model.pkl"
)


def train_degradation_model(
    df
):

    df = df.copy()

    # ------------------------------------------
    # FUTURE LAP TIME
    # ------------------------------------------

    df["FutureLapTime"] = (

        df.groupby(
            "Driver"
        )["LapTimeSeconds"]

        .shift(-1)

    )

    df = df.dropna(
        subset=[
            "FutureLapTime"
        ]
    )

    # ------------------------------------------
    # FEATURES
    # ------------------------------------------

    features = [

        "TyreLife",

        "CurrentStintLength",

        "AvgPaceLast5",

        "DegradationRate"

    ]

    available_features = [

        feature

        for feature in features

        if feature in df.columns

    ]

    X = df[
        available_features
    ]

    y = df[
        "FutureLapTime"
    ]

    # ------------------------------------------
    # TRAIN / TEST SPLIT
    # ------------------------------------------

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42

        )

    )

    # ------------------------------------------
    # MODEL
    # ------------------------------------------

    model = XGBRegressor(

        n_estimators=200,

        max_depth=5,

        learning_rate=0.05,

        random_state=42

    )

    model.fit(
        X_train,
        y_train
    )

    # ------------------------------------------
    # EVALUATION
    # ------------------------------------------

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(

        y_test,

        predictions

    )

    print(
        f"Degradation Model MAE: "
        f"{mae:.3f} seconds"
    )

    # ------------------------------------------
    # SAVE
    # ------------------------------------------

    joblib.dump(
        model,
        MODEL_PATH
    )

    print(
        f"✅ Model saved to: "
        f"{MODEL_PATH}"
    )

    return model