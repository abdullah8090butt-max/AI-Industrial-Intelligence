# AI Industrial Intelligence & Predictive Maintenance System

A full-stack AI/ML application for industrial machine monitoring, anomaly detection, predictive maintenance, sensor forecasting, explainable AI, maintenance recommendations, simulation, and a grounded AI Industrial Copilot.

## Overview

The **AI Industrial Intelligence & Predictive Maintenance System** combines machine-learning models with a FastAPI backend and React + TypeScript frontend to provide an integrated industrial intelligence platform.

The system can:

* Monitor machine sensor conditions
* Detect abnormal machine behavior
* Estimate machine failure risk
* Predict future temperature readings
* Explain model-level feature importance
* Generate maintenance recommendations
* Simulate different machine operating conditions
* Provide a grounded AI Industrial Copilot
* Expose AI capabilities through REST APIs
* Display results through a web dashboard

The project is designed as a practical portfolio project for AI and Python development.

---

# Architecture

```text id="d8x4te"
                         USER
                           │
                           ▼
                React + TypeScript Frontend
                           │
                           │ REST API
                           ▼
                    FastAPI Backend
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Predictive     Anomaly       Forecasting
        Maintenance    Detection      Service
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                  Explainable AI
                           │
                           ▼
              Recommendation Engine
                           │
                           ▼
                  Machine Simulator
                           │
                           ▼
                 AI Industrial Copilot
```

## Main Layers

### Frontend

* React
* TypeScript
* Vite
* Recharts
* REST API integration

### Backend

* FastAPI
* Pydantic
* Uvicorn
* CORS

### AI/ML

* Scikit-learn
* Random Forest
* Isolation Forest
* StandardScaler
* Feature engineering
* Time-series lag features

### Data Processing & Visualization

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly

### Data

* UCI AI4I 2020 Predictive Maintenance Dataset
* IoT sensor telemetry dataset

---

# Main AI Components

## 1. Predictive Maintenance

A Random Forest classifier estimates machine failure risk from industrial sensor conditions.

Features include:

* Air temperature
* Process temperature
* Rotational speed
* Torque
* Tool wear
* Machine type

The final decision threshold is:

```text
0.40
```

### Unseen Test Results

| Metric            | Result |
| ----------------- | -----: |
| Accuracy          |   0.97 |
| Failure Precision |   0.56 |
| Failure Recall    |   0.69 |
| Failure F1        |   0.61 |
| ROC-AUC           | 0.9575 |
| PR-AUC            | 0.7300 |

The model is intended as a portfolio demonstration and has not been validated as a production industrial safety system.

---

## 2. Anomaly Detection

The system uses Isolation Forest to identify unusual machine conditions.

Final configuration:

```text
n_estimators = 100
contamination = 0.05
random_state = 42
```

The detector is integrated with the machine-status and recommendation services.

An anomaly indicates an unusual sensor pattern. It does not automatically mean that a machine has failed.

---

## 3. Temperature Forecasting

A Random Forest forecasting model predicts the next temperature reading using recent historical values.

### Lag Features

```text
lag_1
lag_2
lag_3
lag_6
lag_12
```

### Time Features

```text
hour
day_of_week
```

### Final Results

| Metric                       | Result |
| ---------------------------- | -----: |
| MAE                          | 3.8896 |
| RMSE                         | 4.8093 |
| MAE Improvement vs Baseline  | 30.50% |
| RMSE Improvement vs Baseline | 29.70% |

The API requires at least 12 historical temperature readings.

---

## 4. Explainable AI

The project uses **Random Forest's built-in feature importance** for model-level explanation.

### Feature Importance

| Feature             | Importance |
| ------------------- | ---------: |
| Torque              |     30.52% |
| Rotational speed    |     29.75% |
| Tool wear           |     20.40% |
| Air temperature     |     10.12% |
| Process temperature |      7.20% |

The implementation intentionally does not claim SHAP-based explanations.

Feature importance describes how the trained model uses features overall. It should not be interpreted as a causal explanation or as an exact contribution for an individual prediction.

---

## 5. Recommendation Engine

Maintenance recommendations combine:

* Failure-risk level
* Sensor conditions
* Anomaly detection

The system can recommend actions such as:

* Machine inspection
* Torque and rotational-speed checks
* Tool-wear inspection
* Temperature-condition checks
* Preventive maintenance
* Continued monitoring

Recommendations are rule-based and are intended to support, rather than replace, qualified maintenance decisions.

