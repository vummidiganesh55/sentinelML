from src.healing.verification import verify_recovery


# =========================================================
# SIMULATED SUCCESSFUL RESTART
# =========================================================

healing_result = {
    "status": "EXECUTED",
    "action": "restart_service"
}


result = verify_recovery(
    healing_result
)


print("\n====================================")
print("    SENTINELML RECOVERY TEST")
print("====================================")

print(result)