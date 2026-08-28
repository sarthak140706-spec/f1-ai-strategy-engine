/*
F1 AI STRATEGIST
PHASE 7.10.4 — STRATEGY ENGINEER + WHAT-IF FRONTEND INTEGRATION
*/

"use strict";


// ==========================================================
// API ENDPOINTS
// ==========================================================

const STRATEGY_API =
    "/api/engineer/analyse";

const WHAT_IF_API =
    "/api/engineer/what-if";


// ==========================================================
// 2025 FORMULA ONE GRID
// ==========================================================

const DRIVERS = [

    {
        code: "NOR",
        name: "Lando Norris",
        team: "McLaren"
    },

    {
        code: "PIA",
        name: "Oscar Piastri",
        team: "McLaren"
    },

    {
        code: "LEC",
        name: "Charles Leclerc",
        team: "Ferrari"
    },

    {
        code: "HAM",
        name: "Lewis Hamilton",
        team: "Ferrari"
    },

    {
        code: "VER",
        name: "Max Verstappen",
        team: "Red Bull Racing"
    },

    {
        code: "TSU",
        name: "Yuki Tsunoda",
        team: "Red Bull Racing"
    },

    {
        code: "RUS",
        name: "George Russell",
        team: "Mercedes"
    },

    {
        code: "ANT",
        name: "Kimi Antonelli",
        team: "Mercedes"
    },

    {
        code: "ALO",
        name: "Fernando Alonso",
        team: "Aston Martin"
    },

    {
        code: "STR",
        name: "Lance Stroll",
        team: "Aston Martin"
    },

    {
        code: "GAS",
        name: "Pierre Gasly",
        team: "Alpine"
    },

    {
        code: "COL",
        name: "Franco Colapinto",
        team: "Alpine"
    },

    {
        code: "OCO",
        name: "Esteban Ocon",
        team: "Haas"
    },

    {
        code: "BEA",
        name: "Oliver Bearman",
        team: "Haas"
    },

    {
        code: "LAW",
        name: "Liam Lawson",
        team: "Racing Bulls"
    },

    {
        code: "HAD",
        name: "Isack Hadjar",
        team: "Racing Bulls"
    },

    {
        code: "ALB",
        name: "Alexander Albon",
        team: "Williams"
    },

    {
        code: "SAI",
        name: "Carlos Sainz",
        team: "Williams"
    },

    {
        code: "HUL",
        name: "Nico Hulkenberg",
        team: "Kick Sauber"
    },

    {
        code: "BOR",
        name: "Gabriel Bortoleto",
        team: "Kick Sauber"
    }

];


// ==========================================================
// TEAMS
// ==========================================================

const TEAMS = [

    "McLaren",

    "Ferrari",

    "Red Bull Racing",

    "Mercedes",

    "Aston Martin",

    "Alpine",

    "Haas",

    "Racing Bulls",

    "Williams",

    "Kick Sauber"

];


// ==========================================================
// 2025 GRAND PRIX / CIRCUIT DATA
// ==========================================================

const GRAND_PRIX_DATA = [

    {
        grandPrix:
            "Australian Grand Prix",

        circuit:
            "Albert Park Grand Prix Circuit",

        laps:
            58
    },

    {
        grandPrix:
            "Chinese Grand Prix",

        circuit:
            "Shanghai International Circuit",

        laps:
            56
    },

    {
        grandPrix:
            "Japanese Grand Prix",

        circuit:
            "Suzuka International Racing Course",

        laps:
            53
    },

    {
        grandPrix:
            "Bahrain Grand Prix",

        circuit:
            "Bahrain International Circuit",

        laps:
            57
    },

    {
        grandPrix:
            "Saudi Arabian Grand Prix",

        circuit:
            "Jeddah Corniche Circuit",

        laps:
            50
    },

    {
        grandPrix:
            "Miami Grand Prix",

        circuit:
            "Miami International Autodrome",

        laps:
            57
    },

    {
        grandPrix:
            "Emilia Romagna Grand Prix",

        circuit:
            "Autodromo Enzo e Dino Ferrari",

        laps:
            63
    },

    {
        grandPrix:
            "Monaco Grand Prix",

        circuit:
            "Circuit de Monaco",

        laps:
            78
    },

    {
        grandPrix:
            "Spanish Grand Prix",

        circuit:
            "Circuit de Barcelona-Catalunya",

        laps:
            66
    },

    {
        grandPrix:
            "Canadian Grand Prix",

        circuit:
            "Circuit Gilles Villeneuve",

        laps:
            70
    },

    {
        grandPrix:
            "Austrian Grand Prix",

        circuit:
            "Red Bull Ring",

        laps:
            71
    },

    {
        grandPrix:
            "British Grand Prix",

        circuit:
            "Silverstone Circuit",

        laps:
            52
    },

    {
        grandPrix:
            "Belgian Grand Prix",

        circuit:
            "Circuit de Spa-Francorchamps",

        laps:
            44
    },

    {
        grandPrix:
            "Hungarian Grand Prix",

        circuit:
            "Hungaroring",

        laps:
            70
    },

    {
        grandPrix:
            "Dutch Grand Prix",

        circuit:
            "Circuit Zandvoort",

        laps:
            72
    },

    {
        grandPrix:
            "Italian Grand Prix",

        circuit:
            "Autodromo Nazionale Monza",

        laps:
            53
    },

    {
        grandPrix:
            "Azerbaijan Grand Prix",

        circuit:
            "Baku City Circuit",

        laps:
            51
    },

    {
        grandPrix:
            "Singapore Grand Prix",

        circuit:
            "Marina Bay Street Circuit",

        laps:
            62
    },

    {
        grandPrix:
            "United States Grand Prix",

        circuit:
            "Circuit of the Americas",

        laps:
            56
    },

    {
        grandPrix:
            "Mexico City Grand Prix",

        circuit:
            "Autodromo Hermanos Rodriguez",

        laps:
            71
    },

    {
        grandPrix:
            "Sao Paulo Grand Prix",

        circuit:
            "Autodromo Jose Carlos Pace",

        laps:
            71
    },

    {
        grandPrix:
            "Las Vegas Grand Prix",

        circuit:
            "Las Vegas Strip Circuit",

        laps:
            50
    },

    {
        grandPrix:
            "Qatar Grand Prix",

        circuit:
            "Lusail International Circuit",

        laps:
            57
    },

    {
        grandPrix:
            "Abu Dhabi Grand Prix",

        circuit:
            "Yas Marina Circuit",

        laps:
            58
    }

];


