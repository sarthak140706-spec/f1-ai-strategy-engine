"""
F1 AI STRATEGIST
FLASK APPLICATION

Purpose
-------
Main Flask application for the F1 AI Strategist.

Current architecture:

    Frontend
        ↓
    Flask Application
        ↓
    Historical Race API
        +
    Phase 7 AI Strategy Engineer API

Phase 7 Pipeline
----------------

    7.1 Manual Race-State Builder
        ↓
    7.2 AI Strategy Engineer
        ↓
    7.3 Strategy Alternatives Engine
        ↓
    7.4 Pit Window Optimizer
        ↓
    7.5 Explanation & Confidence Engine
        ↓
    7.6 Strategy Engineer REST API

IMPORTANT
---------
The previous real-live timing feature is no longer part of
the active application architecture.

Historical analysis remains available.

The AI Strategy Engineer replaces the live strategy feature.
"""


from __future__ import annotations


import os

from flask import (
    Flask,
    send_from_directory,
    jsonify,
)

from flask_cors import CORS


# ============================================================
# PROJECT API IMPORTS
# ============================================================

from api.routes import api


# ============================================================
# PHASE 7.6 — STRATEGY ENGINEER API
# ============================================================

from api.strategy_engineer_routes import (
    strategy_engineer_api
)


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)


CSS_DIR = os.path.join(
    FRONTEND_DIR,
    "css"
)


JS_DIR = os.path.join(
    FRONTEND_DIR,
    "js"
)


