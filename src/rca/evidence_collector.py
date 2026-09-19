from datetime import datetime, timezone


def collect_evidence(
    incident: dict,
    drift_result=None,
    production_df=None
):

    # =========================================================
    # API ALERT EVIDENCE
    # =========================================================

    if incident["incident_type"] == "API_ALERT":

        evidence = {
            "evidence_timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "incident": {
                "incident_id": incident["incident_id"],
                "incident_type": incident["incident_type"],
                "severity": incident["severity"],
                "status": incident["status"],
                "reason": incident["reason"],
                "affected_features": incident.get(
                    "affected_features",
                    []
                )
            },

            "api_alert_evidence": {
                "alert_name": incident["reason"],
                "alert_status": incident["status"],
                "severity": incident["severity"]
            },

            "model": {
                "model_version": "v1",
                "performance_evidence_available": False,
                "performance_note": (
                    "The API alert does not provide production "
                    "ground-truth labels. Model performance "
                    "degradation cannot be confirmed from this "
                    "evidence alone."
                )
            }
        }

        return evidence


    # =========================================================
    # DATA DRIFT EVIDENCE
    # =========================================================

    drifted_features = []

    for feature, result in drift_result["features"].items():

        if result["drift_detected"]:

            reference_mean = float(
                result["reference_mean"]
            )

            production_mean = float(
                result["production_mean"]
            )

            if production_mean > reference_mean:
                direction = "increased"

            elif production_mean < reference_mean:
                direction = "decreased"

            else:
                direction = "unchanged"

            drifted_features.append({
                "feature": feature,
                "reference_mean": reference_mean,
                "production_mean": production_mean,
                "relative_change": float(
                    result["relative_change"]
                ),
                "direction": direction
            })


    production_summary = {
        "number_of_predictions": len(
            production_df
        ),

        "failure_predictions": int(
            (
                production_df.get(
                    "prediction",
                    []
                ) == 1
            ).sum()
        )
        if "prediction" in production_df.columns
        else 0
    }


    evidence = {

        "evidence_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "incident": {
            "incident_id": incident["incident_id"],
            "incident_type": incident["incident_type"],
            "severity": incident["severity"],
            "status": incident["status"],
            "reason": incident["reason"],
            "affected_features": incident[
                "affected_features"
            ]
        },

        "drift_evidence": {
            "drift_detected": drift_result[
                "drift_detected"
            ],

            "drifted_features": drifted_features
        },

        "production_summary": production_summary,

        "model": {
            "model_version": "v1",
            "performance_evidence_available": False,
            "performance_note": (
                "Production ground-truth labels are not "
                "currently available. Model performance "
                "degradation cannot be confirmed from the "
                "available evidence."
            )
        }
    }

    return evidence