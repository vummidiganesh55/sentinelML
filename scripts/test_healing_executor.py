from src.healing.healing_executor import execute_healing


# =========================================================
# TEST API RESTART ACTION
# =========================================================

policy_result = {
    "incident_id": "test-api-healing-001",
    "ai_recommendation": "human_review",
    "selected_action": "restart_service",
    "allowed": True,
    "reason": (
        "API alert detected. "
        "Controlled service restart is allowed by policy."
    )
}


result = execute_healing(policy_result)


print("\n====================================")
print("      SENTINELML HEALING TEST")
print("====================================")

print(result)