import importlib.util
from pathlib import Path


def load_strategy_class(path: Path, class_name: str):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)  # type: ignore[attr-defined]
    return getattr(mod, class_name)


def test_generate_signal_shape():
    StrategyCls = load_strategy_class(Path(__file__).parents[1] / "strategy.py", "MyStrategy")
    strat = StrategyCls()

    team = {"id": "t1", "name": "Test", "cash": 100000, "params": {}, "api": object()}
    bars = {"AAPL": {"timestamp": ["2025-01-01T00:00:00Z"], "open": [1.0], "high": [1.0], "low": [1.0], "close": [1.0], "volume": [100]}}
    prices = {"AAPL": 1.0}

    out = strat.generate_signal(team, bars, prices)

    if out is None:
        return

    assert isinstance(out, dict)
    for k in ("symbol", "action", "quantity", "price"):
        assert k in out
    assert out["action"] in ("buy", "sell")