// ==========================================================
// ELEMENTS
// ==========================================================

const strategyForm =
    document.getElementById(
        "strategy-form"
    );


const analyseButton =
    document.getElementById(
        "analyse-button"
    );


const emptyState =
    document.getElementById(
        "empty-state"
    );


const loadingState =
    document.getElementById(
        "loading-state"
    );


const resultContent =
    document.getElementById(
        "result-content"
    );


const formError =
    document.getElementById(
        "form-error"
    );


const driverSelect =
    document.getElementById(
        "driver"
    );


const teamSelect =
    document.getElementById(
        "team"
    );


const grandPrixSelect =
    document.getElementById(
        "grand-prix"
    );


const circuitSelect =
    document.getElementById(
        "circuit"
    );


const totalLapsInput =
    document.getElementById(
        "total-laps"
    );


const currentLapInput =
    document.getElementById(
        "current-lap"
    );


// ==========================================================
// GENERAL DOM HELPERS
// ==========================================================

function getElement(id) {

    return document.getElementById(
        id
    );

}


function setText(
    id,
    text
) {

    const element =
        getElement(id);


    if (element) {

        element.textContent =
            text;

    }

}


// ==========================================================
// POPULATE DRIVER DROPDOWN
// ==========================================================

function populateDrivers() {

    driverSelect.innerHTML = `
        <option value="">
            Select Driver
        </option>
    `;


    DRIVERS.forEach(
        driver => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                driver.code;


            option.textContent =
                `${driver.name} (${driver.code})`;


            driverSelect.appendChild(
                option
            );

        }
    );

}


// ==========================================================
// POPULATE TEAM DROPDOWN
// ==========================================================

function populateTeams() {

    teamSelect.innerHTML = `
        <option value="">
            Select Team
        </option>
    `;


    TEAMS.forEach(
        team => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                team;


            option.textContent =
                team;


            teamSelect.appendChild(
                option
            );

        }
    );

}


// ==========================================================
// POPULATE GRAND PRIX DROPDOWN
// ==========================================================

function populateGrandPrix() {

    grandPrixSelect.innerHTML = `
        <option value="">
            Select Grand Prix
        </option>
    `;


    GRAND_PRIX_DATA.forEach(
        event => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                event.grandPrix;


            option.textContent =
                event.grandPrix;


            grandPrixSelect.appendChild(
                option
            );

        }
    );

}


// ==========================================================
// POPULATE CIRCUIT DROPDOWN
// ==========================================================

function populateCircuits() {

    circuitSelect.innerHTML = `
        <option value="">
            Select Circuit
        </option>
    `;


    GRAND_PRIX_DATA.forEach(
        event => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                event.circuit;


            option.textContent =
                event.circuit;


            circuitSelect.appendChild(
                option
            );

        }
    );

}


// ==========================================================
// DRIVER → TEAM
// ==========================================================

function updateTeamFromDriver() {

    const driverCode =
        driverSelect.value;


    const driver =
        DRIVERS.find(
            item =>
                item.code ===
                driverCode
        );


    if (!driver) {

        return;

    }


    teamSelect.value =
        driver.team;

}


// ==========================================================
// TEAM → DRIVER SUPPORT
// ==========================================================

function validateDriverTeam() {

    /*
    Manual team changes are intentionally allowed.

    This allows hypothetical simulations where
    a driver may be evaluated with another team.
    */

}


// ==========================================================
// GRAND PRIX EVENT HELPER
// ==========================================================

function applyGrandPrixEvent(
    event
) {

    if (!event) {

        return;

    }


    circuitSelect.value =
        event.circuit;


    grandPrixSelect.value =
        event.grandPrix;


    totalLapsInput.value =
        event.laps;


    const currentLap =
        Number(
            currentLapInput.value
        );


    if (
        Number.isFinite(
            currentLap
        ) &&
        currentLap >
        event.laps
    ) {

        currentLapInput.value =
            event.laps;

    }

}


