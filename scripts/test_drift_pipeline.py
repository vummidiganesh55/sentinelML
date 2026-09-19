import pandas as pd

from src.monitoring.drift import (
    calculate_drift,
    REFERENCE_FILE
)

from src.incidents.incident_engine import (
    create_incident
)

from src.rca.evidence_collector import (
    collect_evidence
)

from src.rca.ai_rca_engine import (
    analyze_with_ai
)

from src.healing.policy_engine import (
    evaluate_action
)

from src.healing.healing_executor import (
    execute_healing
)

from src.healing.verification import (
    verify_recovery
)
from src.incidents.incident_lifecycle import (
    update_incident_status
)

# =========================================================
# 1. LOAD REFERENCE DATA
# =========================================================

reference_df = pd.read_csv(
    REFERENCE_FILE
)


# =========================================================
# 2. SIMULATE PRODUCTION DRIFT
# =========================================================

production_df = reference_df.copy()

production_df["Torque [Nm]"] = (
    production_df["Torque [Nm]"] * 1.50
)


# =========================================================
# 3. DETECT DRIFT
# =========================================================

drift_result = calculate_drift(
    reference_df,
    production_df
)

print("\n=== DRIFT RESULT ===")
print(drift_result)


# =========================================================
# 4. CREATE INCIDENT
# =========================================================

incident = create_incident(
    drift_result
)
update_incident_status(
    incident["incident_id"],
    "HEALING"
)
incident["status"] = "HEALING"
print("\n=== INCIDENT STATUS ===")
print("Incident status: HEALING")
print("\n=== INCIDENT ===")
print(incident)


if incident is None:
    print("No incident created.")
    raise SystemExit


# =========================================================
# 5. COLLECT EVIDENCE
# =========================================================

evidence = collect_evidence(
    incident=incident,
    drift_result=drift_result,
    production_df=production_df
)

print("\n=== EVIDENCE ===")
print(evidence)


# =========================================================
# 6. AI ROOT CAUSE ANALYSIS
# =========================================================

ai_result = analyze_with_ai(
    evidence
)

ai_rca = ai_result["ai_rca"]

print("\n=== AI RCA ===")
print(ai_rca)


# =========================================================
# 7. POLICY ENGINE
# =========================================================

policy_result = evaluate_action(
    incident,
    ai_rca
)

print("\n=== POLICY RESULT ===")
print(policy_result)


# =========================================================
# 8. SELF-HEALING
# =========================================================

healing_result = execute_healing(
    policy_result,
    production_df=production_df
)

print("\n=== HEALING RESULT ===")
print(healing_result)


# =========================================================
# 9. VERIFY RECOVERY
# =========================================================

verification_result = verify_recovery(
    healing_result,
    drift_result
)
if verification_result["verification_status"] == "RECOVERED":
    update_incident_status(
        incident["incident_id"],
        "RECOVERED"
    )
else:
    update_incident_status(
        incident["incident_id"],
        "FAILED"
    )
    incident["status"] = "FAILED"

print("\n=== INCIDENT LIFECYCLE ===")
print(
    "Final status:",
    verification_result["verification_status"]
)
print("\n=== VERIFICATION ===")
print(verification_result)


# =========================================================
# 10. FINAL RESULT
# =========================================================

print("\n======================================")
print("      DATA DRIFT PIPELINE COMPLETE")
print("======================================")

print(
    "Drift:",
    drift_result["drift_detected"]
)

print(
    "Incident:",
    incident["incident_type"]
)

print(
    "AI RCA:",
    ai_rca.get(
        "root_cause_hypothesis"
    )
)

print(
    "Policy:",
    policy_result["selected_action"]
)

print(
    "Healing:",
    healing_result["status"]
)

print(
    "Verification:",
    verification_result[
        "verification_status"
    ]
)