from sqlalchemy import func

from src.database.database import SessionLocal
from src.database.models import QuarantinedPrediction


db = SessionLocal()

try:
    total = db.query(
        func.count(QuarantinedPrediction.id)
    ).scalar()

    latest = (
        db.query(QuarantinedPrediction)
        .order_by(QuarantinedPrediction.id.desc())
        .limit(5)
        .all()
    )

    print("\n=== QUARANTINE VERIFICATION ===")

    print("Total quarantined records:", total)

    print("\nLatest 5 records:")

    for record in latest:
        print({
            "id": record.id,
            "incident_id": record.incident_id,
            "machine_type": record.machine_type,
            "torque": record.torque,
            "prediction": record.prediction,
            "reason": record.reason
        })

finally:
    db.close()