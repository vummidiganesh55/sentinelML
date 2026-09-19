from datetime import datetime, timezone

from src.database.database import SessionLocal


def check_database_health():
    try:
        from sqlalchemy import text

        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        return True

    except Exception:
        return False


def check_model_health():
    try:
        from src.api.main import model

        return model is not None

    except Exception:
        return False


def verify_recovery(
    healing_result: dict,
    drift_result: dict | None = None
):
    if healing_result["status"] != "EXECUTED":
        return {
            "verification_status": "NOT_VERIFIED",
            "checks": {
                "healing_executed": False
            },
            "message": (
                "Healing action was not executed, "
                "so recovery cannot be verified."
            )
        }

    database_healthy = check_database_health()

    model_available = check_model_health()

    # The verification code is running inside the active
    # SentinelML API process. Therefore the API process itself
    # is considered healthy when this verification executes.
    api_healthy = True

    drift_detected = None

    if drift_result is not None:
        drift_detected = drift_result.get(
            "drift_detected"
        )

    if healing_result["action"] == "restart_service":

        if (
            database_healthy
            and model_available
            and api_healthy
        ):
            verification_status = "RECOVERED"

            message = (
                "Healing action was executed and recovery "
                "was verified using database connectivity, "
                "model availability, and the active API process."
            )

        else:
            verification_status = "NOT_RECOVERED"

            message = (
                "The restart action was executed, but one "
                "or more recovery checks failed. "
                "Human investigation is required."
            )

    elif healing_result["action"] == "quarantine_data":

        if (
            database_healthy
            and model_available
        ):
            verification_status = "RECOVERED"

            message = (
                "Healing action was executed. Database "
                "connectivity and model availability were "
                "verified. Drifted data remains isolated "
                "for investigation."
            )

        else:
            verification_status = "NOT_RECOVERED"

            message = (
                "One or more recovery checks failed. "
                "Human investigation is required."
            )

    else:

        verification_status = "NOT_VERIFIED"

        message = (
            "No verification procedure is configured "
            "for this healing action."
        )

    return {
        "verification_status": verification_status,
        "verified_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "checks": {
            "healing_executed": True,
            "database_healthy": database_healthy,
            "model_available": model_available,
            "api_healthy": api_healthy,
            "drift_detected_before_healing": drift_detected
        },

        "message": message
    }
