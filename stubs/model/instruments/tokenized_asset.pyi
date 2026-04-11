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


class TokenizedAsset(Instrument):
    """
    Represents a tokenized real-world asset traded as a pair on a crypto venue.

    Covers tokenized equities, ETFs, commodities, and other asset classes where
    the underlying is represented as a base token traded against a quote currency.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID for the instrument.
    raw_symbol : Symbol
        The raw/local/native symbol for the instrument, assigned by the venue.
    asset_class : AssetClass
        The asset class of the underlying (e.g. EQUITY, COMMODITY, INDEX).
    base_currency : Currency
        The base currency (the tokenized asset).
    quote_currency : Currency
        The quote currency.
    price_precision : int
        The price decimal precision.
    size_precision : int
        The trading size decimal precision.
    price_increment : Price
        The minimum price increment (tick size).
    size_increment : Quantity
        The minimum size increment.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the data event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the data object was initialized.
    isin : str, optional
        The ISIN of the underlying asset.
    multiplier : Quantity, default 1
        The contract multiplier.
    lot_size : Quantity, optional
        The rounded lot unit size.
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
    info : dict[str, object], optional
        The additional instrument information.

    """
    base_currency: Currency
    isin: str | None

    def __init__(
        self,
        instrument_id: InstrumentId,
        raw_symbol: Symbol,
        asset_class: AssetClass,
        base_currency: Currency,
        quote_currency: Currency,
        price_precision: int,
        size_precision: int,
        price_increment: Price,
        size_increment: Quantity,
        ts_event: int,
        ts_init: int,
        isin: str | None = None,
        multiplier: Quantity = ...,
        lot_size: Quantity | None = None,
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
        info: dict[str, object] | None = None,
    ) -> None: ...

    def get_base_currency(self) -> Currency:
        """
        Return the instruments base currency.

        Returns
        -------
        Currency

        """
        ...

    @staticmethod
    def from_dict(values: dict) -> TokenizedAsset:
        """
        Return an instrument from the given initialization values.

        Parameters
        ----------
        values : dict[str, object]
            The values to initialize the instrument with.

        Returns
        -------
        TokenizedAsset

        """
        ...

    @staticmethod
    def to_dict(obj: TokenizedAsset) -> dict[str, object]:
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """
        ...

    @staticmethod
    def from_pyo3(pyo3_instrument: Any) -> TokenizedAsset: ...