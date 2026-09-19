from src.database.database import SessionLocal
from src.database.models import HealingAction


db = SessionLocal()

try:

    actions = (
        db.query(HealingAction)
        .order_by(HealingAction.id.desc())
        .limit(10)
        .all()
    )

    print("\n=== HEALING ACTION AUDIT LOG ===")

    if not actions:
        print("No healing actions found.")
        raise SystemExit

    for action in actions:

        print(f"\nID: {action.id}")
        print(f"Incident ID: {action.incident_id}")
        print(f"Action: {action.action}")
        print(f"Status: {action.status}")
        print(f"Reason: {action.reason}")
        print(f"Executed At: {action.executed_at}")

finally:
    db.close()