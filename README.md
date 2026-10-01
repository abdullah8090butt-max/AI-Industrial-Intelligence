# AI Industrial Intelligence & Predictive Maintenance System

An AI-powered industrial monitoring and predictive maintenance platform that combines **machine health monitoring, anomaly detection, failure-risk prediction, time-series forecasting, explainable AI, AI-assisted recommendations, and an intelligent Copilot** in a full-stack web application.

The system demonstrates the integration of **Python AI/ML services with FastAPI and a React + TypeScript frontend**.

---

## 🚀 Live Demo

### Frontend

https://ai-industrial-intelligence-01.onrender.com

### Backend API

https://ai-industrial-intelligence-06.onrender.com

### API Documentation

https://ai-industrial-intelligence-06.onrender.com/docs

---

# 📌 Project Overview

Industrial machines continuously generate operational data such as:

* Temperature
* Vibration
* Pressure
* RPM
* Load
* Machine status
* Timestamp
* Machine ID

Analyzing these signals manually can make it difficult to identify abnormal behavior and potential maintenance risks early.

This project provides an AI-powered system that analyzes machine information and presents actionable intelligence through a modern web dashboard.

The system can:

* Monitor machine health
* Detect abnormal conditions
* Estimate machine failure/maintenance risk
* Forecast sensor values
* Explain AI predictions
* Generate maintenance recommendations
* Simulate machine conditions
* Answer operational questions through an AI Copilot
* Generate intelligence reports in PDF format

---

# 👤 How to Use the Application

The application is designed to be easy to use even if you are not familiar with the underlying AI/ML system.

## 1. Open the Application

Open the live frontend:

https://ai-industrial-intelligence-01.onrender.com

The **Dashboard** will appear first.

---

## 2. Understand the Dashboard

The Dashboard gives you a quick overview of the industrial system.

You can see:

* **Total Machines** — number of machines being monitored
* **Healthy** — machines currently operating normally
* **Warning** — machines that may require attention
* **Critical** — machines with a higher level of concern
* **System Status** — overall system availability

Use the Dashboard as the starting point for understanding the current machine environment.

---

## 3. Check Machine Status

Open the **Machines** page.

Select or inspect a machine to view its current condition.

The system analyzes machine parameters such as:

* Temperature
* Vibration
* Pressure
* RPM
* Load

The result helps you understand whether the machine is operating normally or requires attention.

---

## 4. Check for Anomalies

Open **Anomalies**.

This section helps identify unusual machine behavior.

Review:

* Anomaly score
* Machine condition
* Affected machine
* Sensor information
* Severity

A higher anomaly level indicates that the machine's current behavior differs more from expected operating conditions.

---

## 5. Check Maintenance Risk

Open **Maintenance**.

This section shows the predicted maintenance/failure risk for machines.

Review:

* Risk score
* Risk level
* Important contributing factors
* Recommended maintenance actions

Use this information to understand which machine conditions may require further investigation.

> The predictions are AI/ML-based decision-support information and should not replace professional industrial safety or maintenance procedures.

---

## 6. View Forecasts

Open **Forecasting**.

Choose the available machine/sensor information and view the forecast.

The page provides:

* Historical values
* Predicted future values
* Actual vs. predicted visualization
* Forecast information

This helps you understand how a selected machine measurement may change over time.

---

## 7. Understand an AI Prediction

Open **AI Explanation**.

This section explains the factors that contributed to an AI prediction.

You can use the feature-importance information to understand which machine parameters had greater influence on the model's result.

For example, the system may indicate that factors such as temperature, vibration, pressure, RPM, or load contributed to a prediction.

---

## 8. Use the AI Copilot

Open **Copilot** to interact with the industrial intelligence system using natural-language questions.

You can ask questions such as:

```text
What is the current machine status?
```

```text
Which machines have a high maintenance risk?
```

```text
What recent anomalies were detected?
```

```text
What factors are contributing to the risk?
```

```text
What maintenance recommendation is available?
```

The Copilot uses backend tools to retrieve information from the application's machine-intelligence services.

---

