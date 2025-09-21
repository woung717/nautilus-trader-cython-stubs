from decimal import Decimal

from nautilus_trader.core.rust.model import PositionSide
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity


class MarginModel:
    """
    Abstract base class for margin calculation models.

    Different venues and instrument types may have varying approaches to
    calculating margin requirements. This abstraction allows for flexible
    margin calculation strategies.
    """

    def calculate_margin_init(
        self,
        instrument: Instrument,
        quantity: Quantity,
        price: Price,
        leverage: Decimal,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate the initial (order) margin requirement.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        quantity : Quantity
            The order quantity.
        price : Price
            The order price.
        leverage : Decimal
            The account leverage for this instrument.
        use_quote_for_inverse : bool, default False
            If inverse instrument calculations use quote currency (instead of base).

        Returns
        -------
        Money
            The initial margin requirement.
        """
        ...

    def calculate_margin_maint(
        self,
        instrument: Instrument,
        side: PositionSide,
        quantity: Quantity,
        price: Price,
        leverage: Decimal,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate the maintenance (position) margin requirement.

        Parameters
        ----------
        instrument : Instrument
            The instrument for the calculation.
        side : PositionSide
            The position side.
        quantity : Quantity
            The position quantity.
        price : Price
            The current price.
        leverage : Decimal
            The account leverage for this instrument.
        use_quote_for_inverse : bool, default False
            If inverse instrument calculations use quote currency (instead of base).

        Returns
        -------
        Money
            The maintenance margin requirement.
        """
        ...


class StandardMarginModel(MarginModel):
    """
    Standard margin model that uses fixed percentages without leverage division.

    This model matches traditional broker behavior (e.g., Interactive Brokers)
    where margin requirements are fixed percentages of notional value regardless
    of account leverage. Leverage affects buying power but not margin requirements.

    Formula:
    - Initial Margin = notional_value * instrument.margin_init
    - Maintenance Margin = notional_value * instrument.margin_maint
    """

    def calculate_margin_init(
        self,
        instrument: Instrument,
        quantity: Quantity,
        price: Price,
        leverage: Decimal,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate initial margin using fixed percentage of notional value.
        """
        ...

    def calculate_margin_maint(
        self,
        instrument: Instrument,
        side: PositionSide,
        quantity: Quantity,
        price: Price,
        leverage: Decimal,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate maintenance margin using fixed percentage of notional value.
        """
        ...


class LeveragedMarginModel(MarginModel):
    """
    Leveraged margin model that divides margin requirements by leverage.

    This model represents the current Nautilus behavior and may be appropriate
    for certain crypto exchanges or specific trading scenarios where leverage
    directly reduces margin requirements.

    Formula:
    - Initial Margin = (notional_value / leverage) * instrument.margin_init
    - Maintenance Margin = (notional_value / leverage) * instrument.margin_maint
    """

    def calculate_margin_init(
        self,
        instrument: Instrument,
        quantity: Quantity,
        price: Price,
        leverage: Decimal,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate initial margin with leverage division.
        """
        ...

    def calculate_margin_maint(
        self,
        instrument: Instrument,
        side: PositionSide,
        quantity: Quantity,
        price: Price,
        leverage: Decimal,
        use_quote_for_inverse: bool = False,
    ) -> Money:
        """
        Calculate maintenance margin with leverage division.
        """
        ...