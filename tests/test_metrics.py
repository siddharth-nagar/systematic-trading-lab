import numpy as np
import pandas as pd

from lib import backtest, metrics


def test_max_drawdown_hand_value():
    assert np.isclose(metrics.max_drawdown(pd.Series([0.1, -0.5, 0.2])), -0.5)
    assert np.isclose(metrics.max_drawdown(pd.Series([-0.1, 0.05])), -0.1)   # loss from start


def test_cagr_doubling_in_one_year():
    r = pd.Series(np.full(252, 2 ** (1 / 252) - 1))
    assert np.isclose(metrics.cagr(r, 252), 1.0)


def test_sharpe_edge_cases():
    assert np.isnan(metrics.sharpe(pd.Series([0.01] * 10), 252))
    assert np.isclose(metrics.sharpe(pd.Series([0.01, -0.01] * 50), 252), 0)


def test_profit_factor():
    assert np.isclose(metrics.profit_factor(pd.Series([0.1, -0.05, 0.2, -0.1])), 2.0)


def test_summary_runs_on_backtest():
    close = pd.Series([100.0, 100.0, 110.0, 121.0, 121.0, 108.9])
    res = backtest.run(close, pd.Series([0.0, 1.0, 1.0, 0.0, -1.0, -1.0]))
    out = metrics.summary(res, 252)
    assert out['trades'] == 1 and out['win_rate'] == 1.0
    assert np.isclose(out['total_return'], 1.21 * 1.1 - 1)
