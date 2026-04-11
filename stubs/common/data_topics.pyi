"""Provides a centralized topic cache for managing message bus topic generation and caching.

The `TopicCache` consolidates all topic generation methods and their caching dictionaries
that were previously scattered across the data engine and other components.
"""

from nautilus_trader.model.data import BarType, DataType
from nautilus_trader.model.identifiers import InstrumentId, Venue


class TopicCache:
    """Provides a centralized cache for message bus topic generation and caching.

    This class consolidates all topic generation methods and their caching dictionaries
    that were previously scattered across the data engine and other components.
    """

    def __init__(self) -> None: ...

    def get_instrument_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_instruments_topic(self, venue: Venue) -> str:
        """
        Get the topic pattern for all instruments at a venue.

        Parameters
        ----------
        venue : Venue
            The venue for the pattern.

        Returns
        -------
        str
            The topic pattern string.

        """
        ...

    def get_book_topic(self, book_data_type: type, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_deltas_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_depth_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_quotes_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_trades_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_status_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_mark_prices_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_index_prices_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_funding_rates_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_close_prices_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_snapshots_topic(self, instrument_id: InstrumentId, interval_ms: int, historical: bool = False) -> str: ...

    def get_custom_data_topic(self, data_type: DataType, instrument_id: InstrumentId | None = None, historical: bool = False) -> str: ...

    def get_bars_topic(self, bar_type: BarType, historical: bool = False) -> str: ...

    def get_signal_topic(self, name: str) -> str:
        """
        Get the topic for a signal subscription.

        Parameters
        ----------
        name : str
            The signal name.

        Returns
        -------
        str
            The topic string.

        """
        ...

    def get_option_greeks_topic(self, instrument_id: InstrumentId, historical: bool = False) -> str: ...

    def get_option_chain_topic(self, series_id_str: str) -> str: ...

    def clear_cache(self) -> None: ...