ALLOWED_ACTIONS = {
    "quarantine_data",
    "restart_service",
    "human_review",
}
def evaluate_action(
    incident: dict,
    ai_rca: dict
):

    incident_type = incident["incident_type"]

    recommended_action = ai_rca.get(
        "recommended_action",
        "human_review"
    )

    # =========================================================
    # SENTINELML SAFETY POLICY
    # =========================================================

    # ---------------------------------------------------------
    # DATA DRIFT POLICY
    # ---------------------------------------------------------

    if incident_type == "DATA_DRIFT":

        selected_action = "quarantine_data"

        reason = (
            "Data drift was detected, but model performance "
            "degradation is not confirmed. SentinelML policy "
            "allows data quarantine while preventing automatic "
            "model rollback."
        )


    # ---------------------------------------------------------
    # API ALERT POLICY
    # ---------------------------------------------------------

    elif incident_type == "API_ALERT":

        selected_action = "restart_service"

        reason = (
            "The SentinelML API is unhealthy or unavailable. "
            "The policy allows a controlled service restart "
            "as the first automated recovery action."
        )


    # ---------------------------------------------------------
    # UNKNOWN INCIDENT
    # ---------------------------------------------------------

    else:

        selected_action = "human_review"

        reason = (
            "Incident type is not covered by the current "
            "automated healing policy."
        )


    # =========================================================
    # FINAL SAFETY CHECK
    # =========================================================

    allowed = selected_action in ALLOWED_ACTIONS


    return {
        "incident_id": incident["incident_id"],
        "ai_recommendation": recommended_action,
        "selected_action": selected_action,
        "allowed": allowed,
        "reason": reason
    }