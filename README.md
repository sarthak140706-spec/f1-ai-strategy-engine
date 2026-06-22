# 🏎️ F1 AI Strategy Engine (V4)

An AI-powered Formula 1 race strategy system that predicts pit stop probability and simulates optimal race decisions using machine learning, telemetry-inspired features, and physics-based race modeling.

---

## 🚀 Live Demo

👉 **Streamlit App (Deployed):**  
https://f1-ai-strategy-engine-cj4xvwjwnqk4prdg5hy6hf.streamlit.app/

---

## 🔥 Overview

This project simulates real-world Formula 1 race strategy decisions by combining:

- Machine Learning (XGBoost)
- Race simulation physics
- Tire degradation modeling
- Driver and track-based performance behavior
- Feature engineering from lap-level race data

It helps answer:

> 🧠 “Should the driver pit now or stay out?”

---

## 🧠 Key Features

### 🏁 AI Strategy Engine
- Pit stop probability prediction
- PIT vs STAY decision system
- Confidence scoring

### 📊 Simulation System
- Tire degradation modeling
- Lap time progression simulation
- Pit loss vs time gain comparison

### 📈 Visualization Dashboard
- Interactive Streamlit UI
- Strategy comparison charts
- Pit vs Stay performance graphs
- Decision analytics

---

## 🧱 Tech Stack

- Python
- Pandas, NumPy
- XGBoost
- Scikit-learn
- FastF1 (race data source)
- Streamlit (dashboard)
- Plotly (visualization)

---

## 🗂️ Project Structure


src/
├── predict.py
├── preprocessing.py
├── feature_engineering.py
├── data_loader.py
├── strategy/
│ ├── decision_engine.py
│ ├── simulator.py
│ ├── driver_model.py
│ ├── tyre_model.py
│ └── track_model.py


---

## 📌 Version Roadmap

### 🔵 V4 — Current Version (Data-Driven Strategy Engine)
- ML-based pit stop prediction
- Physics-based race simulation
- Driver + tyre + track modeling
- Interactive Streamlit dashboard

---

### 🟡 V5 — Upcoming Improvements
Planned upgrades include:

- 🧠 Real-time telemetry simulation
- 🌦️ Weather impact modeling (rain / temperature effects)
- 🔄 Multi-stop strategy optimization (2-stop / 3-stop logic)
- 🤖 Reinforcement learning-based strategy agent
- 📡 Live race simulation mode
- ⚡ Performance optimization for real-time response

---

## 🎯 Project Goal

To build a **realistic AI race engineer system** capable of simulating and improving Formula 1 strategy decisions using data-driven intelligence.

---

## 👨‍💻 Author

Built as a Data Science + AI engineering project focused on:

- Sports analytics
- Machine learning systems
- Simulation-based decision making
- Real-world race strategy modeling

---

## ⭐ Future Vision

This project will evolve into a full **AI Race Strategy Simulator**, capable of:

- Acting like a virtual F1 race engineer
- Supporting multiple drivers simultaneously
- Running full race simulations in real time
