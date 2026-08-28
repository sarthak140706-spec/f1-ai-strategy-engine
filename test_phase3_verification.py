"""
test_phase3_verification.py

PHASE 3.10 — COMPLETE PHASE 3 VERIFICATION

Tests:

3.1 Strategy Engine Foundation
3.2 Race Situation Analysis
3.3 Tyre Strategy
3.4 Pit Decision
3.5 Strategy Simulation
3.6 Strategy Scoring
3.7 AI Recommendation
3.8 Backend API
3.9 Frontend Data Contract
"""

from src.data_loader import load_session

from src.race_state import (
    build_race_state
)

from src.strategy.race_situation import (
    analyze_race_situation
)

from src.strategy.tyre_strategy import (
    generate_tyre_strategy
)

from src.strategy.pit_decision import (
    evaluate_pit_decision
)

from src.strategy.strategy_simulation import (
    run_strategy_simulation
)

from src.strategy.strategy_scoring import (
    run_strategy_scoring
)

from src.strategy.ai_recommendation import (
    generate_ai_recommendation
)

from api.services import (
    get_ai_strategy
)

from api.app import app


# ============================================================
# TEST CONFIGURATION
# ============================================================

SEASON = 2024

GRAND_PRIX = "Bahrain"

DRIVER = "VER"

SESSION_TYPE = "R"


# ============================================================
# HELPERS
# ============================================================

def success(step, message):

    print(
        f"✅ {step} PASSED — {message}"
    )


def fail(step, message):

    print(
        f"❌ {step} FAILED — {message}"
    )

    raise AssertionError(
        f"{step}: {message}"
    )


# ============================================================
# PHASE 3 VERIFICATION
# ============================================================