// ==========================================================
// GRAND PRIX → CIRCUIT + TOTAL LAPS
// ==========================================================

function updateCircuitFromGrandPrix() {

    const selectedGrandPrix =
        grandPrixSelect.value;


    const event =
        GRAND_PRIX_DATA.find(
            item =>
                item.grandPrix ===
                selectedGrandPrix
        );


    applyGrandPrixEvent(
        event
    );

}


// ==========================================================
// CIRCUIT → GRAND PRIX + TOTAL LAPS
// ==========================================================

function updateGrandPrixFromCircuit() {

    const selectedCircuit =
        circuitSelect.value;


    const event =
        GRAND_PRIX_DATA.find(
            item =>
                item.circuit ===
                selectedCircuit
        );


    applyGrandPrixEvent(
        event
    );

}


// ==========================================================
// DEFAULT CONFIGURATION
// ==========================================================

function setDefaultConfiguration() {

    /*
    Default verification state:

    Charles Leclerc
    Ferrari
    Italian Grand Prix
    Monza
    */


    driverSelect.value =
        "LEC";


    updateTeamFromDriver();


    grandPrixSelect.value =
        "Italian Grand Prix";


    updateCircuitFromGrandPrix();

}


// ==========================================================
// INITIALISE SELECTORS
// ==========================================================

function initialiseRaceSelectors() {

    populateDrivers();

    populateTeams();

    populateGrandPrix();

    populateCircuits();

    setDefaultConfiguration();

}


// ==========================================================
// SELECTOR EVENTS
// ==========================================================

driverSelect.addEventListener(
    "change",
    updateTeamFromDriver
);


teamSelect.addEventListener(
    "change",
    validateDriverTeam
);


grandPrixSelect.addEventListener(
    "change",
    updateCircuitFromGrandPrix
);


circuitSelect.addEventListener(
    "change",
    updateGrandPrixFromCircuit
);


// ==========================================================
// VALUE HELPERS
// ==========================================================

function value(id) {

    const element =
        document.getElementById(
            id
        );


    if (!element) {

        return "";

    }


    return element.value;

}


function numberValue(id) {

    const raw =
        value(id);


    if (
        raw === null ||
        raw === undefined ||
        raw === ""
    ) {

        return null;

    }


    const number =
        Number(raw);


    return Number.isFinite(
        number
    )
        ? number
        : null;

}


function checked(id) {

    const element =
        document.getElementById(
            id
        );


    return element
        ? element.checked
        : false;

}


// ==========================================================
// BUILD STRATEGY REQUEST
// ==========================================================

function buildStrategyRequest() {

    return {

        driver:
            value(
                "driver"
            ),

        team:
            value(
                "team"
            ),

        grand_prix:
            value(
                "grand-prix"
            ),

        circuit:
            value(
                "circuit"
            ),

        current_lap:
            numberValue(
                "current-lap"
            ),

        total_laps:
            numberValue(
                "total-laps"
            ),

        position:
            numberValue(
                "position"
            ),

        pit_stops:
            numberValue(
                "pit-stops"
            ),

        tyre_compound:
            value(
                "tyre-compound"
            ),

        tyre_age:
            numberValue(
                "tyre-age"
            ),

        recent_pace:
            numberValue(
                "recent-pace"
            ),

        average_pace:
            numberValue(
                "average-pace"
            ),

        degradation_rate:
            numberValue(
                "degradation-rate"
            ),

        gap_ahead:
            numberValue(
                "gap-ahead"
            ),

        gap_behind:
            numberValue(
                "gap-behind"
            ),

        weather:
            value(
                "weather"
            ),

        rainfall:
            numberValue(
                "rainfall"
            ),

        track_status:
            value(
                "track-status"
            ),

        safety_car:
            checked(
                "safety-car"
            ),

        virtual_safety_car:
            checked(
                "virtual-safety-car"
            )

    };

}


// ==========================================================
// VALIDATE REQUEST
// ==========================================================

function validateStrategyRequest(
    raceState
) {

    if (!raceState.driver) {

        throw new Error(
            "Please select a driver."
        );

    }


    if (!raceState.team) {

        throw new Error(
            "Please select a team."
        );

    }


    if (!raceState.grand_prix) {

        throw new Error(
            "Please select a Grand Prix."
        );

    }


    if (!raceState.circuit) {

        throw new Error(
            "Please select a circuit."
        );

    }


    if (
        raceState.current_lap === null ||
        raceState.current_lap < 1
    ) {

        throw new Error(
            "Current lap must be at least 1."
        );

    }


    if (
        raceState.total_laps === null ||
        raceState.total_laps < 1
    ) {

        throw new Error(
            "Total laps must be at least 1."
        );

    }


    if (
        raceState.current_lap >
        raceState.total_laps
    ) {

        throw new Error(
            "Current lap cannot exceed total race laps."
        );

    }


    if (
        raceState.position === null ||
        raceState.position < 1 ||
        raceState.position > 20
    ) {

        throw new Error(
            "Position must be between 1 and 20."
        );

    }


    if (
        raceState.tyre_age === null ||
        raceState.tyre_age < 0
    ) {

        throw new Error(
            "Tyre age cannot be negative."
        );

    }


    if (
        raceState.safety_car &&
        raceState.virtual_safety_car
    ) {

        throw new Error(
            "Safety Car and Virtual Safety Car cannot both be active."
        );

    }

}


