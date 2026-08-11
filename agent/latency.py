import time


class EndToEndLatencyTracker:
    """
    Measures: final user transcript → agent starts speaking.
    """

    def __init__(self):
        self._turn_started_at = None

    def on_user_input_transcribed(self, event) -> None:
        if event.is_final:
            self._turn_started_at = time.perf_counter()

    def on_agent_state_changed(self, event) -> None:
        if event.new_state != "speaking" or self._turn_started_at is None:
            return

        elapsed_ms = (time.perf_counter() - self._turn_started_at) * 1000
        print(f"[latency] end-to-end: {elapsed_ms:.0f} ms")

        # Reset so the same turn is not measured twice.
        self._turn_started_at = None