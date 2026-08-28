/*==========================================================
  API.JS
  F1 AI STRATEGIST — FRONTEND API CLIENT
==========================================================*/

"use strict";


/*==========================================================
  BACKEND CONFIGURATION
==========================================================*/

const API = {
    BASE_URL: "/api"
};


/*==========================================================
  API ENDPOINTS
==========================================================*/

const ENDPOINTS = {
    HEALTH: "/health",
    RACES: "/races",
    RACE: "/race",
    SESSION: "/session"
};


/*==========================================================
  BUILD URL
==========================================================*/

function buildURL(endpoint) {

    return API.BASE_URL + endpoint;

}


/*==========================================================
  GENERIC GET REQUEST
==========================================================*/

async function apiGET(endpoint) {

    try {

        const response = await fetch(

            buildURL(endpoint)

        );


        if (!response.ok) {

            throw new Error(

                `Server Error: ${response.status}`

            );

        }


        return await response.json();

    }


    catch (error) {

        console.error(

            "API GET Error:",

            error

        );

        return null;

    }

}


/*==========================================================
  GENERIC POST REQUEST
==========================================================*/

async function apiPOST(endpoint, data) {

    try {

        const response = await fetch(

            buildURL(endpoint),

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify(data)

            }

        );


        if (!response.ok) {

            throw new Error(

                `Server Error: ${response.status}`

            );

        }


        return await response.json();

    }


    catch (error) {

        console.error(

            "API POST Error:",

            error

        );

        return null;

    }

}


/*==========================================================
  CHECK BACKEND STATUS
==========================================================*/

async function checkBackend() {

    const data = await apiGET(

        ENDPOINTS.HEALTH

    );

    return data !== null;

}


/*==========================================================
  GET AVAILABLE RACES
==========================================================*/

async function getRaces(season) {

    return await apiGET(

        `${ENDPOINTS.RACES}/${season}`

    );

}


/*==========================================================
  GET RACE INFORMATION
==========================================================*/

async function getRace(

    season,

    grandPrix

) {

    const formattedGrandPrix =

        grandPrix.replace(

            / /g,

            "_"

        );


    return await apiGET(

        `${ENDPOINTS.RACE}/` +

        `${season}/` +

        `${formattedGrandPrix}`

    );

}


/*==========================================================
  GET SESSION DATA
==========================================================*/

async function getSessionData(

    season,

    grandPrix,

    sessionType = "R"

) {

    const formattedGrandPrix =

        grandPrix.replace(

            / /g,

            "_"

        );


    return await apiGET(

        `${ENDPOINTS.SESSION}/` +

        `${season}/` +

        `${formattedGrandPrix}/` +

        `${sessionType}`

    );

}

/*==========================================================
  TEST — LOAD RACES FOR A SEASON
==========================================================*/

async function testRaceAPI() {

    const races = await getRaces(2025);

    console.log(

        "2025 F1 Races:",

        races

    );

    return races;

}