---

## 6. Machine Simulator

The simulator provides three operating scenarios:

```text
Normal
Warning
Critical
```

It generates bounded sensor readings and allows the complete AI pipeline to be tested without physical industrial hardware.

Transition testing verified:

```text
Normal → Warning → Critical → Normal
```

The scenario names represent simulated operating conditions and do not necessarily correspond directly to the predictive-maintenance model's risk labels.

---

## 7. AI Industrial Copilot

The Copilot provides natural-language access to verified backend tools.

Supported capabilities include:

```text
get_machine_status
get_failure_risk
get_recent_anomalies
get_machine_history
get_forecast
get_explanation
get_recommendations
```

### Example Questions

```text
What is the current machine status?
What is the failure risk?
Are there any recent anomalies?
What is the temperature forecast?
Explain the prediction.
What maintenance actions are recommended?
Show the recent machine history.
```

The Copilot uses deterministic backend routing and verified system data rather than unsupported industrial claims.

---

# ML Methodology

## Data Preprocessing

The predictive-maintenance dataset is processed through the following pipeline:

1. Remove identifier columns that are not useful for prediction.
2. Convert machine type into numerical/categorical features.
3. Separate numerical sensor features from categorical machine-type features.
4. Standardize numerical features using `StandardScaler`.
5. Split the data into training, validation, and unseen test sets using stratification.
6. Preserve the original failure distribution without synthetic oversampling.

### Main Predictive-Maintenance Features

* Air temperature
* Process temperature
* Rotational speed
* Torque
* Tool wear
* Machine type

---

## Predictive Maintenance Pipeline

```text
Raw Sensor Data
       │
       ▼
Data Preprocessing
       │
       ▼
Feature Transformation
       │
       ▼
Random Forest Model
       │
       ▼
Failure Probability
       │
       ▼
Decision Threshold = 0.40
       │
       ▼
Risk Level
Normal / Warning / Critical
```

The Random Forest model is evaluated on an unseen test set after model selection and threshold tuning on validation data.

---

## Anomaly Detection Pipeline

Isolation Forest is trained using normal operating records and then applied to unseen machine conditions.

```text
Sensor Data
    │
    ▼
Numerical Sensor Features
    │
    ▼
Isolation Forest
    │
    ▼
Anomaly Score
    │
    ▼
Normal / Anomalous
```

Final contamination setting:

```text
0.05
```

---

## Forecasting Pipeline

Temperature forecasting uses chronological time-series data.

Recent temperature observations are converted into lag features:

```text
lag_1
lag_2
lag_3
lag_6
lag_12
```

Time-based features:

```text
hour
day_of_week
```

The forecasting model uses a chronological train/test split to avoid using future observations during training.

```text
Historical Temperature Data
          │
          ▼
Chronological Split
          │
          ▼
Lag Feature Generation
          │
          ▼
Random Forest Forecasting Model
          │
          ▼
Next Temperature Prediction
```

---

## Explainability Methodology

The predictive-maintenance Random Forest exposes built-in feature importance.

This provides a model-level view of which input features are most influential to the trained model across the dataset.

The project does not claim:

* SHAP explanations
* Individual feature contributions
* Causal relationships

---

## Validation Strategy

The project uses separate validation and unseen test data where applicable.

Validation data is used for:

* Model comparison
* Threshold selection
* Pipeline verification

The unseen test set is used for final predictive-maintenance performance reporting.

Additional regression testing validates:

* Saved model loading
* Prediction outputs
* API responses
* Input validation
* Simulator transitions
* Copilot routing
* Frontend/backend integration

---

# API Documentation

The backend is implemented using FastAPI and exposes REST endpoints for machine intelligence and Copilot functionality.

Interactive Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## General Endpoints

### `GET /`

Returns the basic application status, project name, and environment.

### `GET /health`

Returns the backend health status.

### `GET /dashboard/summary`

Returns dashboard-level machine statistics and overall system status.

---

## Machine Intelligence Endpoints

### `POST /machine/status`

Returns a combined machine-status result containing:

* Machine status
* Failure risk
* Predicted failure
* Anomaly status
* Anomaly score
* Sensor data

### `POST /machine/failure-risk`

Runs the predictive-maintenance model and returns:

* Failure risk
* Predicted failure
* Risk level

### `POST /machine/anomaly`

Runs the Isolation Forest anomaly detector and returns:

* Anomaly status
* Anomaly score

### `POST /machine/recommendations`

