/*==========================================================
  HISTORICAL.JS
  F1 AI STRATEGIST — HISTORICAL DASHBOARD

  PHASES:
  2.2   Historical race selection
  2.3.1 Race results
  2.3.2 Race results integration
  2.3.3 Session / lap API
  2.3.4 Frontend session-data integration
==========================================================*/

"use strict";


/*==========================================================
  GLOBAL STATE
==========================================================*/

let historicalState = {

    season: null,

    races: [],

    selectedRace: null,

    selectedSession: null,

    sessionData: null,

    raceResults: null

};


/*==========================================================
  DOM ELEMENT HELPER
==========================================================*/

function getElement(...ids) {

    for (const id of ids) {

        const element =
            document.getElementById(id);

        if (element) {

            return element;

        }

    }

    return null;

}


/*==========================================================
  LOADING
==========================================================*/

function showLoading(
    message = "Loading..."
) {

    const loadingElement = getElement(
        "loading",
        "historicalLoading",
        "loading-overlay"
    );

    if (!loadingElement) return;

    loadingElement.textContent =
        message;

    loadingElement.style.display =
        "flex";

}


function hideLoading() {

    const loadingElement = getElement(
        "loading",
        "historicalLoading",
        "loading-overlay"
    );

    if (!loadingElement) return;

    loadingElement.style.display =
        "none";

}


/*==========================================================
  ERROR DISPLAY
==========================================================*/

function showHistoricalError(
    message
) {

    console.error(
        "[Historical Dashboard]",
        message
    );


    const errorElement = getElement(
        "historicalError",
        "errorMessage",
        "historical-error"
    );


    if (!errorElement) {

        return;

    }


    errorElement.textContent =
        message;


    errorElement.style.display =
        "block";

}


function clearHistoricalError() {

    const errorElement = getElement(
        "historicalError",
        "errorMessage",
        "historical-error"
    );


    if (!errorElement) {

        return;

    }


    errorElement.textContent =
        "";


    errorElement.style.display =
        "none";

}


/*==========================================================
  API HELPER
==========================================================*/

async function historicalFetch(
    url
) {

    const response =
        await fetch(
            url,
            {
                method: "GET",
                headers: {
                    "Accept":
                        "application/json"
                }
            }
        );


    let data;


    try {

        data =
            await response.json();

    }

    catch (error) {

        throw new Error(
            `Invalid JSON response from ${url}`
        );

    }


    if (!response.ok) {

        const message =

            data?.error ||

            data?.message ||

            `HTTP ${response.status}`;


        throw new Error(
            message
        );

    }


    return data;

}


/*==========================================================
  SAFE VALUE HELPERS
==========================================================*/

function firstValue(
    object,
    ...keys
) {

    if (
        !object ||
        typeof object !== "object"
    ) {

        return null;

    }


    for (const key of keys) {

        if (
            Object.prototype.hasOwnProperty.call(
                object,
                key
            )
            &&
            object[key] !== null
            &&
            object[key] !== undefined
        ) {

            return object[key];

        }

    }


    return null;

}


function safeText(
    value,
    fallback = "--"
) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return fallback;

    }


    return String(
        value
    );

}


/*==========================================================
  FORMAT NUMBER
==========================================================*/

