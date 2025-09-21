from typing import Callable

from nautilus_trader.cache.base import CacheFacade
from nautilus_trader.common.component import Clock, Component, MessageBus
from nautilus_trader.model.data import QuoteTick
from nautilus_trader.model.identifiers import InstrumentId


class SpreadQuoteAggregator(Component):
    """
    Provides a spread quote generator for creating synthetic quotes from component instruments.

    The generator subscribes to quotes from component instruments of a spread and generates
    averaged quotes for the spread instrument.

    Parameters
    ----------
    spread_instrument_id : InstrumentId
        The spread instrument ID to generate quotes for.
    handler : Callable[[QuoteTick], None]
        The quote handler for the generator.
    cache : CacheFacade
        The cache facade for accessing market data.
    """
    def __init__(self, spread_instrument_id: InstrumentId, handler: Callable[[QuoteTick], None], msgbus: MessageBus, cache: CacheFacade, clock: Clock, update_interval_seconds: int = 60) -> None: ...
    def stop(self) -> None: ...