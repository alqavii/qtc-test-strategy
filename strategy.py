from typing import Optional, Dict, Any


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
        self.params = kwargs

    def generate_signal(self, team: dict, bars: dict, current_prices: dict):
        # Example no-op: replace with your own logic
        return None
