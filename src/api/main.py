from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
import pandas as pd
import time
from pathlib import Path
import joblib
from fastapi.exceptions import RequestValidationError
# =========================================================
# SENTINELML RCA / HEALING
# =========================================================

from src.rca.evidence_collector import collect_evidence
from src.rca.ai_rca_engine import analyze_with_ai
from src.healing.policy_engine import evaluate_action
from src.healing.healing_executor import execute_healing
from src.healing.verification import verify_recovery

# =========================================================
# PROMETHEUS
# =========================================================

try:
    from importlib import import_module

    _prometheus_client = import_module(
        "prometheus_client"
    )

    generate_latest = (
        _prometheus_client.generate_latest
    )

    CONTENT_TYPE_LATEST = (
        _prometheus_client.CONTENT_TYPE_LATEST
    )

except ImportError:

    CONTENT_TYPE_LATEST = (
        "text/plain; version=0.0.4; charset=utf-8"
    )

    def generate_latest():
        return b""


# =========================================================
# MONITORING
# =========================================================

from src.monitoring.metrics import (
    prediction_requests,
    prediction_failures,
    api_errors,
    prediction_latency
)

from src.monitoring.telemetry import log_prediction

# =========================================================
# DATABASE
# =========================================================

from src.database.database import SessionLocal

from src.database.models import (
    Incident,
    Prediction
)

# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="SentinelML API",
    description=(
        "Real-Time ML API for Machine Failure Prediction"
    ),
    version="1.0.0"
)

# =========================================================
# GLOBAL API ERROR MONITORING
# =========================================================

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    api_errors.inc()

    print(
        f"API ERROR: {request.method} "
        f"{request.url.path} - {exc}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "model"
    / "sentinelml_model.joblib"
)

model = joblib.load(MODEL_PATH)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    api_errors.inc()

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()
        }
    )
# =========================================================
# HEALTH ENDPOINT
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =========================================================
# ALERTMANAGER WEBHOOK
# =========================================================

@app.post("/alerts")
async def receive_alert(
    alert_data: dict
):

    print("\n====================================")
    print("       SENTINELML ALERT RECEIVED")
    print("====================================")

    alerts = alert_data.get(
        "alerts",
        []
    )

    incidents = []

    db = SessionLocal()

    try:

        for alert in alerts:

            labels = alert.get(
                "labels",
                {}
            )

            alert_status = alert.get(
                "status",
                alert_data.get(
                    "status",
                    "unknown"
                )
            ).upper()

            alert_name = labels.get(
                "alertname",
                "UnknownAlert"
            )

            severity = labels.get(
                "severity",
                "warning"
            )

            fingerprint = alert.get(
                "fingerprint",
                "unknown"
            )

            # =================================================
            # FIRING ALERT
            # =================================================

            if alert_status == "FIRING":

                existing_incident = (
                    db.query(Incident)
                    .filter(
                        Incident.incident_id
                        == fingerprint
                    )
                    .first()
                )

                # =============================================
                # EXISTING INCIDENT
                # =============================================

                if existing_incident:

                    existing_incident.status = "OPEN"

                    db.commit()

                    print(
                        "\n=== INCIDENT ALREADY EXISTS ==="
                    )

                    print(
                        existing_incident.incident_id
                    )

                    incident_for_pipeline = {

                        "incident_id": fingerprint,

                        "incident_type": "API_ALERT",

                        "severity": severity,

                        "status": "OPEN",

                        "reason": alert_name,

                        "affected_features": []

                    }

                    incidents.append({

                        "incident_id": fingerprint,

                        "status": "OPEN",

                        "message": (
                            "Existing incident reopened."
                        )

                    })

                # =============================================
                # NEW INCIDENT
                # =============================================

                else:

                    new_incident = Incident(

                        incident_id=fingerprint,

                        incident_type="API_ALERT",

                        severity=severity,

                        status="OPEN",

                        reason=alert_name,

                        affected_features=""

                    )

                    db.add(
                        new_incident
                    )

                    db.commit()

                    print(
                        "\n=== INCIDENT CREATED ==="
                    )

                    print({

                        "incident_id": fingerprint,

                        "incident_type": "API_ALERT",

                        "severity": severity,

                        "status": "OPEN",

                        "reason": alert_name

                    })

                    incident_for_pipeline = {

                        "incident_id": fingerprint,

                        "incident_type": "API_ALERT",

                        "severity": severity,

                        "status": "OPEN",

                        "reason": alert_name,

                        "affected_features": []

                    }

                    incidents.append({

                        "incident_id": fingerprint,

                        "status": "OPEN",

                        "message": "Incident created."

                    })

                # =================================================
                # STEP 1 — COLLECT EVIDENCE
                # =================================================

                print(
                    "\n=== COLLECTING EVIDENCE ==="
                )

                evidence = collect_evidence(
                    incident_for_pipeline
                )

                print(
                    "\n=== EVIDENCE COLLECTED ==="
                )

                print(
                    evidence
                )

                # =================================================
                # STEP 2 — AI ROOT CAUSE ANALYSIS
                # =================================================

                print(
                    "\n=== RUNNING AI RCA ==="
                )

                ai_result = analyze_with_ai(
                    evidence
                )

                ai_rca = ai_result[
                    "ai_rca"
                ]

                print(
                    "\n=== AI RCA RESULT ==="
                )

                print(
                    ai_rca
                )

                # =================================================
                # STEP 3 — POLICY ENGINE
                # =================================================

                print(
                    "\n=== EVALUATING POLICY ==="
                )

                policy_result = evaluate_action(

                    incident_for_pipeline,

                    ai_rca

                )

                print(
                    "\n=== POLICY DECISION ==="
                )

                print(
                    policy_result
                )

                # =================================================
                # STEP 4 — HEALING EXECUTOR
                # =================================================

                print(
                    "\n=== EXECUTING HEALING ==="
                )

                healing_result = execute_healing(
                    policy_result
                )

                print(
                    "\n=== HEALING RESULT ==="
                )

                print(
                    healing_result
                )

                # =================================================
                # STEP 5 — RECOVERY VERIFICATION
                # =================================================

                print(
                    "\n=== VERIFYING RECOVERY ==="
                )

                verification_result = verify_recovery(
                    healing_result
                )

                print(
                    "\n=== RECOVERY VERIFICATION ==="
                )

                print(
                    verification_result
                )

                # =================================================
                # COMPLETE PIPELINE RESULT
                # =================================================

                incidents[-1].update({

                    "ai_rca": ai_rca,

                    "policy": policy_result,

                    "healing": healing_result,

                    "verification": (
                        verification_result
                    )

                })

                print(
                    "\n=== AUTOMATIC INCIDENT "
                    "PIPELINE COMPLETED ==="
                )

            # =================================================
            # RESOLVED ALERT
            # =================================================

            elif alert_status == "RESOLVED":

                existing_incident = (

                    db.query(Incident)

                    .filter(
                        Incident.incident_id
                        == fingerprint
                    )

                    .first()

                )

                # =============================================
                # INCIDENT FOUND
                # =============================================

                if existing_incident:

                    from datetime import (
                        datetime,
                        timezone
                    )

                    existing_incident.status = (
                        "RESOLVED"
                    )

                    existing_incident.resolved_at = (

                        datetime.now(
                            timezone.utc
                        )

                    )

                    db.commit()

                    print(
                        "\n=== INCIDENT RESOLVED ==="
                    )

                    print(
                        existing_incident.incident_id
                    )

                    incidents.append({

                        "incident_id": fingerprint,

                        "status": "RESOLVED",

                        "message": (
                            "Incident resolved."
                        )

                    })

                # =============================================
                # INCIDENT NOT FOUND
                # =============================================

                else:

                    print(
                        "\n=== INCIDENT NOT FOUND ==="
                    )

                    print(
                        fingerprint
                    )

                    incidents.append({

                        "incident_id": fingerprint,

                        "status": "UNKNOWN",

                        "message": (

                            "Resolved alert received, "
                            "but matching incident "
                            "was not found."

                        )

                    })

        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return {

            "status": "received",

            "incidents": incidents

        }

    finally:

        db.close()


