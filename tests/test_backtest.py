import numpy as np
import pandas as pd

from lib import backtest


def test_no_lookahead_position_earns_next_bar():
    close = pd.Series([100.0, 110.0, 121.0])
    res = backtest.run(close, pd.Series([1.0, 1.0, 1.0]))
    assert np.allclose(res.bars['net'], [0.0, 0.1, 0.1])
    # A position taken on the last bar must earn nothing yet.
    late = backtest.run(close, pd.Series([0.0, 0.0, 1.0]))
    assert late.bars['net'].sum() == 0


def test_buy_and_hold_matches_price_ratio():
    rng = np.random.default_rng(0)
    close = pd.Series(100 * np.exp(rng.normal(0, 0.01, 300).cumsum()))
    res = backtest.run(close, pd.Series(1.0, index=close.index))
    assert np.isclose(res.bars['equity'].iloc[-1], close.iloc[-1] / close.iloc[0])


def test_short_profits_from_fall():
    res = backtest.run(pd.Series([100.0, 90.0]), pd.Series([-1.0, -1.0]))
    assert np.isclose(res.bars['net'].iloc[1], 0.1)


def test_costs_charged_on_position_changes():
    close = pd.Series([100.0] * 4)
    res = backtest.run(close, pd.Series([0.0, 1.0, 1.0, 0.0]), cost_bps=10)
    assert np.allclose(res.bars['net'], [0, -0.001, 0, -0.001])
    rev = backtest.run(close, pd.Series([1.0, -1.0, -1.0, -1.0]), cost_bps=10)
    assert np.allclose(rev.bars['cost'], [0.001, 0.002, 0, 0])   # reversal trades 2 units


def test_trade_table():
    close = pd.Series([100.0, 100.0, 110.0, 121.0, 121.0, 108.9])
    pos = pd.Series([0.0, 1.0, 1.0, 0.0, -1.0, -1.0])
    trades = backtest.run(close, pos).trades
    assert len(trades) == 2
    long, short = trades.iloc[0], trades.iloc[1]
    assert long['side'] == 1 and long['bars'] == 2 and np.isclose(long['return'], 0.21) and not long['open']
    assert short['side'] == -1 and np.isclose(short['return'], 0.1) and short['open']
    with_cost = backtest.run(close, pos, cost_bps=10).trades
    assert np.isclose(with_cost.iloc[0]['return'], 0.999 * 1.21 * 0.999 - 1)