// ==========================================================
// PAGE STATES
// ==========================================================

function showLoading() {

    emptyState.classList.add(
        "hidden"
    );


    resultContent.classList.add(
        "hidden"
    );


    loadingState.classList.remove(
        "hidden"
    );


    formError.classList.add(
        "hidden"
    );


    analyseButton.disabled =
        true;


    analyseButton.classList.add(
        "loading"
    );

}


function hideLoading() {

    loadingState.classList.add(
        "hidden"
    );


    analyseButton.disabled =
        false;


    analyseButton.classList.remove(
        "loading"
    );

}


function showError(
    message
) {

    hideLoading();


    formError.textContent =
        message;


    formError.classList.remove(
        "hidden"
    );


    if (
        resultContent.classList.contains(
            "hidden"
        )
    ) {

        emptyState.classList.remove(
            "hidden"
        );

    }

}


// ==========================================================
// SAFE OBJECT HELPERS
// ==========================================================

function objectValue(
    input
) {

    return (
        input &&
        typeof input ===
            "object" &&
        !Array.isArray(
            input
        )
    )
        ? input
        : {};

}


function arrayValue(
    input
) {

    return Array.isArray(
        input
    )
        ? input
        : [];

}


// ==========================================================
// FORMAT HELPERS
// ==========================================================

function displayValue(
    input,
    fallback = "--"
) {

    if (
        input === null ||
        input === undefined ||
        input === ""
    ) {

        return fallback;

    }


    return input;

}


function formatNumber(
    input,
    decimals = 2
) {

    const number =
        Number(
            input
        );


    if (
        !Number.isFinite(
            number
        )
    ) {

        return "--";

    }


    return number.toFixed(
        decimals
    );

}


function formatPercentage(
    input,
    decimals = 1
) {

    const number =
        Number(
            input
        );


    if (
        !Number.isFinite(
            number
        )
    ) {

        return "--";

    }


    const percentage =
        number <= 1
            ? number * 100
            : number;


    return `${percentage.toFixed(
        decimals
    )}%`;

}


// ==========================================================
// EXTRACT STANDARD PIPELINE
// ==========================================================

function extractPipeline(
    response
) {

    const data =
        objectValue(
            response.data
        );


    return objectValue(
        data.result
    );

}


function extractExplanation(
    pipeline
) {

    return objectValue(
        pipeline.explanation
    );

}


function extractStrategy(
    pipeline
) {

    return objectValue(
        pipeline.strategy_engineer
    );

}


function extractRaceState(
    pipeline
) {

    return objectValue(
        pipeline.race_state
    );

}


function extractAlternatives(
    pipeline
) {

    return objectValue(
        pipeline.alternatives
    );

}


function extractPitWindow(
    pipeline
) {

    return objectValue(
        pipeline.pit_window
    );

}


// ==========================================================
// RENDER MAIN DECISION
// ==========================================================

function renderDecision(
    pipeline
) {

    const explanation =
        extractExplanation(
            pipeline
        );


    const strategy =
        extractStrategy(
            pipeline
        );


    const recommendation =
        explanation.final_recommendation ??
        explanation.recommendation ??
        strategy.recommendation ??
        "--";


    const tyre =
        explanation.recommended_tyre ??
        strategy.recommended_tyre ??
        "--";


    const confidence =
        explanation.confidence ??
        explanation.engineer_confidence ??
        strategy.confidence ??
        null;


    const raceSituation =
        strategy.race_situation ??
        explanation.race_situation ??
        "--";


    setText(
        "recommendation",
        displayValue(
            recommendation
        )
    );


    setText(
        "recommended-tyre",
        displayValue(
            tyre
        )
    );


    setText(
        "confidence",
        confidence !== null
            ? formatPercentage(
                confidence
            )
            : "--"
    );


    setText(
        "race-situation",
        displayValue(
            raceSituation
        )
    );


    renderRisk(
        explanation
    );

}


// ==========================================================
// RISK
// ==========================================================

function renderRisk(
    explanation
) {

    const risk =
        String(
            explanation.risk_level ??
            explanation.strategic_risk ??
            "--"
        ).toUpperCase();


    const badge =
        getElement(
            "risk-badge"
        );


    if (!badge) {

        return;

    }


    badge.textContent =
        risk === "--"
            ? "--"
            : `${risk} RISK`;


    badge.classList.remove(
        "risk-low",
        "risk-medium",
        "risk-high"
    );


    badge.style.color =
        "";


    badge.style.borderColor =
        "";


    if (
        risk ===
        "LOW"
    ) {

        badge.classList.add(
            "risk-low"
        );


        badge.style.color =
            "#45d483";


        badge.style.borderColor =
            "#45d483";

    }


    if (
        risk === "MEDIUM" ||
        risk === "MODERATE"
    ) {

        badge.classList.add(
            "risk-medium"
        );


        badge.style.color =
            "#ffb020";


        badge.style.borderColor =
            "#ffb020";

    }


    if (
        risk === "HIGH" ||
        risk === "CRITICAL"
    ) {

        badge.classList.add(
            "risk-high"
        );


        badge.style.color =
            "#ff4747";


        badge.style.borderColor =
            "#ff4747";

    }

}


