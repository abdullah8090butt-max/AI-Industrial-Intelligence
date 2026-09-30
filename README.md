# AI Industrial Intelligence & Predictive Maintenance System

An AI-powered industrial monitoring and predictive maintenance system built with **Python, Machine Learning, FastAPI, React, and TypeScript**.

The system analyzes machine sensor data to detect anomalies, estimate failure risk, forecast temperature trends, provide built-in feature-importance explanations, generate maintenance recommendations, simulate changing machine conditions, and provide a grounded **AI Industrial Copilot** for natural-language machine analysis.

**Project status:** Portfolio-ready and GitHub-published.

---

## Key Capabilities

* Predictive maintenance and machine failure-risk estimation
* Sensor anomaly detection using Isolation Forest
* Temperature time-series forecasting
* Built-in feature-importance XAI
* Automated maintenance recommendations
* Normal/Warning/Critical machine simulation
* FastAPI REST backend
* React + TypeScript dashboard
* Grounded AI Industrial Copilot
* Validated ML models, APIs, simulator transitions, and frontend build

---

## Architecture

```text
React + TypeScript Frontend
          │
          │ REST API
          ▼
FastAPI Backend
          │
          ├── Machine Status
          ├── Failure Risk
          ├── Anomaly Detection
          ├── Recommendations
          ├── Forecasting
          ├── XAI
          └── Industrial Copilot
          │
          ▼
Python ML Services
          │
          ├── Predictive Maintenance
          ├── Isolation Forest
          ├── Time-Series Forecasting
          ├── Feature Importance
          ├── Recommendation Engine
          └── Machine Simulator
```

---

## Main Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn
* Pandas
* NumPy
* Scikit-learn
* Joblib

### Frontend

* React
* TypeScript
* Vite
* Recharts

### Machine Learning

* Random Forest
* Isolation Forest
* Random Forest time-series forecasting
* StandardScaler
* One-hot encoding
* Built-in Random Forest feature importance

---

# Main AI Components

## 1. Predictive Maintenance

A Random Forest classifier estimates machine failure risk from processed sensor and machine-type features.

Input features include:

* Air temperature
* Process temperature
* Rotational speed
* Torque
* Tool wear
* Machine type

The final operating threshold is **0.40**.

Verified unseen test results:

* Failure precision: 0.56
* Failure recall: 0.69
* F1-score: 0.61
* Accuracy: 0.97
* ROC-AUC: 0.9575
* PR-AUC: 0.7300

---

## 2. Anomaly Detection

The system uses **Isolation Forest** to identify unusual machine operating conditions.

Configuration:

```text
n_estimators = 100
contamination = 0.05
random_state = 42
```

The anomaly model was trained using normal operating records and validated on unseen data.

Verified validation:

* Test records: 1,500
* Detected anomalies: 68
* Contamination setting: 5%

Higher anomaly scores represent more unusual observations.

---

## 3. Temperature Forecasting

A Random Forest regression model forecasts the next temperature value using recent temperature history and temporal features.

Features include:

* Lag 1
* Lag 2
* Lag 3
* Lag 6
* Lag 12
* Hour
* Day of week

Verified test results:

* MAE: **3.8896**
* RMSE: **4.8093**

Compared with the persistence baseline:

* MAE improvement: **30.50%**
* RMSE improvement: **29.70%**

The API requires at least **12 historical readings**.

---

## 4. Explainable AI

The project uses **built-in Random Forest feature importance** as its explainability method.

This is documented as feature-importance XAI rather than SHAP-based explainability.

Verified feature importance:

| Feature             | Importance |
| ------------------- | ---------: |
| Torque              |     30.52% |
| Rotational speed    |     29.75% |
| Tool wear           |     20.40% |
| Air temperature     |     10.12% |
| Process temperature |      7.20% |
| Type 0              |      0.94% |
| Type 1              |      0.67% |
| Type 2              |      0.40% |

The top three features account for approximately **84.67%** of total feature importance.

Feature importance describes the model's learned contribution to predictions and should not be interpreted as proof of causation.

---

## 5. Recommendation Engine

The recommendation engine combines:

* Failure-risk level
* Sensor conditions
* Anomaly information
* Maintenance rules

Example recommendations can include:

* Inspect machine condition
* Check torque and rotational speed
* Inspect tool wear
* Monitor temperature conditions
* Continue routine preventive maintenance

