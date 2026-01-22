from collections import deque
from typing import Any
from nautilus_trader.indicators.base import Indicator
from nautilus_trader.model.data import Bar


class RelativeStrengthIndex(Indicator):
    """
    An indicator which calculates a relative strength index (RSI) across a rolling window.

    Parameters
    ----------
    ma_type : int
        The moving average type for average gain/loss.
    period : MovingAverageType
        The rolling window period for the indicator.

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    """
    period: int
    _rsi_max: int
    _average_gain: Any
    _average_loss: Any
    _last_value: float
    value: float

    def __init__(self, period: int, ma_type: Any = None) -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, value: float) -> None: 
        """
        Update the indicator with the given value.

        Parameters
        ----------
        value : double
            The update value.

        """
        ...
    def _reset(self) -> None: ...


class RateOfChange(Indicator):
    """
    An indicator which calculates the rate of change of price over a defined period.
    The return output can be simple or log.

    Parameters
    ----------
    period : int
        The period for the indicator.
    use_log : bool
        Use log returns for value calculation.

    Raises
    ------
    ValueError
        If `period` is not > 1.
    """
    period: int
    _use_log: bool
    _prices: deque
    value: float

    def __init__(self, period: int, use_log: bool = False) -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, price: float) -> None: 
        """
        Update the indicator with the given price.

        Parameters
        ----------
        price : double
            The update price.

        """
        ...
    def _reset(self) -> None: ...


class ChandeMomentumOscillator(Indicator):
    """
    Attempts to capture the momentum of an asset with overbought at 50 and
    oversold at -50.

    Parameters
    ----------
    ma_type : int
        The moving average type for average gain/loss.
    period : MovingAverageType
        The rolling window period for the indicator.
    """
    period: int
    _average_gain: Any
    _average_loss: Any
    _previous_close: float
    value: float

    def __init__(self, period: int, ma_type: Any = None) -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, close: float) -> None: 
        """
        Update the indicator with the given value.

        Parameters
        ----------
        value : double
            The update value.

        """
        ...
    def _reset(self) -> None: ...


class StochasticsDMethod:
    """
    Method for calculating %D in the Stochastics indicator.

    The %D line is the smoothed version of %K and provides trading signals.
    Two calculation methods are supported:

    - **RATIO**: Nautilus original method using `100 * SUM(close-LL) / SUM(HH-LL)` over `period_d`.
      This is range-weighted and has less lag than MA-based methods.
    - **MOVING_AVERAGE**: Standard method using MA of slowed %K values, compatible with
      cTrader/MetaTrader implementations.
    """
    RATIO = "ratio"
    MOVING_AVERAGE = "moving_average"


class Stochastics(Indicator):
    """
    An oscillator which can indicate when an asset may be over bought or over
    sold.

    Parameters
    ----------
    period_k : int
        The period for the K line.
    period_d : int
        The period for the D line.

    Raises
    ------
    ValueError
        If `period_k` is not positive (> 0).
    ValueError
        If `period_d` is not positive (> 0).

    References
    ----------
    https://www.forextraders.com/forex-education/forex-indicators/stochastics-indicator-explained/
    """
    period_k: int
    period_d: int
    _highs: deque
    _lows: deque
    _c_sub_l: deque
    _h_sub_l: deque
    value_k: float
    value_d: float

    def __init__(self, period_k: int, period_d: int, slowing: int = 1, ma_type = None, d_method: str = "ratio") -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, high: float, low: float, close: float) -> None: 
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        high : double
            The high price.
        low : double
            The low price.
        close : double
            The close price.

        """
        ...
    def _reset(self) -> None: ...


class CommodityChannelIndex(Indicator):
    """
    Commodity Channel Index is a momentum oscillator used to primarily identify
    overbought and oversold levels relative to a mean.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    scalar : double
        A positive float to scale the bands
    ma_type : MovingAverageType
        The moving average type for prices.

    References
    ----------
    https://www.tradingview.com/support/solutions/43000502001-commodity-channel-index-cci/
    """
    period: int
    scalar: float
    _prices: deque
    _ma: Any
    _mad: float
    value: float

    def __init__(self, period: int, scalar: float = 0.015, ma_type: Any = None) -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, high: float, low: float, close: float) -> None: 
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        high : double
            The high price.
        low : double
            The low price.
        close : double
            The close price.

        """
        ...
    def _reset(self) -> None: 
        """
        Reset the indicator.

        All stateful fields are reset to their initial value.
        """
        ...


class EfficiencyRatio(Indicator):
    """
    An indicator which calculates the efficiency ratio across a rolling window.
    The Kaufman Efficiency measures the ratio of the relative market speed in
    relation to the volatility, this could be thought of as a proxy for noise.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (>= 2).

    Raises
    ------
    ValueError
        If `period` is not >= 2.
    """
    period: int
    _inputs: deque
    _deltas: deque
    value: float

    def __init__(self, period: int) -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, price: float) -> None: 
        """
        Update the indicator with the given price.

        Parameters
        ----------
        price : double
            The update price.

        """
        ...
    def _reset(self) -> None: ...


class RelativeVolatilityIndex(Indicator):
    """
    The Relative Volatility Index (RVI) was created in 1993 and revised in 1995.
    Instead of adding up price changes like RSI based on price direction, the RVI
    adds up standard deviations based on price direction.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    scalar : double
        A positive float to scale the bands.
    ma_type : MovingAverageType
        The moving average type for the vip and vim (cannot be None).
    """
    period: int
    scalar: float
    _prices: deque
    _ma: Any
    _pos_ma: Any
    _neg_ma: Any
    _previous_close: float
    _std: float
    value: float

    def __init__(self, period: int, scalar: float = 100.0, ma_type: Any = None) -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, close: float) -> None: 
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        close : double
            The close price.

        """
        ...
    def _reset(self) -> None: 
        """
        Reset the indicator.

        All stateful fields are reset to their initial value.
        """
        ...


class PsychologicalLine(Indicator):
    """
    The Psychological Line is an oscillator-type indicator that compares the
    number of the rising periods to the total number of periods. In other
    words, it is the percentage of bars that close above the previous
    bar over a given period.

    Parameters
    ----------
    period : int
        The rolling window period for the indicator (> 0).
    ma_type : MovingAverageType
        The moving average type for the indicator (cannot be None).
    """
    period: int
    _ma: Any
    _diff: float
    _previous_close: float
    value: float

    def __init__(self, period: int, ma_type: Any = None) -> None: ...
    def handle_bar(self, bar: Bar) -> None: 
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(self, close: float) -> None: 
        """
        Update the indicator with the given raw value.

        Parameters
        ----------
        close : double
            The close price.

        """
        ...
    def _reset(self) -> None: ...