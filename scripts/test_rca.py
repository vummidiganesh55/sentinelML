import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.incidents.incident_engine import create_incident
from src.rca.rca_engine import analyze_incident


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


# 1. Detect drift
drift_result = calculate_drift(
    reference_df,
    production_df
)


# 2. Create incident
incident = create_incident(drift_result)


# 3. Run RCA
if incident:

    rca_result = analyze_incident(
        incident,
        drift_result
    )

    print("\nAI RCA Result:")
    print(json.dumps(
        rca_result,
        indent=4
    ))

else:

    print("No incident detected.")