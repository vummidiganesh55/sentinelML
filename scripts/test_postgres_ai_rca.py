import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.monitoring.production_data import get_production_data
from src.incidents.incident_engine import create_incident
from src.rca.evidence_collector import collect_evidence
from src.rca.ai_rca_engine import analyze_with_ai


# -----------------------------
# 1. Reference data
# -----------------------------

reference_df = pd.read_csv(
    "data/reference/reference_data.csv"
)


# -----------------------------
# 2. Production data
# -----------------------------

production_df = get_production_data()


# -----------------------------
# 3. Features used for drift
# -----------------------------

production_features = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

drift_df = production_df[production_features]


# -----------------------------
# 4. Drift detection
# -----------------------------

drift_result = calculate_drift(
    reference_df,
    drift_df
)


# -----------------------------
# 5. Incident creation
# -----------------------------

incident = create_incident(
    drift_result
)


if incident is None:
    print("No incident detected.")
    raise SystemExit


# -----------------------------
# 6. Evidence collection
# -----------------------------

evidence = collect_evidence(
    incident,
    drift_result,
    production_df
)


# -----------------------------
# 7. AI RCA
# -----------------------------

ai_result = analyze_with_ai(
    evidence
)


# -----------------------------
# 8. Display result
# -----------------------------

print("\n=== SENTINELML AI RCA ===")

print(
    json.dumps(
        ai_result,
        indent=4
    )
)