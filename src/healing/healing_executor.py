from datetime import datetime, timezone

from src.database.database import SessionLocal
from src.database.models import (
    HealingAction,
    QuarantinedPrediction,
    Prediction
)


def execute_healing(
    policy_result: dict,
    production_df=None
):
    db = SessionLocal()

    try:
        if not policy_result["allowed"]:
            healing_result = {
                "status": "BLOCKED",
                "action": policy_result["selected_action"],
                "message": (
                    "Healing action is not allowed "
                    "by the SentinelML policy."
                )
            }

        else:
            action = policy_result["selected_action"]

            if action == "quarantine_data":

                quarantined_count = 0

                if production_df is not None:
                    for _, row in production_df.iterrows():

                        record = QuarantinedPrediction(
                            incident_id=policy_result["incident_id"],
                            machine_type=row.get("Type"),
                            air_temperature=row.get(
                                "Air temperature [K]"
                            ),
                            process_temperature=row.get(
                                "Process temperature [K]"
                            ),
                            rotational_speed=row.get(
                                "Rotational speed [rpm]"
                            ),
                            torque=row.get("Torque [Nm]"),
                            tool_wear=row.get("Tool wear [min]"),
                            prediction=row.get("prediction"),
                            failure_probability=row.get(
                                "failure_probability"
                            ),
                            latency_ms=row.get("latency_ms"),
                            model_version=row.get(
                                "model_version"
                            ),
                            reason=(
                                "Production data affected by "
                                "detected data drift."
                            )
                        )

                        db.add(record)
                        quarantined_count += 1

                db.commit()

                healing_result = {
                    "status": "EXECUTED",
                    "action": action,
                    "executed_at": (
                        datetime.now(timezone.utc).isoformat()
                    ),
                    "quarantined_records": quarantined_count,
                    "message": (
                        f"{quarantined_count} production "
                        "records were copied to quarantine "
                        "for investigation."
                    )
                }

            elif action == "restart_service":

                healing_result = {
                    "status": "EXECUTED",
                    "action": action,
                    "executed_at": (
                        datetime.now(timezone.utc).isoformat()
                    ),
                    "message": (
                        "Controlled service restart action "
                        "was approved and simulated. "
                        "Actual service restart is not "
                        "executed in the current MVP."
                    )
                }

            else:

                healing_result = {
                    "status": "NOT_EXECUTED",
                    "action": action,
                    "message": (
                        "No executor is configured "
                        "for this healing action."
                    )
                }

        audit_record = HealingAction(
            incident_id=policy_result["incident_id"],
            action=healing_result["action"],
            status=healing_result["status"],
            reason=policy_result["reason"]
        )

        db.add(audit_record)
        db.commit()

        return healing_result

    finally:
        db.close()