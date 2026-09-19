import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.incidents.incident_engine import create_incident
from src.rca.rca_engine import analyze_incident
from src.healing.policy_engine import evaluate_action
from src.healing.healing_executor import execute_healing
from src.healing.verification import verify_recovery

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


# 1. Drift detection
drift_result = calculate_drift(
    reference_df,
    production_df
)


# 2. Incident creation
incident = create_incident(
    drift_result
)


if incident:

    # 3. RCA
    rca_result = analyze_incident(
        incident,
        drift_result
    )

    # 4. Policy decision
    policy_result = evaluate_action(
        incident,
        rca_result["recommended_action"]
    )

    # 5. Execute approved action
    healing_result = execute_healing(
        policy_result
    )
    verification_result = verify_recovery(
    healing_result,
    drift_result
)

    print("\n=== SENTINELML HEALING PIPELINE ===")

    print("\nIncident:")
    print(json.dumps(
        incident,
        indent=4
    ))

    print("\nRCA:")
    print(json.dumps(
        rca_result,
        indent=4
    ))

    print("\nPolicy:")
    print(json.dumps(
        policy_result,
        indent=4
    ))

    print("\nHealing:")
    print(json.dumps(
        healing_result,
        indent=4
    ))
    print("\nVerification:")
    print(json.dumps(
    verification_result,
    indent=4
))
else:

    print("No incident detected.")