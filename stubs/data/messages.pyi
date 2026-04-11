from typing import Any, Callable
from datetime import datetime

import anyio

from nautilus_trader.model.enums import BookType
from nautilus_trader.core.message import Command, Request, Response
from nautilus_trader.core.uuid import UUID4
from nautilus_trader.model.data import BarType, DataType
from nautilus_trader.model.identifiers import ClientId, InstrumentId, Venue


class DataCommand(Command):
    """
    The base class for all data commands.

    Parameters
    ----------
    data_type : type
        The data type for the command.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the command.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """
    def __init__(
        self,
        data_type: DataType,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeData(DataCommand):
    """
    Represents a command to subscribe to data.

    Parameters
    ----------
    data_type : type
        The data type for the subscription.
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        data_type: DataType,
        instrument_id: InstrumentId | None,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def to_request(
        self,
        start: datetime | None,
        end: datetime | None,
        callback: Callable[[Any], None] | None,
    ) -> RequestData: ...


class SubscribeInstruments(SubscribeData):
    """
    Represents a command to subscribe to all instruments of a venue.

    Parameters
    ----------
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def to_request(
        self,
        start: datetime | None,
        end: datetime | None,
        callback: Callable[[Any], None] | None,
    ) -> RequestInstruments: ...


class SubscribeInstrument(SubscribeData):
    """
    Represents a command to subscribe to an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeOrderBook(SubscribeData):
    """
    Represents a command to subscribe to order book deltas for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    data_type : DataType, {``OrderBookDeltas``, ``OrderBookDepth10``}
        The data type for book updates.
    book_type : BookType
        The order book type.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    depth : int, optional, default 0
        The maximum depth for the subscription.
    managed: bool, optional, default True
        If an order book should be managed by the data engine based on the subscribed feed.
    interval_ms : int, default 0 (no interval snapshots)
        The interval (milliseconds) between snapshots.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).
 ValueError
        If `interval_ms` is negative (< 0).
    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        book_data_type: type,
        book_type: BookType,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        depth: int = 0,
        managed: bool = True,
        interval_ms: int = 0,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def to_request(
        self,
        start: datetime | None,
        end: datetime | None,
        callback: Callable[[Any], None] | None,
    ) -> RequestOrderBookDepth | RequestOrderBookDeltas: ...


class SubscribeQuoteTicks(SubscribeData):
    """
    Represents a command to subscribe to quote ticks.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def to_request(
        self,
        start: datetime | None,
        end: datetime | None,
        callback: Callable[[Any], None] | None
    ) -> RequestQuoteTicks: ...


class SubscribeTradeTicks(SubscribeData):
    """
    Represents a command to subscribe to trade ticks.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def to_request(
        self,
        start: datetime | None,
        end: datetime | None,
        callback: Callable[[Any], None] | None,
    ) -> RequestTradeTicks: ...


class SubscribeMarkPrices(SubscribeData):
    """
    Represents a command to subscribe to mark prices.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeIndexPrices(SubscribeData):
    """
    Represents a command to subscribe to index prices.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeFundingRates(SubscribeData):
    """
    Represents a command to subscribe to funding rates.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeBars(SubscribeData):
    """
    Represents a command to subscribe to bars for an instrument.

    Parameters
    ----------
    bar_type : BarType
        The bar type for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was    await_partial : bool
        If the bar aggregator should await the arrival of a historical partial bar prior to actively aggregating new bars.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        bar_type: BarType,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def to_request(
        self,
        start: datetime | None,
        end: datetime | None,
        callback: Callable[[Any], None] | None,
    ) -> RequestBars: ...


class SubscribeInstrumentStatus(SubscribeData):
    """
    Represents a command to subscribe to the status of an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If bothclient_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeInstrumentClose(SubscribeData):
    """
    Represents a command to subscribe to the close of an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeOptionGreeks(SubscribeData):
    """
    Represents a command to subscribe to option Greeks for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class SubscribeOptionChain(SubscribeData):
    """
    Represents a command to subscribe to an option chain.

    Parameters
    ----------
    series_id : object
        The option series ID for the subscription.
    strike_range : object
        The strike range for filtering the chain.
    snapshot_interval_ms : int, optional
        The snapshot interval in milliseconds (None for raw mode).
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    """
    series_id: object
    strike_range: object
    snapshot_interval_ms: object

    def __init__(
        self,
        series_id: object,
        strike_range: object,
        snapshot_interval_ms: object,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class UnsubscribeData(DataCommand):
    """
    Represents a command to unsubscribe to data.

    Parameters
    ----------
    data_type : type
        The data type for the subscription.
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        data_type: DataType,
        instrument_id: InstrumentId | None,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...

