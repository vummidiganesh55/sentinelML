# 🚨 SentinelML

## Intelligent Self-Healing ML Operations Platform

**Real-Time ML API with Automated Drift Detection, AI-Driven Root Cause Analysis, and Policy-Controlled Self-Healing**

---

## ⭐ Badges

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-orange)
![MLflow](https://img.shields.io/badge/MLflow-Model%20Tracking-blue)
![Ollama](https://img.shields.io/badge/Ollama-LLM-black)

---

# 📌 Description

SentinelML is an **MLOps platform for monitoring and operating a production machine-learning API**.

The platform goes beyond simple model prediction by providing:

- Real-time ML predictions
- Production telemetry
- Data drift detection
- Incident detection
- Evidence collection
- AI-driven Root Cause Analysis
- Policy-controlled self-healing
- Recovery verification
- PostgreSQL persistence
- Prometheus monitoring
- Alertmanager integration
- Grafana dashboards
- Docker Compose deployment

The core idea is:

```text
Observe
   ↓
Detect
   ↓
Investigate
   ↓
Decide
   ↓
Recover
   ↓
Verify
```

---

# 🎯 Problem Statement

Machine-learning systems can continue serving predictions even when production conditions change.

Examples include:

- Production data distribution changes
- API errors increase
- Prediction latency increases
- Database connectivity problems
- Unhealthy services
- Unexpected production inputs

Traditional monitoring can tell engineers that something is wrong, but it does not automatically provide a complete:

```text
Detection → Investigation → Decision → Recovery → Verification
```

workflow.

SentinelML addresses this operational problem by combining **ML monitoring, incident management, AI-assisted investigation, policy-controlled recovery, and post-recovery verification**.

---

# 💡 Solution

SentinelML creates an automated incident-response pipeline:

```text
Production ML API
       ↓
Telemetry
       ↓
Monitoring
       ↓
Incident Detection
       ↓
Evidence Collection
       ↓
AI Root Cause Analysis
       ↓
Policy Engine
       ↓
Controlled Healing
       ↓
Recovery Verification
       ↓
Recovered / Human Investigation
```

A key design principle is that the LLM **does not directly control production actions**.

Instead:

```text
AI Recommendation
       ↓
Policy Engine
       ↓
Allowed Action
       ↓
Healing Executor
       ↓
Verification
```

---

# 🚀 Features

## 🤖 ML Prediction API

FastAPI provides the production prediction service.

The API accepts:

- Machine type
- Air temperature
- Process temperature
- Rotational speed
- Torque
- Tool wear

and predicts whether machine failure is likely.

---

## 📊 Production Telemetry

The system records:

- Prediction
- Failure probability
- Model version
- Request latency
- Timestamp
- Input features

Telemetry can be consumed by the monitoring pipeline.

---

## 📈 Data Drift Detection

SentinelML compares production data against reference data.

The current MVP uses a relative mean-shift detection method.

```text
Relative Change =
|Production Mean - Reference Mean|
----------------------------------
       |Reference Mean|
```

Current drift threshold:

```text
0.20
```

Example:

```text
Reference Torque Mean:   40.0034
Production Torque Mean:  60.0050
Relative Change:          0.50
Drift Detected:           TRUE
```

---

## 🚨 Incident Detection

Detected problems are converted into structured incidents.

Supported incident flows include:

```text
DATA_DRIFT
API_ALERT
```

Incident information includes:

- Incident ID
- Incident type
- Severity
- Status
- Reason
- Affected features
- Detection timestamp
- Resolution timestamp

---

## 🔎 Evidence Collection

Before AI Root Cause Analysis, SentinelML collects structured evidence.

Evidence can include:

- Incident information
- Drift statistics
- Affected features
- Reference statistics
- Production statistics
- Prediction counts
- Failure predictions
- Model version
- Availability of performance evidence

This prevents the LLM from making decisions without context.

---

## 🧠 AI Root Cause Analysis

SentinelML integrates:

```text
Ollama
+
Qwen
```

The AI RCA engine analyzes structured evidence and produces:

- Root-cause hypothesis
- Supporting evidence
- Confidence
- Recommended action
- Safety validation

The system is designed to prevent unsupported conclusions.

For example:

```text
Observed:
Data drift

Not confirmed:
Model performance degradation
```

If production ground-truth labels are unavailable, SentinelML does not claim that model performance has degraded.

---

## 🛡️ Policy-Controlled Self-Healing

The AI recommendation is passed through a policy engine before any healing action.

Supported action types include:

```text
retry_api
restart_service
quarantine_data
rollback_model
```

Example policy:

```text
DATA_DRIFT
     ↓
quarantine_data
```

```text
API_ALERT
     ↓
restart_service
```

Unknown or unsupported incidents require human investigation.

---

## 🗃️ Data Quarantine

When data drift is detected, SentinelML can quarantine affected production records.

```text
Production Data
      ↓
Drift Detection
      ↓
Incident
      ↓
Policy Engine
      ↓
Quarantine
      ↓
Investigation
```

This allows potentially problematic data to be isolated without automatically changing the production model.

---

## 🔄 Recovery Verification

SentinelML does not consider an action successful merely because the command executed.

After healing, the system checks:

- Database connectivity
- Model availability
- API health
- Healing execution status

Example:

```json
{
  "verification_status": "RECOVERED",
  "checks": {
    "healing_executed": true,
    "database_healthy": true,
    "model_available": true,
    "api_healthy": true
  }
}
```

---

## 📋 Incident Lifecycle

```text
OPEN
  ↓
HEALING
  ↓
RECOVERED
```

or:

```text
OPEN
  ↓
HEALING
  ↓
FAILED
```

Incident history is persisted in PostgreSQL.

---

## 📜 Healing Audit Trail

Every healing decision is recorded with:

- Incident ID
- Selected action
- Execution status
- Reason
- Timestamp

This provides traceability for automated operational decisions.

---

## 📡 Prometheus Monitoring

SentinelML exposes Prometheus metrics through:

```text
GET /metrics
```

Current metrics include:

```text
sentinelml_prediction_requests_total
sentinelml_prediction_failures_total
sentinelml_api_errors_total
sentinelml_prediction_latency_seconds
```

---

## 🔔 Alertmanager Integration

Prometheus monitors operational conditions such as:

- API availability
- API errors
- High prediction latency

Alertmanager forwards alerts to the FastAPI alert endpoint.

```text
Prometheus
    ↓
Alertmanager
    ↓
FastAPI /alerts
    ↓
Incident Engine
    ↓
AI RCA
    ↓
Policy Engine
    ↓
Healing
    ↓
Verification
```

---

## 📊 Grafana Dashboard

Grafana provides operational visibility into:

- Prediction requests
- Machine failure predictions
- API errors
- Prediction latency
- API instance health

---

# 🏗️ Architecture

```text
                         SENTINELML
                              │
                              ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │ Prediction API  │
                    └────────┬────────┘
                             │
                             ▼
                       ML Prediction
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
            Telemetry               PostgreSQL
                 │
                 ▼
         Monitoring Engine
                 │
          ┌──────┴──────┐
          ▼             ▼
      Data Drift     API Alerts
          │             │
          └──────┬──────┘
                 ▼
          Incident Engine
                 │
                 ▼
         Evidence Collector
                 │
                 ▼
              AI RCA
          Ollama / Qwen
                 │
                 ▼
          Policy Engine
                 │
                 ▼
        Self-Healing Executor
                 │
                 ▼
        Recovery Verification
             /         \
            /           \
       Recovered       Failed
          │               │
          ▼               ▼
     Resume Service   Human Review


Monitoring:

FastAPI
   │
   ▼
Prometheus
   │
   ├──► Alertmanager ──► FastAPI /alerts
   │
   └──► Grafana
```

---

# 🔄 Workflow

## Normal Prediction Flow

```text
Client
  ↓
FastAPI
  ↓
ML Model
  ↓
Prediction
  ↓
Telemetry
  ↓
PostgreSQL
```

---

## Data Drift Flow

```text
Production Data
      ↓
Reference Comparison
      ↓
Drift Detection
      ↓
DATA_DRIFT Incident
      ↓
Evidence Collection
      ↓
AI RCA
      ↓
Policy Engine
      ↓
Quarantine Data
      ↓
Verification
      ↓
RECOVERED
```

---

## API Alert Flow

```text
API Error
    ↓
Prometheus
    ↓
Alertmanager
    ↓
/alerts
    ↓
API_ALERT Incident
    ↓
Evidence Collection
    ↓
AI RCA
    ↓
Policy Engine
    ↓
Controlled Recovery
    ↓
Verification
    ↓
RECOVERED / HUMAN REVIEW
```

---

# 🛠️ Tech Stack

## Machine Learning

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest
- Joblib

## API

- FastAPI
- Uvicorn
- Pydantic

## MLOps

- MLflow
- PostgreSQL
- SQLAlchemy

## AI

- Ollama
- Qwen

## Monitoring

- Prometheus
- Alertmanager
- Grafana

## Infrastructure

- Docker
- Docker Compose

## Testing

- Pytest
- Integration testing scripts

---

# 📂 Project Structure

```text
sentinelML/
│
├── data/
│   ├── raw/
│   │   └── ai4i2020.csv
│   ├── processed/
│   └── reference/
│       └── reference_data.csv
│
├── monitoring/
│   ├── alert_rules.yml
│   ├── alertmanager.yml
│   └── prometheus.yml
│
├── notebooks/
│   └── data_exploration.ipynb
│
├── scripts/
│   ├── create_tables.py
│   ├── test_drift.py
│   ├── test_drift_pipeline.py
│   ├── test_evidence.py
│   ├── test_rca.py
│   ├── test_policy.py
│   ├── test_healing.py
│   ├── test_verification.py
│   └── ...
│
├── src/
│   ├── api/
│   │   └── main.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── healing/
│   │   ├── healing_executor.py
│   │   ├── policy_engine.py
│   │   └── verification.py
│   │
│   ├── incidents/
│   │   ├── incident_engine.py
│   │   └── incident_lifecycle.py
│   │
│   ├── model/
│   │   └── sentinelml_model.joblib
│   │
│   ├── monitoring/
│   │   ├── drift.py
│   │   ├── metrics.py
│   │   ├── production_data.py
│   │   └── telemetry.py
│   │
│   └── rca/
│       ├── ai_rca_engine.py
│       ├── evidence_collector.py
│       └── rca_engine.py
│
├── tests/
│   └── test_sentinelml.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 📋 Prerequisites

Before running SentinelML, install:

- Python 3.11+
- Docker Desktop
- Git
- PostgreSQL through Docker Compose
- Ollama
- Qwen model for AI RCA

Verify Python:

```bash
python --version
```

Verify Docker:

```bash
docker --version
```

Verify Docker Compose:

```bash
docker compose version
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/vummidiganesh55/sentinelML.git
```

Move into the project:

```bash
cd sentinelML
```

---

## 2. Create Python environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create database tables

```bash
python scripts/create_tables.py
```

---

## 5. Build Docker image

```bash
docker build -t sentinelml-api:latest .
```

---

## 6. Start services

```bash
docker compose up -d
```

Check services:

```bash
docker compose ps
```

Expected services:

```text
sentinelml-api
sentinelml-postgres
sentinelml-prometheus
sentinelml-alertmanager
sentinelml-grafana
```

---

# 🔑 Environment Variables

Create a `.env` file for local configuration.

Example:

```env
DATABASE_URL=postgresql+psycopg2://sentinel:sentinel_password@localhost:5432/sentinelml

OLLAMA_URL=http://localhost:11434/api/generate

OLLAMA_MODEL=qwen2.5-coder:3b
```

### Important

Do not commit `.env` files containing passwords, API keys, tokens, or other secrets.

The repository `.gitignore` excludes `.env`.

---

# ▶️ Usage

## Start FastAPI

```bash
uvicorn src.api.main:app --reload
```

API:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Health endpoint:

```text
http://localhost:8000/health
```

Metrics:

```text
http://localhost:8000/metrics
```

---

# 💡 Example

## Prediction Request

```bash
curl.exe -X POST "http://localhost:8000/predict?machine_type=M&air_temperature=300.5&process_temperature=310.2&rotational_speed=1500&torque=42.5&tool_wear=120"
```

Example response:

```json
{
  "prediction": 0,
  "prediction_label": "normal",
  "failure_probability": 0.0,
  "model_version": "v1",
  "latency_ms": 561.78
}
```

---

## Health Check

```bash
curl.exe http://localhost:8000/health
```

Example:

```json
{
  "status": "healthy"
}
```

---

## Metrics

```bash
curl.exe http://localhost:8000/metrics
```

Example metrics include:

```text
sentinelml_prediction_requests_total
sentinelml_prediction_failures_total
sentinelml_api_errors_total
sentinelml_prediction_latency_seconds
```

---

# 🧪 Testing

Run the test suite:

```bash
pytest
```

The project also contains integration scripts for testing individual components.

Examples:

```bash
python scripts/test_drift.py
```

```bash
python scripts/test_drift_pipeline.py
```

```bash
python scripts/test_evidence.py
```

```bash
python scripts/test_rca.py
```

```bash
python scripts/test_policy.py
```

```bash
python scripts/test_healing.py
```

```bash
python scripts/test_verification.py
```

---

# 📊 Evaluation

## Dataset

SentinelML uses the **AI4I 2020 Predictive Maintenance Dataset**.

Dataset characteristics:

```text
Total records:       10,000
Features used:       6
Target:              Machine failure
Normal:              9,661
Failure:               339
```

The target is highly imbalanced, so evaluation considers multiple classification metrics.

---

## Model Results

| Metric | Result |
|---|---:|
| Accuracy | 97.95% |
| Precision | 72.13% |
| Recall | 64.71% |
| F1 Score | 68.22% |
| ROC-AUC | 96.12% |

The Random Forest model uses class balancing to address the failure-class imbalance.

---

# 📸 Screenshots / Demo

## 📸 Screenshots / Demo

### 🚀 FastAPI Swagger UI

FastAPI provides interactive API documentation for the SentinelML prediction and monitoring endpoints.

![SentinelML FastAPI Swagger UI](docs/images/fastapi-swagger.png)


### 📊 Grafana Production Monitoring

Grafana dashboard visualizing prediction requests, machine failure predictions, prediction latency, and API errors.

![SentinelML Grafana Production Monitoring](docs/images/grafana-dashboard.png)


### 🔍 Prometheus Monitoring

Prometheus monitors the SentinelML API and confirms that the `sentinelml-api` target is healthy and available for metric scraping.

![SentinelML Prometheus Monitoring](docs/images/prometheus-monitoring.png)


### 🤖 AI RCA & Self-Healing Pipeline

The SentinelML incident pipeline detects data drift, collects evidence, performs AI-driven root cause analysis, evaluates the policy, executes the approved healing action, and verifies recovery.

![SentinelML AI RCA and Self-Healing Pipeline](docs/images/self-healing-pipeline.png)


### 🔄 Complete Self-Healing Execution

End-to-end execution showing drift detection, incident creation, AI RCA, policy decision, data quarantine, and successful recovery verification.

![SentinelML Complete Self-Healing Execution](docs/images/self-healing-pipeline-complete.png)

# ⚡ Performance

The current MVP measures prediction API latency using Prometheus histograms.

Tracked metric:

```text
sentinelml_prediction_latency_seconds
```

The system also records:

- Prediction request count
- Failure prediction count
- API error count
- Prediction latency

Performance monitoring allows operational issues to be detected independently from model predictions.

---

# 🔐 Security

SentinelML follows several safety principles.

## Policy-controlled actions

The AI does not directly execute production actions.

```text
LLM
 ↓
Policy Engine
 ↓
Allowed Action
 ↓
Executor
```

---

## Evidence-based AI

The RCA engine receives structured evidence instead of relying only on free-form assumptions.

---

## Performance claims are restricted

If production ground-truth labels are unavailable, the system does not automatically claim model performance degradation.

---

## Secrets protection

Environment files containing credentials are excluded through `.gitignore`.

---

## Human investigation

Unsupported or unknown incident types can be routed for human investigation instead of triggering uncontrolled automation.

---

# 🔮 Future Improvements

Planned improvements include:

- Automated model retraining
- Champion/challenger model evaluation
- Production model rollback
- Advanced drift detection using PSI
- Kolmogorov-Smirnov testing
- Prediction-quality monitoring with delayed labels
- Distributed tracing
- Advanced incident correlation
- Role-based access control
- Authentication and authorization
- Production secrets management
- Kubernetes deployment
- Real controlled service restart
- CI/CD pipeline
- Automated model validation
- Automated deployment gates

---

# ⚠️ Limitations

This project is a portfolio-focused MLOps MVP and is not intended to represent a fully enterprise production platform.

Current limitations include:

1. The drift detector currently uses a relative mean-shift heuristic.
2. Production ground-truth labels are not currently available for real-time model performance monitoring.
3. The current service restart action is simulated.
4. Model rollback is defined in the policy layer but is not currently executed automatically.
5. The system does not directly control the Docker Engine.
6. Authentication and role-based authorization are not implemented.
7. The platform currently runs as a Docker Compose deployment rather than Kubernetes.

These limitations are intentionally documented to distinguish the implemented MVP from future production extensions.

---

# 🤝 Contributing

Contributions are welcome.

Suggested workflow:

```text
Fork
  ↓
Create Feature Branch
  ↓
Implement Change
  ↓
Add Tests
  ↓
Run Tests
  ↓
Create Pull Request
```

Please keep changes focused and include appropriate tests for new functionality.

---

# 📄 License

This project is currently provided for educational and portfolio purposes.

A formal open-source license can be added in a future release.

---

# 👨‍💻 Author

## Ganesh Vummidi

Computer Science Graduate | AI/ML | MLOps | Python | FastAPI

GitHub:

**vummidiganesh55**

---

# ⭐ Project Highlights

SentinelML demonstrates an end-to-end MLOps workflow combining:

```text
Machine Learning
      +
FastAPI
      +
PostgreSQL
      +
MLflow
      +
Data Drift Detection
      +
Prometheus
      +
Alertmanager
      +
Grafana
      +
Ollama / Qwen
      +
AI Root Cause Analysis
      +
Policy Engine
      +
Self-Healing
      +
Recovery Verification
      +
Docker
```

The main engineering principle is:

> **Detect problems automatically, investigate them using evidence, control recovery through explicit policy, and verify the result before considering the incident recovered.**
