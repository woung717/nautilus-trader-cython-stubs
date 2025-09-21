from datetime import datetime
from nautilus_trader.indicators.averages import MovingAverageType
from nautilus_trader.indicators.base import Indicator
from nautilus_trader.model.data import Bar
import pandas as pd


class OnBalanceVolume(Indicator):
    """
    An indicator which calculates the momentum of relative positive or negative
    volume.

    Parameters
    ----------
    period : int
        The period for the indicator, zero indicates no window (>= 0).

    Raises
    ------
    ValueError
        If `period` is negative (< 0).
    """

    def __init__(self, period: int = 0) -> None: ...
    def handle_bar(self, bar: Bar) -> None:
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(
        self,
        open: float,
        close: float,
        volume: float,
    ) -> None:
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        open : float
            The high price.
        close : float
            The low price.
        volume : float
            The close price.

        """
        ...
    def _reset(self) -> None: ...

class VolumeWeightedAveragePrice(Indicator):
    """
    An indicator which calculates the volume weighted average price for the day.
    """

    def __init__(self) -> None: ...
    def handle_bar(self, bar: Bar) -> None:
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(
        self,
        price: float,
        volume: float,
        timestamp: datetime,
    ) -> None:
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        price : float
            The update price.
        volume : float
            The update volume.
        timestamp : datetime
            The current timestamp.

        """
        ...
    
    def _reset(self) -> None: ...

class KlingerVolumeOscillator(Indicator):
    """
    This indicator was developed by Stephen J. Klinger. It is designed to predict
    price reversals in a market by comparing volume to price.

    Parameters
    ----------
    fast_period : int
        The period for the fast moving average (> 0).
    slow_period : int
        The period for the slow moving average (> 0 & > fast_sma).
    signal_period : int
        The period for the moving average difference's moving average (> 0).
    ma_type : MovingAverageType
        The moving average type for the calculations.
    """

    def __init__(
        self,
        fast_period: int,
        slow_period: int,
        signal_period: int,
        ma_type: MovingAverageType = MovingAverageType.EXPONENTIAL,
    ) -> None: ...
    def handle_bar(self, bar: Bar) -> None:
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(
        self,
        high: float,
        low: float,
        close: float,
        volume: float,
    ) -> None:
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        high : float
            The high price.
        low : float
            The low price.
        close : float
            The close price.
        volume : float
            The volume.

        """
        ...

    def _reset(self) -> None: ...

class Pressure(Indicator):
    """
    An indicator which calculates the relative volume (multiple of average volume)
    to move the market across a relative range (multiple of ATR).

    Parameters
    ----------
    period : int
        The period for the indicator (> 0).
    ma_type : MovingAverageType
        The moving average type for the calculations.
    atr_floor : float
        The ATR floor (minimum) output value for the indicator (>= 0.).

    Raises
    ------
    ValueError
        If `period` is not positive (> 0).
    ValueError
        If `atr_floor` is negative (< 0).
    """

    def __init__(
        self,
        period: int,
        ma_type: MovingAverageType = MovingAverageType.EXPONENTIAL,
        atr_floor: float = 0,
    ) -> None: ...
    def handle_bar(self, bar: Bar) -> None:
        """
        Update the indicator with the given bar.

        Parameters
        ----------
        bar : Bar
            The update bar.

        """
        ...
    def update_raw(
        self,
        high: float,
        low: float,
        close: float,
        volume: float,
    ) -> None:
        """
        Update the indicator with the given raw values.

        Parameters
        ----------
        high : float
            The high price.
        low : float
            The low price.
        close : float
            The close price.
        volume : float
            The volume.

        """
        ...
    
    def _reset(self) -> None: ...