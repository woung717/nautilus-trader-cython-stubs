from decimal import Decimal
from typing import Any

import pandas as pd

from nautilus_trader.model.enums import OptionKind
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity

class CryptoOption(Instrument):
    """
    Represents an option instrument with crypto assets as underlying and for settlement.

    Parameters
    ----------
    instrument_id : InstrumentId
        The instrument ID.
    raw_symbol : Symbol
        The raw/local/native symbol for the instrument, assigned by the venue.
    underlying : Currency
        The underlying asset.
    quote_currency : Currency
        The contract quote currency.
    settlement_currency : Currency
        The settlement currency.
    is_inverse : bool
        If the instrument costing is inverse (quantity expressed in quote currency units).
    option_kind : OptionKind
        The kind of option (PUT | CALL).
    strike_price : Price
        The option strike price.
    activation_ns : uint64_t
        UNIX timestamp (nanoseconds) for contract activation.
    expiration_ns : uint64_t
        UNIX timestamp (nanoseconds) for contract expiration.
    price_precision : int
        The price decimal precision.
    size_precision : int
        The trading size decimal precision.
    price_increment : Price
        The minimum price increment (tick size).
    size_increment : Quantity
        The minimum size increment.
    multiplier : Quantity, default 1
        The contract multiplier.
    ts_event : uint64_t
        UNIX timestamp (nanoseconds) when the data event occurred.
    ts_init : uint64_t
        UNIX timestamp (nanoseconds) when the data object was initialized.
    multiplier : Quantity, default 1
        The contract multiplier.
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

    Raises
    ------
    ValueError
        If `price_precision` is negative (< 0).
    ValueError
        If `size_precision` is negative (< 0).
    ValueError
        If `price_increment` is not positive (> 0).
    ValueError
        If `size_increment` is not positive (> 0).
    ValueError
        If `lot size` is not positive (> 0).
    ValueError
        If `max_quantity` is not positive (> 0).
    ValueError
        If `min_quantity` is negative (< 0).
    ValueError
        If `max_notional` is not positive (> 0).
    ValueError
        If `min_notional` is negative (< 0).
    ValueError
        If `max_price` is not positive (> 0).
    ValueError
        If `min_price` is negative (< 0).
    ValueError
        If `margin_init` is negative (< 0).
    ValueError
        If `margin_maint` is negative (< 0).

    """

    underlying: Currency
    settlement_currency: Currency
    option_kind: OptionKind
    strike_price: Price
    activation_ns: int
    expiration_ns: int

    def __init__(
        self,
        instrument_id: InstrumentId,
        raw_symbol: Symbol,
        underlying: Currency,
        quote_currency: Currency,
        settlement_currency: Currency,
        is_inverse: bool,
        option_kind: OptionKind,
        strike_price: Price,
        activation_ns: int,
        expiration_ns: int,
        price_precision: int,
        size_precision: int,
        price_increment: Price,
        size_increment: Quantity,
        ts_event: int,
        ts_init: int,
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
        info: dict | None = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def get_base_currency(self) -> Currency:
        """
        Return the instruments base currency (underlying).

        Returns
        -------
        Currency

        """
        ...
    def get_settlement_currency(self) -> Currency:
        """
        Return the currency used to settle a trade of the instrument.

        Returns
        -------
        Currency

        """
        ...
    def get_cost_currency(self) -> Currency:
        """
        Return the currency used for PnL calculations for the instrument.

        - Standard linear instruments = quote_currency
        - Inverse instruments = underlying (base currency)

        Returns
        -------
        Currency

        """
        ...
    def notional_value(
        self,
        quantity: Quantity,
        price: Price,
        use_quote_for_inverse: bool = False,
        target_currency: Currency | None = None,
        conversion_price: Price | None = None,
    ) -> Money:
        """
        Calculate the notional value.

        Result will be in quote currency for standard instruments, or underlying
        currency for inverse instruments.

        Parameters
        ----------
        quantity : Quantity
            The total quantity.
        price : Price
            The price for the calculation.
        use_quote_for_inverse : bool
            For inverse instruments only: if True, treats the quantity as already representing
            notional value in quote currency and returns it directly without calculation.
            This is useful when quantity already represents a USD value that doesn't need
            conversion (e.g., for display purposes). Has no effect on linear instruments.
        target_currency : Currency, optional
            The currency to convert the result to. If None, uses the default settlement currency.
        conversion_price : Price, optional
            The price to use for currency conversion if target_currency is specified.

        Returns
        -------
        Money

        """
        ...
    @property
    def activation_utc(self) -> pd.Timestamp:
        """
        Return the contract activation timestamp (UTC).

        Returns
        -------
        pd.Timestamp
            tz-aware UTC.

        """
        ...
    @property
    def expiration_utc(self) -> pd.Timestamp:
        """
        Return the contract expriation timestamp (UTC).

        Returns
        -------
        pd.Timestamp
            tz-aware UTC.

        """
        ...
    @staticmethod
    def from_dict(values: dict) -> CryptoOption:
        """
        Return an instrument from the given initialization values.

        Parameters
        ----------
        values : dict[str, object]
            The values to initialize the instrument with.

        Returns
        -------
        CryptoOption

        """
        ...
    @staticmethod
    def to_dict(obj: CryptoOption) -> dict[str, Any]:
        """
        Return a dictionary representation of this object.

        Returns
        -------
        dict[str, object]

        """
        ...
    @staticmethod
    def from_pyo3(pyo3_instrument: Any) -> CryptoOption:
        """
        Return legacy Cython option contract instrument converted from the given pyo3 Rust object.

        Parameters
        ----------
        pyo3_instrument : nautilus_pyo3.CryptoOption
            The pyo3 Rust option contract instrument to convert from.

        Returns
        -------
        CryptoOption

        """
        ...