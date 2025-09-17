import random
from typing import Optional, Dict, Any, Sequence


def make_signal(
    symbol: str,
    action: str,
    quantity: float,
    price: float,
    confidence: Optional[float] = None,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    sig: Dict[str, Any] = {
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "price": price,
    }
    if confidence is not None:
        sig["confidence"] = float(confidence)
    if reason is not None:
        sig["reason"] = str(reason)
    return sig


class MyStrategy:
    def __init__(self, **kwargs):
        self.symbol = str(kwargs.get("symbol", "BTCUSD")).upper()
        self.fast_period = max(1, int(kwargs.get("fast_period", 12)))
        self.slow_period = max(self.fast_period + 1, int(kwargs.get("slow_period", 26)))
        self.quantity = float(kwargs.get("quantity", 1.0))
        self.noise_quantity = max(1e-6, float(kwargs.get("noise_quantity", 0.001)))
        seed = kwargs.get("random_seed")
        self._rng = random.Random(seed)
        self._last_macd_sign: int = 0

    @staticmethod
    def _ema(values: Sequence[float], period: int) -> Optional[float]:
        if len(values) < period:
            return None
        multiplier = 2 / (period + 1)
        ema = sum(values[:period]) / period
        for price in values[period:]:
            ema = (price - ema) * multiplier + ema
        return ema

    @staticmethod
    def _select_symbol(target: str, bars: dict) -> tuple[str, Optional[dict]]:
        data = bars.get(target)
        if data is not None:
            return target, data
        for key, value in bars.items():
            if "BTC" in key.upper():
                return key, value
        return target, None

    def generate_signal(self, team: dict, bars: dict, current_prices: dict):
        symbol, data = self._select_symbol(self.symbol, bars)

        closes: list[float] = []
        if data:
            closes_raw = data.get("close") or []
            closes = [float(x) for x in closes_raw if x is not None]

        price_val = current_prices.get(symbol)
        if price_val is None and closes:
            price_val = closes[-1]
        if price_val is None:
            return None
        price = float(price_val)
        if price <= 0:
            return None

        fast: Optional[float] = None
        slow: Optional[float] = None
        macd: Optional[float] = None

        if len(closes) >= self.slow_period:
            fast = self._ema(closes, self.fast_period)
            slow = self._ema(closes, self.slow_period)
            if fast is not None and slow is not None:
                macd = fast - slow
                macd_sign = 1 if macd > 0 else -1 if macd < 0 else 0
                if macd_sign != 0 and macd_sign != self._last_macd_sign:
                    self._last_macd_sign = macd_sign
                    action = "buy" if macd_sign > 0 else "sell"
                    confidence = min(1.0, abs(macd) / price)
                    reason = (
                        f"MACD crossover detected for {symbol}: fast={fast:.2f}, slow={slow:.2f}"
                    )
                    return make_signal(
                        symbol,
                        action,
                        self.quantity,
                        price,
                        confidence=confidence,
                        reason=reason,
                    )
                if macd_sign == 0:
                    self._last_macd_sign = 0

        random_action = self._rng.choice(["buy", "sell"])
        macd_note = (
            f" | MACD fast={fast:.2f}, slow={slow:.2f}, spread={(macd or 0.0):.4f}"
            if fast is not None and slow is not None
            else ""
        )
        reason = f"Random heartbeat {random_action} for visibility{macd_note}"
        return make_signal(
            symbol,
            random_action,
            self.noise_quantity,
            price,
            confidence=0.05,
            reason=reason,
        )