Combines predictive-maintenance and anomaly results with rule-based maintenance recommendations.

Returns information about:

* Risk level
* Maintenance actions
* Sensor conditions
* Anomaly information

### `POST /machine/forecast`

Accepts recent temperature history and predicts the next temperature value.

The endpoint requires at least **12 historical temperature readings**.

Returns:

* Sensor name
* Forecast value
* Number of history points

### `POST /machine/explanation`

Processes machine sensor data through the predictive-maintenance preprocessing pipeline and returns model-level feature-importance information.

---

## Copilot Endpoints

### `POST /machine/copilot/status`

Returns machine-status information through the Copilot service.

### `POST /machine/copilot/query`

Accepts a natural-language industrial question and sensor data.

The backend routes the question to the appropriate verified Copilot tool.

Supported tool routing includes:

```text
get_machine_status
get_failure_risk
get_recent_anomalies
get_machine_history
get_forecast
get_explanation
get_recommendations
```

---

## API Input Validation

Pydantic validation protects the API from invalid sensor values and malformed requests.

Examples:

```text
Invalid tool wear value → HTTP 422
Out-of-range temperature → HTTP 422
Insufficient forecast history → HTTP 422
Empty Copilot query → HTTP 422
```

---

# Frontend Pages

The React application includes:

```text
/
/machines
/anomalies
/maintenance
/forecasting
/copilot
```

The frontend provides access to:

* Dashboard monitoring
* Machine monitoring
* Anomaly information
* Predictive maintenance
* Temperature forecasting
* AI Industrial Copilot

---

# Project Structure

```text
AI-Industrial-Intelligence/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   ├── raw/
│   └── processed/
│
├── ml/
│   ├── preprocessing/
│   ├── anomaly_detection/
│   ├── predictive_maintenance/
│   ├── forecasting/
│   ├── explainability/
│   ├── recommendations/
│   └── simulator/
│
├── simulator/
├── reports/
├── notebooks/
├── tests/
├── docs/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Installation

## 1. Clone the Repository

Replace the placeholder with the actual GitHub repository URL after the repository is created.

```powershell
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd AI-Industrial-Intelligence
```

## 2. Create the Python Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

## 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

## 4. Install Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

---

# Run the Backend

From the project root:

```powershell
.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Run the Frontend

Open a second terminal:

```powershell
cd frontend
npm run dev
```

Frontend:

```text
http://localhost:5173/
```

---

# Testing

The project includes validation and regression testing for:

* ML model artifacts
* Predictive-maintenance predictions
* Anomaly detection
* Forecasting
* Explainable AI
* Recommendations
* Simulator transitions
* FastAPI endpoints
* Input validation
* Copilot routing
* React frontend integration
* End-to-end application flow

### Example Validation

```text
Invalid tool wear value → HTTP 422
Insufficient forecast history → HTTP 422
Empty Copilot query → HTTP 422
Valid Copilot request → Successful verified result
```

Core end-to-end regression testing verified successful communication between the React frontend, FastAPI backend, and AI/ML services.

---

# Model Limitations

The project is intended as an AI engineering and portfolio demonstration.

Important limitations include:

* Benchmark datasets do not represent every real industrial environment.
* An anomaly does not automatically mean machine failure.
* Forecasting performance depends on the available telemetry pattern.
* Built-in feature importance is not a causal explanation.
* Rule-based recommendations should support qualified maintenance decisions rather than replace them.
* The simulator does not control or connect to physical industrial machinery.
* Model performance can change when applied to different machines, sensors, operating conditions, or datasets.
* The system has not been validated for real-world industrial safety or production deployment.

---

# Project Status

Core project development is complete.

Completed areas include:

* Data processing
* Machine-learning models
* Anomaly detection
* Predictive maintenance
* Forecasting
* Explainable AI
* Recommendations
* Simulation
* FastAPI backend
* React + TypeScript frontend
* AI Industrial Copilot
* Error handling
* Regression testing
* End-to-end integration

The final professional PDF report is maintained separately as the project documentation deliverable.

---

# Future Improvements

Possible future improvements include:

* Dynamic PDF report generation inside the deployed application
* Database-backed historical machine records
* More advanced forecasting models
* Per-instance explainability
* Authentication and user management
* Real industrial sensor integration
* Additional machine types and datasets
* Cloud deployment
* Automated monitoring and alerting

---

# Developer

**Abdullah Butt**

**AI & Python Developer**

---

## License

This project is intended as a portfolio and educational AI engineering project.
