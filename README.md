# 🏎️ F1 AI Strategy Engine (V4)

An end-to-end **AI-powered Formula 1 race strategy system** that predicts pit stop probability and simulates optimal race decisions using machine learning, physics-based modeling, and real telemetry-inspired features.

---

## 🔥 Overview

The F1 AI Strategy Engine simulates real-world race strategy decisions used in Formula 1 teams.

It combines:
- Machine Learning (XGBoost)
- Race simulation physics
- Feature engineering from telemetry-style data
- Interactive Streamlit dashboard

The system answers:

> ❓ Should the driver pit now or stay out?

---

## 🎯 Key Features

### 🧠 Machine Learning Layer
- Pit stop probability prediction
- XGBoost classification model
- SMOTE handling for class imbalance
- Feature-rich race state representation

### 🏁 Strategy Simulation Engine
- Pit vs Stay time simulation
- Tyre degradation modeling
- Track + driver-specific logic
- Race progression awareness

### 📊 Feature Engineering
- Lap-wise performance trends
- Tire life modeling
- Degradation rate estimation
- Stint length tracking
- Pit stop history encoding

### 📈 Visualization Dashboard
Built using **Streamlit + Plotly**

- Interactive sliders (lap, tyre, driver, track)
- Real-time strategy decision output
- Bar chart: Pit vs Stay comparison
- Pie chart: strategy advantage breakdown
- Confidence-based decision UI

---

## 🧱 Project Architecture

User Input (Streamlit UI)
↓
Feature Engineering Layer
↓
ML Model (Pit Probability)
↓
Strategy Simulation Engine
↓
Decision Logic (Pit / Stay)
↓
Visualization Dashboard


---

## 🗂️ Project Structure


f1-ai-strategy-engine/
│
├── app.py # Streamlit dashboard entry point
├── main.py # Data pipeline runner
├── requirements.txt
│
├── src/
│ ├── predict.py # ML inference pipeline
│ ├── preprocessing.py # Data cleaning + transformations
│ ├── feature_engineering.py # Feature creation logic
│ ├── data_loader.py # FastF1 race data ingestion
│ │
│ └── strategy/
│ ├── decision_engine.py # Final race decision logic
│ ├── simulator.py # Pit vs stay simulation
│ ├── tyre_model.py # Tire degradation model
│ ├── driver_model.py # Driver performance modeling
│ └── track_model.py # Circuit-specific behavior
│
├── models/
│ ├── pit_strategy_model.pkl
│ └── degradation_model.pkl
│
├── data/
│ ├── processed/
│ └── strategy_params.py
│
└── notebooks/


---

## ⚙️ Tech Stack

- **Python 3.10+**
- Pandas, NumPy
- Scikit-learn
- XGBoost
- imbalanced-learn (SMOTE)
- FastF1 (telemetry data)
- Streamlit (UI)
- Plotly (visualization)

---

## 🚀 How to Run Locally

### 1. Clone repository
```bash
git clone https://github.com/<your-username>/f1-ai-strategy-engine.git
cd f1-ai-strategy-engine
2. Install dependencies
pip install -r requirements.txt
3. Run dashboard
streamlit run app.py
📊 Example Output
Strategy Decision
🟢 Decision: PIT NOW
📊 Confidence: HIGH
⏱ Pit Advantage: +1.41 sec
Visualization
Pit vs Stay time comparison chart
Strategy advantage pie breakdown
🧠 Core Idea

Instead of static race rules, this system learns from:

historical lap data
tire degradation patterns
driver performance trends
race progression dynamics

and generates adaptive race strategy decisions.

📌 Future Improvements
🔴 Real-time telemetry streaming
🌦️ Weather impact modeling
🟣 Multi-stop optimization engine
🧮 Reinforcement learning strategy agent
📡 Live race simulation mode
🏁 Project Impact

This project demonstrates:

End-to-end ML pipeline design
Real-world sports analytics application
Simulation + prediction hybrid system
Production-style project architecture
Interactive data product development
