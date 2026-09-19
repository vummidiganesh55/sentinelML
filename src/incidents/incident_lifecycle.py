from datetime import datetime, timezone

from src.database.database import SessionLocal
from src.database.models import Incident


def update_incident_status(
    incident_id: str,
    status: str
):
    db = SessionLocal()

    try:
        incident = (
            db.query(Incident)
            .filter(
                Incident.incident_id == incident_id
            )
            .first()
        )

        if incident is None:
            return False

        incident.status = status

        if status in {"RECOVERED", "FAILED"}:
            incident.resolved_at = datetime.now(
                timezone.utc
            )

        db.commit()

        return True

    finally:
        db.close()