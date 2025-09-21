from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import Money, Price, Quantity
from nautilus_trader.model.orders.base import Order


class FeeModel:
    """
    Provides an abstract fee model for trades.
    """

    def get_commission(
        self,
        order: Order,
        fill_qty: Quantity,
        fill_px: Price,
        instrument: Instrument,
    ) -> Money:
        """
        Return the commission for a trade.

        Parameters
        ----------
        order : Order
            The order to calculate the commission for.
        fill_qty : Quantity
            The fill quantity of the order.
        fill_px : Price
            The fill price of the order.
        instrument : Instrument
            The instrument for the order.

        Returns
        -------
        Money

        """
        ...


class MakerTakerFeeModel(FeeModel):
    """
    Provide a fee model for trades based on a maker/taker fee schedule
    and notional value of the trade.

    Parameters
    ----------
    config : MakerTakerFeeModelConfig, optional
        The configuration for the fee model.
    """

    def __init__(self, config = None) -> None: ...

    def get_commission(
        self,
        order: Order,
        fill_qty: Quantity,
        fill_px: Price,
        instrument: Instrument,
    ) -> Money:
        ...


class FixedFeeModel(FeeModel):
    """
    Provides a fixed fee model for trades.

    Parameters
    ----------
    commission : Money, optional
        The fixed commission amount for trades.
    charge_commission_once : bool, default True
        Whether to charge the commission once per order or per fill.
    config : FixedFeeModelConfig, optional
        The configuration for the model.

    Raises
    ------
    ValueError
        If both ``commission`` **and** ``config`` are provided, **or** if both are ``None`` (exactly one must be supplied).
    ValueError
        If `commission` is not a positive amount.
    """

    def __init__(
        self,
        commission: Money | None = None,
        charge_commission_once: bool = True,
        config = None,
    ) -> None: ...

    def get_commission(
        self,
        order: Order,
        fill_qty: Quantity,
        fill_px: Price,
        instrument: Instrument,
    ) -> Money:
        ...


class PerContractFeeModel(FeeModel):
    """
    Provides a fee model which charges a commission per contract traded.

    Parameters
    ----------
    commission : Money, optional
        The commission amount per contract.
    config : PerContractFeeModelConfig, optional
        The configuration for the model.

    Raises
    ------
    ValueError
        If both ``commission`` **and** ``config`` are provided, **or** if both are ``None`` (exactly one must be supplied).
    ValueError
        If `commission` is negative (< 0).
    """

    def __init__(
        self,
        commission: Money | None = None,
        config = None,
    ) -> None: ...

    def get_commission(
        self,
        order: Order,
        fill_qty: Quantity,
        fill_px: Price,
        instrument: Instrument,
    ) -> Money:
        ...