ASSETS_DIR = os.path.join(
    FRONTEND_DIR,
    "assets"
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app.config.update({

    "JSON_SORT_KEYS":
        False,

    "JSONIFY_PRETTYPRINT_REGULAR":
        True,

})


# ============================================================
# CORS
# ============================================================

CORS(
    app
)


# ============================================================
# HISTORICAL / EXISTING API BLUEPRINT
# ============================================================

app.register_blueprint(
    api,
    url_prefix="/api"
)


print(
    "[API] Historical F1 API registered."
)


# ============================================================
# PHASE 7.6 — AI STRATEGY ENGINEER API
# ============================================================

app.register_blueprint(
    strategy_engineer_api,
    url_prefix="/api/engineer"
)


print(
    "[ENGINEER] Phase 7.6 Strategy Engineer API registered."
)


# ============================================================
# FRONTEND HOME
# ============================================================

@app.route("/")
def home():
    """
    Serve the main F1 AI Strategist landing page.
    """

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ============================================================
# HISTORICAL PAGE
# ============================================================

@app.route("/historical.html")
def historical_page():
    """
    Serve the historical race-analysis page.
    """

    return send_from_directory(
        FRONTEND_DIR,
        "historical.html"
    )


# ============================================================
# STRATEGY ENGINEER PAGE
# ============================================================

@app.route("/engineer.html")
def strategy_engineer_page():
    """
    Serve the Phase 7 AI Strategy Engineer page.

    The frontend file will be created during Phase 7.7.
    """

    engineer_file = os.path.join(
        FRONTEND_DIR,
        "engineer.html"
    )


    if not os.path.exists(
        engineer_file
    ):

        return jsonify({

            "application":
                "F1 AI Strategist",

            "component":
                "AI Strategy Engineer",

            "phase":
                "7.6",

            "status":
                "BACKEND_READY",

            "message":
                (
                    "Phase 7.6 Strategy Engineer backend is "
                    "available. The engineer frontend will be "
                    "added in Phase 7.7."
                )

        }), 200


    return send_from_directory(
        FRONTEND_DIR,
        "engineer.html"
    )


# ============================================================
# DOCUMENTATION PAGE
# ============================================================

@app.route("/documentation.html")
def documentation_page():
    """
    Serve project documentation.
    """

    return send_from_directory(
        FRONTEND_DIR,
        "documentation.html"
    )


# ============================================================
# FRONTEND CSS
# ============================================================

@app.route("/css/<path:filename>")
def css_files(
    filename
):
    """
    Serve frontend CSS files.
    """

    return send_from_directory(
        CSS_DIR,
        filename
    )


# ============================================================
# FRONTEND JAVASCRIPT
# ============================================================

@app.route("/js/<path:filename>")
def js_files(
    filename
):
    """
    Serve frontend JavaScript files.
    """

    return send_from_directory(
        JS_DIR,
        filename
    )


# ============================================================
# FRONTEND ASSETS
# ============================================================

@app.route("/assets/<path:filename>")
def asset_files(
    filename
):
    """
    Serve frontend assets.
    """

    return send_from_directory(
        ASSETS_DIR,
        filename
    )


# ============================================================
# APPLICATION HEALTH
# ============================================================

@app.route("/health")
def application_health():
    """
    Return overall application health information.
    """

    return jsonify({

        "application":
            "F1 AI Strategist",

        "status":
            "OPERATIONAL",

        "historical_api":
            True,

        "strategy_engineer":
            True,

        "strategy_engineer_phase":
            "7.6",

        "live_timing":
            False,

        "architecture": {

            "historical_analysis":
                "ACTIVE",

            "ai_strategy_engineer":
                "ACTIVE",

            "live_strategy":
                "REMOVED",

        }

    }), 200


# ============================================================
# API INFORMATION
# ============================================================

@app.route("/api")
def api_information():
    """
    Display the active application APIs.
    """

    return jsonify({

        "application":
            "F1 AI Strategist",

        "status":
            "OPERATIONAL",

        "apis": {

            "historical": {

                "status":
                    "ACTIVE",

                "base":
                    "/api",

            },

            "strategy_engineer": {

                "status":
                    "ACTIVE",

                "phase":
                    "7.6",

                "base":
                    "/api/engineer",

                "health":
                    "/api/engineer/health",

                "race_state":
                    "/api/engineer/race-state",

                "analyse":
                    "/api/engineer/analyse",

            }

        },

        "features": {

            "historical_race_analysis":
                True,

            "manual_race_state":
                True,

            "ai_strategy_engineer":
                True,

            "strategy_alternatives":
                True,

            "pit_window_optimizer":
                True,

            "explanation_engine":
                True,

            "confidence_engine":
                True,

            "live_timing":
                False,

        }

    }), 200


# ============================================================
# 404 HANDLER
# ============================================================

@app.errorhandler(404)
def not_found(
    error
):
    """
    Application-wide 404 response.

    API requests receive JSON while normal frontend requests
    continue to receive a simple JSON error response.
    """

    return jsonify({

        "application":
            "F1 AI Strategist",

        "status":
            "ERROR",

        "error":
            "NOT_FOUND",

        "message":
            "The requested resource was not found.",

        "path":
            getattr(
                request_safe_path(),
                "path",
                None
            )

    }), 404


# ============================================================
# SAFE REQUEST PATH
# ============================================================

def request_safe_path():
    """
    Safely obtain the active Flask request.

    This helper prevents application-startup errors when the
    request context is unavailable.
    """

    try:

        from flask import request

        return request

    except RuntimeError:

        return None


# ============================================================
# 500 HANDLER
# ============================================================

@app.errorhandler(500)
def internal_server_error(
    error
):
    """
    Application-wide internal error response.
    """

    return jsonify({

        "application":
            "F1 AI Strategist",

        "status":
            "ERROR",

        "error":
            "INTERNAL_SERVER_ERROR",

        "message":
            "An unexpected application error occurred."

    }), 500


# ============================================================
# STARTUP INFORMATION
# ============================================================

def display_startup_information():
    """
    Display the currently active project architecture.
    """

    print(
        "\n" + "=" * 76
    )

    print(
        "F1 AI STRATEGIST"
    )

    print(
        "=" * 76
    )

    print(
        "Historical Analysis:        ACTIVE"
    )

    print(
        "AI Strategy Engineer:       ACTIVE"
    )

    print(
        "Strategy Engineer Phase:    7.6"
    )

    print(
        "Live Timing:                DISABLED"
    )

    print(
        "-" * 76
    )

    print(
        "Frontend:"
    )

    print(
        "  Home:                     /"
    )

    print(
        "  Historical Analysis:      /historical.html"
    )

    print(
        "  Strategy Engineer:        /engineer.html"
    )

    print(
        "  Documentation:            /documentation.html"
    )

    print(
        "-"
        * 76
    )

    print(
        "Strategy Engineer API:"
    )

    print(
        "  Root:                     /api/engineer/"
    )

    print(
        "  Health:                   /api/engineer/health"
    )

    print(
        "  Race State:               /api/engineer/race-state"
    )

    print(
        "  Analyse Strategy:         /api/engineer/analyse"
    )

    print(
        "=" * 76
    )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    display_startup_information()

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True,

        # Prevent Flask's development reloader from creating
        # duplicate application instances while Phase 7 is
        # being tested.
        use_reloader=False

    )