Risk levels are represented as:

```text
Normal
Warning
Critical
```

The recommendation system was validated with normal, warning, and critical operating conditions.

---

## 6. Real-Time Machine Simulator

The simulator generates sensor readings for three operating scenarios:

```text
Normal
Warning
Critical
```

The simulator adds controlled sensor variation while keeping readings within defined physical ranges.

Verified transition test:

```text
Normal → Warning → Critical → Normal
```

Result:

```text
Sequence valid: True
All transition results valid: True
```

The simulator also produces machine risk, anomaly, and recommendation information.

---

## 7. AI Industrial Copilot

The AI Industrial Copilot provides natural-language access to verified backend functions.

Supported tools:

```text
get_machine_status()
get_failure_risk()
get_recent_anomalies()
get_machine_history()
get_forecast()
get_explanation()
get_recommendations()
```

Example questions:

```text
What is the current machine status?
What is the failure risk?
Are there any anomalies?
Explain the prediction.
What is the temperature forecast?
What maintenance is recommended?
Show the machine history.
```

The Copilot uses deterministic query routing to select the appropriate backend tool. It is designed as a **grounded industrial assistant**, rather than an autonomous system that invents machine information.

---

# API Documentation

Base URL during local development:

```text
http://127.0.0.1:8000
```

## Machine APIs

| Method | Endpoint                   | Purpose                                                  |
| ------ | -------------------------- | -------------------------------------------------------- |
| POST   | `/machine/status`          | Get machine status and combined risk/anomaly information |
| POST   | `/machine/failure-risk`    | Calculate failure risk                                   |
| POST   | `/machine/anomaly`         | Detect anomaly status                                    |
| POST   | `/machine/recommendations` | Generate maintenance recommendations                     |
| POST   | `/machine/forecast`        | Forecast temperature                                     |
| POST   | `/machine/explanation`     | Return feature-importance explanation                    |

## Copilot APIs

| Method | Endpoint                  | Purpose                                  |
| ------ | ------------------------- | ---------------------------------------- |
| POST   | `/machine/copilot/status` | Get Copilot machine status               |
| POST   | `/machine/copilot/query`  | Process a natural-language Copilot query |

## System APIs

| Method | Endpoint             | Purpose             |
| ------ | -------------------- | ------------------- |
| GET    | `/`                  | Backend root/status |
| GET    | `/health`            | Health check        |
| GET    | `/dashboard/summary` | Dashboard summary   |

FastAPI automatically provides interactive API documentation at:

```text
/docs
```

---

# Frontend

The frontend is built using React, TypeScript, Vite, and Recharts.

## Pages

### Dashboard

Provides an overall system overview including machine KPIs and system status.

### Machine Monitoring

Displays machine sensor information and current machine analysis.

### Anomalies

Displays anomaly-related machine information.

### Predictive Maintenance

Displays failure risk and maintenance information.

### Forecasting

Displays temperature forecasting information.

### AI Industrial Copilot

Provides natural-language access to the backend industrial intelligence tools.

## Frontend Routes

```text
/
 /machines
 /anomalies
 /maintenance
 /forecasting
 /copilot
```

The production frontend build was successfully verified using:

```text
npm run build
```

Result:

```text
TypeScript compilation: SUCCESS
Vite production build: SUCCESS
598 modules transformed
Build completed successfully
```

Vite reported a JavaScript chunk-size warning above 500 KB. This is an optimization warning and does not prevent the production build from succeeding.

---

# Dataset Overview

## AI4I 2020 Predictive Maintenance Dataset

The primary predictive-maintenance dataset contains:

* 10,000 records
* Machine sensor measurements
* Machine failure labels
* Failure-type indicators

Main sensor features:

```text
Air temperature
Process temperature
Rotational speed
Torque
Tool wear
```

The dataset contains **339 machine-failure records** and **9,661 normal records**.

## Temperature Telemetry Dataset

A secondary telemetry dataset is used for time-series forecasting.

The project selects temperature readings and prepares them chronologically for model training and testing.

---

# ML Methodology

## Data Preprocessing

The preprocessing pipeline:

1. Removes identifier fields that are not useful for prediction.
2. Converts machine type into numerical/categorical features.
3. Standardizes numerical features.
4. One-hot encodes machine type.
5. Performs a stratified train/validation/test split.
6. Preserves the failure class distribution across splits.

