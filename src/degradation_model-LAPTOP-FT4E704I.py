import joblib

from xgboost import XGBRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split


def train_degradation_model(df):

    df = df.copy()

    df["FutureLapTime"] = (
        df.groupby(["Race", "Driver"])["LapTimeSeconds"]
        .shift(-1)
    )

    features = [
        "TyreLife",
        "CurrentStintLength",
        "AvgPaceLast5",
        "DegradationRate"
    ]

    df = df.dropna(
        subset=features + ["FutureLapTime"]
    )

    print("Training samples:", len(df))

    X = df[features]

    y = df["FutureLapTime"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print(
        "MAE:",
        mean_absolute_error(y_test, predictions)
    )

    joblib.dump(
        model,
        "models/degradation_model.pkl"
    )

    return model