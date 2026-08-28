// ============================================================
// F1 AI STRATEGIST
// PHASE 3.9 — FRONTEND STRATEGY INTEGRATION
// ============================================================

const API_BASE_URL = "/api";


// ============================================================
// GLOBAL STATE
// ============================================================

let strategyData = null;


// ============================================================
// API URL
// ============================================================

function buildStrategyURL(
    season,
    grandPrix,
    driver
) {

    const formattedGrandPrix =
        grandPrix.replace(
            / /g,
            "_"
        );

    return (
        `${API_BASE_URL}/strategy/` +
        `${season}/` +
        `${formattedGrandPrix}/` +
        `${driver}`
    );
}


// ============================================================
// LOAD AI STRATEGY
// ============================================================

async function loadAIStrategy(
    season,
    grandPrix,
    driver
) {

    showStrategyLoading();

    try {

        const url = buildStrategyURL(
            season,
            grandPrix,
            driver
        );

        const response =
            await fetch(url);

        if (!response.ok) {

            throw new Error(
                `API request failed: ${response.status}`
            );

        }

        strategyData =
            await response.json();

        console.log(
            "AI Strategy API Response:",
            strategyData
        );

        renderAIStrategy(
            strategyData
        );

    }

    catch (error) {

        console.error(
            "Strategy API Error:",
            error
        );

        showStrategyError(
            error.message
        );

    }

}


// ============================================================
// MAIN RENDER FUNCTION
// ============================================================

function renderAIStrategy(
    data
) {

    if (!data) {

        showStrategyError(
            "No strategy data received."
        );

        return;

    }

    renderRecommendation(
        data.ai_recommendation
    );

    renderRaceSituation(
        data.race_situation
    );

    renderPitDecision(
        data.pit_decision
    );

    renderTyreStrategy(
        data.tyre_strategy
    );

    renderStrategySimulation(
        data.strategy_simulation
    );

    renderStrategyScoring(
        data.strategy_scoring
    );

    renderStrategyInputs(
        data.strategy_inputs
    );

    renderRaceInformation(
        data
    );

}


// ============================================================
// RACE INFORMATION
// ============================================================

function renderRaceInformation(
    data
) {

    setText(
        "strategy-season",
        data.season
    );

    setText(
        "strategy-grand-prix",
        data.grand_prix
    );

    setText(
        "strategy-driver",
        data.driver
    );

    setText(
        "strategy-mode",
        data.strategy_mode
    );

}


// ============================================================
// AI RECOMMENDATION
// ============================================================

function renderRecommendation(
    recommendation
) {

    if (!recommendation) {

        return;

    }

    setText(
        "ai-recommendation",
        recommendation.recommendation
    );

    setText(
        "ai-tyre",
        recommendation.recommended_tyre
    );

    setText(
        "ai-confidence",
        formatPercent(
            recommendation.confidence
        )
    );

    setText(
        "ai-score",
        formatNumber(
            recommendation.overall_score,
            2
        )
    );

    setText(
        "ai-benefit",
        formatSeconds(
            recommendation.expected_benefit_seconds
        )
    );

    setText(
        "ai-projected-time",
        formatSeconds(
            recommendation.projected_total_time
        )
    );

    setText(
        "ai-rank",
        recommendation.strategy_rank
    );

    setText(
        "ai-reason",
        recommendation.reason
    );

}


// ============================================================
// RACE SITUATION
// ============================================================

function renderRaceSituation(
    situation
) {

    if (!situation) {

        return;

    }

    setText(
        "situation-status",
        situation.race_situation
    );

    setText(
        "situation-position",
        `P${situation.position}`
    );

    setText(
        "situation-lap",
        `${situation.current_lap} / ${situation.total_laps}`
    );

    setText(
        "situation-tyre",
        situation.tyre_compound
    );

    setText(
        "situation-tyre-life",
        formatNumber(
            situation.tyre_life,
            1
        )
    );

    setText(
        "situation-pace",
        formatNumber(
            situation.recent_pace,
            3
        ) + "s"
    );

    setText(
        "situation-pace-status",
        situation.pace_status
    );

    setText(
        "situation-traffic",
        situation.traffic_status
    );

    setText(
        "situation-opportunity",
        situation.opportunity
    );

    setText(
        "situation-threat",
        situation.threat
    );

    setText(
        "situation-pit-urgency",
        situation.pit_urgency
    );

}


