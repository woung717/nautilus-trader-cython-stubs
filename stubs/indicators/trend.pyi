from datetime import datetime
from nautilus_trader.model.enums import PriceType
from nautilus_trader.indicators.averages import MovingAverageType
from nautilus_trader.indicators.base import Indicator
from nautilus_trader.model.data import Bar, QuoteTick, TradeTick


class ArcherMovingAveragesTrends(Indicator):
    """
    Archer Moving Averages Trends indicator.

    Parameters
    ----------
    fast_period : int
        The period for the fast moving average (> 0).
    slow_period : int
        The period for the slow moving average (> 0 & > fast_sma).
    signal_period : int
        The period for lookback price array (> 0).
    ma_type : MovingAverageType
        The moving average type for the calculations.

    References
    ----------
    https://github.com/twopirllc/pandas-ta/blob/bc3b292bf1cc1d5f2aba50bb750a75209d655b37/pandas_ta/trend/amat.py
    """
    fast_period: int
    slow_period: int
    signal_period: int
    long_run: int
    short_run: int

    def __init__(
        self,
        fast_period: int,
        slow_period: int,
        signal_period: int,
        ma_type: MovingAverageType = MovingAverageType.EXPONENTIAL,
    ) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, close: float) -> None: ...

class AroonOscillator(Indicator):
    """
    The Aroon (AR) indicator developed by Tushar Chande attempts to
    determine whether an instrument is trending, and how strong the trend is.
    AroonUp and AroonDown lines make up the indicator with their formulas below.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    """
    period: int
    aroon_up: float
    aroon_down: float
    value: float

    def __init__(self, period: int) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, high: float, low: float) -> None: ...

class DirectionalMovement(Indicator):
    """
    Two oscillators that capture positive and negative trend movement.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    ma_type : MovingAverageType
        The moving average type for the indicator (cannot be None).
    """
    period: int
    pos: float
    neg: float

    def __init__(
        self,
        period: int,
        ma_type: MovingAverageType = MovingAverageType.EXPONENTIAL,
    ) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, high: float, low: float) -> None: ...

class MovingAverageConvergenceDivergence(Indicator):
    """
    An indicator which calculates the difference between two moving averages.
    Different moving average types can be selected for the inner calculation.

    Parameters
    ----------
    fast_period : int
        The period for the fast moving average (> 0).
    slow_period : int
        The period for the slow moving average (> 0 & > fast_sma).
    ma_type : MovingAverageType
        The moving average type for the calculations.
    price_type : PriceType
        The specified price type for extracting values from quotes.

    Raises
    ------
    ValueError
        If `fast_period` is not positive (> 0).
    ValueError
        If `slow_period` is not positive (> 0).
    ValueError
        If `fast_period` is not < `slow_period`.
    """
    fast_period: int
    slow_period: int
    price_type: PriceType
    value: float

    def __init__(
        self,
        fast_period: int,
        slow_period: int,
        ma_type: MovingAverageType = MovingAverageType.EXPONENTIAL,
        price_type: PriceType = PriceType.LAST,
    ) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None: ...

    def handle_trade_tick(self, tick: TradeTick) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, close: float) -> None: ...

class LinearRegression(Indicator):
    """
    An indicator that calculates a simple linear regression.

    Parameters
    ----------
    period : int
        The period for the indicator.

    Raises
    ------
    ValueError
        If `period` is not greater than zero.
    """
    period: int
    slope: float
    intercept: float
    degree: float
    cfo: float
    R2: float
    value: float

    def __init__(self, period: int = 0) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, close: float) -> None: ...

class Bias(Indicator):
    """
    Rate of change between the source and a moving average.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    ma_type : MovingAverageType
        The moving average type for the indicator (cannot be None).
    """
    period: int
    value: float

    def __init__(
        self,
        period: int,
        ma_type: MovingAverageType = MovingAverageType.SIMPLE,
    ) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, close: float) -> None: ...

class Swings(Indicator):
    """
    A swing indicator which calculates and stores various swing metrics.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    """
    period: int
    direction: int
    changed: bool
    high_datetime: datetime | None
    low_datetime: datetime | None
    high_price: float
    low_price: float
    length: float
    duration: int
    since_high: int
    since_low: int

    def __init__(self, period: int) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, high: float, low: float, timestamp: datetime) -> None: ...