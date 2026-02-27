#!/usr/bin/env python3
"""Measure p95 latency (ms) for realtime-fraud-detection. Run from kpi_scripts with fraud repo on PYTHONPATH."""
import sys
import os
import time
import statistics

# Add fraud repo so we can import
FRAUD_REPO = os.path.join(os.path.dirname(__file__), "..", "realtime-fraud-detection")
sys.path.insert(0, FRAUD_REPO)

def main():
    try:
        from src.streaming_features import RealTimeFeatureEngine
        from src.utils.validation_utils import sanitize_event
    except Exception as e:
        print(f"IMPORT_ERROR: {e}", file=sys.stderr)
        print("P95_LAT_MS=0  # run from shipped or set PYTHONPATH", file=sys.stderr)
        return 1

    engine = RealTimeFeatureEngine()
    # Minimal valid event (from api.py TransactionEvent)
    event = {
        "user_id": "bench-user",
        "transaction_id": "tx-001",
        "amount": 25.0,
        "timestamp": "2024-01-15T12:00:00Z",
        "merchant": "Test",
    }
    from src.utils.time_utils import parse_timestamp
    event["timestamp_unix"] = parse_timestamp(event["timestamp"])

    # Include score calc like api.py
    def _score(features):
        w = {'transaction_velocity_1h': 0.2, 'amount_zscore': 0.25, 'location_anomaly': 0.3, 'time_pattern_score': 0.15, 'merchant_diversity': -0.05, 'payment_method_consistency': -0.05}
        s = sum(features.get(k, 0) * v for k, v in w.items())
        return 1 / (1 + __import__("math").exp(-s))
    N = 50
    latencies = []
    for _ in range(N):
        t0 = time.perf_counter()
        engine.process_event(event.copy())
        feats = engine.get_features("bench-user")
        _score(feats)
        latencies.append((time.perf_counter() - t0) * 1000)

    latencies.sort()
    p50 = statistics.median(latencies)
    p95 = latencies[int(0.95 * (N - 1))] if N else 0
    # Sub-ms possible; report 2 decimals
    print(f"P95_LAT_MS={p95:.2f}")
    print(f"p50={p50:.2f} ms  p95={p95:.2f} ms  (N={N})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
