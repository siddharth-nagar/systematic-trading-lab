"""The one backtest engine used by every strategy.

Timing rule (no look-ahead): position[t] is decided with data up to the close of bar t and
traded at that close. It earns the return from close t to close t+1. Costs are charged on
the bar where the position changes.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    bars: pd.DataFrame      # per-bar: close, position, held, gross, cost, net, equity
    trades: pd.DataFrame    # one row per completed or open trade


def run(close, position, cost_bps=0.0):
    """Backtest a target position series (any real number, e.g. -1/0/1 or fractional sizing).

    cost_bps: cost per unit of position traded, in basis points of price (commission + slippage).
    """
    close = close.astype(float)
    position = position.reindex(close.index).fillna(0.0).astype(float)
    ret = close.pct_change().fillna(0.0)
    held = position.shift(1).fillna(0.0)                     # position earning this bar's return
    turnover = position.diff().abs().fillna(position.abs())  # first bar trades from flat
    gross = held * ret
    cost = turnover * cost_bps / 1e4
    net = gross - cost
    bars = pd.DataFrame({'close': close, 'position': position, 'held': held,
                         'gross': gross, 'cost': cost, 'net': net,
                         'equity': (1 + net).cumprod()})
    bars.attrs['cost_bps'] = cost_bps
    return BacktestResult(bars=bars, trades=_trades(bars))


def _trades(bars):
    """Group consecutive bars with the same non-zero position into trades.

    A trade entered at the close of bar s and exited at the close of bar e earns
    side * return over bars s+1..e. It pays |side| * cost on entry and again on exit,
    so a reversal (turnover 2) charges one unit to each trade.
    Resizing (e.g. 1 -> 0.5) is treated as exit + new entry, which overstates its cost in this
    table only; the per-bar P&L in `bars` is always exact.
    """
    pos = bars['position'].to_numpy()
    ret = bars['close'].pct_change().fillna(0.0).to_numpy()
    unit_cost = bars.attrs['cost_bps'] / 1e4
    idx = bars.index
    rows = []
    i, n = 0, len(pos)
    while i < n:
        if pos[i] == 0:
            i += 1
            continue
        side, start = pos[i], i
        while i + 1 < n and pos[i + 1] == side:
            i += 1
        is_open = i + 1 >= n
        end = i if is_open else i + 1                      # bar on whose close we exit
        growth = (1 - abs(side) * unit_cost) * np.prod(1 + side * ret[start + 1:end + 1])
        if not is_open:
            growth *= 1 - abs(side) * unit_cost
        rows.append({'entry': idx[start], 'exit': None if is_open else idx[end], 'side': side,
                     'bars': end - start, 'return': growth - 1, 'open': is_open})
        i += 1
    return pd.DataFrame(rows, columns=['entry', 'exit', 'side', 'bars', 'return', 'open'])