Final predictive-maintenance split:

```text
Training:   7,000
Validation: 1,500
Testing:    1,500
```

---

## Predictive Maintenance Pipeline

```text
Raw Sensor Data
      ↓
Preprocessing
      ↓
Feature Engineering
      ↓
Random Forest
      ↓
Failure Probability
      ↓
Threshold 0.40
      ↓
Risk Level
```

---

## Anomaly Detection Pipeline

```text
Normal Training Records
          ↓
Isolation Forest
          ↓
Anomaly Score
          ↓
Anomaly Detection
```

---

## Forecasting Pipeline

```text
Historical Temperature
          ↓
Lag Features
          ↓
Temporal Features
          ↓
Random Forest Regression
          ↓
Next Temperature Forecast
```

---

# Project Structure

```text
AI-Industrial-Intelligence/
│
├── backend/
│   ├── api/
│   ├── app/
│   ├── schemas/
│   ├── services/
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── App.tsx
│
├── ml/
│   ├── anomaly_detection/
│   ├── explainability/
│   ├── forecasting/
│   ├── predictive_maintenance/
│   ├── preprocessing/
│   ├── recommendations/
│   └── simulator/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
├── schemas/
├── docs/
├── tests/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Installation

## Backend

From the project root:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

---

## Frontend

Move into the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

---

# Running the Application

## Start the FastAPI Backend

From the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start the React Frontend

From the frontend directory:

```powershell
npm run dev
```

Frontend:

```text
http://localhost:5173/
```

---

# Testing

The system was tested across multiple layers.

## ML Validation

* Predictive maintenance model validation
* Anomaly detection validation
* Forecasting validation
* Saved-model reload verification

## Edge Cases

The API correctly rejects:

* Negative tool-wear values
* Out-of-range sensor values
* Insufficient forecasting history
* Empty Copilot queries

Invalid requests return appropriate **HTTP 422** validation responses.

## Simulator

Verified:

```text
Normal → Warning → Critical → Normal
```

## API Regression

Verified successful responses from:

```text
/machine/status
/machine/failure-risk
/machine/anomaly
/machine/recommendations
/machine/forecast
/machine/copilot/query
```

## Frontend

Verified that the main application routes load successfully:

```text
Dashboard
Machines
Anomalies
Maintenance
Forecasting
Copilot
```

Production build:

```text
npm run build
```

Result:

```text
SUCCESS
```

---

# Model Limitations

The system is a portfolio and educational industrial-intelligence project and has important limitations.

* The predictive-maintenance model is trained on the AI4I 2020 dataset.
* The forecasting model uses a separate telemetry dataset.
* The simulator generates controlled synthetic variations.
* Feature importance indicates model behavior, not causality.
* Anomaly detection does not guarantee that an anomaly represents a mechanical failure.
* Forecasting performance may differ on real industrial equipment.
* The current dashboard uses a lightweight machine representation rather than a live industrial deployment.
* Real industrial deployment would require domain-specific validation, monitoring, safety procedures, and production-grade infrastructure.

---

# Project Status

## Completed

* Project architecture
* Dataset understanding
* Data preprocessing
* Feature engineering
* Predictive maintenance
* Anomaly detection
* Temperature forecasting
* Explainable AI
* Recommendation engine
* Machine simulator
* FastAPI backend
* React + TypeScript frontend
* AI Industrial Copilot
* API validation
* Frontend integration testing
* End-to-end regression testing
* Git initialization
* GitHub repository publication
* Production frontend build verification

The project has been validated locally and published to GitHub.

---

# Future Improvements

Potential future improvements include:

* More industrial datasets
* Additional sensor forecasting
* More advanced anomaly-detection approaches
* SHAP-based instance-level explanations
* Real-time streaming telemetry
* Persistent machine history
* Authentication and user roles
* Cloud deployment
* Automated report generation
* More advanced Copilot capabilities
* Model monitoring and retraining workflows

These are future extensions rather than requirements for the current portfolio version.

---

# Developer

**Abdullah Butt**

AI & Python Developer

Focus areas:

* Python
* Machine Learning
* Computer Vision
* Generative AI
* AI Automation
* FastAPI
* React + TypeScript
* Industrial AI

---

# License

This project is provided for educational, portfolio, and demonstration purposes.