// ==========================================================
// RENDER METRICS
// ==========================================================

function renderMetrics(
    pipeline
) {

    const state =
        extractRaceState(
            pipeline
        );


    const pit =
        extractPitWindow(
            pipeline
        );


    const currentLap =
        state.CurrentLap ??
        state.current_lap;


    const totalLaps =
        state.TotalLaps ??
        state.total_laps;


    const position =
        state.Position ??
        state.position;


    const tyreAge =
        state.TyreAge ??
        state.TyreLife ??
        state.tyre_age ??
        state.tyre_life;


    setText(
        "result-lap",

        (
            currentLap !== undefined &&
            totalLaps !== undefined
        )

            ? `${currentLap}/${totalLaps}`

            : "--"
    );


    setText(
        "result-position",

        position !== undefined

            ? `P${position}`

            : "--"
    );


    setText(
        "result-tyre-age",

        tyreAge !== undefined

            ? `${tyreAge} laps`

            : "--"
    );


    const urgency =
        pit.pit_urgency ??
        pit.PitUrgency ??
        null;


    setText(
        "pit-urgency",

        urgency !== null

            ? `${formatNumber(
                urgency,
                1
            )}/100`

            : "--"
    );

}


// ==========================================================
// RENDER PIT WINDOW
// ==========================================================

function renderPitWindow(
    pipeline
) {

    const pit =
        extractPitWindow(
            pipeline
        );


    const recommendedLap =
        pit.recommended_pit_lap ??
        pit.optimal_pit_lap ??
        "--";


    let optimalWindow =
        pit.optimal_window ??
        pit.pit_window ??
        "--";


    if (
        typeof optimalWindow ===
            "object" &&
        optimalWindow !== null
    ) {

        const start =
            optimalWindow.start ??
            optimalWindow.start_lap;


        const end =
            optimalWindow.end ??
            optimalWindow.end_lap;


        if (
            start !== undefined &&
            end !== undefined
        ) {

            optimalWindow =
                `Lap ${start} – ${end}`;

        }

    }


    const confidence =
        pit.window_confidence ??
        pit.confidence ??
        null;


    setText(
        "recommended-pit-lap",

        recommendedLap !== "--"

            ? `Lap ${recommendedLap}`

            : "--"
    );


    setText(
        "optimal-window",

        displayValue(
            optimalWindow
        )
    );


    setText(
        "window-confidence",

        confidence !== null

            ? formatPercentage(
                confidence
            )

            : "--"
    );

}


// ==========================================================
// RENDER STRATEGY ALTERNATIVES
// ==========================================================

function renderAlternatives(
    pipeline
) {

    const alternativesData =
        extractAlternatives(
            pipeline
        );


    let alternatives =
        arrayValue(
            alternativesData.alternatives ??
            alternativesData.strategies ??
            alternativesData.ranked_strategies
        );


    if (
        !alternatives.length &&
        Array.isArray(
            pipeline.alternatives
        )
    ) {

        alternatives =
            pipeline.alternatives;

    }


    const table =
        getElement(
            "alternatives-table"
        );


    if (!table) {

        return;

    }


    table.innerHTML =
        "";


    if (
        !alternatives.length
    ) {

        table.innerHTML = `
            <tr>
                <td colspan="5">
                    No strategy alternatives available.
                </td>
            </tr>
        `;


        return;

    }


    alternatives.forEach(
        (
            strategy,
            index
        ) => {

            const row =
                document.createElement(
                    "tr"
                );


            const rank =
                strategy.rank ??
                index + 1;


            const name =
                strategy.strategy ??
                strategy.name ??
                strategy.display_name ??
                strategy.recommendation ??
                "--";


            const score =
                strategy.dynamic_score ??
                strategy.StrategyScore ??
                strategy.score ??
                "--";


            const projectedTime =
                strategy.projected_time ??
                strategy.total_time ??
                strategy.time ??
                "--";


            const stops =
                strategy.stops ??
                strategy.pit_stops ??
                strategy.number_of_stops ??
                "--";


            const values = [

                rank,

                displayValue(
                    name
                ),

                score !== "--"
                    ? formatNumber(
                        score,
                        2
                    )
                    : "--",

                projectedTime !== "--"
                    ? `${formatNumber(
                        projectedTime,
                        3
                    )}s`
                    : "--",

                displayValue(
                    stops
                )

            ];


            values.forEach(
                item => {

                    const cell =
                        document.createElement(
                            "td"
                        );


                    cell.textContent =
                        item;


                    row.appendChild(
                        cell
                    );

                }
            );


            table.appendChild(
                row
            );

        }
    );

}


// ==========================================================
// RENDER EXPLANATION
// ==========================================================

function renderExplanation(
    pipeline
) {

    const explanation =
        extractExplanation(
            pipeline
        );


    const text =
        explanation.engineer_explanation ??
        explanation.explanation ??
        explanation.reasoning ??
        explanation.strategy_summary ??
        "--";


    setText(
        "engineer-explanation",

        displayValue(
            text
        )
    );

}


// ==========================================================
// RENDER STRATEGIC FACTORS
// ==========================================================

