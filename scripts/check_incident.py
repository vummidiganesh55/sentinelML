from src.database.database import SessionLocal
from src.database.models import Incident


db = SessionLocal()

try:
    incidents = (
        db.query(Incident)
        .order_by(Incident.id.desc())
        .limit(5)
        .all()
    )

    print("\n=== INCIDENT DATABASE VERIFICATION ===")

    for incident in incidents:
        print({
            "id": incident.id,
            "incident_id": incident.incident_id,
            "type": incident.incident_type,
            "severity": incident.severity,
            "status": incident.status,
            "reason": incident.reason,
            "detected_at": str(incident.detected_at),
            "resolved_at": str(incident.resolved_at)
        })

finally:
    db.close()