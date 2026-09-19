import pandas as pd

from src.monitoring.drift import calculate_drift, REFERENCE_FILE
from src.incidents.incident_engine import create_incident


reference_df = pd.read_csv(REFERENCE_FILE)

production_df = reference_df.copy()

# Simulate production drift
production_df["Torque [Nm]"] = (
    production_df["Torque [Nm]"] * 1.50
)

# Detect drift
drift_result = calculate_drift(
    reference_df,
    production_df
)

print("\n=== DRIFT RESULT ===")
print(drift_result)

# Create incident
incident = create_incident(
    drift_result
)

print("\n=== INCIDENT RESULT ===")
print(incident)