## 9. Generate an Intelligence Report

Open **Reports**.

Use the available report-generation option to create a PDF intelligence report.

The report can contain information such as:

* Machine status
* Risk information
* Anomalies
* Forecast information
* AI explanations
* Recommendations

The generated PDF can then be viewed or saved for further reference.

---

## 🔄 Recommended User Workflow

For a quick analysis, the recommended workflow is:

```text
Dashboard
    ↓
Machines
    ↓
Anomalies
    ↓
Maintenance
    ↓
Forecasting
    ↓
AI Explanation
    ↓
Copilot
    ↓
Reports
```

### Example Scenario

A user wants to investigate a machine that may have a problem:

**Step 1:** Open **Dashboard** to check the overall system.

**Step 2:** Open **Machines** and identify the machine requiring attention.

**Step 3:** Open **Anomalies** to investigate unusual behavior.

**Step 4:** Open **Maintenance** to check the predicted maintenance/failure risk.

**Step 5:** Open **AI Explanation** to understand the important factors behind the prediction.

**Step 6:** Open **Forecasting** to examine the expected future behavior of a selected sensor.

**Step 7:** Ask the **AI Copilot** for a summary or recommendation.

**Step 8:** Generate a **PDF Report** to document the analysis.

---

## 💡 Understanding the Results

The application uses AI/ML models to provide analytical results.

These results should be interpreted as **decision-support information** rather than guaranteed predictions.

For real industrial environments, maintenance decisions should also consider:

* Equipment specifications
* Manufacturer recommendations
* Physical inspections
* Safety procedures
* Qualified maintenance personnel
* Actual operating conditions

---

# ✨ Features

## 📊 Dashboard

Provides a high-level overview of the industrial environment.

Displays:

* Total machines
* Healthy machines
* Warning machines
* Critical machines
* Overall system status
* Machine health information

---

## 🏭 Machine Monitoring

The Machines section provides individual machine information and health status.

The backend analyzes machine parameters and returns machine-health information through REST APIs.

---

## 🚨 Anomaly Detection

The anomaly detection module identifies unusual machine behavior.

It provides:

* Anomaly score
* Machine condition
* Normal / Warning / Critical classification
* Sensor-based analysis

The system uses machine sensor values to identify potentially abnormal operating conditions.

---

## 🔧 Predictive Maintenance

The predictive maintenance module estimates maintenance/failure risk based on machine conditions.

It provides:

* Failure-risk score
* Risk classification
* Important contributing features
* Maintenance recommendations

This demonstrates how machine data can be used to support preventive maintenance decisions.

---

## 📈 Forecasting

The forecasting module predicts future sensor values based on historical machine data.

The interface provides:

* Historical sensor values
* Predicted values
* Actual vs predicted visualization
* Forecast information

---

## 🧠 AI Explanation

The system provides an explanation of the factors contributing to a prediction.

Feature importance is used to identify which machine parameters have the greatest influence on the model output.

This makes the AI system easier to understand and interpret.

---

## 🤖 AI Copilot

The project includes an intelligent Copilot for interacting with the industrial intelligence system.

The Copilot can access backend tools such as:

* Machine status
* Recent anomalies
* Machine history
* Failure risk
* Forecast information
* Prediction explanations
* Maintenance recommendations

---

## 📄 Intelligence Reports

The system can generate PDF intelligence reports containing machine and AI analysis.

Reports can include information related to:

* Machine status
* Risk information
* Anomalies
* Predictions
* Recommendations
* AI-generated explanations

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │     React Frontend      │
                    │     TypeScript + Vite   │
                    │                         │
                    │  Dashboard              │
                    │  Machines               │
                    │  Anomalies              │
                    │  Maintenance            │
                    │  Forecasting            │
                    │  AI Explanation         │
                    │  Copilot                │
                    │  Reports                │
                    └────────────┬────────────┘
                                 │
                                 │ REST API
                                 ▼
                    ┌─────────────────────────┐
                    │       FastAPI           │
                    │       Backend            │
                    │                         │
                    │ Machine APIs             │
                    │ Dashboard API            │
                    │ Copilot APIs             │
                    │ Forecast API             │
                    │ Explanation API          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      AI / ML Layer      │
                    │                         │
                    │ Anomaly Detection       │
                    │ Failure-Risk Prediction │
                    │ Forecasting              │
                    │ Feature Importance       │
                    │ Recommendations          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Machine Data        │
                    │                         │
                    │ Temperature             │
                    │ Vibration               │
                    │ Pressure                │
                    │ RPM                     │
                    │ Load                    │
                    │ Status                  │
                    └─────────────────────────┘
