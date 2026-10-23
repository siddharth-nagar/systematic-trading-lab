"""NNN-strategy-name. Rules must match HYPOTHESIS.md exactly.

Run from the repository root: python strategies/NNN-strategy-name/strategy.py
"""
from pathlib import Path

import pandas as pd

from lib import backtest, indicators, metrics, signals  # noqa: F401  (use the shared, tested code)

HERE = Path(__file__).resolve().parent


def positions(df, params):
    """Return a position Series (-1/0/1 or sizes) decided on each bar's close."""
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit("Copy this template and implement positions() after writing HYPOTHESIS.md.")
