import time
from contextlib import contextmanager


@contextmanager
def measure_latency(label: str):
    start = time.perf_counter()

    try:
        yield

    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"[latency] {label}: {elapsed_ms:.0f} ms")