def analyze_incident(incident: dict, drift_result: dict):

    affected_features = incident["affected_features"]

    evidence = []

    for feature in affected_features:
        result = drift_result["features"][feature]

        evidence.append({
            "feature": feature,
            "reference_mean": float(result["reference_mean"]),
            "production_mean": float(result["production_mean"]),
            "relative_change": float(result["relative_change"])
        })

    if len(affected_features) >= 3:
        hypothesis = (
            "Multiple production features have shifted significantly "
            "from the training reference distribution."
        )
        confidence = "HIGH"
    else:
        hypothesis = (
            "A limited number of production features have shifted "
            "from the training reference distribution."
        )
        confidence = "MEDIUM"

    return {
        "incident_id": incident["incident_id"],
        "root_cause_hypothesis": hypothesis,
        "evidence": evidence,
        "confidence": confidence,
        "recommended_action": (
            "Investigate sensor calibration and production "
            "conditions before taking automated recovery action."
        )
    }