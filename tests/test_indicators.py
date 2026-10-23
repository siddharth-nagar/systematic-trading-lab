import numpy as np
import pandas as pd
import pytest

from lib import indicators as ind


def s(values):
    return pd.Series(values, dtype=float)


def test_sma_ema_wma_hand_values():
    assert ind.sma(s([1, 2, 3, 4]), 2).tolist()[1:] == [1.5, 2.5, 3.5]
    assert np.allclose(ind.ema(s([1, 2, 4]), 3), [1, 1.5, 2.75])      # alpha = 0.5
    assert np.isclose(ind.wma(s([1, 2, 3]), 3).iloc[-1], 14 / 6)


def test_triangular_weights_match_book_and_sum_to_period():
    assert np.allclose(ind.triangular_weights(10), [0.4, 0.8, 1.2, 1.6, 2.0, 1.6, 1.2, 0.8, 0.4])
    for p in (10, 20, 40):
        assert np.isclose(ind.triangular_weights(p).sum(), p)


def test_tma_of_ramp_lags_by_half_window():
    ramp = s(np.arange(50))
    out = ind.tma(ramp, 10)                       # 9 weights -> centre lags 4 bars
    assert np.allclose(out.dropna(), ramp.iloc[8:] - 4)
    assert np.allclose(ind.triangular_macd(s(np.full(60, 7.0)), 20).dropna(), 0)


def test_momentum():
    assert ind.momentum(s([1, 3, 6, 10]), 2).tolist()[2:] == [5, 7]


def test_rsi_extremes_and_bounds():
    assert np.allclose(ind.rsi_wilder(s(np.arange(1, 40)), 14).dropna(), 100)
    assert np.allclose(ind.rsi_wilder(s(np.arange(40, 1, -1)), 14).dropna(), 0)
    rng = np.random.default_rng(0)
    r = ind.rsi_wilder(s(100 + rng.normal(0, 1, 500).cumsum()), 14).dropna()
    assert r.between(0, 100).all()
    assert ind.rsi_wilder(s(np.arange(20)), 14).iloc[:14].isna().all()


def test_stochastic_at_range_extremes():
    high, low = s([10, 11, 12, 13]), s([8, 9, 10, 11])
    assert ind.stochastic_k(high, low, s([9, 10, 11, 13]), 3).iloc[-1] == 100
    assert ind.stochastic_k(high, low, s([9, 10, 11, 9]), 3).iloc[-1] == 0


def test_macd_of_constant_is_zero():
    line, signal, hist = ind.macd(s(np.full(100, 50.0)))
    assert np.allclose(line, 0) and np.allclose(signal, 0) and np.allclose(hist, 0)


def test_true_range_uses_previous_close_gap():
    tr = ind.true_range(s([11, 15]), s([9, 12]), s([10, 13]))
    assert tr.iloc[1] == 5                         # high 15 - previous close 10


def test_atr_of_constant_range():
    n = 40
    out = ind.atr(s(np.full(n, 12.0)), s(np.full(n, 10.0)), s(np.full(n, 11.0)), 14)
    assert np.allclose(out.dropna(), 2.0)


def test_efficiency_ratio_line_and_zigzag():
    assert np.allclose(ind.efficiency_ratio(s(np.arange(30.0)), 10).dropna(), 1)
    assert np.allclose(ind.efficiency_ratio(s([1, 2] * 15), 2).dropna(), 0)


def test_adx_strong_uptrend():
    t = np.arange(200.0)
    out = ind.adx(s(t + 1), s(t), s(t + 0.5), 14)
    assert out['minus_di'].dropna().eq(0).all()
    assert out['adx'].iloc[-1] > 99


def test_cci_of_ramp_is_exactly_100():
    ramp = s(np.arange(10.0))
    out = ind.cci(ramp, ramp, ramp, 4)             # x - mean = 1.5, mean deviation = 1
    assert np.allclose(out.dropna(), 100)


def test_fisher_and_inverse_fisher_bounds():
    rng = np.random.default_rng(1)
    price = s(100 + rng.normal(0, 1, 400).cumsum())
    fish = ind.fisher_transform(price, 12).dropna()
    assert np.isfinite(fish).all()
    assert fish.abs().max() <= 0.5 * np.log(1.999 / 0.001) + 1e-9
    assert ind.inverse_fisher_rsi(price).dropna().between(-100, 100).all()


@pytest.mark.parametrize('period', [15, 20, 30])
def test_hilbert_phase_advances_360_over_period(period):
    sine = np.sin(2 * np.pi * np.arange(300) / period)
    steps = np.diff(ind.hilbert_phase(sine, period).dropna().to_numpy()) % 360
    assert abs(np.median(steps) - 360 / period) < 1


def test_regression_slope_of_line():
    assert np.allclose(ind.regression_slope(s(3 + 0.5 * np.arange(30)), 10).dropna(), 0.5)
