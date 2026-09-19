import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.incidents.incident_engine import create_incident
from src.rca.evidence_collector import collect_evidence
from src.rca.ai_rca_engine import analyze_with_ai
from src.healing.policy_engine import evaluate_action
from src.healing.healing_executor import execute_healing
from src.healing.verification import verify_recovery


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
        records.append(json.loads(line))


# 3. Create production dataframe
production_df = pd.DataFrame(
    [record["input"] for record in records]
)

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


# 7. AI Root Cause Analysis
ai_result = analyze_with_ai(
    evidence
)


# 8. Policy decision
policy_result = evaluate_action(
    incident,
    ai_result["ai_rca"]
)


# 9. Execute healing
healing_result = execute_healing(
    policy_result
)


# 10. Verify recovery
verification_result = verify_recovery(
    healing_result,
    drift_result
)


# 11. Display pipeline
print("\n=== SENTINELML AI HEALING PIPELINE ===")

print("\nAI RCA:")
print(
    json.dumps(
        ai_result,
        indent=4
    )
)

print("\nPolicy:")
print(
    json.dumps(
        policy_result,
        indent=4
    )
)

print("\nHealing:")
print(
    json.dumps(
        healing_result,
        indent=4
    )
)

print("\nVerification:")
print(
    json.dumps(
        verification_result,
        indent=4
    )
)