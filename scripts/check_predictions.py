from sqlalchemy import select

from src.database.database import SessionLocal
from src.database.models import Prediction


db = SessionLocal()

try:
    predictions = db.execute(
        select(Prediction)
        .order_by(Prediction.id.desc())
        .limit(5)
    ).scalars().all()

    print("\n=== RECENT PREDICTIONS ===")

    for prediction in predictions:
        print(
            f"ID: {prediction.id} | "
            f"Type: {prediction.machine_type} | "
            f"Prediction: {prediction.prediction} | "
            f"Failure Probability: {prediction.failure_probability} | "
            f"Latency: {prediction.latency_ms} ms | "
            f"Model: {prediction.model_version}"
        )

finally:
    db.close()