function formatNumber(
    value,
    decimals = 2
) {

    const number =
        Number(
            value
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


/*==========================================================
  FORMAT POSITION
==========================================================*/

function formatPosition(
    position
) {

    if (
        position === null ||
        position === undefined ||
        position === ""
    ) {

        return "--";

    }


    const numericPosition =
        Number(
            position
        );


    if (
        Number.isFinite(
            numericPosition
        )
    ) {

        return `P${numericPosition}`;

    }


    return safeText(
        position
    );

}


/*==========================================================
  FORMAT LAP TIME
==========================================================*/

function formatLapTime(
    seconds
) {

    if (
        seconds === null ||
        seconds === undefined ||
        seconds === ""
    ) {

        return "--";

    }


    const value =
        Number(
            seconds
        );


    if (
        !Number.isFinite(
            value
        )
    ) {

        return safeText(
            seconds
        );

    }


    const minutes =
        Math.floor(
            value / 60
        );


    const remainingSeconds =
        value - (
            minutes * 60
        );


    return (
        `${minutes}:` +
        `${remainingSeconds
            .toFixed(3)
            .padStart(6, "0")}`
    );

}


/*==========================================================
  RESET DASHBOARD
==========================================================*/

function resetHistoricalDashboard() {

    historicalState.selectedRace =
        null;


    historicalState.selectedSession =
        null;


    historicalState.sessionData =
        null;


    historicalState.raceResults =
        null;


    clearRaceInformation();

    clearRaceResults();

    clearSessionData();

}


/*==========================================================
  CLEAR RACE INFORMATION
==========================================================*/

function clearRaceInformation() {

    const section = getElement(
        "raceInformation",
        "raceInfo",
        "race-information"
    );


    if (section) {

        section.style.display =
            "none";

    }


    const fields = [

        "raceName",
        "raceCircuit",
        "raceLocation",
        "raceCountry",
        "raceDate",
        "raceRound"

    ];


    for (const field of fields) {

        const element =
            getElement(
                field
            );


        if (element) {

            element.textContent =
                "--";

        }

    }

}


/*==========================================================
  CLEAR SESSION DATA
==========================================================*/

function clearSessionData() {

    const section = getElement(
        "sessionData",
        "session-data",
        "historicalSessionData"
    );


    if (section) {

        section.style.display =
            "none";

    }


    const body = getElement(
        "sessionDataBody",
        "lapDataBody",
        "historicalSessionBody"
    );


    if (body) {

        body.innerHTML =
            "";

    }

}


/*==========================================================
  PHASE 2.3.1 / 2.3.2
  CLEAR OFFICIAL RACE RESULTS
==========================================================*/

function clearRaceResults() {

    historicalState.raceResults =
        null;


    const section = getElement(
        "raceResults",
        "officialRaceResults",
        "race-results"
    );


    if (section) {

        section.style.display =
            "none";

    }


    const body = getElement(
        "raceResultsBody",
        "officialRaceResultsBody",
        "race-results-body"
    );


    if (body) {

        body.innerHTML =
            "";

    }


    const message = getElement(
        "raceResultsMessage",
        "race-results-message"
    );


    if (message) {

        message.textContent =
            "";

        message.style.display =
            "none";

    }

}


/*==========================================================
  GET SEASON SELECT
==========================================================*/

function getSeasonSelect() {

    return getElement(
        "seasonSelect",
        "historicalSeason",
        "season"
    );

}


/*==========================================================
  GET RACE SELECT
==========================================================*/

function getRaceSelect() {

    return getElement(
        "raceSelect",
        "grandPrixSelect",
        "historicalRace",
        "grandPrix"
    );

}


/*==========================================================
  GET SESSION SELECT
==========================================================*/

function getSessionSelect() {

    return getElement(
        "sessionSelect",
        "historicalSession",
        "session"
    );

}


/*==========================================================
  INITIALISE SEASON OPTIONS
==========================================================*/

function initialiseSeasonOptions() {

    const seasonSelect =
        getSeasonSelect();


    if (!seasonSelect) {

        console.warn(
            "Historical season selector was not found."
        );

        return;

    }


    const existingOptions =
        seasonSelect.querySelectorAll(
            "option"
        );


    /*
    ----------------------------------------------------------
    If HTML already contains multiple season options,
    preserve them.
    ----------------------------------------------------------
    */

    if (
        existingOptions.length > 1
    ) {

        return;

    }


    const currentYear =
        new Date()
            .getFullYear();


    /*
    ----------------------------------------------------------
    Historical FastF1 data is available for previous seasons.
    Keep a reasonable starting range.
    ----------------------------------------------------------
    */

    const firstSeason =
        2018;


    seasonSelect.innerHTML =
        "";


    const placeholder =
        document.createElement(
            "option"
        );


    placeholder.value =
        "";


    placeholder.textContent =
        "Select Season";


    seasonSelect.appendChild(
        placeholder
    );


    for (
        let year = currentYear;
        year >= firstSeason;
        year--
    ) {

        const option =
            document.createElement(
                "option"
            );


        option.value =
            String(
                year
            );


        option.textContent =
            String(
                year
            );


        seasonSelect.appendChild(
            option
        );

    }

}


/*==========================================================
  PHASE 2.2
  LOAD SEASON
==========================================================*/

async function loadSeason(
    season
) {

    clearHistoricalError();

    resetHistoricalDashboard();


    const numericSeason =
        Number(
            season
        );


    if (
        !Number.isInteger(
            numericSeason
        )
    ) {

        return;

    }


    historicalState.season =
        numericSeason;


    showLoading(
        `Loading ${numericSeason} Formula One season...`
    );


    try {

        /*
        ------------------------------------------------------
        Historical schedule endpoint.

        Multiple endpoint patterns are supported because
        different backend versions of this project used
        slightly different route names.
        ------------------------------------------------------
        */

        let data = null;

        let lastError = null;


        const endpoints = [

            `/api/historical/${numericSeason}/races`,

            `/api/historical/races?season=${numericSeason}`,

            `/api/historical/schedule/${numericSeason}`,

            `/api/historical/schedule?season=${numericSeason}`

        ];


        for (const endpoint of endpoints) {

            try {

                data =
                    await historicalFetch(
                        endpoint
                    );


                if (data) {

                    break;

                }

            }

            catch (error) {

                lastError =
                    error;

            }

        }


        if (!data) {

            throw (
                lastError ||
                new Error(
                    "Unable to load historical race schedule."
                )
            );

        }


        const races = extractRaces(
            data
        );


        historicalState.races =
            races;


        populateRaceSelector(
            races
        );

    }

    catch (error) {

        historicalState.races =
            [];


        populateRaceSelector(
            []
        );


        showHistoricalError(
            `Unable to load ${numericSeason} season: ${error.message}`
        );

    }

    finally {

        hideLoading();

    }

}


/*==========================================================
  EXTRACT RACES
==========================================================*/

function extractRaces(
    data
) {

    if (
        Array.isArray(
            data
        )
    ) {

        return data;

    }


    const possibleKeys = [

        "races",
        "schedule",
        "events",
        "data",
        "results"

    ];


    for (const key of possibleKeys) {

        if (
            Array.isArray(
                data?.[key]
            )
        ) {

            return data[key];

        }

    }


    return [];

}


/*==========================================================
  POPULATE RACE SELECTOR
==========================================================*/

function populateRaceSelector(
    races
) {

    const raceSelect =
        getRaceSelect();


    if (!raceSelect) {

        return;

    }


    raceSelect.innerHTML =
        "";


    const placeholder =
        document.createElement(
            "option"
        );


    placeholder.value =
        "";


    placeholder.textContent =
        races.length
            ?
            "Select Grand Prix"
            :
            "No races available";


    raceSelect.appendChild(
        placeholder
    );


    races.forEach(
        (
            race,
            index
        ) => {

            const raceName =

                firstValue(

                    race,

                    "grand_prix",
                    "GrandPrix",
                    "race_name",
                    "RaceName",
                    "event_name",
                    "EventName",
                    "name",
                    "OfficialEventName"

                )
                ||
                `Round ${index + 1}`;


            const round =

                firstValue(

                    race,

                    "round",
                    "Round",
                    "round_number",
                    "RoundNumber"

                );


            const option =
                document.createElement(
                    "option"
                );


            /*
            --------------------------------------------------
            Store index rather than race name.

            This avoids problems with spaces, punctuation and
            duplicate display names.
            --------------------------------------------------
            */

            option.value =
                String(
                    index
                );


            option.textContent =

                round !== null
                &&
                round !== undefined

                    ?
                    `R${round} — ${raceName}`

                    :
                    raceName;


            raceSelect.appendChild(
                option
            );

        }
    );


    raceSelect.disabled =
        races.length === 0;

}


/*==========================================================
  GET SELECTED RACE
==========================================================*/

function getSelectedRaceFromSelector() {

    const raceSelect =
        getRaceSelect();


    if (!raceSelect) {

        return null;

    }


    const value =
        raceSelect.value;


    if (
        value === ""
        ||
        value === null
        ||
        value === undefined
    ) {

        return null;

    }


    const index =
        Number(
            value
        );


    if (
        Number.isInteger(
            index
        )
        &&
        historicalState.races[index]
    ) {

        return historicalState.races[index];

    }


    /*
    ----------------------------------------------------------
    Fallback for HTML/backend versions where option.value is
    the Grand Prix name instead of the array index.
    ----------------------------------------------------------
    */

    return (
        historicalState.races.find(
            race => {

                const raceName =
                    firstValue(

                        race,

                        "grand_prix",
                        "GrandPrix",
                        "race_name",
                        "RaceName",
                        "event_name",
                        "EventName",
                        "name",
                        "OfficialEventName"

                    );


                return (
                    String(
                        raceName
                    )
                    ===
                    String(
                        value
                    )
                );

            }
        )
        ||
        null
    );

}


/*==========================================================
  GET RACE NAME
==========================================================*/

function getRaceName(
    race
) {

    return firstValue(

        race,

        "grand_prix",
        "GrandPrix",

        "race_name",
        "RaceName",

        "event_name",
        "EventName",

        "name",
        "OfficialEventName"

    );

}


/*==========================================================
  PHASE 2.2
  LOAD SELECTED RACE

  IMPORTANT FIX:
  Race Results are now explicitly loaded here.
==========================================================*/

async function loadSelectedRace() {

    clearHistoricalError();


    const race =
        getSelectedRaceFromSelector();


    if (!race) {

        historicalState.selectedRace =
            null;


        clearRaceInformation();

        clearRaceResults();

        clearSessionData();


        return;

    }


    historicalState.selectedRace =
        race;


    /*
    ----------------------------------------------------------
    Clear the previous race's data immediately.
    ----------------------------------------------------------
    */

    clearRaceResults();

    clearSessionData();


    /*
    ----------------------------------------------------------
    Display basic race information.
    ----------------------------------------------------------
    */

    displayRaceInformation(
        race
    );


    const grandPrix =
        getRaceName(
            race
        );


    if (!grandPrix) {

        showHistoricalError(
            "Unable to determine the selected Grand Prix name."
        );

        return;

    }


    showLoading(
        `Loading ${grandPrix}...`
    );


    try {

        /*
        ------------------------------------------------------
        Load session/lap data and official race results.

        Race Results used to be omitted from this flow.
        This is the key Phase 2.3.2 integration fix.
        ------------------------------------------------------
        */

        const operations = [];


        if (
            typeof loadSessionData ===
            "function"
        ) {

            operations.push(

                loadSessionData(
                    grandPrix
                )

            );

        }


        operations.push(

            loadRaceResults(
                grandPrix
            )

        );


        const results =
            await Promise.allSettled(
                operations
            );


        /*
        ------------------------------------------------------
        Promise.allSettled lets the race information page
        remain usable even if one optional historical endpoint
        fails.
        ------------------------------------------------------
        */

        const failures =
            results.filter(
                result =>
                    result.status ===
                    "rejected"
            );


        if (
            failures.length ===
            results.length
        ) {

            throw (
                failures[0]
                    ?.reason
                ||
                new Error(
                    "Unable to load historical race data."
                )
            );

        }


        failures.forEach(
            failure => {

                console.warn(
                    "Historical data component failed:",
                    failure.reason
                );

            }
        );

    }

    catch (error) {

        showHistoricalError(
            `Unable to load ${grandPrix}: ${error.message}`
        );

    }

    finally {

        hideLoading();

    }

}


/*==========================================================
  DISPLAY RACE INFORMATION
==========================================================*/

function displayRaceInformation(
    race
) {

    if (!race) {

        clearRaceInformation();

        return;

    }


    const section = getElement(
        "raceInformation",
        "raceInfo",
        "race-information"
    );


    const raceName =
        getRaceName(
            race
        );


    const circuit =

        firstValue(

            race,

            "circuit",
            "Circuit",

            "circuit_name",
            "CircuitName",

            "track",
            "Track"

        );


    const location =

        firstValue(

            race,

            "location",
            "Location",

            "locality",
            "Locality",

            "city",
            "City"

        );


    const country =

        firstValue(

            race,

            "country",
            "Country"

        );


    const date =

        firstValue(

            race,

            "date",
            "Date",

            "race_date",
            "RaceDate",

            "event_date",
            "EventDate"

        );


    const round =

        firstValue(

            race,

            "round",
            "Round",

            "round_number",
            "RoundNumber"

        );


    setText(
        "raceName",
        raceName
    );


    setText(
        "raceCircuit",
        circuit
    );


    setText(
        "raceLocation",
        location
    );


    setText(
        "raceCountry",
        country
    );


    setText(
        "raceDate",
        date
    );


    setText(
        "raceRound",
        round
    );


    if (section) {

        section.style.display =
            "";

    }

}


/*==========================================================
  SET TEXT
==========================================================*/

function setText(
    id,
    value
) {

    const element =
        getElement(
            id
        );


    if (!element) {

        return;

    }


    element.textContent =
        safeText(
            value
        );

}


/*==========================================================
  LOAD RACE RESULTS
  PHASE 2.3.1 / 2.3.2
==========================================================*/

async function loadRaceResults(
    grandPrix
) {

    const season =
        historicalState.season;


    if (!season) {

        throw new Error(
            "Season is not selected."
        );

    }


    if (
        !grandPrix ||
        !String(
            grandPrix
        ).trim()
    ) {

        throw new Error(
            "Grand Prix is not selected."
        );

    }


    /*
    ----------------------------------------------------------
    Always clear the previous race classification first.
    ----------------------------------------------------------
    */

    clearRaceResults();


    const encodedGrandPrix =
        encodeURIComponent(
            grandPrix
        );


    /*
    ----------------------------------------------------------
    Try the project's historical race-result endpoint patterns.

    The first successful endpoint is used.
    ----------------------------------------------------------
    */

    const endpoints = [

        `/api/historical/${season}/${encodedGrandPrix}/results`,

        `/api/historical/results?season=${season}&grand_prix=${encodedGrandPrix}`,

        `/api/historical/race-results?season=${season}&grand_prix=${encodedGrandPrix}`,

        `/api/historical/${season}/results?grand_prix=${encodedGrandPrix}`

    ];


    let data = null;

    let lastError = null;


    for (const endpoint of endpoints) {

        try {

            data =
                await historicalFetch(
                    endpoint
                );


            if (data) {

                break;

            }

        }

        catch (error) {

            lastError =
                error;

        }

    }


    if (!data) {

        throw (
            lastError
            ||
            new Error(
                "Unable to load official race results."
            )
        );

    }


    historicalState.raceResults =
        data;


    /*
    ----------------------------------------------------------
    IMPORTANT:
    Previous code checked whether displayRaceResults existed,
    but no renderer was actually defined.

    The renderer now exists below and is called directly.
    ----------------------------------------------------------
    */

    displayRaceResults(
        data
    );


    return data;

}


/*==========================================================
  EXTRACT RACE RESULT ROWS
==========================================================*/

function extractRaceResultRows(
    data
) {

    if (
        Array.isArray(
            data
        )
    ) {

        return data;

    }


    const possibleKeys = [

        "results",
        "race_results",
        "raceResults",
        "classification",
        "drivers",
        "data"

    ];


    for (const key of possibleKeys) {

        if (
            Array.isArray(
                data?.[key]
            )
        ) {

            return data[key];

        }

    }


    /*
    ----------------------------------------------------------
    Some backend responses wrap data one level deeper.
    ----------------------------------------------------------
    */

    const nestedObjects = [

        data?.race,
        data?.session,
        data?.result

    ];


    for (const object of nestedObjects) {

        if (
            !object ||
            typeof object !== "object"
        ) {

            continue;

        }


        for (const key of possibleKeys) {

            if (
                Array.isArray(
                    object[key]
                )
            ) {

                return object[key];

            }

        }

    }


    return [];

}


/*==========================================================
  NORMALISE ONE RACE RESULT
==========================================================*/

function normaliseRaceResult(
    result,
    index
) {

    const position =

        firstValue(

            result,

            "position",
            "Position",

            "classified_position",
            "ClassifiedPosition",

            "finish_position",
            "FinishPosition"

        )
        ??
        (
            index + 1
        );


    const driverNumber =

        firstValue(

            result,

            "driver_number",
            "DriverNumber",

            "number",
            "Number",

            "driver_no",
            "DriverNo"

        );


    let driver =

        firstValue(

            result,

            "driver",
            "Driver",

            "driver_name",
            "DriverName",

            "full_name",
            "FullName",

            "broadcast_name",
            "BroadcastName",

            "abbreviation",
            "Abbreviation"

        );


    /*
    ----------------------------------------------------------
    Handle nested driver objects.
    ----------------------------------------------------------
    */

    if (
        driver &&
        typeof driver === "object"
    ) {

        driver =

            firstValue(

                driver,

                "full_name",
                "FullName",

                "name",
                "Name",

                "broadcast_name",
                "BroadcastName",

                "abbreviation",
                "Abbreviation",

                "code",
                "Code"

            );

    }


    let team =

        firstValue(

            result,

            "team",
            "Team",

            "team_name",
            "TeamName",

            "constructor",
            "Constructor",

            "constructor_name",
            "ConstructorName"

        );


    /*
    ----------------------------------------------------------
    Handle nested constructor/team objects.
    ----------------------------------------------------------
    */

    if (
        team &&
        typeof team === "object"
    ) {

        team =

            firstValue(

                team,

                "name",
                "Name",

                "team_name",
                "TeamName",

                "constructor_name",
                "ConstructorName"

            );

    }


    const laps =

        firstValue(

            result,

            "laps",
            "Laps",

            "laps_completed",
            "LapsCompleted",

            "completed_laps",
            "CompletedLaps"

        );


    const points =

        firstValue(

            result,

            "points",
            "Points",

            "championship_points",
            "ChampionshipPoints"

        );


    return {

        position:
            position,

        driver:
            driver,

        driverNumber:
            driverNumber,

        team:
            team,

        laps:
            laps,

        points:
            points

    };

}


/*==========================================================
  CREATE TABLE CELL
==========================================================*/

function createRaceResultCell(
    value,
    className = ""
) {

    const cell =
        document.createElement(
            "td"
        );


    if (className) {

        cell.className =
            className;

    }


    cell.textContent =
        safeText(
            value
        );


    return cell;

}


/*==========================================================
  DISPLAY RACE RESULTS
  PHASE 2.3.2 — FIXED

  TABLE:
      Position
      Driver
      Driver Number
      Team
      Laps
      Points
==========================================================*/

function displayRaceResults(
    data
) {

    const section = getElement(
        "raceResults",
        "officialRaceResults",
        "race-results"
    );


    const body = getElement(
        "raceResultsBody",
        "officialRaceResultsBody",
        "race-results-body"
    );


    const message = getElement(
        "raceResultsMessage",
        "race-results-message"
    );


    if (!body) {

        console.warn(
            "Race results table body was not found. " +
            "Expected element id: raceResultsBody"
        );

        return;

    }


    const rows =
        extractRaceResultRows(
            data
        );


    body.innerHTML =
        "";


    /*
    ----------------------------------------------------------
    EMPTY RESULTS
    ----------------------------------------------------------
    */

    if (
        !rows.length
    ) {

        if (section) {

            section.style.display =
                "";

        }


        if (message) {

            message.textContent =
                "Official race results are unavailable for this event.";

            message.style.display =
                "block";

        }


        return;

    }


    if (message) {

        message.textContent =
            "";

        message.style.display =
            "none";

    }


    /*
    ----------------------------------------------------------
    BUILD CLASSIFICATION TABLE
    ----------------------------------------------------------
    */

    rows.forEach(
        (
            rawResult,
            index
        ) => {

            const result =
                normaliseRaceResult(
                    rawResult,
                    index
                );


            const row =
                document.createElement(
                    "tr"
                );


            /*
            --------------------------------------------------
            Position
            --------------------------------------------------
            */

            row.appendChild(

                createRaceResultCell(

                    formatPosition(
                        result.position
                    ),

                    "race-result-position"

                )

            );


            /*
            --------------------------------------------------
            Driver
            --------------------------------------------------
            */

            row.appendChild(

                createRaceResultCell(

                    result.driver,

                    "race-result-driver"

                )

            );


            /*
            --------------------------------------------------
            Driver Number
            --------------------------------------------------
            */

            row.appendChild(

                createRaceResultCell(

                    result.driverNumber,

                    "race-result-number"

                )

            );


            /*
            --------------------------------------------------
            Team
            --------------------------------------------------
            */

            row.appendChild(

                createRaceResultCell(

                    result.team,

                    "race-result-team"

                )

            );


            /*
            --------------------------------------------------
            Laps
            --------------------------------------------------
            */

            row.appendChild(

                createRaceResultCell(

                    result.laps,

                    "race-result-laps"

                )

            );


            /*
            --------------------------------------------------
            Points
            --------------------------------------------------
            */

            row.appendChild(

                createRaceResultCell(

                    result.points,

                    "race-result-points"

                )

            );


            body.appendChild(
                row
            );

        }
    );


    /*
    ----------------------------------------------------------
    SHOW THE OFFICIAL RACE RESULTS SECTION
    ----------------------------------------------------------
    */

    if (section) {

        section.style.display =
            "";

        section.hidden =
            false;

    }


    console.log(
        `[Historical Dashboard] Displayed ${rows.length} official race results.`
    );

}


/*==========================================================
  SESSION DATA
==========================================================*/

async function loadSessionData(
    grandPrix
) {

    const season =
        historicalState.season;


    if (
        !season ||
        !grandPrix
    ) {

        return null;

    }


    const sessionSelect =
        getSessionSelect();


    const selectedSession =

        sessionSelect?.value
        ||
        historicalState.selectedSession
        ||
        "R";


    historicalState.selectedSession =
        selectedSession;


    const encodedGrandPrix =
        encodeURIComponent(
            grandPrix
        );


    const encodedSession =
        encodeURIComponent(
            selectedSession
        );


    const endpoints = [

        `/api/historical/${season}/${encodedGrandPrix}/session/${encodedSession}`,

        `/api/historical/session?season=${season}&grand_prix=${encodedGrandPrix}&session=${encodedSession}`,

        `/api/historical/laps?season=${season}&grand_prix=${encodedGrandPrix}&session=${encodedSession}`

    ];


    let data = null;

    let lastError = null;


    for (const endpoint of endpoints) {

        try {

            data =
                await historicalFetch(
                    endpoint
                );


            if (data) {

                break;

            }

        }

        catch (error) {

            lastError =
                error;

        }

    }


    if (!data) {

        /*
        ------------------------------------------------------
        Session data may be optional for some pages, therefore
        we log and return instead of breaking race results.
        ------------------------------------------------------
        */

        console.warn(
            "Historical session data unavailable:",
            lastError
        );


        return null;

    }


    historicalState.sessionData =
        data;


    if (
        typeof displaySessionData ===
        "function"
    ) {

        displaySessionData(
            data
        );

    }


    return data;

}


/*==========================================================
  HANDLE SESSION CHANGE
==========================================================*/

async function handleSessionChange() {

    const sessionSelect =
        getSessionSelect();


    if (!sessionSelect) {

        return;

    }


    historicalState.selectedSession =
        sessionSelect.value;


    const race =
        historicalState.selectedRace;


    if (!race) {

        return;

    }


    const grandPrix =
        getRaceName(
            race
        );


    if (!grandPrix) {

        return;

    }


    showLoading(
        "Loading session data..."
    );


    try {

        await loadSessionData(
            grandPrix
        );

    }

    catch (error) {

        showHistoricalError(
            `Unable to load session data: ${error.message}`
        );

    }

    finally {

        hideLoading();

    }

}

/*==========================================================
  DISPLAY SESSION DATA
==========================================================*/

function displaySessionData(
    data
) {

    if (!data) {

        return;

    }


    const sessionDriverCount =
        getElement(
            "sessionDriverCount",
            "driverCount",
            "session-driver-count"
        );


    const sessionLapCount =
        getElement(
            "sessionLapCount",
            "lapCount",
            "session-lap-count"
        );


    const sessionName =
        getElement(
            "sessionName",
            "session-name"
        );


    const sessionDataSection =
        getElement(
            "sessionData",
            "session-data",
            "sessionDataSection"
        );


    if (sessionDriverCount) {

        sessionDriverCount.textContent =

            data.driver_count
            ??
            data.drivers?.length
            ??
            "--";

    }


    if (sessionLapCount) {

        sessionLapCount.textContent =

            data.lap_count
            ??
            data.laps?.length
            ??
            "--";

    }


    if (sessionName) {

        sessionName.textContent =

            data.session
            ||
            data.session_name
            ||
            "Race";

    }


    if (sessionDataSection) {

        sessionDataSection.style.display =
            "block";

    }


    console.log(
        "Session data prepared for frontend."
    );

}


/*==========================================================
  IMPORTANT COMPATIBILITY FIX

  Your current historical.html uses:

      eventName
      countryName
      locationName
      totalLaps
      raceInfo

  Therefore we keep compatibility with those exact IDs.
==========================================================*/

function displayRaceInfo(
    data
) {

    if (!data) {

        clearRaceInfo();

        return;

    }


    const eventName =
        getElement(
            "eventName",
            "event-name",
            "raceName"
        );


    const countryName =
        getElement(
            "countryName",
            "country-name",
            "raceCountry"
        );


    const locationName =
        getElement(
            "locationName",
            "location-name",
            "raceLocation"
        );


    const totalLaps =
        getElement(
            "totalLaps",
            "total-laps",
            "laps"
        );


    const raceInfo =
        getElement(
            "raceInfo",
            "race-info",
            "raceInformation"
        );


    const eventValue =

        data.event
        ||
        data.event_name
        ||
        data.EventName
        ||
        data.name
        ||
        "--";


    const countryValue =

        data.country
        ||
        data.Country
        ||
        "--";


    const locationValue =

        data.location
        ||
        data.Location
        ||
        "--";


    const lapsValue =

        data.laps
        ??
        data.total_laps
        ??
        data.TotalLaps
        ??
        "--";


    if (eventName) {

        eventName.textContent =
            eventValue;

    }


    if (countryName) {

        countryName.textContent =
            countryValue;

    }


    if (locationName) {

        locationName.textContent =
            locationValue;

    }


    if (totalLaps) {

        totalLaps.textContent =
            lapsValue;

    }


    if (raceInfo) {

        raceInfo.style.display =
            "block";

    }

}


/*==========================================================
  CLEAR RACE INFO
==========================================================*/

function clearRaceInfo() {

    const eventName =
        getElement(
            "eventName",
            "event-name",
            "raceName"
        );


    const countryName =
        getElement(
            "countryName",
            "country-name",
            "raceCountry"
        );


    const locationName =
        getElement(
            "locationName",
            "location-name",
            "raceLocation"
        );


    const totalLaps =
        getElement(
            "totalLaps",
            "total-laps",
            "laps"
        );


    const raceInfo =
        getElement(
            "raceInfo",
            "race-info",
            "raceInformation"
        );


    if (eventName) {

        eventName.textContent =
            "--";

    }


    if (countryName) {

        countryName.textContent =
            "--";

    }


    if (locationName) {

        locationName.textContent =
            "--";

    }


    if (totalLaps) {

        totalLaps.textContent =
            "--";

    }


    if (raceInfo) {

        raceInfo.style.display =
            "none";

    }

}


/*==========================================================
  RESULTS EMPTY STATE
==========================================================*/

function displayEmptyRaceResults(
    message = "No race results available."
) {

    const raceResultsSection =
        getElement(
            "raceResults",
            "officialRaceResults",
            "race-results"
        );


    const body =
        getElement(
            "raceResultsBody",
            "officialRaceResultsBody",
            "race-results-body"
        );


    if (!body) {

        return;

    }


    body.innerHTML =
        "";


    const row =
        document.createElement(
            "tr"
        );


    const cell =
        document.createElement(
            "td"
        );


    cell.colSpan =
        6;


    const empty =
        document.createElement(
            "div"
        );


    empty.className =
        "historical-results-empty";


    empty.textContent =
        message;


    cell.appendChild(
        empty
    );


    row.appendChild(
        cell
    );


    body.appendChild(
        row
    );


    if (raceResultsSection) {

        raceResultsSection.style.display =
            "block";

        raceResultsSection.hidden =
            false;

    }

}


/*==========================================================
  DRIVER NAME NORMALISER
==========================================================*/

function extractDriverName(
    result
) {

    let value =

        result.driver
        ??
        result.Driver
        ??
        result.driver_name
        ??
        result.DriverName
        ??
        result.full_name
        ??
        result.FullName
        ??
        result.name
        ??
        null;


    if (
        value &&
        typeof value === "object"
    ) {

        value =

            value.full_name
            ??
            value.FullName
            ??
            value.name
            ??
            value.Name
            ??
            value.broadcast_name
            ??
            value.BroadcastName
            ??
            value.abbreviation
            ??
            value.Abbreviation
            ??
            null;

    }


    return (
        value
        ??
        "--"
    );

}


/*==========================================================
  DRIVER ABBREVIATION NORMALISER
==========================================================*/

function extractDriverCode(
    result
) {

    let value =

        result.abbreviation
        ??
        result.Abbreviation
        ??
        result.driver_code
        ??
        result.DriverCode
        ??
        result.code
        ??
        null;


    const driverObject =

        result.driver
        ??
        result.Driver;


    if (
        !value &&
        driverObject &&
        typeof driverObject === "object"
    ) {

        value =

            driverObject.abbreviation
            ??
            driverObject.Abbreviation
            ??
            driverObject.code
            ??
            driverObject.Code
            ??
            driverObject.tla
            ??
            driverObject.Tla
            ??
            null;

    }


    return value;

}


/*==========================================================
  TEAM NORMALISER
==========================================================*/

function extractTeamName(
    result
) {

    let value =

        result.team
        ??
        result.Team
        ??
        result.team_name
        ??
        result.TeamName
        ??
        result.constructor
        ??
        result.Constructor
        ??
        result.constructor_name
        ??
        result.ConstructorName
        ??
        null;


    if (
        value &&
        typeof value === "object"
    ) {

        value =

            value.name
            ??
            value.Name
            ??
            value.team_name
            ??
            value.TeamName
            ??
            value.constructor_name
            ??
            value.ConstructorName
            ??
            null;

    }


    return (
        value
        ??
        "--"
    );

}


/*==========================================================
  FULL RACE RESULTS RENDERER
==========================================================*/

function displayRaceResults(
    data
) {

    console.log(
        "Rendering race results:",
        data
    );


    const raceResultsSection =
        getElement(
            "raceResults",
            "officialRaceResults",
            "race-results"
        );


    const body =
        getElement(
            "raceResultsBody",
            "officialRaceResultsBody",
            "race-results-body"
        );


    if (!body) {

        console.error(
            "raceResultsBody element was not found."
        );

        return;

    }


    const results =
        extractRaceResultRows(
            data
        );


    if (
        !Array.isArray(
            results
        )
        ||
        results.length === 0
    ) {

        displayEmptyRaceResults(
            "No official driver classification is available for this Grand Prix."
        );

        return;

    }


    body.innerHTML =
        "";


    results.forEach(
        (
            result,
            index
        ) => {

            const row =
                document.createElement(
                    "tr"
                );


            /*================================================
              POSITION
            ================================================*/

            const positionCell =
                document.createElement(
                    "td"
                );


            const position =

                result.position
                ??
                result.Position
                ??
                result.finish_position
                ??
                result.FinishPosition
                ??
                (
                    index + 1
                );


            positionCell.textContent =
                position;


            /*================================================
              DRIVER
            ================================================*/

            const driverCell =
                document.createElement(
                    "td"
                );


            const driverName =
                extractDriverName(
                    result
                );


            const driverCode =
                extractDriverCode(
                    result
                );


            const driverNameElement =
                document.createElement(
                    "span"
                );


            driverNameElement.className =
                "historical-driver-name";


            driverNameElement.textContent =
                driverName;


            driverCell.appendChild(
                driverNameElement
            );


            if (driverCode) {

                const codeElement =
                    document.createElement(
                        "span"
                    );


                codeElement.className =
                    "historical-driver-code";


                codeElement.textContent =
                    driverCode;


                driverCell.appendChild(
                    codeElement
                );

            }


            /*================================================
              DRIVER NUMBER
            ================================================*/

            const numberCell =
                document.createElement(
                    "td"
                );


            const driverNumber =

                result.driver_number
                ??
                result.DriverNumber
                ??
                result.number
                ??
                result.Number
                ??
                result.driver_no
                ??
                "--";


            numberCell.textContent =
                driverNumber;


            /*================================================
              TEAM
            ================================================*/

            const teamCell =
                document.createElement(
                    "td"
                );


            const teamName =
                extractTeamName(
                    result
                );


            const teamElement =
                document.createElement(
                    "span"
                );


            teamElement.className =
                "historical-team-name";


            teamElement.textContent =
                teamName;


            teamCell.appendChild(
                teamElement
            );


            /*================================================
              LAPS
            ================================================*/

            const lapsCell =
                document.createElement(
                    "td"
                );


            const laps =

                result.laps
                ??
                result.Laps
                ??
                result.laps_completed
                ??
                result.LapsCompleted
                ??
                result.completed_laps
                ??
                "--";


            lapsCell.textContent =
                laps;


            /*================================================
              POINTS
            ================================================*/

            const pointsCell =
                document.createElement(
                    "td"
                );


            const points =

                result.points
                ??
                result.Points
                ??
                result.championship_points
                ??
                0;


            const pointsElement =
                document.createElement(
                    "span"
                );


            pointsElement.className =
                "historical-points";


            pointsElement.textContent =
                points;


            pointsCell.appendChild(
                pointsElement
            );


            /*================================================
              BUILD ROW
            ================================================*/

            row.appendChild(
                positionCell
            );


            row.appendChild(
                driverCell
            );


            row.appendChild(
                numberCell
            );


            row.appendChild(
                teamCell
            );


            row.appendChild(
                lapsCell
            );


            row.appendChild(
                pointsCell
            );


            body.appendChild(
                row
            );

        }
    );


    if (raceResultsSection) {

        raceResultsSection.style.display =
            "block";

        raceResultsSection.hidden =
            false;

    }


    console.log(
        `✅ ${results.length} race result rows rendered.`
    );

}


/*==========================================================
  IMPORTANT:
  BACKEND-COMPATIBLE LOAD RACE RESULTS

  This uses the API helper already present in your api.js
  first, matching your original historical.js.
==========================================================*/

async function loadRaceResultsCompatible(
    grandPrix
) {

    const season =
        historicalState.season;


    if (
        !season ||
        !grandPrix
    ) {

        return null;

    }


    console.log(
        "Loading official race results:",
        season,
        grandPrix
    );


    try {

        let data;


        /*====================================================
          PRIMARY METHOD:
          Existing api.js function
        ====================================================*/

        if (
            typeof getRaceResults ===
            "function"
        ) {

            data =
                await getRaceResults(
                    season,
                    grandPrix
                );

        }


        /*====================================================
          FALLBACK:
          Original project Flask endpoint
        ====================================================*/

        else {

            const encodedRace =
                String(
                    grandPrix
                )
                .replace(
                    / /g,
                    "_"
                );


            const response =
                await fetch(

                    `http://127.0.0.1:5000/api/race/${season}/${encodeURIComponent(encodedRace)}/results`

                );


            if (!response.ok) {

                throw new Error(
                    `Backend HTTP ${response.status}`
                );

            }


            data =
                await response.json();

        }


        if (!data) {

            throw new Error(
                "No race result response received."
            );

        }


        if (data.error) {

            throw new Error(
                data.error
            );

        }


        historicalState.raceResults =
            data;


        displayRaceResults(
            data
        );


        console.log(
            "✅ Race results loaded successfully."
        );


        return data;

    }

    catch (error) {

        console.error(
            "Race results loading error:",
            error
        );


        historicalState.raceResults =
            null;


        displayEmptyRaceResults(
            "Unable to load official race results."
        );


        /*
        ------------------------------------------------------
        Do not throw here.

        Race Information and session analytics should remain
        usable even if the results endpoint fails.
        ------------------------------------------------------
        */

        return null;

    }

}


/*==========================================================
  POPULATE ORIGINAL RACE DROPDOWN
==========================================================*/

function populateRaceDropdown(
    races
) {

    const raceSelect =
        getElement(
            "raceSelect",
            "race",
            "race-selector",
            "grandPrix"
        );


    if (!raceSelect) {

        console.error(
            "Race dropdown not found."
        );

        return;

    }


    raceSelect.innerHTML =
        "";


    if (
        !Array.isArray(
            races
        )
        ||
        races.length === 0
    ) {

        const option =
            document.createElement(
                "option"
            );


        option.value =
            "";


        option.textContent =
            "No races available";


        raceSelect.appendChild(
            option
        );


        return;

    }


    const defaultOption =
        document.createElement(
            "option"
        );


    defaultOption.value =
        "";


    defaultOption.textContent =
        "Select a Grand Prix";


    defaultOption.selected =
        true;


    raceSelect.appendChild(
        defaultOption
    );


    races.forEach(
        (
            race,
            index
        ) => {

            const option =
                document.createElement(
                    "option"
                );


            let raceName =
                "";


            if (
                typeof race ===
                "string"
            ) {

                raceName =
                    race;

            }

            else if (
                race &&
                typeof race ===
                "object"
            ) {

                raceName =

                    race.event_name
                    ||
                    race.EventName
                    ||
                    race.event
                    ||
                    race.name
                    ||
                    race.Event
                    ||
                    race.grand_prix
                    ||
                    race.GrandPrix
                    ||
                    "";

            }


            if (!raceName) {

                raceName =
                    `Race ${index + 1}`;

            }


            option.value =
                raceName;


            option.textContent =
                raceName;


            option.dataset.index =
                index;


            raceSelect.appendChild(
                option
            );

        }
    );


    console.log(
        "Race dropdown populated:",
        raceSelect.options.length,
        "options"
    );

}


/*==========================================================
  ORIGINAL BACKEND-COMPATIBLE SEASON LOADER
==========================================================*/

async function loadHistoricalRaces(
    season
) {

    hideError();

    clearRaceInfo();

    clearRaceResults();


    historicalState.sessionData =
        null;


    historicalState.raceResults =
        null;


    if (!season) {

        return;

    }


    const numericSeason =
        Number(
            season
        );


    if (
        !Number.isInteger(
            numericSeason
        )
    ) {

        showError(
            "Please select a valid F1 season."
        );


        return;

    }


    historicalState.season =
        numericSeason;


    historicalState.races =
        [];


    historicalState.selectedRace =
        null;


    historicalState.selectedSession =
        null;


    console.log(
        "Selected season:",
        numericSeason
    );


    showLoading(
        `Loading ${numericSeason} races...`
    );


    try {

        if (
            typeof getRaces !==
            "function"
        ) {

            throw new Error(
                "getRaces() is not available from api.js."
            );

        }


        const data =
            await getRaces(
                numericSeason
            );


        if (!data) {

            throw new Error(
                "No response received from backend."
            );

        }


        if (
            !Array.isArray(
                data.races
            )
        ) {

            throw new Error(
                "Invalid race data received."
            );

        }


        historicalState.races =
            data.races;


        populateRaceDropdown(
            data.races
        );


        console.log(
            `Loaded ${data.races.length} races for ${numericSeason}.`
        );

    }

    catch (error) {

        console.error(
            "Race loading error:",
            error
        );


        historicalState.races =
            [];


        const raceSelect =
            getElement(
                "raceSelect",
                "race",
                "race-selector",
                "grandPrix"
            );


        if (raceSelect) {

            raceSelect.innerHTML =
                "";


            const option =
                document.createElement(
                    "option"
                );


            option.value =
                "";


            option.textContent =
                "Unable to load races";


            raceSelect.appendChild(
                option
            );

        }


        showError(
            `Unable to load races for ${numericSeason}.`
        );

    }

    finally {

        hideLoading();

    }

}


/*==========================================================
  UPDATED SELECTED RACE LOADER

  THIS IS THE MAIN FIX.

  After loading race info we now load BOTH:

      Session data
      Official race results
==========================================================*/

async function loadSelectedRaceCompatible(
    grandPrix
) {

    hideError();

    clearRaceInfo();

    clearRaceResults();


    historicalState.selectedRace =
        null;


    historicalState.selectedSession =
        null;


    historicalState.sessionData =
        null;


    historicalState.raceResults =
        null;


    if (!grandPrix) {

        return;

    }


    const season =
        historicalState.season;


    if (!season) {

        showError(
            "Please select a season first."
        );


        return;

    }


    showLoading(
        "Loading race information..."
    );


    try {

        if (
            typeof getRace !==
            "function"
        ) {

            throw new Error(
                "getRace() is not available from api.js."
            );

        }


        const data =
            await getRace(
                season,
                grandPrix
            );


        if (!data) {

            throw new Error(
                "No race information received."
            );

        }


        historicalState.selectedRace =
            data;


        displayRaceInfo(
            data
        );


        console.log(
            "Selected race:",
            data
        );


        /*====================================================
          LOAD SESSION DATA
        ====================================================*/

        const sessionPromise =
            loadSessionData(
                grandPrix,
                "R"
            );


        /*====================================================
          LOAD OFFICIAL RACE RESULTS

          This call was missing in your old code.
        ====================================================*/

        const resultsPromise =
            loadRaceResultsCompatible(
                grandPrix
            );


        await Promise.allSettled(
            [
                sessionPromise,
                resultsPromise
            ]
        );


        console.log(
            "✅ Historical race data loading completed."
        );

    }

    catch (error) {

        console.error(
            "Race information error:",
            error
        );


        historicalState.selectedRace =
            null;


        showError(
            `Unable to load information for ${grandPrix}.`
        );

    }

    finally {

        hideLoading();

    }

}


/*==========================================================
  ORIGINAL LOADING / ERROR COMPATIBILITY
==========================================================*/

function showError(
    message
) {

    console.error(
        "Historical Dashboard Error:",
        message
    );


    const errorElement =
        getElement(
            "error",
            "historicalError",
            "error-message"
        );


    if (!errorElement) {

        return;

    }


    errorElement.textContent =
        message;


    errorElement.style.display =
        "block";

}


function hideError() {

    const errorElement =
        getElement(
            "error",
            "historicalError",
            "error-message"
        );


    if (!errorElement) {

        return;

    }


    errorElement.textContent =
        "";


    errorElement.style.display =
        "none";

}


/*==========================================================
  RACE CHANGE
==========================================================*/

async function handleRaceChange(
    event
) {

    console.log(
        "RACE CHANGE EVENT FIRED"
    );


    const grandPrix =
        event.target.value;


    console.log(
        "Grand Prix selected:",
        grandPrix
    );


    await loadSelectedRaceCompatible(
        grandPrix
    );

}


/*==========================================================
  SEASON CHANGE
==========================================================*/

function handleSeasonChange(
    event
) {

    console.log(
        "SEASON CHANGE EVENT FIRED"
    );


    const season =
        event.target.value;


    console.log(
        "Season selected:",
        season
    );


    clearRaceResults();


    loadHistoricalRaces(
        season
    );

}


/*==========================================================
  ATTACH EVENT LISTENERS
==========================================================*/

function attachEventListeners() {

    const seasonSelect =
        getElement(
            "seasonSelect",
            "season",
            "season-selector"
        );


    const raceSelect =
        getElement(
            "raceSelect",
            "race",
            "race-selector",
            "grandPrix"
        );


    const sessionSelect =
        getElement(
            "sessionSelect",
            "session",
            "historicalSession"
        );


    if (seasonSelect) {

        seasonSelect.removeEventListener(
            "change",
            handleSeasonChange
        );


        seasonSelect.addEventListener(
            "change",
            handleSeasonChange
        );


        console.log(
            "Season change listener attached."
        );

    }


    if (raceSelect) {

        raceSelect.removeEventListener(
            "change",
            handleRaceChange
        );


        raceSelect.addEventListener(
            "change",
            handleRaceChange
        );


        console.log(
            "Race change listener attached."
        );

    }


    if (sessionSelect) {

        sessionSelect.removeEventListener(
            "change",
            handleSessionChange
        );


        sessionSelect.addEventListener(
            "change",
            handleSessionChange
        );

    }

}


/*==========================================================
  BACKEND CONNECTION
==========================================================*/

async function verifyBackendConnection() {

    try {

        if (
            typeof checkBackend !==
            "function"
        ) {

            console.warn(
                "checkBackend() is unavailable. Continuing initialization."
            );


            return true;

        }


        const connected =
            await checkBackend();


        if (!connected) {

            throw new Error(
                "Backend is not reachable."
            );

        }


        console.log(
            "F1 backend connection successful."
        );


        return true;

    }

    catch (error) {

        console.error(
            "Backend connection failed:",
            error
        );


        showError(
            "Backend connection failed. Please start the Flask server."
        );


        return false;

    }

}


/*==========================================================
  INITIALIZE DASHBOARD
==========================================================*/

async function initializeHistoricalDashboard() {

    console.log(
        "============================================"
    );


    console.log(
        "F1 AI STRATEGIST — HISTORICAL DASHBOARD"
    );


    console.log(
        "Initializing Historical Dashboard..."
    );


    console.log(
        "============================================"
    );


    attachEventListeners();


    clearRaceResults();


    const backendAvailable =
        await verifyBackendConnection();


    if (!backendAvailable) {

        return;

    }


    const seasonSelect =
        getElement(
            "seasonSelect",
            "season",
            "season-selector"
        );


    if (
        seasonSelect &&
        seasonSelect.value
    ) {

        await loadHistoricalRaces(
            seasonSelect.value
        );

    }


    console.log(
        "✅ Historical Dashboard initialized."
    );

}


/*==========================================================
  DOM READY
==========================================================*/

document.addEventListener(
    "DOMContentLoaded",
    initializeHistoricalDashboard
);


/*==========================================================
  DEBUG / MANUAL ACCESS
==========================================================*/

window.historicalState =
    historicalState;


window.loadHistoricalRaces =
    loadHistoricalRaces;


window.loadSelectedRace =
    loadSelectedRaceCompatible;


window.loadSessionData =
    loadSessionData;


window.loadRaceResults =
    loadRaceResultsCompatible;


window.displayRaceResults =
    displayRaceResults;


window.clearRaceResults =
    clearRaceResults;


window.displayRaceInfo =
    displayRaceInfo;


window.displaySessionData =
    displaySessionData;


window.handleSeasonChange =
    handleSeasonChange;


window.handleRaceChange =
    handleRaceChange;


window.initializeHistoricalDashboard =
    initializeHistoricalDashboard;


/*==========================================================
  QUICK RACE RESULTS VERIFICATION

  You can run this manually in browser console:

      verifyHistoricalRaceResults()

==========================================================*/

async function verifyHistoricalRaceResults() {

    console.log(
        "============================================"
    );


    console.log(
        "HISTORICAL RACE RESULTS VERIFICATION"
    );


    console.log(
        "============================================"
    );


    historicalState.season =
        2024;


    const testRace =
        "Bahrain Grand Prix";


    console.log(
        "Testing:",
        historicalState.season,
        testRace
    );


    const data =
        await loadRaceResultsCompatible(
            testRace
        );


    if (!data) {

        console.error(
            "❌ Race results API returned no data."
        );


        return false;

    }


    const results =
        extractRaceResultRows(
            data
        );


    if (
        !Array.isArray(
            results
        )
        ||
        results.length === 0
    ) {

        console.error(
            "❌ Race classification contains no drivers."
        );


        return false;

    }


    const section =
        getElement(
            "raceResults"
        );


    const body =
        getElement(
            "raceResultsBody"
        );


    if (!section) {

        console.error(
            "❌ raceResults section not found."
        );


        return false;

    }


    if (!body) {

        console.error(
            "❌ raceResultsBody not found."
        );


        return false;

    }


    const renderedRows =
        body.querySelectorAll(
            "tr"
        );


    if (
        renderedRows.length ===
        0
    ) {

        console.error(
            "❌ No race-result rows were rendered."
        );


        return false;

    }


    console.log(
        `✅ API returned ${results.length} drivers.`
    );


    console.log(
        `✅ Frontend rendered ${renderedRows.length} rows.`
    );


    console.log(
        "✅ OFFICIAL RACE RESULTS INTEGRATION PASSED"
    );


    console.log(
        "============================================"
    );


    return true;

}


window.verifyHistoricalRaceResults =
    verifyHistoricalRaceResults;


/*==========================================================
  HISTORICAL DOM VERIFICATION
==========================================================*/

function verifyHistoricalDOM() {

    console.log(
        "============================================"
    );


    console.log(
        "HISTORICAL DOM VERIFICATION"
    );


    console.log(
        "============================================"
    );


    const requiredElements = [

        "seasonSelect",

        "raceSelect",

        "raceInfo",

        "eventName",

        "countryName",

        "locationName",

        "totalLaps",

        "raceResults",

        "raceResultsBody",

        "loading",

        "error"

    ];


    let passed =
        0;


    requiredElements.forEach(
        id => {

            const element =
                document.getElementById(
                    id
                );


            if (element) {

                console.log(
                    `✅ ${id}`
                );


                passed++;

            }

            else {

                console.error(
                    `❌ ${id} NOT FOUND`
                );

            }

        }
    );


    console.log(
        `DOM verification: ${passed}/${requiredElements.length}`
    );


    return (
        passed ===
        requiredElements.length
    );

}


window.verifyHistoricalDOM =
    verifyHistoricalDOM;


/*==========================================================
  COMPLETE UPDATED HISTORICAL.JS INITIALIZED
==========================================================*/

console.log(
    "historical.js loaded — Official Race Results integration enabled."
);