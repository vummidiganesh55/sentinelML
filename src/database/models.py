from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime, timezone

from src.database.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    timestamp = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    machine_type = Column(String(10))

    air_temperature = Column(Float)
    process_temperature = Column(Float)
    rotational_speed = Column(Integer)
    torque = Column(Float)
    tool_wear = Column(Integer)

    prediction = Column(Integer)
    failure_probability = Column(Float)
    latency_ms = Column(Float)

    model_version = Column(String(20))
class HealingAction(Base):
    __tablename__ = "healing_actions"

    id = Column(Integer, primary_key=True, index=True)

    incident_id = Column(String(100), index=True)

    action = Column(String(50))

    status = Column(String(30))

    reason = Column(String(500))

    executed_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    incident_id = Column(
        String(100),
        unique=True,
        index=True
    )

    incident_type = Column(String(50))

    severity = Column(String(30))

    status = Column(String(30))

    reason = Column(String(500))

    affected_features = Column(String(1000))

    detected_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    resolved_at = Column(
        DateTime,
        nullable=True
    )
class QuarantinedPrediction(Base):
    __tablename__ = "quarantined_predictions"

    id = Column(Integer, primary_key=True, index=True)

    incident_id = Column(
        String(100),
        nullable=False,
        index=True
    )

    machine_type = Column(String(10))

    air_temperature = Column(Float)
    process_temperature = Column(Float)
    rotational_speed = Column(Integer)
    torque = Column(Float)
    tool_wear = Column(Integer)

    prediction = Column(Integer)
    failure_probability = Column(Float)
    latency_ms = Column(Float)

    model_version = Column(String(20))

    reason = Column(String(500), nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )