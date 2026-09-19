import json

from src.rca.evidence_collector import collect_evidence
from src.rca.ai_rca_engine import analyze_with_ai


incident = {
    "incident_id": "test-api-001",
    "incident_type": "API_ALERT",
    "severity": "critical",
    "status": "OPEN",
    "reason": "SentinelMLAPIDown",
    "affected_features": []
}


evidence = collect_evidence(
    incident
)


ai_result = analyze_with_ai(
    evidence
)


print("\n==============================================")
print("        SENTINELML API ALERT AI RCA")
print("==============================================")

print(
    json.dumps(
        ai_result,
        indent=4
    )
)