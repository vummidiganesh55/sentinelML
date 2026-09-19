import json
import requests
import os

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

MODEL_NAME = "qwen2.5-coder:3b"


def analyze_with_ai(evidence: dict):

    prompt = f"""
You are an ML Operations Root Cause Analysis assistant.

Analyze the SentinelML production incident using ONLY the evidence provided.

IMPORTANT RULES:

1. Use ONLY the evidence provided below.
2. Do not invent facts, metrics, labels, or missing evidence.
3. Use the provided evidence fields exactly.
4. Data drift is an observed input-distribution change.
5. Data drift alone does NOT prove model performance degradation.
6. If performance_evidence_available is false, you MUST NOT say that
   model performance has changed, decreased, degraded, or been affected.
7. Distinguish observed evidence from root-cause hypotheses.
8. A root-cause hypothesis must describe only what can reasonably
   be inferred from the supplied evidence.
9. Do not directly execute any action.
10. Return ONLY valid JSON.
11. Do not use markdown or code fences.

Required JSON format:

{{
    "root_cause_hypothesis": "short explanation based only on available evidence",
    "evidence": [
        "observed evidence 1",
        "observed evidence 2"
    ],
    "confidence": "LOW",
    "recommended_action": "safe recommended action"
}}

EVIDENCE:

{json.dumps(evidence, indent=2)}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    ai_text = result["response"].strip()

    if ai_text.startswith("```"):

        ai_text = ai_text.replace(
            "```json",
            "",
            1
        )

        ai_text = ai_text.replace(
            "```",
            "",
            1
        )

        ai_text = ai_text.strip()

    try:

        structured_rca = json.loads(
            ai_text
        )

    except json.JSONDecodeError:

        structured_rca = {
            "root_cause_hypothesis": (
                "AI returned an unstructured response."
            ),
            "evidence": [],
            "confidence": "LOW",
            "recommended_action": "human_review",
            "raw_response": ai_text
        }

    performance_available = (
        evidence["model"][
            "performance_evidence_available"
        ]
    )

    incident_type = (
        evidence["incident"][
            "incident_type"
        ]
    )

    if incident_type == "API_ALERT":

        structured_rca[
            "root_cause_hypothesis"
        ] = (
            "The SentinelML API is currently unavailable "
            "or unhealthy according to the received API "
            "alert. The available evidence does not identify "
            "the underlying infrastructure or application cause."
        )

        structured_rca["evidence"] = [

            (
                f"API alert "
                f"'{evidence['api_alert_evidence']['alert_name']}' "
                f"is in "
                f"{evidence['api_alert_evidence']['alert_status']} "
                f"state."
            ),

            (
                f"Alert severity is "
                f"{evidence['api_alert_evidence']['severity']}."
            )
        ]

        structured_rca["confidence"] = "LOW"

        structured_rca[
            "recommended_action"
        ] = (
            "Check API health, application logs, container "
            "status, and infrastructure connectivity before "
            "performing an automated recovery action."
        )

        structured_rca[
            "safety_validation"
        ] = "API_CAUSE_NOT_CONFIRMED"

    elif not performance_available:

        structured_rca[
            "root_cause_hypothesis"
        ] = (
            "Input data drift was observed in the affected "
            "production features. The available evidence does "
            "not establish that model performance has degraded."
        )

        structured_rca["evidence"] = [

            *structured_rca.get(
                "evidence",
                []
            ),

            (
                "Production ground-truth labels are unavailable. "
                "Therefore model performance degradation cannot "
                "be confirmed."
            )
        ]

        structured_rca["confidence"] = "LOW"

        structured_rca[
            "recommended_action"
        ] = (
            "Continue monitoring production data and collect "
            "ground-truth labels before making decisions about "
            "model performance, retraining, or rollback."
        )

        structured_rca[
            "safety_validation"
        ] = "PERFORMANCE_CLAIM_BLOCKED"

    return {
        "incident_id": evidence[
            "incident"
        ][
            "incident_id"
        ],
        "ai_rca": structured_rca
    }