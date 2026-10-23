"""The one backtest engine used by every strategy.

Timing rule (no look-ahead): position[t] is decided with data up to the close of bar t.
It is then executed according to `fill`:

- 'close'      : at the close of bar t (needs an order placed just before the close);
- 'next_open'  : at the open of bar t+1 (needs `open_`); the default protocol in Research 002
                 and the Chapter 8 lab;
- 'next_close' : at the close of bar t+1.

Costs (`cost_bps` per unit of position traded) are charged on the bar where the trade happens.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

FILLS = ('close', 'next_open', 'next_close')


@dataclass
class BacktestResult:
    bars: pd.DataFrame      # per-bar: close, position, held, gross, cost, net, equity
    trades: pd.DataFrame    # one row per completed or open trade


def run(close, position, cost_bps=0.0, fill='close', open_=None):
    """Backtest a target position series (any real number, e.g. -1/0/1 or fractional sizing)."""
    if fill not in FILLS:
        raise ValueError(f'fill must be one of {FILLS}')
    if fill == 'next_open' and open_ is None:
        raise ValueError("fill='next_open' needs open_")
    close = close.astype(float)
    position = position.reindex(close.index).fillna(0.0).astype(float)
    c = cost_bps / 1e4

    if fill == 'next_open':
        o = open_.reindex(close.index).astype(float)
        before = position.shift(2).fillna(0.0)   # held through the overnight gap into bar t
        after = position.shift(1).fillna(0.0)    # held from the open of bar t
        gross = ((1 + before * (o / close.shift(1) - 1)) * (1 + after * (close / o - 1)) - 1).fillna(0.0)
        held = after
        turnover = (after - before).abs()
    else:
        executed = position if fill == 'close' else position.shift(1).fillna(0.0)
        held = executed.shift(1).fillna(0.0)
        gross = held * close.pct_change().fillna(0.0)
        turnover = executed.diff().abs().fillna(executed.abs())   # first bar trades from flat

    cost = turnover * c
    net = gross - cost
    bars = pd.DataFrame({'close': close, 'position': position, 'held': held,
                         'gross': gross, 'cost': cost, 'net': net,
                         'equity': (1 + net).cumprod()})
    if fill == 'next_open':
        bars.insert(0, 'open', o)
    bars.attrs.update(cost_bps=cost_bps, fill=fill)
    return BacktestResult(bars=bars, trades=_trades(bars))


def _trades(bars):
    """Group consecutive bars with the same non-zero decided position into trades.

    A trade decided on bars s..e-1 (the decision changes on bar e) is entered and exited at the
    fill prices implied by `fill`. Its return compounds side * the price returns while held and
    pays |side| * cost on entry and again on exit, so a reversal (turnover 2) charges one unit
    to each trade. Resizing (e.g. 1 -> 0.5) is treated as exit + new entry, which overstates
    its cost in this table only; the per-bar P&L in `bars` is always exact.
    """
    fill = bars.attrs['fill']
    unit_cost = bars.attrs['cost_bps'] / 1e4
    pos = bars['position'].to_numpy()
    close = bars['close'].to_numpy()
    n = len(pos)
    cc = np.r_[0.0, close[1:] / close[:-1] - 1]                    # close-to-close return of bar t
    if fill == 'next_open':
        op = bars['open'].to_numpy()
        overnight = np.r_[0.0, op[1:] / close[:-1] - 1]            # close t-1 -> open t
        intraday = close / op - 1                                  # open t -> close t
    lag = 0 if fill == 'close' else 1                              # bars between decision and fill
    idx = bars.index
    rows = []
    i = 0
    while i < n:
        if pos[i] == 0:
            i += 1
            continue
        side, s = pos[i], i
        while i + 1 < n and pos[i + 1] == side:
            i += 1
        entry, exit_ = s + lag, i + 1 + lag                        # fill bars
        if entry > n - 1:                                          # decided on the last bar: not filled yet
            break
        is_open = exit_ > n - 1
        last = n - 1 if is_open else exit_
        if fill == 'next_open':
            growth = 1 + side * intraday[entry]
            for t in range(entry + 1, last + 1):
                growth *= 1 + side * overnight[t]
                if t < exit_:                                      # the exit fills at the open of exit_
                    growth *= 1 + side * intraday[t]
        else:
            growth = np.prod(1 + side * cc[entry + 1:last + 1])
        growth *= 1 - abs(side) * unit_cost
        if not is_open:
            growth *= 1 - abs(side) * unit_cost
        rows.append({'entry': idx[entry], 'exit': None if is_open else idx[exit_], 'side': side,
                     'bars': last - entry, 'return': growth - 1, 'open': is_open})
        i += 1
    return pd.DataFrame(rows, columns=['entry', 'exit', 'side', 'bars', 'return', 'open'])
