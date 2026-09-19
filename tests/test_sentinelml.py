from src.monitoring.drift import calculate_drift
from src.incidents.incident_engine import create_incident
from src.healing.policy_engine import evaluate_action


def test_no_drift_creates_no_incident():

    reference = {
        "Air temperature [K]": 300,
        "Process temperature [K]": 310,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 40,
        "Tool wear [min]": 100
    }

    production = {
        "Air temperature [K]": 300,
        "Process temperature [K]": 310,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 40,
        "Tool wear [min]": 100
    }

    import pandas as pd

    reference_df = pd.DataFrame([reference])
    production_df = pd.DataFrame([production])

    result = calculate_drift(
        reference_df,
        production_df
    )

    incident = create_incident(result)

    assert result["drift_detected"] is False
    assert incident is None


def test_drift_creates_incident():

    import pandas as pd

    reference_df = pd.DataFrame({
        "Air temperature [K]": [300, 300, 300],
        "Process temperature [K]": [310, 310, 310],
        "Rotational speed [rpm]": [1500, 1500, 1500],
        "Torque [Nm]": [40, 40, 40],
        "Tool wear [min]": [100, 100, 100]
    })

    production_df = pd.DataFrame({
        "Air temperature [K]": [500, 500, 500],
        "Process temperature [K]": [310, 310, 310],
        "Rotational speed [rpm]": [1500, 1500, 1500],
        "Torque [Nm]": [40, 40, 40],
        "Tool wear [min]": [100, 100, 100]
    })

    result = calculate_drift(
        reference_df,
        production_df
    )

    incident = create_incident(result)

    assert result["drift_detected"] is True
    assert incident is not None
    assert incident["incident_type"] == "DATA_DRIFT"
    assert incident["status"] == "OPEN"


def test_policy_allows_quarantine():

    incident = {
        "incident_id": "test-123",
        "incident_type": "DATA_DRIFT"
    }

    ai_rca = {
        "root_cause_hypothesis": "Data drift detected",
        "recommended_action": "monitor"
    }

    result = evaluate_action(
        incident,
        ai_rca
    )

    assert result["selected_action"] == "quarantine_data"
    assert result["allowed"] is True