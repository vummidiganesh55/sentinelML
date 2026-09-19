from importlib import import_module


try:
    _prometheus_client = import_module("prometheus_client")
    Counter = _prometheus_client.Counter
    Histogram = _prometheus_client.Histogram
except ImportError:
    class _Metric:
        """Fallback metric used when prometheus-client is not installed."""

        def __init__(self, *_args, **_kwargs):
            pass

        def inc(self, *_args, **_kwargs):
            pass

        def observe(self, *_args, **_kwargs):
            pass

    Counter = Histogram = _Metric


# Total prediction requests
prediction_requests = Counter(
    "sentinelml_prediction_requests_total",
    "Total number of prediction requests"
)


# Total prediction failures
prediction_failures = Counter(
    "sentinelml_prediction_failures_total",
    "Total number of predictions classified as machine failure"
)


# API errors
api_errors = Counter(
    "sentinelml_api_errors_total",
    "Total number of API errors"
)


# Prediction latency
prediction_latency = Histogram(
    "sentinelml_prediction_latency_seconds",
    "Prediction API latency in seconds"
)