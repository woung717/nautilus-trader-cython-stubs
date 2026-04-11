from decimal import Decimal
from typing import Any

from nautilus_trader.model.enums import AssetClass
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity


class PerpetualContract(Instrument):
    """
    Represents a perpetual contract instrument (perpetual swap).

    Supports perpetuals on any asset class including FX, equities,
    commodities, indexes, and cryptocurrencies.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the instrument.
    raw_symbol : Symbol
        The raw/local/native symbol for the instrument, assigned by the venue.
    underlying : str
        The underlying asset identifier (e.g., "EURUSD", "NVDA", "GC").
    asset_class : AssetClass
        The asset class of the perpetual contract.
    quote_currency : Currency
        The quote currency.
    settlement_currency : Currency
        The settlement currency.
    is_inverse : bool
        If the instrument costing is inverse (quantity expressed in quote currency units).
    price_precision : int
        The price decimal precision.
    size_precision : int
        The trading size decimal precision.
    price_increment : Price
        The minimum price increment (tick size).
    size_increment : Quantity
        The minimum size increment.
    ts_event : int
        UNIX timestamp (nanoseconds) when the data event occurred.
    ts_init : int
        UNIX timestamp (nanoseconds) when the data object was initialized.
    base_currency : Currency, optional
        The base currency (for FX/crypto underlyings).
    multiplier : Quantity, default 1
        The contract multiplier.
    lot_size : Quantity, default 1
        The rounded lot unit size (standard/board).
    max_quantity : Quantity, optional
        The maximum allowable order quantity.
    min_quantity : Quantity, optional
        The minimum allowable order quantity.
    max_notional : Money, optional
        The maximum allowable order notional value.
    min_notional : Money, optional
        The minimum allowable order notional value.
    max_price : Price, optional
        The maximum allowable quoted price.
    min_price : Price, optional
        The minimum allowable quoted price.
    margin_init : Decimal, optional
        The initial (order) margin requirement in percentage of order value.
    margin_maint : Decimal, optional
        The maintenance (position) margin in percentage of position value.
    maker_fee : Decimal, optional
        The fee rate for liquidity makers as a percentage of order value.
    taker_fee : Decimal, optional
        The fee rate for liquidity takers as a percentage of order value.
    tick_scheme_name : str, optional
        The name of the tick scheme.
    info : dict[str, object], optional
        The additional instrument information.

    """

    def __init__(
        self,
        instrument_id: InstrumentId,
        raw_symbol: Symbol,
        underlying: str,
        asset_class: AssetClass,
        quote_currency: Currency,
        settlement_currency: Currency,
        is_inverse: bool,
        price_precision: int,
        size_precision: int,
        price_increment: Price,
        size_increment: Quantity,
        ts_event: int,
        ts_init: int,
        base_currency: Currency | None = None,
        multiplier: Quantity = ...,
        lot_size: Quantity = ...,
        max_quantity: Quantity | None = None,
        min_quantity: Quantity | None = None,
        max_notional: Money | None = None,
        min_notional: Money | None = None,
        max_price: Price | None = None,
        min_price: Price | None = None,
        margin_init: Decimal | None = None,
        margin_maint: Decimal | None = None,
        maker_fee: Decimal | None = None,
        taker_fee: Decimal | None = None,
        tick_scheme_name: str | None = None,
        info: dict[str, Any] | None = None,
    ) -> None: ...

    underlying: str
    base_currency: Currency | None
    settlement_currency: Currency
    is_quanto: bool

    @staticmethod
    def from_dict(values: dict[str, Any]) -> PerpetualContract:
        """
        Return an instrument from the given initialization values.

        Parameters
        ----------
        values : dict[str, object]
            The values to initialize the instrument with.

        Returns
        -------
        PerpetualContract

        """
        ...

    @staticmethod
    def to_dict(obj: PerpetualContract) -> dict[str, Any]:
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """
        ...

    @staticmethod
    def from_pyo3(pyo3_instrument: Any) -> PerpetualContract: ...

    def get_base_currency(self) -> Currency | None: ...

    def get_settlement_currency(self) -> Currency: ...

    def get_cost_currency(self) -> Currency: ...

    def notional_value(
        self,
        quantity: Quantity,
        price: Price,
        use_quote_for_inverse: bool = False,
        target_currency: Currency | None = None,
        conversion_price: Price | None = None,
    ) -> Money: ...