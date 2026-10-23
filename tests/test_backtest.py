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


def test_next_open_hand_values():
    close = pd.Series([100.0, 100.0, 110.0, 121.0])
    open_ = pd.Series([100.0, 102.0, 105.0, 120.0])
    res = backtest.run(close, pd.Series([1.0, 1.0, 0.0, 0.0]), fill='next_open', open_=open_)
    # Long from the open of bar 1 to the open of bar 3.
    assert np.allclose(res.bars['net'], [0, 100 / 102 - 1, 0.1, 120 / 110 - 1])
    assert np.isclose(res.bars['equity'].iloc[-1], 120 / 102)
    assert np.isclose(res.trades.iloc[0]['return'], 120 / 102 - 1)


def test_next_open_matches_research_002_engine():
    """Same formula as research/002-nifty-cycle-tools/run_tests.py, so results are interchangeable."""
    rng = np.random.default_rng(4)
    n = 300
    close = pd.Series(100 * np.exp(rng.normal(0, 0.01, n).cumsum()))
    open_ = close.shift(1).fillna(100) * np.exp(rng.normal(0, 0.003, n))
    pos = pd.Series(rng.choice([-1.0, 0.0, 1.0], n))
    cost = 0.0003
    before, after = pos.shift(2).fillna(0), pos.shift(1).fillna(0)
    ref = (1 + before * (open_ / close.shift(1) - 1)) * (1 + after * (close / open_ - 1)) - 1
    ref = ref.fillna(0) - (after - before).abs() * cost
    res = backtest.run(close, pos, cost_bps=3, fill='next_open', open_=open_)
    assert np.allclose(res.bars['net'], ref)


def test_next_open_trades_compound_to_bar_pnl_for_long_only():
    rng = np.random.default_rng(5)
    n = 250
    close = pd.Series(100 * np.exp(rng.normal(0, 0.01, n).cumsum()))
    open_ = close.shift(1).fillna(100) * np.exp(rng.normal(0, 0.003, n))
    pos = pd.Series((rng.random(n) > 0.5).astype(float))
    res = backtest.run(close, pos, cost_bps=5, fill='next_open', open_=open_)
    # Long/flat only, so trades never overlap and their product equals total equity.
    assert np.isclose(np.prod(1 + res.trades['return']), res.bars['equity'].iloc[-1])


def test_next_close_delays_one_bar():
    res = backtest.run(pd.Series([100.0, 110.0, 121.0]), pd.Series([1.0, 0.0, 0.0]), fill='next_close')
    assert np.allclose(res.bars['net'], [0, 0, 0.1])
    assert np.isclose(res.trades.iloc[0]['return'], 0.1)


def test_decision_on_last_bar_is_not_a_trade_yet():
    close, open_ = pd.Series([100.0, 101.0]), pd.Series([100.0, 100.5])
    res = backtest.run(close, pd.Series([0.0, 1.0]), fill='next_open', open_=open_)
    assert res.bars['net'].sum() == 0 and res.trades.empty


def test_next_open_requires_open():
    import pytest
    with pytest.raises(ValueError):
        backtest.run(pd.Series([1.0, 2.0]), pd.Series([1.0, 1.0]), fill='next_open')
