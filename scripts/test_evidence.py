import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.incidents.incident_engine import create_incident
from src.rca.evidence_collector import collect_evidence


# 1. Load reference data
reference_df = pd.read_csv(
    "data/reference/reference_data.csv"
)


# 2. Load production telemetry
records = []

with open(
    "data/processed/predictions.jsonl",
    "r",
    encoding="utf-8"
) as file:

    for line in file:
        record = json.loads(line)
        records.append(record)


# 3. Create production dataframe
production_df = pd.DataFrame(
    [record["input"] for record in records]
)

# Add prediction information
production_df["prediction"] = [
    record["prediction"]
    for record in records
]


# 4. Detect drift
drift_result = calculate_drift(
    reference_df,
    production_df
)


# 5. Create incident
incident = create_incident(
    drift_result
)


# 6. Collect evidence
evidence = collect_evidence(
    incident,
    drift_result,
    production_df
)


# 7. Display evidence
print("\n=== SENTINELML EVIDENCE ===")

print(
    json.dumps(
        evidence,
        indent=4
    )
)