function renderFactors(
    pipeline
) {

    const explanation =
        extractExplanation(
            pipeline
        );


    const state =
        extractRaceState(
            pipeline
        );


    let factors =
        explanation.strategic_factors ??
        explanation.key_factors ??
        {};


    if (
        !factors ||
        typeof factors !==
            "object" ||
        Array.isArray(
            factors
        )
    ) {

        factors =
            {};

    }


    if (
        Object.keys(
            factors
        ).length === 0
    ) {

        factors = {

            "Current Lap":
                state.CurrentLap ??
                state.current_lap,

            "Laps Remaining":
                state.LapsRemaining ??
                state.laps_remaining,

            "Position":
                state.Position ??
                state.position,

            "Current Tyre":
                state.TyreCompound ??
                state.tyre_compound,

            "Tyre Age":
                state.TyreAge ??
                state.TyreLife ??
                state.tyre_age,

            "Tyre Condition":
                state.TyreCondition ??
                state.tyre_condition,

            "Degradation":
                state.DegradationRate ??
                state.degradation_rate,

            "Gap Ahead":
                state.GapAhead ??
                state.gap_ahead,

            "Gap Behind":
                state.GapBehind ??
                state.gap_behind

        };

    }


    const container =
        getElement(
            "strategic-factors"
        );


    if (!container) {

        return;

    }


    container.innerHTML =
        "";


    Object.entries(
        factors
    ).forEach(
        (
            [
                key,
                factorValue
            ]
        ) => {

            if (
                factorValue === undefined ||
                factorValue === null ||
                factorValue === ""
            ) {

                return;

            }


            const item =
                document.createElement(
                    "div"
                );


            item.className =
                "factor";


            const label =
                document.createElement(
                    "span"
                );


            const result =
                document.createElement(
                    "strong"
                );


            label.textContent =
                key;


            result.textContent =
                factorValue;


            item.append(
                label,
                result
            );


            container.appendChild(
                item
            );

        }
    );

}


// ==========================================================
// RENDER WARNINGS
// ==========================================================

function renderWarnings(
    pipeline
) {

    const explanation =
        extractExplanation(
            pipeline
        );


    const warnings =
        arrayValue(
            explanation.warnings ??
            explanation.strategy_warnings
        );


    const card =
        getElement(
            "warnings-card"
        );


    const list =
        getElement(
            "strategy-warnings"
        );


    if (
        !card ||
        !list
    ) {

        return;

    }


    list.innerHTML =
        "";


    if (
        !warnings.length
    ) {

        card.classList.add(
            "hidden"
        );


        return;

    }


    card.classList.remove(
        "hidden"
    );


    warnings.forEach(
        warning => {

            const item =
                document.createElement(
                    "li"
                );


            item.textContent =
                typeof warning ===
                    "string"

                    ? warning

                    : JSON.stringify(
                        warning
                    );


            list.appendChild(
                item
            );

        }
    );

}


// ==========================================================
// RENDER COMPLETE STANDARD STRATEGY RESULT
// ==========================================================

function renderStrategyResult(
    response
) {

    const pipeline =
        extractPipeline(
            response
        );


    if (
        !pipeline ||
        Object.keys(
            pipeline
        ).length === 0
    ) {

        throw new Error(
            "Strategy Engineer returned an empty result."
        );

    }


    renderDecision(
        pipeline
    );


    renderMetrics(
        pipeline
    );


    renderPitWindow(
        pipeline
    );


    renderAlternatives(
        pipeline
    );


    renderExplanation(
        pipeline
    );


    renderFactors(
        pipeline
    );


    renderWarnings(
        pipeline
    );


    hideLoading();


    emptyState.classList.add(
        "hidden"
    );


    resultContent.classList.remove(
        "hidden"
    );


    resultContent.scrollIntoView(
        {

            behavior:
                "smooth",

            block:
                "start"

        }
    );

}


// ==========================================================
// PHASE 7.8
// EXTRACT WHAT-IF RESULT
// ==========================================================

function extractWhatIfResult(
    response
) {

    const data =
        objectValue(
            response.data
        );


    return objectValue(
        data.result
    );

}


// ==========================================================
// PHASE 7.8
// WHAT-IF LOADING STATE
// ==========================================================

