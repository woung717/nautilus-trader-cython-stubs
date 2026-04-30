from decimal import Decimal
from typing import Any

from nautilus_trader.model.enums import LiquiditySide
from nautilus_trader.model.enums import OrderSide
from nautilus_trader.model.enums import PositionSide
from nautilus_trader.accounting.accounts.base import Account
from nautilus_trader.model.events.account import AccountState
from nautilus_trader.model.events.order import OrderFilled
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.objects import MarginBalance
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity
from nautilus_trader.model.position import Position
from nautilus_trader.accounting.margin_models import MarginModel

class MarginAccount(Account):
    """
    Provides a margin account.

    Parameters
    ----------
    event : AccountState
        The initial account state event.
    calculate_account_state : bool, optional
        If the account state should be calculated from order fills.

    Raises
    ------
    ValueError
        If `event.account_type` is not equal to ``MARGIN``.
    """

    default_leverage: Decimal
    _leverages: dict[InstrumentId, Decimal]
    _margins: dict[InstrumentId, MarginBalance]

    def __init__(self, event: AccountState, calculate_account_state: bool = False) -> None: ...
    @staticmethod
    def to_dict(obj: MarginAccount) -> dict: ...
    @staticmethod
    def from_dict(values: dict) -> Any: ...
    def margins(self) -> dict[InstrumentId, Money]:
        """
        Return the initial (order) margins for the account.

        Returns
        -------
        dict[InstrumentId, Money]

        """
        ...
    def margins_init(self) -> dict[InstrumentId, Money]:
        """
        Return the initial (order) margins for the account.

        Returns
        -------
        dict[InstrumentId, Money]

        """
        ...
    def margins_maint(self) -> dict[InstrumentId, Money]:
        """
        Return the maintenance (position) margins for the account.

        Returns
        -------
        dict[InstrumentId, Money]

        """
        ...
    def account_margins(self) -> dict[Currency, MarginBalance]:
        """
        Return the account-wide (cross-margin) margin balances keyed by collateral currency.

        Returns
        -------
        dict[Currency, MarginBalance]

        """
        ...
    def account_margins_init(self) -> dict[Currency, Money]:
        """
        Return the account-wide initial (order) margins keyed by collateral currency.

        Returns
        -------
        dict[Currency, Money]

        """
        ...
    def account_margins_maint(self) -> dict[Currency, Money]:
        """
        Return the account-wide maintenance (position) margins keyed by collateral currency.

        Returns
        -------
        dict[Currency, Money]

        """
        ...
    def leverages(self) -> dict[InstrumentId, Decimal]:
        """
        Return the account leverages.

        Returns
        -------
        dict[InstrumentId, Decimal]

        """
        ...
    def leverage(self, instrument_id: InstrumentId) -> Decimal | None:
        """
        Return the leverage for the given instrument (if found).

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the leverage.

        Returns
        -------
        Decimal or ``None``

        """
        ...
    def margin_init(self, instrument_id: InstrumentId) -> Money | None:
        """
        Return the current initial (order) margin.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the query.

        Returns
        -------
        Money or ``None``

        Warnings
        --------
        Returns ``None`` if there is no applicable information for the query,
        rather than `Money` of zero amount.

        """
        ...
    def margin_maint(self, instrument_id: InstrumentId) -> Money | None:
        """
        Return the current maintenance (position) margin.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the query.

        Returns
        -------
        Money or ``None``

        Warnings
        --------
        Returns ``None`` if there is no applicable information for the query,
        rather than `Money` of zero amount.

        """
        ...
    def margin(self, instrument_id: InstrumentId) -> MarginBalance | None:
        """
        Return the current margin balance.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the query.

        Returns
        -------
        MarginBalance or ``None``

        Warnings
        --------
        Returns ``None`` if there is no applicable information for the query,
        rather than `MarginBalance` with zero amounts.

        """
        ...
    def margin_for_currency(self, currency: Currency) -> MarginBalance | None:
        """
        Return the account-wide (cross-margin) balance for the given collateral currency.

        Parameters
        ----------
        currency : Currency
            The collateral currency for the query.

        Returns
        -------
        MarginBalance or ``None``

        """
        ...
    def margin_init_for_currency(self, currency: Currency) -> Money | None:
        """
        Return the account-wide initial (order) margin for the given collateral currency.

        Parameters
        ----------
        currency : Currency
            The collateral currency for the query.

        Returns
        -------
        Money or ``None``

        """
        ...
    def margin_maint_for_currency(self, currency: Currency) -> Money | None:
        """
        Return the account-wide maintenance (position) margin for the given collateral currency.

        Parameters
        ----------
        currency : Currency
            The collateral currency for the query.

        Returns
        -------
        Money or ``None``

        """
        ...
    def total_margin_init(self, currency: Currency) -> Money:
        """
        Return the total initial margin reserved in the given currency.

        Sums per-instrument and account-wide entries whose currency matches.

        Parameters
        ----------
        currency : Currency
            The currency to total.

        Returns
        -------
        Money

        """
        ...
    def total_margin_maint(self, currency: Currency) -> Money:
        """
        Return the total maintenance margin reserved in the given currency.

        Sums per-instrument and account-wide entries whose currency matches.

        Parameters
        ----------
        currency : Currency
            The currency to total.

        Returns
        -------
        Money

        """
        ...
    def set_default_leverage(self, leverage: Decimal) -> None:
        """
        Set the default leverage for the account (if not specified by instrument).

        Parameters
        ----------
        leverage : Decimal
            The default leverage value

        Returns
        -------
        TypeError
            If leverage is not of type `Decimal`.
        ValueError
            If leverage is not >= 1.

        """
        ...
    def set_leverage(self, instrument_id: InstrumentId, leverage: Decimal) -> None:
        """
        Set the leverage for the given instrument.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the leverage.
        leverage : Decimal
            The leverage value

        Returns
        -------
        TypeError
            If leverage is not of type `Decimal`.
        ValueError
            If leverage is not >= 1.

        """
        ...
    def set_margin_model(self, margin_model: MarginModel) -> None:
        """
        Set the margin calculation model for the account.

        Parameters
        ----------
        margin_model : MarginModel
            The margin model to use for calculations.

        """
        ...
    def apply(self, event: AccountState) -> None:
        """
        Apply the given account event to the account.

        Replaces the stored margin balances with the event margins so
        externally reported account state stays queryable through the account.

        Parameters
        ----------
        event : AccountState
            The account event to apply.

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def update_margin_init(self, instrument_id: InstrumentId, margin_init: Money) -> None:
        """
        Update the initial (order) margin.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the update.
        margin_init : Money
            The current initial (order) margin for the instrument.

        Raises
        ------
        ValueError
            If `margin_init` is negative (< 0).

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def update_margin_maint(self, instrument_id: InstrumentId, margin_maint: Money) -> None:
        """
        Update the maintenance (position) margin.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument ID for the update.
        margin_maint : Money
            The current maintenance (position) margin for the instrument.

        Raises
        ------
        ValueError
            If `margin_maint` is negative (< 0).

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def update_margin(self, margin: MarginBalance) -> None:
        """
        Update the margin balance.

        Parameters
        ----------
        margin : MarginBalance

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def clear_margin_init(self, instrument_id: InstrumentId) -> None:
        """
        Clear the initial (order) margins for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the initial margin to clear.

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def clear_margin_maint(self, instrument_id: InstrumentId) -> None:
        """
        Clear the maintenance (position) margins for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the maintenance margin to clear.

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def clear_margin(self, instrument_id: InstrumentId) -> None:
        """
        Clear the maintenance (position) margins for the given instrument ID.

        Parameters
        ----------
        instrument_id : InstrumentId
            The instrument for the maintenance margin to clear.

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def clear_account_margin(self, currency: Currency) -> None:
        """
        Clear the account-wide (cross-margin) margin for the given collateral currency.

        Parameters
        ----------
        currency : Currency
            The collateral currency to clear.

        Warnings
        --------
        System method (not intended to be called by user code).

        """
        ...
    def is_unleveraged(self, instrument_id: InstrumentId) -> bool: ...
    def calculate_commission(
        self,
        instrument: Instrument,
        last_qty: Quantity,
        last_px: Price,
        liquidity_side: LiquiditySide,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate the commission generated from a transaction with the given
        parameters.

        Result will be in quote currency for standard instruments, or base
        currency for inverse instruments.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        last_qty : Quantity
            The transaction quantity.
        last_px : Price
            The transaction price.
        liquidity_side : LiquiditySide {``MAKER``, ``TAKER``}
            The liquidity side for the transaction.
        use_quote_for_inverse : bool
            If inverse instrument calculations use quote currency (instead of base).

        Returns
        -------
        Money

        Raises
        ------
        ValueError
            If `liquidity_side` is ``NO_LIQUIDITY_SIDE``.

        """
        ...
    def calculate_margin_init(
        self,
        instrument: Instrument,
        quantity: Quantity,
        price: Price,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate the initial (order) margin.

        Result will be in quote currency for standard instruments, or base
        currency for inverse instruments.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        quantity : Quantity
            The order quantity.
        price : Price
            The order price.
        use_quote_for_inverse : bool
            If inverse instrument calculations use quote currency (instead of base).

        Returns
        -------
        Money

        """
        ...
    def calculate_margin_maint(
        self,
        instrument: Instrument,
        side: PositionSide,
        quantity: Quantity,
        price: Price,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate the maintenance (position) margin.

        Result will be in quote currency for standard instruments, or base
        currency for inverse instruments.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        side : PositionSide {``LONG``, ``SHORT``}
            The currency position side.
        quantity : Quantity
            The currency position quantity.
        price : Price
            The positions current price.
        use_quote_for_inverse : bool
            If inverse instrument calculations use quote currency (instead of base).

        Returns
        -------
        Money

        """
        ...
    def calculate_pnls(self, instrument: Instrument, fill: OrderFilled, position: Position | None = None) -> list[Money]:
        """
        Return the calculated PnL.

        The calculation does not include any commissions.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        fill : OrderFilled
            The fill for the calculation.
        position : Position, optional
            The position for the calculation.

        Returns
        -------
        list[Money]

        """
        ...
    def balance_impact(self, instrument: Instrument, quantity: Quantity, price: Price, order_side: OrderSide) -> Money: ...
