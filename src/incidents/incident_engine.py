from datetime import datetime, timezone
import uuid


def create_incident(drift_result: dict):
    """
    Create an incident when data drift is detected.
    """

    if not drift_result["drift_detected"]:
        return None

    affected_features = []

    for feature, result in drift_result["features"].items():
        if result["drift_detected"]:
            affected_features.append(feature)

    incident = {
        "incident_id": str(uuid.uuid4()),
        "incident_type": "DATA_DRIFT",
        "severity": "HIGH",
        "status": "OPEN",
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "reason": "Production data distribution has changed.",
        "affected_features": affected_features
    }

    return incident