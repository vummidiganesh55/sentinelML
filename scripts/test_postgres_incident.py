import pandas as pd

from src.monitoring.drift import calculate_drift
from src.monitoring.production_data import get_production_data
from src.incidents.incident_engine import create_incident


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
# 3. Keep model input features
# -----------------------------

production_features = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

production_df = production_df[production_features]


# -----------------------------
# 4. Calculate drift
# -----------------------------

drift_result = calculate_drift(
    reference_df,
    production_df
)


# -----------------------------
# 5. Create incident
# -----------------------------

incident = create_incident(
    drift_result
)


# -----------------------------
# 6. Display results
# -----------------------------

print("\n=== SENTINELML INCIDENT MONITORING ===")

print("\nDrift detected:")
print(drift_result["drift_detected"])

print("\nIncident:")
print(incident)