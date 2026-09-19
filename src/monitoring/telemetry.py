import json
from pathlib import Path
from datetime import datetime, timezone


TELEMETRY_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "predictions.jsonl"

TELEMETRY_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_prediction(
    input_data: dict,
    prediction: int,
    failure_probability: float,
    latency_ms: float,
    model_version: str
):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": input_data,
        "prediction": prediction,
        "failure_probability": failure_probability,
        "latency_ms": latency_ms,
        "model_version": model_version
    }

    with open(TELEMETRY_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")