def run_verification():

    print()
    print("=" * 70)
    print("F1 AI STRATEGIST")
    print("PHASE 3.10 — COMPLETE VERIFICATION")
    print("=" * 70)

    # ========================================================
    # 3.1
    # LOAD SESSION / FOUNDATION
    # ========================================================

    print(
        "\n[3.1] Testing Strategy Engine Foundation..."
    )

    session = load_session(
        season=SEASON,
        grand_prix=GRAND_PRIX,
        session_type=SESSION_TYPE
    )

    if session is None:

        fail(
            "3.1",
            "FastF1 session was not loaded."
        )

    success(
        "3.1",
        "Session loaded successfully."
    )


    # ========================================================
    # 3.2
    # RACE STATE + SITUATION
    # ========================================================

    print(
        "\n[3.2] Testing Race Situation Analysis..."
    )

    race_state = build_race_state(
        session=session,
        driver=DRIVER
    )

    if not race_state:

        fail(
            "3.2",
            "Race state is empty."
        )

    required_race_state_fields = [

        "CurrentLap",
        "TotalLaps",
        "Position",
        "TyreCompound",
        "TyreLife",
        "RecentPace",
        "AveragePace"

    ]

    for field in required_race_state_fields:

        if field not in race_state:

            fail(
                "3.2",
                f"Missing race-state field: {field}"
            )

    race_situation = analyze_race_situation(
        race_state
    )

    if not race_situation:

        fail(
            "3.2",
            "Race situation returned no data."
        )

    success(
        "3.2",
        "Race state and situation analysis working."
    )


    # ========================================================
    # USE FIXED STRATEGIC SNAPSHOT
    #
    # Historical race is already complete.
    # Therefore remaining laps from FastF1 = 0.
    #
    # This snapshot matches the Phase 3 test scenario.
    # ========================================================

    current_lap = 35

    remaining_laps = 22

    current_tyre = "HARD"

    tyre_age = 22

    base_lap_time = 96.2

    pit_loss = 22.0

    degradation_rate = 0.735

    position = 4

    gap_ahead = 1.8

    gap_behind = 12.4


    # ========================================================
    # 3.3
    # TYRE STRATEGY
    # ========================================================

    print(
        "\n[3.3] Testing Tyre Strategy Decision Engine..."
    )

    tyre_strategy = generate_tyre_strategy(

        base_lap_time=base_lap_time,

        current_tyre=current_tyre,

        tyre_age=tyre_age,

        remaining_laps=remaining_laps,

        pit_loss=pit_loss

    )

    if not tyre_strategy:

        fail(
            "3.3",
            "Tyre strategy returned no data."
        )

    required_tyre_fields = [

        "Recommendation",
        "Compound",
        "ProjectedTotalTime",
        "AverageLapTime",
        "StrategyQuality"

    ]

    for field in required_tyre_fields:

        if field not in tyre_strategy:

            fail(
                "3.3",
                f"Missing tyre-strategy field: {field}"
            )

    success(
        "3.3",
        f"Tyre recommendation: "
        f"{tyre_strategy['Recommendation']} "
        f"{tyre_strategy['Compound']}"
    )


    # ========================================================
    # 3.4
    # PIT DECISION
    # ========================================================

    print(
        "\n[3.4] Testing Pit-Stop Decision Engine..."
    )

    pit_decision = evaluate_pit_decision(

        current_lap=current_lap,

        remaining_laps=remaining_laps,

        current_tyre=current_tyre,

        tyre_age=tyre_age,

        recent_pace=base_lap_time,

        position=position,

        gap_ahead=gap_ahead,

        gap_behind=gap_behind,

        pit_loss=pit_loss,

        recommended_tyre=(
            tyre_strategy.get(
                "Compound"
            )
        ),

        degradation_rate=degradation_rate,

        race_situation=race_situation

    )

    if not pit_decision:

        fail(
            "3.4",
            "Pit decision returned no data."
        )

    required_pit_fields = [

        "decision",
        "recommended_tyre",
        "pit_loss",
        "pace_gain_per_lap",
        "estimated_benefit",
        "confidence"

    ]

    for field in required_pit_fields:

        if field not in pit_decision:

            fail(
                "3.4",
                f"Missing pit-decision field: {field}"
            )

    success(
        "3.4",
        f"Pit decision: "
        f"{pit_decision['decision']}"
    )


    # ========================================================
    # 3.5
    # STRATEGY SIMULATION
    # ========================================================

    print(
        "\n[3.5] Testing Strategy Simulation..."
    )

    simulation = run_strategy_simulation(

        base_lap_time=base_lap_time,

        current_tyre=current_tyre,

        tyre_age=tyre_age,

        remaining_laps=remaining_laps,

        pit_loss=pit_loss

    )

    if not simulation:

        fail(
            "3.5",
            "Simulation returned no data."
        )

    strategies = simulation.get(
        "strategies",
        []
    )

    if len(strategies) != 4:

        fail(
            "3.5",
            f"Expected 4 strategies, "
            f"received {len(strategies)}."
        )

    required_simulation_fields = [

        "strategy",
        "tyre_plan",
        "stops",
        "stint_length",
        "pit_loss",
        "projected_total_time",
        "average_lap_time",
        "time_difference",
        "strategy_rank"

    ]

    for strategy in strategies:

        for field in required_simulation_fields:

            if field not in strategy:

                fail(
                    "3.5",
                    f"Missing simulation field: {field}"
                )

    success(
        "3.5",
        "4 strategy alternatives generated and ranked."
    )


    # ========================================================
    # 3.6
    # STRATEGY SCORING
    # ========================================================

    print(
        "\n[3.6] Testing Strategy Scoring..."
    )

    scoring = run_strategy_scoring(
        strategies
    )

    if not scoring:

        fail(
            "3.6",
            "Strategy scoring returned no data."
        )

    scored_strategies = scoring.get(
        "strategies",
        []
    )

    if len(scored_strategies) != 4:

        fail(
            "3.6",
            f"Expected 4 scored strategies, "
            f"received {len(scored_strategies)}."
        )

    required_scoring_fields = [

        "score_rank",
        "pace_score",
        "tyre_score",
        "pit_score",
        "traffic_score",
        "position_score",
        "degradation_score",
        "risk_score",
        "overall_score"

    ]

    for strategy in scored_strategies:

        for field in required_scoring_fields:

            if field not in strategy:

                fail(
                    "3.6",
                    f"Missing scoring field: {field}"
                )

        score = strategy[
            "overall_score"
        ]

        if not 0 <= score <= 100:

            fail(
                "3.6",
                f"Invalid overall score: {score}"
            )

    success(
        "3.6",
        f"Best score: {scoring['best_score']}"
    )


    # ========================================================
    # 3.7
    # AI RECOMMENDATION
    # ========================================================

    print(
        "\n[3.7] Testing AI Recommendation..."
    )

    recommendation = generate_ai_recommendation(

        scoring_result=scoring,

        race_situation=race_situation,

        tyre_decision=tyre_strategy,

        pit_decision=pit_decision

    )

    if not recommendation:

        fail(
            "3.7",
            "AI recommendation returned no data."
        )

    required_recommendation_fields = [

        "recommendation",
        "recommended_tyre",
        "confidence",
        "overall_score",
        "reason",
        "strategy_comparison"

    ]

    for field in required_recommendation_fields:

        if field not in recommendation:

            fail(
                "3.7",
                f"Missing AI recommendation field: {field}"
            )

    success(
        "3.7",
        f"{recommendation['recommendation']} "
        f"| Confidence: "
        f"{recommendation['confidence']}%"
    )


    # ========================================================
    # 3.8
    # BACKEND SERVICE
    # ========================================================

    print(
        "\n[3.8] Testing Backend API Service..."
    )

    result = get_ai_strategy(

        season=SEASON,

        grand_prix=GRAND_PRIX,

        driver=DRIVER,

        session_type=SESSION_TYPE

    )

    if not result:

        fail(
            "3.8",
            "get_ai_strategy returned no data."
        )

    required_api_sections = [

        "race_state",
        "race_situation",
        "tyre_strategy",
        "pit_decision",
        "strategy_simulation",
        "strategy_scoring",
        "ai_recommendation"

    ]

    for section in required_api_sections:

        if section not in result:

            fail(
                "3.8",
                f"Missing API section: {section}"
            )

    success(
        "3.8",
        "Complete strategy response generated."
    )


    # ========================================================
    # 3.8
    # FLASK ROUTE
    # ========================================================

    print(
        "\n[3.8 API] Testing Flask endpoint..."
    )

    client = app.test_client()

    response = client.get(

        f"/api/strategy/"
        f"{SEASON}/"
        f"{GRAND_PRIX}/"
        f"{DRIVER}"

    )

    if response.status_code != 200:

        fail(
            "3.8 API",
            f"HTTP status: "
            f"{response.status_code}"
        )

    api_json = response.get_json()

    if not api_json:

        fail(
            "3.8 API",
            "Flask endpoint returned no JSON."
        )

    success(
        "3.8 API",
        "HTTP 200 + valid JSON."
    )


    # ========================================================
    # 3.9
    # FRONTEND DATA CONTRACT
    # ========================================================

    print(
        "\n[3.9] Testing Frontend Integration Data..."
    )

    simulation_frontend = (
        api_json
        .get(
            "strategy_simulation",
            {}
        )
        .get(
            "strategies",
            []
        )
    )

    scoring_frontend = (
        api_json
        .get(
            "strategy_scoring",
            {}
        )
        .get(
            "strategies",
            []
        )
    )

    if not simulation_frontend:

        fail(
            "3.9",
            "Simulation table has no API records."
        )

    if not scoring_frontend:

        fail(
            "3.9",
            "Scoring table has no API records."
        )

    if len(simulation_frontend) != 4:

        fail(
            "3.9",
            "Simulation table should receive "
            "4 rows."
        )

    if len(scoring_frontend) != 4:

        fail(
            "3.9",
            "Scoring table should receive "
            "4 rows."
        )

    success(
        "3.9",
        "Simulation and scoring tables "
        "receive 4 records each."
    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 70)
    print("PHASE 3 VERIFICATION RESULTS")
    print("=" * 70)

    print("3.1 Strategy Foundation       ✅")
    print("3.2 Race Situation            ✅")
    print("3.3 Tyre Strategy             ✅")
    print("3.4 Pit Decision              ✅")
    print("3.5 Strategy Simulation       ✅")
    print("3.6 Strategy Scoring          ✅")
    print("3.7 AI Recommendation         ✅")
    print("3.8 Backend API               ✅")
    print("3.9 Frontend Data Contract    ✅")

    print()
    print("🏁 PHASE 3.10 VERIFICATION PASSED")
    print()
    print("✅ PHASE 3 — 100% COMPLETE")
    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    run_verification()