// ============================================================
// PIT DECISION
// ============================================================

function renderPitDecision(
    pit
) {

    if (!pit) {

        return;

    }

    setText(
        "pit-action",
        pit.action
    );

    setText(
        "pit-decision",
        pit.decision
    );

    setText(
        "pit-current-tyre",
        pit.current_tyre
    );

    setText(
        "pit-recommended-tyre",
        pit.recommended_tyre
    );

    setText(
        "pit-age",
        formatNumber(
            pit.tyre_age,
            1
        )
    );

    setText(
        "pit-loss",
        formatSeconds(
            pit.pit_loss
        )
    );

    setText(
        "pit-pace-gain",
        formatSeconds(
            pit.pace_gain_per_lap
        )
    );

    setText(
        "pit-benefit",
        formatSeconds(
            pit.estimated_benefit
        )
    );

    setText(
        "pit-confidence",
        formatPercent(
            pit.confidence
        )
    );

    setText(
        "pit-reason",
        pit.reason
    );

}


// ============================================================
// TYRE STRATEGY
// ============================================================

function renderTyreStrategy(
    tyre
) {

    if (!tyre) {

        return;

    }

    setText(
        "tyre-recommendation",
        tyre.Recommendation
    );

    setText(
        "tyre-compound",
        tyre.Compound
    );

    setText(
        "tyre-strategy-type",
        tyre.StrategyType
    );

    setText(
        "tyre-quality",
        formatNumber(
            tyre.StrategyQuality,
            2
        )
    );

    setText(
        "tyre-average-lap",
        formatSeconds(
            tyre.AverageLapTime
        )
    );

    setText(
        "tyre-degradation",
        formatSeconds(
            tyre.DegradationImpact
        )
    );

    setText(
        "tyre-projected-time",
        formatSeconds(
            tyre.ProjectedTotalTime
        )
    );

    setText(
        "tyre-confidence",
        formatPercent(
            tyre.Confidence
        )
    );

}


// ============================================================
// STRATEGY SIMULATION
// ============================================================

function renderStrategySimulation(
    simulation
) {

    if (!simulation) {

        return;

    }

    setText(
        "simulation-best",
        simulation.best_strategy
    );

    setText(
        "simulation-rank",
        simulation.best_strategy_rank
    );

    setText(
        "simulation-count",
        simulation.strategy_count
    );

    const strategies =
        simulation.strategies || [];

    const container =
        document.getElementById(
            "strategy-simulation-table"
        );

    if (!container) {

        return;

    }

    container.innerHTML = "";

    strategies.forEach(
        (strategy) => {

            const row =
                document.createElement(
                    "tr"
                );

            row.innerHTML = `
                <td>${strategy.Rank ?? strategy.StrategyRank ?? "-"}</td>
                <td>${strategy.Strategy ?? strategy.Action ?? "-"}</td>
                <td>${strategy.TyrePlan ?? strategy.Compound ?? "-"}</td>
                <td>${strategy.Stops ?? "-"}</td>
                <td>${formatSeconds(
                    strategy.ProjectedTotalTime
                    ?? strategy.ProjectedTotalTimeSeconds
                )}</td>
                <td>${formatNumber(
                    strategy.AverageLapTime,
                    3
                )}s</td>
            `;

            container.appendChild(
                row
            );

        }
    );

}


// ============================================================
// STRATEGY SCORING
// ============================================================

