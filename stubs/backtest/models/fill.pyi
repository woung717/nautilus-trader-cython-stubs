from nautilus_trader.model.book import OrderBook
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.objects import Price
from nautilus_trader.model.orders.base import Order


class FillModel:
    """
    Provides probabilistic modeling for order fill dynamics including probability
    of fills and slippage by order type.

    Parameters
    ----------
    prob_fill_on_limit : double
        The probability of limit order filling if the market rests on its price.
    prob_fill_on_stop : double
        The probability of stop orders filling if the market rests on its price.
    prob_slippage : double
        The probability of order fill prices slipping by one tick.
    random_seed : int, optional
        The random seed (if None then no random seed).
    config : FillModelConfig, optional
        The configuration for the model.

    Raises
    ------
    ValueError
        If any probability argument is not within range [0, 1].
    TypeError
        If `random_seed` is not None and not of type `int`.
    """
    def __init__(
        self,
        prob_fill_on_limit: float = 1.0,
        prob_slippage: float = 0.0,
        random_seed: int | None = None,
        config = None,
    ) -> None: ...

    def fill_limit_inside_spread(self) -> bool:
        """
        Return whether limit orders at or inside the spread are fillable.

        When True, the matching core treats a limit order as fillable if its
        price is at or better than the current best quote on its own side
        (BUY >= bid, SELL <= ask), not just when it crosses the spread.

        Override to return True in fill models that provide simulated
        liquidity inside the spread (e.g. best bid/ask).

        Returns
        -------
        bool

        """
        ...

    def is_limit_filled(self) -> bool:
        """
        Return a value indicating whether a ``LIMIT`` order filled.

        Returns
        -------
        bool

        """
        ...

    def is_slipped(self) -> bool:
        """
        Return a value indicating whether an order fill slipped.

        Returns
        -------
        bool

        """
        ...

    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return a simulated OrderBook for fill simulation.

        This method allows custom fill models to provide their own liquidity
        simulation by returning a custom OrderBook that represents the expected
        market liquidity. The matching engine will use this simulated OrderBook
        to determine fills.

        The default implementation returns None, which means the matching engine
        will use its standard fill logic (maintaining backward compatibility).

        Parameters
        ----------
        instrument : Instrument
            The instrument being traded.
        order : Order
            The order to simulate fills for.
        best_bid : Price
            The current best bid price.
        best_ask : Price
            The current best ask price.

        Returns
        -------
        OrderBook or None
            The simulated OrderBook for fill simulation, or None to use default logic.

        """
        ...


class BestPriceFillModel(FillModel):
    """
    Fill model that executes all orders at the best available price.

    This model simulates optimistic market conditions where every order gets filled
    immediately at the best available price. Ideal for testing basic strategy logic.

    """
    def fill_limit_inside_spread(self) -> bool: ...

    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with unlimited liquidity at best prices.
        """
        ...


class OneTickSlippageFillModel(FillModel):
    """
    Fill model that forces exactly one tick of slippage for all orders.

    This model demonstrates how to create deterministic slippage by setting zero volume
    at best prices and unlimited volume one tick away.

    """
    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with no volume at best prices, unlimited volume one tick away.
        """
        ...


class TwoTierFillModel(FillModel):
    """
    Fill model with two-tier pricing: first 10 contracts at best price, remainder one tick worse.

    This model simulates basic market depth behavior and provides realistic simulation
    of basic market impact for small to medium orders.
    """
    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with two-tier liquidity structure.
        """
        ...


class ProbabilisticFillModel(FillModel):
    """
    Fill model that replicates the current probabilistic behavior.

    This model demonstrates how to implement the existing FillModel's probabilistic
    behavior using the new simulation approach: 50% chance of best price fill,
    50% chance of one tick slippage.

    """
    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook based probabilistic logic.
        """
        ...


class SizeAwareFillModel(FillModel):
    """
    Fill model that applies different execution models based on order size.

    Small orders (<=10) get good liquidity at best prices. Large orders experience price
    impact with partial fills at worse prices.

    """
    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with size-dependent liquidity.
        """
        ...


class LimitOrderPartialFillModel(FillModel):
    """
    Fill model that simulates partial fills for limit orders.

    When price touches the limit level, only fills maximum 5 contracts of the order
    quantity, modeling typical limit order queue behavior.

    """
    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with limited fills at limit prices.
        """
        ...


class ThreeTierFillModel(FillModel):
    """
    Fill model with three-tier pricing for realistic market depth simulation.

    Distributes 100-contract order fills across three price levels:
    - 50 contracts at best price
    - 30 contracts 1 tick worse
    - 20 contracts 2 ticks worse

    """
    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with three-tier liquidity structure.
        """
        ...


class MarketHoursFillModel(FillModel):
    """
    Fill model that simulates varying market conditions based on time.

    Implements wider spreads during low liquidity periods (e.g., outside market hours).
    Essential for strategies that trade across different market sessions.

    """
    def __init__(
        self,
        prob_fill_on_limit: float = 1.0,
        prob_slippage: float = 0.0,
        random_seed: int | None = None,
    ) -> None: ...

    def is_low_liquidity_period(self) -> bool:
        """
        Check if current time is during low liquidity period.
        """
        ...

    def set_low_liquidity_period(self, is_low_liquidity: bool) -> None:
        """
        Set the liquidity period for testing purposes.
        """
        ...

    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with time-dependent liquidity.
        """
        ...


class VolumeSensitiveFillModel(FillModel):
    """
    Fill model that adjusts liquidity based on recent trading volume.

    Creates realistic market depth based on actual market activity by using recent bar
    volume data to determine available liquidity.

    """
    def __init__(
        self,
        prob_fill_on_limit: float = 1.0,
        prob_slippage: float = 0.0,
        random_seed: int | None = None,
    ) -> None: ...

    def set_recent_volume(self, volume: float) -> None:
        """
        Set recent volume for testing purposes.
        """
        ...

    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with volume-based liquidity.
        """
        ...


class CompetitionAwareFillModel(FillModel):
    """
    Fill model that simulates market competition effects.

    Makes only a percentage of visible liquidity actually available, reflecting
    realistic conditions where multiple traders compete for the same liquidity.

    """
    def __init__(
        self,
        prob_fill_on_limit: float = 1.0,
        prob_slippage: float = 0.0,
        random_seed: int | None = None,
        liquidity_factor: float = 0.3,
    ) -> None: ...

    def get_orderbook_for_fill_simulation(
        self,
        instrument: Instrument,
        order: Order,
        best_bid: Price,
        best_ask: Price,
    ) -> OrderBook | None:
        """
        Return OrderBook with competition-adjusted liquidity.
        """
        ...