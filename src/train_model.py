import joblib

from xgboost import XGBClassifier

from sklearn.metrics import (
    classification_report,
    accuracy_score,
    roc_auc_score
)

from sklearn.model_selection import (
    train_test_split
)

from imblearn.over_sampling import SMOTE


MODEL_PATH = (
    "models/pit_strategy_model.pkl"
)


def train_model(
    model_data
):

    X = model_data.drop(
        columns=[
            "PitNextLap"
        ]
    )

    y = model_data[
        "PitNextLap"
    ]

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42,

            stratify=y

        )

    )

    # ------------------------------------------
    # HANDLE CLASS IMBALANCE
    # ------------------------------------------

    smote = SMOTE(
        random_state=42
    )

    X_train, y_train = (

        smote.fit_resample(
            X_train,
            y_train
        )

    )

    # ------------------------------------------
    # MODEL
    # ------------------------------------------

    model = XGBClassifier(

        n_estimators=300,

        max_depth=6,

        learning_rate=0.05,

        random_state=42,

        eval_metric="logloss"

    )

    model.fit(
        X_train,
        y_train
    )

    # ------------------------------------------
    # EVALUATION
    # ------------------------------------------

    y_pred = model.predict(
        X_test
    )

    y_probability = (
        model.predict_proba(
            X_test
        )[:, 1]
    )

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    print(
        "Accuracy:",
        accuracy_score(
            y_test,
            y_pred
        )
    )

    print(
        "ROC-AUC:",
        roc_auc_score(
            y_test,
            y_probability
        )
    )

    # ------------------------------------------
    # SAVE MODEL
    # ------------------------------------------

    joblib.dump(
        model,
        MODEL_PATH
    )

    print(
        f"\n✅ Model saved to: "
        f"{MODEL_PATH}"
    )

    return model