function renderStrategyScoring(
    scoring
) {

    if (!scoring) {

        return;

    }

    setText(
        "scoring-best",
        scoring.best_strategy
    );

    setText(
        "scoring-best-score",
        formatNumber(
            scoring.best_score,
            2
        )
    );

    setText(
        "scoring-count",
        scoring.strategy_count
    );

    const strategies =
        scoring.strategies || [];

    const container =
        document.getElementById(
            "strategy-scoring-table"
        );

    if (!container) {

        return;

    }

    container.innerHTML = "";

    strategies.forEach(
        (strategy) => {

            const row =
                document.createElement(
                    "tr"
                );

            row.innerHTML = `
                <td>${strategy.ScoreRank ?? strategy.Rank ?? "-"}</td>

                <td>${strategy.Strategy ?? "-"}</td>

                <td>${strategy.TyrePlan ?? "-"}</td>

                <td>${formatNumber(
                    strategy.PaceScore,
                    2
                )}</td>

                <td>${formatNumber(
                    strategy.TyreScore,
                    2
                )}</td>

                <td>${formatNumber(
                    strategy.PitScore,
                    2
                )}</td>

                <td>${formatNumber(
                    strategy.TrafficScore,
                    2
                )}</td>

                <td>${formatNumber(
                    strategy.PositionScore,
                    2
                )}</td>

                <td>${formatNumber(
                    strategy.DegradationScore,
                    2
                )}</td>

                <td>${formatNumber(
                    strategy.RiskScore,
                    2
                )}</td>

                <td><strong>${formatNumber(
                    strategy.OverallScore,
                    2
                )}</strong></td>
            `;

            container.appendChild(
                row
            );

        }
    );

}


// ============================================================
// STRATEGY INPUTS
// ============================================================

function renderStrategyInputs(
    inputs
) {

    if (!inputs) {

        return;

    }

    setText(
        "input-lap",
        inputs.current_lap
    );

    setText(
        "input-remaining",
        inputs.remaining_laps
    );

    setText(
        "input-tyre",
        inputs.current_tyre
    );

    setText(
        "input-tyre-age",
        inputs.tyre_age
    );

    setText(
        "input-position",
        `P${inputs.position}`
    );

    setText(
        "input-gap-ahead",
        formatSeconds(
            inputs.gap_ahead
        )
    );

    setText(
        "input-gap-behind",
        formatSeconds(
            inputs.gap_behind
        )
    );

    setText(
        "input-pit-loss",
        formatSeconds(
            inputs.pit_loss
        )
    );

}


// ============================================================
// LOADING STATE
// ============================================================

function showStrategyLoading() {

    const container =
        document.getElementById(
            "strategy-loading"
        );

    if (container) {

        container.style.display =
            "block";

    }

}


// ============================================================
// ERROR STATE
// ============================================================

function showStrategyError(
    message
) {

    const loading =
        document.getElementById(
            "strategy-loading"
        );

    if (loading) {

        loading.style.display =
            "none";

    }

    const error =
        document.getElementById(
            "strategy-error"
        );

    if (error) {

        error.style.display =
            "block";

        error.textContent =
            `Strategy API Error: ${message}`;

    }

}


// ============================================================
// HELPER FUNCTIONS
// ============================================================

function setText(
    id,
    value
) {

    const element =
        document.getElementById(
            id
        );

    if (!element) {

        return;

    }

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        element.textContent =
            "-";

        return;

    }

    element.textContent =
        value;

}


function formatNumber(
    value,
    decimals = 2
) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(
            Number(value)
        )
    ) {

        return "-";

    }

    return Number(value).toFixed(
        decimals
    );

}


function formatSeconds(
    value
) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(
            Number(value)
        )
    ) {

        return "-";

    }

    return `${Number(value).toFixed(3)}s`;

}


function formatPercent(
    value
) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(
            Number(value)
        )
    ) {

        return "-";

    }

    return `${Number(value).toFixed(1)}%`;

}


// ============================================================
// AUTO LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        /*
         * Default Phase 3.9 integration test.
         *
         * This uses the same endpoint that was
         * successfully tested in Phase 3.8.
         */

        loadAIStrategy(
            2025,
            "British Grand Prix",
            "VER"
        );

    }
);