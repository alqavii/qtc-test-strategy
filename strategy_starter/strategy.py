from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy import make_signal, MyStrategy  # noqa: E402

__all__ = ["make_signal", "MyStrategy"]
