import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.monitoring.production_data import get_production_data
from src.incidents.incident_engine import create_incident
from src.rca.evidence_collector import collect_evidence


# -----------------------------
# 1. Load reference data
# -----------------------------

reference_df = pd.read_csv(
    "data/reference/reference_data.csv"
)


# -----------------------------
# 2. Load production data
#    from PostgreSQL
# -----------------------------

production_df = get_production_data()


# -----------------------------
# 3. Keep model inputs
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
# 4. Calculate drift
# -----------------------------

drift_result = calculate_drift(
    reference_df,
    drift_df
)


# -----------------------------
# 5. Create incident
# -----------------------------

incident = create_incident(
    drift_result
)


if incident is None:
    print("No incident detected.")
    raise SystemExit


# -----------------------------
# 6. Collect evidence
# -----------------------------

evidence = collect_evidence(
    incident,
    drift_result,
    production_df
)


# -----------------------------
# 7. Display evidence
# -----------------------------

print("\n=== SENTINELML EVIDENCE COLLECTION ===")

print(
    json.dumps(
        evidence,
        indent=4,
        default=str
    )
)