class UnsubscribeInstruments(UnsubscribeData):
    """
    Represents a command to unsubscribe to all instruments.

    Parameters
    ----------
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeInstrument(UnsubscribeData):
    """
    Represents a command to unsubscribe to an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeOrderBook(UnsubscribeData):
    """
    Represents a command to unsubscribe from order book updates for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    book_data_type : type, {``OrderBookDelta``, ``OrderBookDepth10``}
        The data type for book updates.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        book_data_type: type,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeQuoteTicks(UnsubscribeData):
    """
    Represents a command to unsubscribe from quote ticks for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeTradeTicks(UnsubscribeData):
    """
    Represents a command to unsubscribe from trade ticks for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeMarkPrices(UnsubscribeData):
    """
    Represents a command to unsubscribe from mark prices for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeIndexPrices(UnsubscribeData):
    """
    Represents a command to unsubscribe from index prices for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeFundingRates(UnsubscribeData):
    """
    Represents a command to unsubscribe from funding rates for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeBars(UnsubscribeData):
    """
    Represents a command to unsubscribe from bars for an instrument.

    Parameters
    ----------
    bar_type : BarType
        The bar type for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        bar_type: BarType,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeInstrumentStatus(UnsubscribeData):
    """
    Represents a command to unsubscribe from instrument status.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeInstrumentClose(UnsubscribeData):
    """
    Represents a command to unsubscribe from instrument close for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeOptionGreeks(UnsubscribeData):
    """
    Represents a command to unsubscribe from option Greeks for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class UnsubscribeOptionChain(UnsubscribeData):
    """
    Represents a command to unsubscribe from an option chain.

    Parameters
    ----------
    series_id : object
        The option series ID for the subscription.
    client_id : ClientId or ``None``
        The data client ID for the command.
    venue : Venue or ``None``
        The venue for the command.
    command_id : UUID4
        The command ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object], optional
        Additional parameters for the subscription.

    """
    series_id: object

    def __init__(
        self,
        series_id: object,
        client_id: ClientId | None,
        venue: Venue | None,
        command_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4  = None
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class RequestData(Request):
    """
    Represents a request for data.

    Parameters
    ----------
    data_type : type
        The data type for the request.
    instrument_id : InstrumentId
        The instrument ID for the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    limit : int
        The limit on the amount of data to return for the request.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        data_type: DataType,
        instrument_id: InstrumentId | None,
        start: datetime | None,
        end: datetime | None,
        limit: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestData: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestInstrument(RequestData):
    """
    Represents a request for an instrument.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    client_id : ClientId or ``None``
        The client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        start: datetime | None,
        end: datetime | None,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestInstruments(RequestData):
    """
    Represents a request for instruments.

    Parameters
    ----------
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range The inclusiveness depends on individual data client implementation.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        start: datetime | None,
        end: datetime | None,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestInstruments: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestOrderBookSnapshot(RequestData):
    """
    Represents a request for an order book snapshot.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the request.
    limit : int
        The limit on the depth of the order book snapshot (default is None).
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        limit: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class RequestOrderBookDepth(RequestData):
    """
    Represents a request for historical `OrderBookDepth10` data.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    limit : int
        The limit on the amount of depth snapshots received.
    depth : int
        The maximum depth for the order book depth data (default is 10).
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    depth: int

    def __init__(
        self,
        instrument_id: InstrumentId,
        start: datetime | None,
        end: datetime | None,
        limit: int,
        depth: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...

    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestOrderBookDepth: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestOrderBookDeltas(RequestData):
    """
    Represents a request for historical `OrderBookDeltas` data.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    limit : int
        The limit on the amount of deltas received.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        start: datetime | None,
        end: datetime | None,
        limit: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestOrderBookDeltas: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestQuoteTicks(RequestData):
    """
    Represents a request for quote ticks.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    limit : int
        The limit on the amount of quote ticks received.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        start: datetime | None,
        end: datetime | None,
        limit: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestQuoteTicks: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestTradeTicks(RequestData):
    """
    Represents a request for trade ticks.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    limit : int
        The limit on the amount of trade ticks received.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        start: datetime | None,
        end: datetime | None,
        limit: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestTradeTicks: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestBars(RequestData):
    """
    Represents a request for bars.

    Parameters
    ----------
    bar_type : BarType
        The bar type for the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    limit : int
        The limit on the amount of bars received.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
 callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        bar_type: BarType,
        start: datetime | None,
        end: datetime | None,
        limit: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestBars: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestFundingRates(RequestData):
    """
    Represents a request for funding rates.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the request.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    limit : int
        The limit on the amount of trade ticks received.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """
    def __init__(
        self,
        instrument_id: InstrumentId,
        start: datetime | None,
        end: datetime | None,
        limit: int,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestFundingRates: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestForwardPrices(RequestData):
    """
    Represents a request for forward prices for option chain ATM tracking.

    Parameters
    ----------
    underlying : str
        The underlying asset symbol.
    client_id : ClientId or ``None``
        The data client ID for the request.
    venue : Venue or ``None``
        The venue for the request.
    callback : Callable, optional
        The registered callback for the response.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    sample_instrument_id : InstrumentId, optional
        A sample instrument ID for single-instrument fast path (1 HTTP call).
    params : dict[str, object], optional
        Additional parameters for the request.
    correlation_id : UUID4, optional
        The correlation ID for the request.

    """
    underlying: str
    sample_instrument_id: InstrumentId | None

    def __init__(
        self,
        underlying: str,
        client_id: ClientId | None,
        venue: Venue | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        sample_instrument_id: InstrumentId | None = None,
        params: dict[str, Any] | None = None,
        correlation_id: UUID4 = None,
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...


class RequestJoin(RequestData):
    """
    Represents a request to join multiple data requests.

    Parameters
    ----------
    request_ids : tuple[UUID4]
        The tuple of sub-request IDs to join.
    start : datetime
        The start datetime (UTC) of request time range (inclusive).
    end : datetime
        The end datetime (UTC) of request time range.
        The inclusiveness depends on individual data client implementation.
    callback : Callable[[Any], None]
        The delegate to call with the data.
    request_id : UUID4
        The request ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    params : dict[str, object]
        Additional parameters for the request.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """

    def __init__(
        self,
        request_ids: tuple,
        start: datetime | None,
        end: datetime | None,
        callback: Callable[[Any], None] | None,
        request_id: UUID4,
        ts_init: int,
        params: dict[str, Any] | None,
        correlation_id: UUID4 = None,
    ) -> None: ...

    def with_dates(self, start: datetime, end: datetime, ts_init: int, callback: Callable[[Any], None] | None = None) -> RequestJoin:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...


class DataResponse(Response):
    """
    Represents a response with data.

    Parameters
    ----------
    client_id : ClientId or ``None``
        The data client ID of the response.
    venue : Venue or ``None``
        The venue for the response.
    data_type : type
        The data type of the response.
    data : object
        The data of the response.
    correlation_id : UUID4
        The correlation ID.
    response_id : UUID4
        The response ID.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the object was initialized.
    start : datetime
        The start datetime (UTC) of response time range (inclusive).
    end : datetime
        The end datetime (UTC) of response time range (inclusive).
    params : dict[str, object], optional
        Additional parameters for the response.

    Raises
    ------
    ValueError
        If both `client_id` and `venue` are both ``None`` (not enough routing info).

    """

    client_id: ClientId
    venue: Venue
    data_type: DataType
    data: anyio
    start: datetime
    end: datetime
    params: dict[str, Any]

    def __init__(
        self,
        client_id: ClientId | None,
        venue: Venue | None,
        data_type: DataType,
        data: Any,
        correlation_id: UUID4,
        response_id: UUID4,
        ts_init: int,
        start: datetime,
        end: datetime,
        params: dict[str, Any] | None = None
    ) -> None: ...

    def __str__(self) -> str: ...

    def __repr__(self) -> str: ...
