Strategy Quickstart
===================

This starter shows how to build a minimal strategy that plugs into the QTC Alpha orchestrator.

Contract
--------
- Provide a file `strategy.py` with a class named `MyStrategy` (or your class) and set entry point in the registry as `strategy:MyStrategy`.
- Implement:
  - `__init__(self, **kwargs)` to accept optional params
  - `generate_signal(self, team: dict, bars: dict, current_prices: dict) -> dict | None`
- Return `None` to take no action, or a dict (StrategySignal):
  { "symbol": str, "action": "buy"|"sell", "quantity": number, "price": number, "confidence"?: float, "reason"?: str }

Inputs provided each minute
---------------------------
- team: { id, name, cash, params, api }
- bars: { ticker: { timestamp: [...], open: [...], high: [...], low: [...], close: [...], volume: [...] } }
- current_prices: { ticker: price }

Reading stored price data
-------------------------
Use the provided data API object on the team dict:

```
api = team["api"]
hist = api.getLastN("AAPL", 200)          # pandas DataFrame
day = api.getDay("AAPL", date(2025, 1, 15))
span = api.getRange("AAPL", start_dt, end_dt)
```

Allowed imports
---------------
- Only: numpy, pandas, scipy, and safe stdlib modules (math, statistics, decimal, collections, typing)
- No file I/O, no network calls, no os/subprocess.

Testing locally
---------------
```
python -m pytest -q
```

See `tests/test_strategy.py` for a basic shape/health check.


