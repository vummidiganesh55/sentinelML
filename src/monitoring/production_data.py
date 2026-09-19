import pandas as pd

from src.database.database import SessionLocal
from src.database.models import Prediction


def get_production_data(limit=1000):

    db = SessionLocal()

    try:
        predictions = (
            db.query(Prediction)
            .order_by(Prediction.id.desc())
            .limit(limit)
            .all()
        )

        records = []

        for prediction in predictions:
            records.append({
                "Type": prediction.machine_type,
                "Air temperature [K]": prediction.air_temperature,
                "Process temperature [K]": prediction.process_temperature,
                "Rotational speed [rpm]": prediction.rotational_speed,
                "Torque [Nm]": prediction.torque,
                "Tool wear [min]": prediction.tool_wear,
                "prediction": prediction.prediction,
                "failure_probability": prediction.failure_probability,
                "latency_ms": prediction.latency_ms,
                "model_version": prediction.model_version
            })

        return pd.DataFrame(records)

    finally:
        db.close()