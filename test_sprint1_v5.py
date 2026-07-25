import numbers
import pandas as pd

from src.data_loader import (
    get_race_schedule,
    get_available_drivers,
    get_driver_laps
)

from src.preprocessing import (
    preprocess_data
)

from src.feature_engineering import (
    detect_pit_stops,
    create_race_features
)

from src.predict import (
    predict_pit_probability
)


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2025

TEST_RACES = [

    "Bahrain Grand Prix",

    "Monaco Grand Prix",

    "British Grand Prix",

    "Italian Grand Prix"

]


# ============================================================
# TEST RACE
# ============================================================

def test_race(

    season,

    grand_prix

):

    print("\n" + "=" * 60)

    print(

        f"TESTING: "

        f"{season} "

        f"{grand_prix}"

    )

    print("=" * 60)


    # --------------------------------------------------------
    # LOAD DRIVERS
    # --------------------------------------------------------

    print(

        "\n[1/6] Loading drivers..."

    )


    drivers = get_available_drivers(

        season,

        grand_prix,

        "R"

    )


    if not drivers:

        raise RuntimeError(

            "No drivers found."

        )


    print(

        f"Found {len(drivers)} drivers."

    )


    # --------------------------------------------------------
    # TEST FIRST AVAILABLE DRIVER
    # --------------------------------------------------------

    driver = drivers[0]


    print(

        f"Testing driver: "

        f"{driver}"

    )


    # --------------------------------------------------------
    # LOAD DRIVER LAPS
    # --------------------------------------------------------

    print(

        "\n[2/6] Loading driver lap data..."

    )


    driver_laps = get_driver_laps(

        season,

        grand_prix,

        driver,

        "R"

    )


    if driver_laps.empty:

        raise RuntimeError(

            "Driver lap data is empty."

        )


    print(

        f"Loaded "

        f"{len(driver_laps)} "

        f"lap records."

    )


    # --------------------------------------------------------
    # PREPROCESS
    # --------------------------------------------------------

    print(

        "\n[3/6] Preprocessing..."

    )


    driver_laps = preprocess_data(

        driver_laps

    )


    # --------------------------------------------------------
    # FEATURE ENGINEERING
    # --------------------------------------------------------

    print(

        "\n[4/6] Creating race features..."

    )


    driver_laps = detect_pit_stops(

        driver_laps

    )


    driver_laps = create_race_features(

        driver_laps

    )


    if driver_laps.empty:

        raise RuntimeError(

            "Feature engineering "

            "returned empty data."

        )


    print(

        "Race features created successfully."

    )


    # --------------------------------------------------------
    # GET LATEST RACE STATE
    # --------------------------------------------------------

    latest = (

        driver_laps

        .sort_values(

            "LapNumber"

        )

        .iloc[-1]

    )


    # --------------------------------------------------------
    # MODEL FEATURES
    # --------------------------------------------------------

    model_features = [

        "LapNumber",

        "TyreLife",

        "Position",

        "LapsRemaining",

        "RaceProgress",

        "AvgPaceLast3",

        "AvgPaceLast5",

        "AvgPaceLast10",

        "DegradationRate",

        "CurrentStintLength",

        "PitStopsCompleted"

    ]


    # --------------------------------------------------------
    # CHECK MISSING FEATURES
    # --------------------------------------------------------

    missing_features = [

        feature

        for feature in model_features

        if feature

        not in latest.index

    ]


    if missing_features:

        raise RuntimeError(

            "Missing features: "

            + ", ".join(

                missing_features

            )

        )


    # --------------------------------------------------------
    # BUILD MODEL INPUT
    # --------------------------------------------------------

    model_input = pd.DataFrame(

        [[

            latest[feature]

            for feature

            in model_features

        ]],

        columns=model_features

    )


    print(

        "\n[5/6] Running XGBoost prediction..."

    )


    # --------------------------------------------------------
    # PREDICT PIT PROBABILITY
    # --------------------------------------------------------

    probability = (

        predict_pit_probability(

            model_input

        )

    )


    print(

        f"Pit Probability: "

        f"{probability}%"

    )


    # --------------------------------------------------------
    # FINAL VALIDATION
    # --------------------------------------------------------

    print(

        "\n[6/6] Validating output..."

    )


    # Accept Python and NumPy numeric types

    if not isinstance(

        probability,

        numbers.Number

    ):

        raise RuntimeError(

            "Invalid probability output."

        )


    # Probability must be between 0 and 100

    if probability < 0 or probability > 100:

        raise RuntimeError(

            "Probability outside "

            "valid range."

        )


    print(

        "\n✅ TEST PASSED"

    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    for race in TEST_RACES:

        try:

            test_race(

                SEASON,

                race

            )

        except Exception as e:

            print(

                "\n❌ TEST FAILED"

            )

            print(

                f"Race: {race}"

            )

            print(

                f"Error: {e}"

            )