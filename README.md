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
