from src.database.database import engine, Base
from src.database.models import (
    Prediction,
    HealingAction,
    Incident,
    QuarantinedPrediction
)

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")