```

---

# 🛠️ Technology Stack

## Frontend

* React
* TypeScript
* Vite
* Recharts
* HTML
* CSS

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* REST APIs

## AI / Machine Learning

* Pandas
* NumPy
* Scikit-learn
* Machine Learning models
* Anomaly detection
* Predictive maintenance
* Time-series forecasting
* Feature importance

## Reporting

* ReportLab
* PDF generation

## Deployment

* Render
* GitHub

---

# 📂 Project Structure

```text
AI-Industrial-Intelligence/
│
├── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── schemas/
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│
├── reports/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🔌 API Endpoints

The FastAPI backend provides endpoints for the major AI capabilities.

### System

```text
GET /
GET /health
GET /dashboard/summary
```

### Machine Intelligence

```text
POST /machine/status
POST /machine/failure-risk
POST /machine/anomaly
POST /machine/recommendations
POST /machine/forecast
POST /machine/explanation
```

### AI Copilot

```text
POST /machine/copilot/status
POST /machine/copilot/query
```

Interactive API documentation:

https://ai-industrial-intelligence-06.onrender.com/docs

---

# 💻 Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/abdullah8090butt-max/AI-Industrial-Intelligence.git
cd AI-Industrial-Intelligence
```

---

# ⚙️ Backend Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🌐 Production Deployment

The project is deployed using Render.

## Frontend

```text
React + TypeScript + Vite
```

Deployment configuration:

```text
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: dist
```

## Backend

```text
FastAPI + Uvicorn
```

Deployment configuration:

```text
Build Command:
pip install -r requirements.txt

Start Command:
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

---

# 🧪 Testing & Verification

The deployed application was manually verified across its major functional areas.

### Verified Components

* [x] Dashboard
* [x] Machines
* [x] Anomalies
* [x] Maintenance
* [x] Forecasting
* [x] AI Explanation
* [x] AI Copilot
* [x] PDF Reports
* [x] Production frontend
* [x] Production backend
* [x] Frontend-to-backend API communication
* [x] Production CORS configuration

The application was tested after deployment to ensure that the React frontend could communicate correctly with the production FastAPI backend.

---

# 🔐 Production Configuration

The frontend communicates with the deployed FastAPI backend through the production API URL.

The backend allows the deployed frontend origin through its CORS configuration.

No private API keys or sensitive credentials should be committed to the repository.

---

# 🎯 Project Goals

This project was developed to demonstrate practical skills in:

* Artificial Intelligence
* Machine Learning
* Predictive Maintenance
* Anomaly Detection
* Time-Series Forecasting
* Explainable AI
* Python
* FastAPI
* REST API development
* React
* TypeScript
* Data Visualization
* Full-Stack AI Application Development
* Cloud Deployment

---

# 📚 Learning Outcomes

Through this project, the development process covered:

1. Dataset understanding
2. Data preprocessing
3. Machine-learning model development
4. Anomaly detection
5. Predictive maintenance
6. Forecasting
7. Explainable AI
8. Recommendation systems
9. Machine simulation
10. FastAPI backend development
11. React + TypeScript frontend development
12. AI Copilot integration
13. PDF report generation
14. Production deployment
15. Full-stack API integration
16. Production testing

---

# 👨‍💻 Developer

**Abdullah Butt**

AI & Python Developer

GitHub:
https://github.com/abdullah8090butt-max

LinkedIn:
https://linkedin.com/in/abdullah-butt-878a31429

---

# 📜 License

This project is intended for educational, portfolio, and demonstration purposes.