function showWhatIfLoading() {

    const table =
        getElement(
            "what-if-scenarios"
        );


    if (table) {

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    Analysing what-if race scenarios...
                </td>
            </tr>
        `;

    }


    setText(
        "decision-stability",
        "--"
    );


    setText(
        "stability-classification",
        "ANALYSING"
    );


    setText(
        "stability-badge",
        "ANALYSING"
    );


    setText(
        "stable-scenarios",
        "--"
    );


    setText(
        "changed-scenarios",
        "--"
    );


    setText(
        "most-sensitive-scenario",
        "--"
    );


    setText(
        "maximum-sensitivity",
        "--"
    );


    setText(
        "what-if-base-recommendation",
        "--"
    );


    setText(
        "what-if-base-tyre",
        "--"
    );


    setText(
        "what-if-base-confidence",
        "--"
    );


    const progress =
        getElement(
            "stability-progress"
        );


    if (progress) {

        progress.style.width =
            "0%";

    }

}


// ==========================================================
// PHASE 7.8
// RENDER WHAT-IF SCENARIO TABLE
// ==========================================================

function renderWhatIfScenarios(
    result
) {

    const scenarios =
        arrayValue(
            result.scenarios
        );


    const ranking =
        arrayValue(
            result.sensitivity_ranking
        );


    const table =
        getElement(
            "what-if-scenarios"
        );


    if (!table) {

        return;

    }


    table.innerHTML =
        "";


    if (
        !scenarios.length
    ) {

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    No what-if scenario results are available.
                </td>
            </tr>
        `;


        return;

    }


    const rankMap =
        new Map();


    ranking.forEach(
        item => {

            rankMap.set(
                item.scenario,
                item.rank
            );

        }
    );


    const ordered =
        [
            ...scenarios
        ].sort(
            (
                first,
                second
            ) => {

                const firstRank =
                    rankMap.get(
                        first.name
                    ) ??
                    Number.MAX_SAFE_INTEGER;


                const secondRank =
                    rankMap.get(
                        second.name
                    ) ??
                    Number.MAX_SAFE_INTEGER;


                return (
                    firstRank -
                    secondRank
                );

            }
        );


    ordered.forEach(
        (
            scenario,
            index
        ) => {

            const decision =
                objectValue(
                    scenario.decision
                );


            const rank =
                rankMap.get(
                    scenario.name
                ) ??
                index + 1;


            const recommendation =
                decision.recommendation ??
                "--";


            const tyre =
                decision.recommended_tyre ??
                "--";


            const risk =
                decision.risk_level ??
                "--";


            const sensitivity =
                scenario.sensitivity_score;


            const row =
                document.createElement(
                    "tr"
                );


            const values = [

                rank,

                scenario.name ??
                    "--",

                recommendation,

                tyre,

                risk,

                (
                    sensitivity !== undefined &&
                    sensitivity !== null
                )

                    ? `${formatNumber(
                        sensitivity,
                        2
                    )}/100`

                    : "--"

            ];


            values.forEach(
                (
                    item,
                    cellIndex
                ) => {

                    const cell =
                        document.createElement(
                            "td"
                        );


                    cell.textContent =
                        item;


                    if (
                        cellIndex === 0
                    ) {

                        cell.classList.add(
                            "what-if-rank"
                        );

                    }


                    if (
                        cellIndex === 1
                    ) {

                        cell.classList.add(
                            "what-if-scenario"
                        );

                    }


                    if (
                        cellIndex === 2
                    ) {

                        cell.classList.add(
                            "what-if-recommendation"
                        );

                    }


                    if (
                        cellIndex === 5
                    ) {

                        cell.classList.add(
                            "what-if-sensitivity"
                        );

                    }


                    row.appendChild(
                        cell
                    );

                }
            );


            table.appendChild(
                row
            );

        }
    );

}


// ==========================================================
// PHASE 7.8
// RENDER DECISION STABILITY
// ==========================================================

function renderDecisionStability(
    result
) {

    const stability =
        objectValue(
            result.decision_stability
        );


    const percentage =
        Number(
            stability.stability_percentage
        );


    const safePercentage =
        Number.isFinite(
            percentage
        )

            ? Math.max(
                0,
                Math.min(
                    100,
                    percentage
                )
            )

            : 0;


    setText(
        "decision-stability",

        Number.isFinite(
            percentage
        )

            ? `${formatNumber(
                percentage,
                1
            )}%`

            : "--"
    );


    setText(
        "stability-classification",

        displayValue(
            stability.classification
        )
    );


    setText(
        "stability-badge",

        displayValue(
            stability.classification
        )
    );


    setText(
        "stable-scenarios",

        displayValue(
            stability.stable_scenarios
        )
    );


    setText(
        "changed-scenarios",

        displayValue(
            stability.changed_scenarios
        )
    );


    const progress =
        getElement(
            "stability-progress"
        );


    if (progress) {

        progress.style.width =
            `${safePercentage}%`;

    }

}


// ==========================================================
// PHASE 7.8
// RENDER SENSITIVITY SUMMARY
// ==========================================================

function renderSensitivitySummary(
    result
) {

    const mostSensitive =
        objectValue(
            result.most_sensitive_scenario
        );


    setText(
        "most-sensitive-scenario",

        displayValue(
            mostSensitive.scenario
        )
    );


    setText(
        "maximum-sensitivity",

        (
            mostSensitive.sensitivity_score !==
                undefined &&
            mostSensitive.sensitivity_score !==
                null
        )

            ? `${formatNumber(
                mostSensitive.sensitivity_score,
                2
            )}/100`

            : "--"
    );

}


// ==========================================================
// PHASE 7.8
// RENDER BASE DECISION
// ==========================================================

function renderWhatIfBaseDecision(
    result
) {

    const baseDecision =
        objectValue(
            result.base_decision
        );


    setText(
        "what-if-base-recommendation",

        displayValue(
            baseDecision.recommendation
        )
    );


    setText(
        "what-if-base-tyre",

        displayValue(
            baseDecision.recommended_tyre
        )
    );


    setText(
        "what-if-base-confidence",

        (
            baseDecision.confidence !==
                undefined &&
            baseDecision.confidence !==
                null
        )

            ? formatPercentage(
                baseDecision.confidence
            )

            : "--"
    );

}


