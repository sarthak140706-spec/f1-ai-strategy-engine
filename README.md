# 🏎️ F1 AI Strategy Engine

An AI-powered **Formula 1 race strategy and historical analysis platform** designed to act like a virtual race engineer.

The system combines **historical Formula 1 data, race-state analysis, strategy simulation, pit-window optimization, explainable AI, and What-If scenario comparison** to generate intelligent race strategy recommendations.

---

## 🚀 Live Website

👉 **F1 AI Strategy Engine:**  
https://f1-ai-strategy-engine.onrender.com/

### Main Modules

- 🏠 Home Dashboard
- 📊 Historical Race Analysis
- 🧠 AI Strategy Engineer
- 🔄 What-If Scenario Analysis

---

## 🔥 Overview

Formula 1 strategy depends on many interacting factors such as:

- Current race position
- Lap number
- Tyre compound
- Tyre age
- Tyre degradation
- Recent race pace
- Gaps to surrounding drivers
- Pit-stop history
- Weather conditions
- Safety Car / Virtual Safety Car
- Remaining race distance

The **F1 AI Strategy Engine** combines these factors into a structured race state and evaluates possible strategic decisions.

The central question the system attempts to answer is:

> **“Given the current race situation, what should the driver do next?”**

Instead of producing only a simple PIT or STAY decision, the platform provides a complete strategy analysis including alternative strategies, pit-window recommendations, confidence, risk, explanations, and scenario sensitivity.

---

# 🧠 Core Features

## 1. AI Strategy Engineer

The Strategy Engineer is the central decision-making system.

Users can manually construct a race situation by providing information such as:

- Driver
- Team
- Grand Prix
- Circuit
- Current lap
- Total race laps
- Position
- Number of pit stops
- Current tyre compound
- Tyre age
- Recent pace
- Average pace
- Degradation rate
- Gap ahead
- Gap behind
- Weather
- Rainfall
- Track status
- Safety Car
- Virtual Safety Car

The engine processes this race state and generates an AI-assisted strategy recommendation.

### Strategy Output

The system can provide:

- Final strategy recommendation
- Recommended tyre
- Strategy confidence
- Strategic risk level
- Race situation classification
- Pit decision
- Pit urgency
- Recommended pit lap
- Optimal pit window
- Alternative strategies
- Strategic factors
- Race-engineer explanation
- Strategy warnings

---

## 2. Race-State Builder

The Race-State Builder converts user inputs into a standardized representation of the current race situation.

It validates important constraints such as:

- Current lap cannot exceed total laps
- Driver position must be valid
- Tyre age cannot be negative
- Tyre compound must be supported
- Safety Car and Virtual Safety Car states cannot conflict

This provides a consistent input contract for the strategy pipeline.

---

## 3. Strategy Alternatives Engine

Instead of evaluating only one decision, the system generates and compares multiple possible race strategies.

Strategies can be evaluated using factors such as:

- Expected race performance
- Pit-stop cost
- Tyre degradation
- Race position
- Remaining race distance
- Strategic risk
- Current race conditions

The alternatives are ranked so the user can compare the primary recommendation against other possible decisions.

---

## 4. Pit Window Optimizer

The Pit Window Optimizer determines when a pit stop would be strategically most effective.

It provides information including:

- Pit decision
- Pit urgency score
- Recommended pit lap
- Optimal pit window
- Pit-window confidence

This allows the system to answer not only:

> **“Should we pit?”**

but also:

> **“When should we pit?”**

---

## 5. Explanation & Confidence Engine

The system includes an explainability layer so that recommendations are not presented as unexplained outputs.

The Strategy Engineer can provide:

- Confidence score
- Risk classification
- Race situation
- Strategic reasoning
- Important decision factors
- Strategy warnings

This makes the system closer to a virtual race engineer rather than a basic prediction model.

---

## 6. What-If Scenario Analysis

The platform can test how stable a strategy recommendation remains when race conditions change.

Default What-If scenarios evaluate situations such as changes in:

- Tyre age
- Pace
- Degradation
- Gaps
- Race conditions

The comparison engine reports:

- Number of scenarios tested
- Decision stability
- Stability classification
- Most sensitive scenario
- Maximum sensitivity

This helps determine whether a recommendation is robust or highly dependent on the current race conditions.

---

# 📊 Historical Race Analysis

The Historical Analysis module allows users to explore Formula 1 race data from previous seasons.

Users can select:

- Season
- Grand Prix

The backend retrieves race information using **FastF1** and exposes it through the project's Flask API.

### Historical Analysis Includes

- Grand Prix information
- Circuit/location information
- Race date
- Total race laps
- Official race classification
- Driver positions
- Driver numbers
- Teams
- Laps completed
- Championship points earned

This module provides historical context alongside the AI Strategy Engineer.

---

# 🏁 Official Race Results

Historical race results are dynamically retrieved and displayed through the backend.

For each driver, the system can show:

- Finishing position
- Driver name
- Driver abbreviation
- Driver number
- Constructor/team
- Laps completed
- Points scored

The application uses optimized FastF1 session loading to make historical analysis suitable for web deployment.

---

# 🔌 REST API

The project includes a Flask-based REST API connecting the frontend with the strategy and historical-analysis engines.

### Strategy Engineer API

```text
/api/engineer/
/api/engineer/health
/api/engineer/race-state
/api/engineer/analyse