# =========================================================
# MODEL INFO
# =========================================================

@app.get("/model-info")
def model_info():

    return {

        "model": "RandomForestClassifier",

        "version": "v1"

    }


# =========================================================
# PREDICTION ENDPOINT
# =========================================================

@app.post("/predict")
def predict(

    machine_type: str,

    air_temperature: float,

    process_temperature: float,

    rotational_speed: int,

    torque: float,

    tool_wear: int

):

    start_time = time.time()

    # =====================================================
    # PROMETHEUS REQUEST COUNTER
    # =====================================================

    prediction_requests.inc()

    # =====================================================
    # CREATE MODEL INPUT
    # =====================================================

    input_data = pd.DataFrame([{

        "Type": machine_type,

        "Air temperature [K]":
            air_temperature,

        "Process temperature [K]":
            process_temperature,

        "Rotational speed [rpm]":
            rotational_speed,

        "Torque [Nm]":
            torque,

        "Tool wear [min]":
            tool_wear

    }])

    # =====================================================
    # MODEL PREDICTION
    # =====================================================

    prediction = model.predict(
        input_data
    )[0]

    probability = model.predict_proba(
        input_data
    )[0][1]

    # =====================================================
    # LATENCY
    # =====================================================

    latency = (
        time.time()
        - start_time
    ) * 1000

    # =====================================================
    # SAVE PREDICTION TO POSTGRESQL
    # =====================================================

    db = SessionLocal()

    try:

        prediction_record = Prediction(

            machine_type=machine_type,

            air_temperature=air_temperature,

            process_temperature=process_temperature,

            rotational_speed=rotational_speed,

            torque=torque,

            tool_wear=tool_wear,

            prediction=int(
                prediction
            ),

            failure_probability=float(
                probability
            ),

            latency_ms=float(
                latency
            ),

            model_version="v1"

        )

        db.add(
            prediction_record
        )

        db.commit()

    finally:

        db.close()

    # =====================================================
    # JSONL TELEMETRY
    # =====================================================

    log_prediction(

        input_data=(

            input_data

            .iloc[0]

            .to_dict()

        ),

        prediction=int(
            prediction
        ),

        failure_probability=float(
            probability
        ),

        latency_ms=latency,

        model_version="v1"

    )

    # =====================================================
    # PROMETHEUS FAILURE COUNTER
    # =====================================================

    if prediction == 1:

        prediction_failures.inc()

    # =====================================================
    # PROMETHEUS LATENCY
    # =====================================================

    prediction_latency.observe(
        latency / 1000
    )

    # =====================================================
    # API RESPONSE
    # =====================================================

    return {

        "prediction": int(
            prediction
        ),

        "prediction_label": (

            "failure"

            if prediction == 1

            else "normal"

        ),

        "failure_probability": round(

            float(probability),

            4

        ),

        "model_version": "v1",

        "latency_ms": round(

            latency,

            2

        )

    }


# =========================================================
# PROMETHEUS METRICS ENDPOINT
# =========================================================

@app.get("/metrics")
def metrics():

    return Response(

        content=generate_latest(),

        media_type=CONTENT_TYPE_LATEST

    )