// ==========================================================
// PHASE 7.8
// COMPLETE WHAT-IF RENDER
// ==========================================================

function renderWhatIfResult(
    response
) {

    const result =
        extractWhatIfResult(
            response
        );


    if (
        !result ||
        Object.keys(
            result
        ).length === 0
    ) {

        throw new Error(
            "What-If Strategy Engine returned an empty result."
        );

    }


    if (
        result.status &&
        result.status !==
            "SUCCESS"
    ) {

        throw new Error(
            "What-If Strategy Engine did not complete successfully."
        );

    }


    renderWhatIfScenarios(
        result
    );


    renderDecisionStability(
        result
    );


    renderSensitivitySummary(
        result
    );


    renderWhatIfBaseDecision(
        result
    );

}


// ==========================================================
// GENERIC POST JSON API HELPER
// ==========================================================

async function postJson(
    endpoint,
    body
) {

    const response =
        await fetch(
            endpoint,
            {

                method:
                    "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body:
                    JSON.stringify(
                        body
                    )

            }
        );


    let payload;


    try {

        payload =
            await response.json();

    }

    catch {

        throw new Error(
            "The AI service returned an invalid response."
        );

    }


    if (
        !response.ok
    ) {

        const message =
            payload?.error?.message ??
            payload?.detail ??
            payload?.message ??
            "AI strategy request failed.";


        throw new Error(
            message
        );

    }


    if (
        payload.status &&
        payload.status !==
            "SUCCESS"
    ) {

        throw new Error(
            payload?.error?.message ??
            payload?.message ??
            "AI strategy request failed."
        );

    }


    return payload;

}


// ==========================================================
// STANDARD STRATEGY API
// ==========================================================

async function runStrategyAnalysis(
    raceState
) {

    return postJson(
        STRATEGY_API,
        raceState
    );

}


// ==========================================================
// PHASE 7.8 WHAT-IF API
// ==========================================================

async function runWhatIfAnalysis(
    raceState
) {

    return postJson(
        WHAT_IF_API,
        raceState
    );

}


// ==========================================================
// PHASE 7.8 FAILURE DISPLAY
// ==========================================================

function renderWhatIfFailure(
    message
) {

    const table =
        getElement(
            "what-if-scenarios"
        );


    if (table) {

        table.innerHTML = `
            <tr>
                <td colspan="6">
                    What-if analysis unavailable: ${message}
                </td>
            </tr>
        `;

    }


    setText(
        "decision-stability",
        "--"
    );


    setText(
        "stability-classification",
        "UNAVAILABLE"
    );


    setText(
        "stability-badge",
        "UNAVAILABLE"
    );


    setText(
        "stable-scenarios",
        "--"
    );


    setText(
        "changed-scenarios",
        "--"
    );


    setText(
        "most-sensitive-scenario",
        "--"
    );


    setText(
        "maximum-sensitivity",
        "--"
    );


    const progress =
        getElement(
            "stability-progress"
        );


    if (progress) {

        progress.style.width =
            "0%";

    }

}


// ==========================================================
// FORM SUBMISSION
// ==========================================================

strategyForm.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        try {

            const raceState =
                buildStrategyRequest();


            validateStrategyRequest(
                raceState
            );


            showLoading();


            // ==================================================
            // MAIN STRATEGY ANALYSIS
            // ==================================================

            const strategyResponse =
                await runStrategyAnalysis(
                    raceState
                );


            renderStrategyResult(
                strategyResponse
            );


            // ==================================================
            // PHASE 7.8 WHAT-IF ANALYSIS
            // ==================================================

            showWhatIfLoading();


            try {

                const whatIfResponse =
                    await runWhatIfAnalysis(
                        raceState
                    );


                renderWhatIfResult(
                    whatIfResponse
                );

            }

            catch (
                whatIfError
            ) {

                console.error(
                    "What-If Strategy Error:",
                    whatIfError
                );


                /*
                The main Strategy Engineer result remains
                available even if scenario comparison fails.
                */


                renderWhatIfFailure(
                    whatIfError?.message ??
                    "Unable to evaluate scenarios."
                );

            }

        }

        catch (
            error
        ) {

            console.error(
                "Strategy Engineer Error:",
                error
            );


            showError(
                error?.message ??
                "Unable to run strategy analysis."
            );

        }

    }
);


// ==========================================================
// NAVBAR SCROLL EFFECT
// ==========================================================

function initialiseNavbar() {

    const navbar =
        document.getElementById(
            "navbar"
        );


    if (!navbar) {

        return;

    }


    const updateNavbar =
        () => {

            if (
                window.scrollY >
                20
            ) {

                navbar.classList.add(
                    "navbar-scrolled"
                );

            }

            else {

                navbar.classList.remove(
                    "navbar-scrolled"
                );

            }

        };


    window.addEventListener(
        "scroll",
        updateNavbar,
        {
            passive:
                true
        }
    );


    updateNavbar();

}


// ==========================================================
// INITIALISE PAGE
// ==========================================================

function initialisePage() {

    initialiseRaceSelectors();

    initialiseNavbar();

}


// ==========================================================
// START
// ==========================================================

if (
    document.readyState ===
    "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initialisePage
    );

}

else {

    initialisePage();

}