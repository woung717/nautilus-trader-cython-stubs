from typing import Any

from nautilus_trader.accounting.accounts.base import Account
from nautilus_trader.model.identifiers import AccountId
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.objects import Currency
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price

class PortfolioFacade:
    """
    Provides a read-only facade for a `Portfolio`.
    """

    def account(self, venue: Venue | None = None, account_id: AccountId | None = None) -> Account:
        """Abstract method (implement in subclass)."""
        ...
    def balances_locked(self, venue: Venue | None = None, account_id: AccountId | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def margins_init(self, venue: Venue | None = None, account_id: AccountId | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def margins_maint(self, venue: Venue | None = None, account_id: AccountId | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def realized_pnls(self, venue: Venue | None = None, account_id: AccountId | None = None, target_currency: Currency | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def unrealized_pnls(self, venue: Venue | None = None, account_id: AccountId | None = None, target_currency: Currency | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def total_pnls(self, venue: Venue | None = None, account_id: AccountId | None = None, target_currency: Currency | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def net_exposures(self, venue: Venue | None = None, account_id: AccountId | None = None, target_currency: Currency | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def mark_values(self, venue: Venue | None = None, account_id: AccountId | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def equity(self, venue: Venue | None = None, account_id: AccountId | None = None) -> dict[Any, Any]:
        """Abstract method (implement in subclass)."""
        ...
    def missing_price_instruments(self, venue: Venue) -> list[Any]:
        """Abstract method (implement in subclass)."""
        ...
    def realized_pnl(self, instrument_id: InstrumentId, account_id: AccountId | None = None, target_currency: Currency | None = None) -> Money:
        """Abstract method (implement in subclass)."""
        ...
    def unrealized_pnl(self, instrument_id: InstrumentId, price: Price | None = None, account_id: AccountId | None = None, target_currency: Currency | None = None) -> Money:
        """Abstract method (implement in subclass)."""
        ...
    def total_pnl(self, instrument_id: InstrumentId, price: Price | None = None, account_id: AccountId | None = None, target_currency: Currency | None = None) -> Money:
        """Abstract method (implement in subclass)."""
        ...
    def net_exposure(self, instrument_id: InstrumentId, price: Price | None = None, account_id: AccountId | None = None, target_currency: Currency | None = None) -> Money:
        """Abstract method (implement in subclass)."""
        ...
    def net_position(self, instrument_id: InstrumentId, account_id: AccountId | None = None) -> object:
        """Abstract method (implement in subclass)."""
        ...
    def is_net_long(self, instrument_id: InstrumentId, account_id: AccountId | None = None) -> bool:
        """Abstract method (implement in subclass)."""
        ...
    def is_net_short(self, instrument_id: InstrumentId, account_id: AccountId | None = None) -> bool:
        """Abstract method (implement in subclass)."""
        ...
    def is_flat(self, instrument_id: InstrumentId, account_id: AccountId | None = None) -> bool:
        """Abstract method (implement in subclass)."""
        ...
    def is_completely_flat(self, account_id: AccountId | None = None) -> bool:
        """Abstract method (implement in subclass)."""
        ...
