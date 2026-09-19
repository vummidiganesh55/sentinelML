import json
import pandas as pd

from src.monitoring.drift import calculate_drift
from src.monitoring.production_data import get_production_data
from src.incidents.incident_engine import create_incident
from src.rca.evidence_collector import collect_evidence
from src.rca.ai_rca_engine import analyze_with_ai
from src.healing.policy_engine import evaluate_action
from src.healing.healing_executor import execute_healing
from src.healing.verification import verify_recovery


# ---------------------------------------------------------
# 1. LOAD REFERENCE DATA
# ---------------------------------------------------------

reference_df = pd.read_csv(
    "data/reference/reference_data.csv"
)


# ---------------------------------------------------------
# 2. READ PRODUCTION DATA FROM POSTGRESQL
# ---------------------------------------------------------

production_df = get_production_data()

print("\nProduction records:", len(production_df))

if production_df.empty:
    print("No production predictions found.")
    raise SystemExit


# ---------------------------------------------------------
# 3. CALCULATE DRIFT
# ---------------------------------------------------------

production_features = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

drift_df = production_df[production_features]

drift_result = calculate_drift(
    reference_df,
    drift_df
)


# ---------------------------------------------------------
# 4. CREATE INCIDENT
# ---------------------------------------------------------

incident = create_incident(
    drift_result
)

if incident is None:
    print("\nNo incident detected.")
    raise SystemExit


# ---------------------------------------------------------
# 5. COLLECT EVIDENCE
# ---------------------------------------------------------

evidence = collect_evidence(
    incident,
    drift_result,
    production_df
)


# ---------------------------------------------------------
# 6. AI ROOT CAUSE ANALYSIS
# ---------------------------------------------------------

ai_result = analyze_with_ai(
    evidence
)

ai_rca = ai_result["ai_rca"]


# ---------------------------------------------------------
# 7. POLICY DECISION
# ---------------------------------------------------------

policy_result = evaluate_action(
    incident,
    ai_rca
)


# ---------------------------------------------------------
# 8. EXECUTE HEALING
# ---------------------------------------------------------

healing_result = execute_healing(
    policy_result
)


# ---------------------------------------------------------
# 9. VERIFY RECOVERY
# ---------------------------------------------------------

verification_result = verify_recovery(
    healing_result,
    drift_result
)


# ---------------------------------------------------------
# FINAL PIPELINE OUTPUT
# ---------------------------------------------------------

print("\n==============================================")
print("       SENTINELML AI SELF-HEALING PIPELINE")
print("==============================================")

print("\n[1] DRIFT")
print(json.dumps(
    drift_result,
    indent=4,
    default=str
))

print("\n[2] INCIDENT")
print(json.dumps(
    incident,
    indent=4,
    default=str
))

print("\n[3] EVIDENCE")
print(json.dumps(
    evidence,
    indent=4,
    default=str
))

print("\n[4] AI RCA")
print(json.dumps(
    ai_result,
    indent=4,
    default=str
))

print("\n[5] POLICY")
print(json.dumps(
    policy_result,
    indent=4,
    default=str
))

print("\n[6] HEALING")
print(json.dumps(
    healing_result,
    indent=4,
    default=str
))

print("\n[7] VERIFICATION")
print(json.dumps(
    verification_result,
    indent=4,
    default=str
))

print("\n==============================================")
print("              PIPELINE COMPLETE")
print("==============================================")