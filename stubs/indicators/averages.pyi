from enum import Enum
from typing import Any

from nautilus_trader.model.enums import PriceType
from nautilus_trader.indicators.base import Indicator
from nautilus_trader.indicators.momentum import ChandeMomentumOscillator
from nautilus_trader.model.data import Bar, QuoteTick, TradeTick


class MovingAverageType(Enum): # skip-validate
    SIMPLE = 0
    EXPONENTIAL = 1
    DOUBLE_EXPONENTIAL = 2
    WILDER = 3
    HULL = 4
    ADAPTIVE = 5
    WEIGHTED = 6
    VARIABLE_INDEX_DYNAMIC = 7
    

class MovingAverage(Indicator):
    """The base class for all moving average type indicators.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    params : list
        The initialization parameters for the indicator.
    price_type : PriceType, optional
        The specified price type for extracting values from quotes.

    Warnings
    --------
    This class should not be used directly, but through a concrete subclass.
    """

    period: int
    price_type: PriceType
    value: float
    count: int

    def __init__(self, period: int, params: list[Any], price_type: PriceType) -> None: ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...
    
    def _increment_count(self) -> None:
        ...
    def _reset(self) -> None:
        ...
    def _reset_ma(self) -> None:
        ...


class SimpleMovingAverage(MovingAverage):
    """An indicator which calculates a simple moving average across a rolling window.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    price_type : PriceType
        The specified price type for extracting values from quotes.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    """

    value: float

    def __init__(self, period: int, price_type: PriceType = PriceType.LAST) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...

    def _reset_ma(self) -> None:
        ...


class ExponentialMovingAverage(MovingAverage):
    """An indicator which calculates an exponential moving average across a
    rolling window.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    price_type : PriceType
        The specified price type for extracting values from quotes.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    """

    alpha: float
    value: float

    def __init__(self, period: int, price_type: PriceType = PriceType.LAST) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...


class DoubleExponentialMovingAverage(MovingAverage):
    """The Double Exponential Moving Average attempts to a smoother average with less
    lag than the normal Exponential Moving Average (EMA).

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    price_type : PriceType
        The specified price type for extracting values from quotes.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    """

    value: float

    def __init__(self, period: int, price_type: PriceType = PriceType.LAST) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...

    def _reset_ma(self) -> None:
        ...


class WeightedMovingAverage(MovingAverage):
    """An indicator which calculates a weighted moving average across a rolling window.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    weights : iterable
        The weights for the moving average calculation (if not ``None`` then = period).
    price_type : PriceType
        The specified price type for extracting values from quotes.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    """

    weights: Any
    value: float

    def __init__(self, period: int, weights: Any = None, price_type: PriceType = PriceType.LAST) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...

    def _reset_ma(self) -> None:
        ...


class HullMovingAverage(MovingAverage):
    """An indicator which calculates a Hull Moving Average (HMA) across a rolling
    window. The HMA, developed by Alan Hull, is an extremely fast and smooth
    moving average.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    price_type : PriceType
        The specified price type for extracting values from quotes.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    """

    value: float

    def __init__(self, period: int, price_type: PriceType = PriceType.LAST) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...

    def _reset_ma(self) -> None:
        ...


class AdaptiveMovingAverage(MovingAverage):
    """An indicator which calculates an adaptive moving average (AMA) across a
    rolling window. Developed by Perry Kaufman, the AMA is a moving average
    designed to account for market noise and volatility. The AMA will closely
    follow prices when the price swings are relatively small and the noise is
    low. The AMA will increase lag when the price swings increase.

    Parameters
    ----------
    period_er : int
        The period for the internal `EfficiencyRatio` indicator (> 0).
    period_alpha_fast : int
        The period for the fast smoothing constant (> 0).
    period_alpha_slow : int
        The period for the slow smoothing constant (> 0 < alpha_fast).
    price_type : PriceType
        The specified price type for extracting values from quotes.
    """

    period_er: int
    period_alpha_fast: int
    period_alpha_slow: int
    alpha_fast: float
    alpha_slow: float
    alpha_diff: float
    value: float

    def __init__(
        self,
        period_er: int,
        period_alpha_fast: int,
        period_alpha_slow: int,
        price_type: PriceType = PriceType.LAST,
    ) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...

    def _reset_ma(self) -> None:
        ...


class WilderMovingAverage(MovingAverage):
    """The Wilder's Moving Average is simply an Exponential Moving Average (EMA) with
    a modified alpha = 1 / period.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    price_type : PriceType
        The specified price type for extracting values from quotes.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    """

    alpha: float
    value: float

    def __init__(self, period: int, price_type: PriceType = PriceType.LAST) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...


class VariableIndexDynamicAverage(MovingAverage):
    """Variable Index Dynamic Average (VIDYA) was developed by Tushar Chande. It is
    similar to an Exponential Moving Average, but it has a dynamically adjusted
    lookback period dependent on relative price volatility as measured by Chande
    Momentum Oscillator (CMO). When volatility is high, VIDYA reacts faster to
    price changes. It is often used as moving average or trend identifier.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    price_type : PriceType
        The specified price type for extracting values from quotes.
    cmo_ma_type : int
        The moving average type for CMO indicator.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
        If `cmo_ma_type` is ``VARIABLE_INDEX_DYNAMIC``.
    """

    cmo: ChandeMomentumOscillator
    cmo_pct: float
    alpha: float
    value: float

    def __init__(
        self,
        period: int,
        price_type: PriceType = PriceType.LAST,
        cmo_ma_type: MovingAverageType = MovingAverageType.SIMPLE,
    ) -> None: ...

    def handle_quote_tick(self, tick: QuoteTick) -> None:
        """Update the indicator with the given quote tick.

        Parameters
        ----------
        tick : QuoteTick
            The update tick to handle.
        """
        ...

    def handle_trade_tick(self, tick: TradeTick) -> None:
        """Update the indicator with the given trade tick.

        Parameters
        ----------
        tick : TradeTick
            The update tick to handle.
        """
        ...

    def handle_bar(self, bar: Bar) -> None:
        """Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar to handle.
        """
        ...

    def update_raw(self, value: float) -> None:
        """Update the indicator with the given raw value.

        Parameters
        ----------
        value : double
            The update value.
        """
        ...


class MovingAverageFactory:
    """
    Provides a factory to construct different moving average indicators.
    """

    @staticmethod
    def create(period: int, ma_type: MovingAverageType, **kwargs: Any) -> MovingAverage:
        """Create a moving average indicator corresponding to the given ma_type.

        Parameters
        ----------
        period : int
            The period of the moving average (> 0).
        ma_type : MovingAverageType
            The moving average type.

        Returns
        -------
        MovingAverage

        Raises
        ------
        ValueError
            If `period` is not positive (> 0).

        """
        ...