from nautilus_trader.backtest.config import SimulationModuleConfig
from nautilus_trader.model.enums import PositionSide
from nautilus_trader.backtest.engine import SimulatedExchange
from nautilus_trader.backtest.modules import SimulationModule
from nautilus_trader.common.component import Logger, TimeEvent
from nautilus_trader.core.data import Data
from nautilus_trader.model.events.order import OrderFilled
from nautilus_trader.model.instruments.base import Instrument
from nautilus_trader.model.instruments.crypto_option import CryptoOption
from nautilus_trader.model.instruments.option_contract import OptionContract
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.model.position import Position


class OptionExerciseConfig(SimulationModuleConfig):
    auto_exercise_enabled: bool


class OptionExerciseModule(SimulationModule):
    def __init__(self, config: OptionExerciseConfig) -> None: ...

    def reset(self) -> None: ...

    def log_diagnostics(self, logger: Logger) -> None: ...

    def register_venue(self, exchange: SimulatedExchange) -> None: ...

    def pre_process(self, data: Data) -> None: ...

    def process(self, ts_now: int) -> None: ...

    def on_position_event(self, event) -> None: ...

    def _cleanup_timer_if_no_positions(self, expiry_ns: int) -> None: ...

    def _on_expiry_timer(self, event: TimeEvent) -> None: ...

    def _process_expiring_options(self, ts_now: int) -> None: ...

    def _process_option_expiry(
        self,
        option: OptionContract | CryptoOption,
        ts_now: int,
    ) -> None: ...

    def _get_underlying_price(
        self,
        option: OptionContract | CryptoOption,
    ) -> Price | None: ...

    def _should_exercise(
        self,
        option: OptionContract | CryptoOption,
        underlying_price: Price,
    ) -> bool: ...

    def _is_option_itm(
        self,
        option: OptionContract | CryptoOption,
        underlying_price: Price,
    ) -> tuple[bool, float]: ...

    def _generate_otm_expiry_events(
        self,
        option: OptionContract | CryptoOption,
        position: Position,
        ts_now: int,
    ) -> None: ...

    def _exercise(
        self,
        option: OptionContract | CryptoOption,
        position: Position,
        underlying_price: Price,
        ts_now: int,
    ) -> None: ...

    def _calculate_underlying_position(
        self,
        option: OptionContract | CryptoOption,
        position,
    ) -> tuple[Quantity, PositionSide]: ...

    def _generate_cash_settlement_events(
        self,
        option: OptionContract | CryptoOption,
        position: Position,
        underlying_price: Price,
        ts_now: int,
    ) -> None: ...

    def _create_cash_settlement_fill(
        self,
        option,
        position,
        settlement_price: Price,
        trade_id_suffix: str,
        venue_id_suffix: str,
        ts_now: int,
    ) -> OrderFilled: ...

    def _generate_physical_settlement_events(
        self,
        option: OptionContract | CryptoOption,
        position: Position,
        underlying_instrument,
        underlying_quantity: Quantity,
        underlying_side: PositionSide,
        underlying_price: Price,
        ts_now: int,
    ) -> None: ...

    def _calculate_settlement_price(
        self,
        option,
        underlying_price: Price,
    ) -> Price: ...

    def _get_underlying_instrument(self, option: object) -> Instrument: ...

    def _create_option_fill(
        self,
        option,
        position,
        trade_id_suffix: str,
        venue_id_suffix: str,
        ts_now: int,
        use_avg_price: bool = True,
    ) -> OrderFilled: ...

    def _create_underlying_fill(
        self,
        position,
        underlying_instrument,
        quantity: Quantity,
        side: PositionSide,
        price: Price,
        trade_id_suffix: str,
        venue_id_suffix: str,
        ts_now: int,
    ) -> OrderFilled: ...

    def _send_events(self, events: list) -> None: ...