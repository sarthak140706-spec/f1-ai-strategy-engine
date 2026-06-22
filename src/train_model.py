import joblib

from xgboost import XGBClassifier

from sklearn.metrics import classification_report

from sklearn.model_selection import train_test_split

from imblearn.over_sampling import SMOTE


def train_model(model_data):

    X = model_data.drop(columns=["PitNextLap"])

    y = model_data["PitNextLap"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    smote = SMOTE(random_state=42)

    X_train, y_train = smote.fit_resample(
        X_train,
        y_train
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(classification_report(y_test, y_pred))

    joblib.dump(
        model,
        "models/pit_strategy_model.pkl"
    )

    return model