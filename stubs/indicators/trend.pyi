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
    def _reset(self) -> None: ...

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

    def _reset(self) -> None: ...

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

    def _reset(self) -> None: ...

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

    def _reset(self) -> None: ...

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

    def _reset(self) -> None: ...

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

    def _reset(self) -> None: ...

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

    def _reset(self) -> None: ...

class IchimokuCloud(Indicator):
    """
    Ichimoku Cloud (Kinko Hyo) with five components.

    - Tenkan-sen (Conversion Line): (tenkan_period high + tenkan_period low) / 2.
    - Kijun-sen (Base Line): (kijun_period high + kijun_period low) / 2.
    - Senkou Span A (Leading Span A): (Tenkan + Kijun) / 2, displaced forward by displacement.
    - Senkou Span B (Leading Span B): (senkou_period high + senkou_period low) / 2, displaced forward by displacement.
    - Chikou Span (Lagging Span): Close displaced backward by displacement.

    The indicator becomes ``initialized`` after ``senkou_period`` bars,
    at which point tenkan_sen, kijun_sen are valid. The displaced outputs
    (senkou_span_a, senkou_span_b, chikou_span) require an additional
    ``displacement`` bars before they become non-zero.

    Parameters
    ----------
    tenkan_period : int
        Period for Tenkan-sen (default 9).
    kijun_period : int
        Period for Kijun-sen (default 26).
    senkou_period : int
        Period for Senkou Span B (default 52).
    displacement : int
        Displacement for leading/lagging spans (default 26).

    Raises
    ------
    ValueError
        If any period or displacement is not positive.
    ValueError
        If senkou_period is not >= kijun_period or kijun_period is not >= tenkan_period.
    """
    tenkan_period: int
    kijun_period: int
    senkou_period: int
    displacement: int
    tenkan_sen: float
    kijun_sen: float
    senkou_span_a: float
    senkou_span_b: float
    chikou_span: float

    def __init__(
        self,
        tenkan_period: int = 9,
        kijun_period: int = 26,
        senkou_period: int = 52,
        displacement: int = 26,
    ) -> None: ...

    def handle_bar(self, bar: Bar) -> None: ...

    def update_raw(self, high: float, low: float, close: float) -> None: ...

    def _reset(self) -> None: ...
