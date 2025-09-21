from typing import Any

from nautilus_trader.core.nautilus_pyo3 import NANOSECONDS_IN_MILLISECOND

class LatencyModel:
    """
    Provides a latency model for simulated exchange message I/O.

    Parameters
    ----------
    base_latency_nanos : int, default 1_000_000_000
        The base latency (nanoseconds) for the model.
    insert_latency_nanos : int, default 0
        The order insert latency (nanoseconds) for the model.
    update_latency_nanos : int, default 0
        The order update latency (nanoseconds) for the model.
    cancel_latency_nanos : int, default 0
        The order cancel latency (nanoseconds) for the model.
    config : FillModelConfig, optional
        The configuration for the model.

    Raises
    ------
    ValueError
        If `base_latency_nanos` is negative (< 0).
    ValueError
        If `insert_latency_nanos` is negative (< 0).
    ValueError
        If `update_latency_nanos` is negative (< 0).
    ValueError
        If `cancel_latency_nanos` is negative (< 0).
    """
    def __init__(
        self,
        base_latency_nanos: int = NANOSECONDS_IN_MILLISECOND,
        insert_latency_nanos: int = 0,
        update_latency_nanos: int = 0,
        cancel_latency_nanos: int = 0,
        config: Any | None = None,
    ) -> None: ...

    base_latency_nanos: int
    insert_latency_nanos: int
    update_latency_nanos: int
    cancel_latency_nanos: int