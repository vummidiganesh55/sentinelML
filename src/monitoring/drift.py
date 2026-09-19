import pandas as pd
from pathlib import Path


REFERENCE_FILE = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "reference"
    / "reference_data.csv"
)


def calculate_drift(reference_df, production_df, threshold=0.20):

    numerical_features = [
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]

    drift_results = {}

    for feature in numerical_features:

        reference_mean = reference_df[feature].mean()
        production_mean = production_df[feature].mean()

        if reference_mean != 0:
            change = abs(
                production_mean - reference_mean
            ) / abs(reference_mean)
        else:
            change = 0

        drift_results[feature] = {
            "reference_mean": round(reference_mean, 4),
            "production_mean": round(production_mean, 4),
            "relative_change": round(change, 4),
            "drift_detected": change > threshold
        }

    overall_drift = any(
        result["drift_detected"]
        for result in drift_results.values()
    )

    return {
        "drift_detected": overall_drift,
        "features": drift_results
    }