from src.healing.policy_engine import evaluate_action


# =========================================================
# TEST 1: DATA DRIFT
# =========================================================

drift_incident = {
    "incident_id": "test-drift-001",
    "incident_type": "DATA_DRIFT",
    "reason": "Production data drift detected"
}

drift_rca = {
    "recommended_action": "rollback_model"
}

drift_result = evaluate_action(
    drift_incident,
    drift_rca
)

print("\n====================================")
print("       DATA DRIFT POLICY TEST")
print("====================================")

print(drift_result)


# =========================================================
# TEST 2: API ALERT
# =========================================================

api_incident = {
    "incident_id": "test-api-001",
    "incident_type": "API_ALERT",
    "reason": "SentinelMLAPIDown"
}

api_rca = {
    "recommended_action": "human_review"
}

api_result = evaluate_action(
    api_incident,
    api_rca
)

print("\n====================================")
print("       API ALERT POLICY TEST")
print("====================================")

print(api_result)