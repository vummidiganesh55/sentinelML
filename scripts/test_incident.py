import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.incidents.incident_engine import create_incident


# Load reference data
reference_df = pd.read_csv(
    "data/reference/reference_data.csv"
)


# Load production telemetry
records = []

with open(
    "data/processed/predictions.jsonl",
    "r",
    encoding="utf-8"
) as file:

    for line in file:
        record = json.loads(line)
        records.append(record["input"])


production_df = pd.DataFrame(records)


# Detect drift
drift_result = calculate_drift(
    reference_df,
    production_df
)


# Create incident
incident = create_incident(drift_result)


print("\nIncident:")
print(json.dumps(incident, indent=4))