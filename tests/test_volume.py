import numpy as np
import pandas as pd
import pytest

from lib import volume as vol


def s(values):
    return pd.Series(values, dtype=float)


def test_obv_reproduces_kaufman_table_12_2():
    close = s([310, 315, 318, 316, 314, 320])
    volume = s([25, 30, 27, 15, 12, 28])
    assert vol.obv(close, volume).tolist() == [0, 30, 57, 42, 30, 58]


def test_basic_volume_measures():
    v = s([10, 20, 30, 40])
    assert vol.normalized_volume(v, 2).tolist()[1:] == [100 * 20 / 15, 100 * 30 / 25, 100 * 40 / 35]
    assert vol.volume_momentum(v, 2).tolist()[2:] == [20, 20]
    assert vol.volume_pct_change(v, 2).tolist()[2:] == [2.0, 1.0]
    assert vol.force_index(s([10, 12, 11]), s([5, 5, 5])).tolist()[1:] == [10, -5]


def test_volume_oscillator_methods():
    v = s([1, 2, 3, 4, 5, 6])
    assert np.isclose(vol.volume_oscillator(v, 2, 4, 'diff').iloc[-1], 5.5 - 4.5)
    assert np.isclose(vol.volume_oscillator(v, 2, 4, 'ratio').iloc[-1], 11 / 18)
    with pytest.raises(ValueError):
        vol.volume_oscillator(v, method='other')


def test_filtered_obv_skips_small_volume_and_small_moves():
    close = s([10, 11, 12, 13, 14, 15, 14])
    volume = s([100, 100, 100, 100, 100, 100, 1])        # last day: tiny volume
    full = vol.obv(close, volume)
    f = vol.filtered_obv(close, volume, n=3, volume_sd=1)
    assert f.iloc[-1] == f.iloc[-2] and full.iloc[-1] != full.iloc[-2]
    tiny_move = s([10, 11, 12, 13, 13.01])
    p = vol.filtered_obv(tiny_move, s([1, 1, 1, 1, 1]), n=3, price_sd=0)
    assert p.iloc[-1] == p.iloc[-2]                       # 0.01 move is below the average move


def test_money_flow_index_bounds_and_extremes():
    up = s(np.arange(1, 30))                          # typical price rises every day: no negative flow
    assert np.allclose(vol.money_flow_index(up, up, up, s(np.ones(29)), 14).dropna(), 100)
    rng = np.random.default_rng(0)
    c = s(100 + rng.normal(0, 1, 300).cumsum())
    mfi = vol.money_flow_index(c + 1, c - 1, c, s(rng.integers(1, 100, 300)), 14).dropna()
    assert mfi.between(0, 100).all()


def test_volume_count_and_chaikin_family():
    assert vol.volume_count_indicator(s([5, 6, 4, 4, 9])).tolist() == [0, 1, 0, 0, 1]
    h, l = s([10, 10]), s([8, 8])
    # close at the high -> all volume to buyers; at the mid -> none.
    assert vol.volume_accumulator(h, l, s([10, 9]), s([50, 50])).tolist() == [50, 50]
    assert vol.accumulation_distribution(s([8, 8]), h, l, s([10, 9]), s([50, 50])).tolist() == [50, 75]
    assert vol.intraday_intensity(h, l, s([10, 8]), s([50, 50])).tolist() == [50, 0]


def test_price_volume_trend():
    assert np.allclose(vol.price_volume_trend(s([100, 110, 99]), s([1, 10, 10])), [0, 1, 0])


def test_positive_negative_volume_index():
    close = s([100, 110, 99, 99])
    volume = s([10, 20, 15, 30])
    pn = vol.positive_negative_volume_index(close, volume, 'close')
    assert pn['pvi'].tolist() == [0, 20, 20, 20] and pn['nvi'].tolist() == [0, 0, 15, 15]
    fb = vol.positive_negative_volume_index(close, volume, 'fosback')
    assert np.allclose(fb['pvi'], [100, 110, 110, 110])   # volume up on day 1 (+10%) and day 3 (0%)
    assert np.allclose(fb['nvi'], [100, 100, 90, 90])     # volume down on day 2 (-10%)


def test_demand_oscillator_hand_value():
    # H = 101, L = 99 every day -> 2-day range 2, K = 3 x C / 2.
    close = s([100] * 10 + [102])
    d = vol.demand_oscillator(s([101] * 11), s([99] * 11), close, s([1000] * 11))
    k = 3 * 102 / 2
    assert np.isclose(d.iloc[-1], 1000 - 1000 / (k * 0.02))
    # A small up move (K x |%| < 1) makes the scaled selling pressure exceed buying pressure.
    small = vol.demand_oscillator(s([101] * 11), s([99] * 11), s([100] * 10 + [100.2]), s([1000] * 11))
    assert small.iloc[-1] < 0


def test_vwmacd_equal_volume_is_sma_macd():
    rng = np.random.default_rng(2)
    c = s(100 + rng.normal(0, 1, 80).cumsum())
    line, _ = vol.vwmacd(c, s(np.ones(80)))
    assert np.allclose(line.dropna(), (c.rolling(12).mean() - c.rolling(26).mean()).dropna())


def test_elastic_vwma():
    out = vol.elastic_vwma(s([10, 20]), s([0, 50]), 100)
    assert out.tolist() == [10, 15]                        # half the shares traded at 20


def test_volume_spike_uses_lagged_average():
    v = s([100] * 30 + [150, 220, 250])
    spikes = vol.volume_spike(v, n=20, multiple=2.0, lag=5)
    assert spikes.tolist()[-3:] == [False, True, True]     # threshold stays at 2 x 100


def test_market_facilitation_index():
    assert vol.market_facilitation_index(s([12]), s([10]), s([4])).iloc[0] == 0.5


# --- Breadth -----------------------------------------------------------------------

A, D, U = s([300, 200, 250]), s([200, 300, 250]), s([50, 50, 100])
AV, DV = s([6e6, 2e6, 3e6]), s([2e6, 6e6, 3e6])


def test_ad_line_sign_is_corrected():
    assert vol.ad_oscillator(A, D).tolist() == [100, -100, 0]
    assert vol.ad_line(A, D).tolist() == [100, 0, 0]


def test_bolton_tremblay_handles_negative_days():
    bt = vol.bolton_tremblay(A, D, U)
    assert np.allclose(bt, [np.sqrt(2), 0, 0])             # +sqrt(2), then -sqrt(2), then 0


def test_schultz_and_mcclellan():
    assert vol.schultz(A, A + D + U).tolist()[0] == 100 * 300 / 550
    mc = vol.mcclellan_oscillator(s([10] * 200), s([0] * 200))
    assert abs(mc.iloc[-1]) < 1e-3                          # constant net advances -> oscillator -> 0


def test_trin_thrust_udr_demand_index():
    assert np.allclose(vol.trin(A, D, AV, DV), [1.5 / 3, (2 / 3) / (1 / 3), 1])
    to = vol.thrust_oscillator(A, D, AV, DV)
    assert np.isclose(to.iloc[0], 100 * (300 * 6e6 - 200 * 2e6) / (300 * 6e6 + 200 * 2e6))
    assert to.iloc[2] == 0
    assert vol.upside_downside_ratio(AV, DV).tolist() == [3, 1 / 3, 1]
    assert np.isclose(vol.demand_index(AV, DV, 3).iloc[-1], 11 / 11)


def test_high_low_index_ratio_and_chadtp():
    nh, nl = s([5, 0, 3]), s([1, 4, 0])
    assert vol.high_low_index(nh, nl).tolist() == [4, 0, 3]
    assert np.isclose(vol.high_low_ratio(nh, nl, 3).iloc[-1], 8 / 13)
    assert vol.chadtp(A, D, 3).iloc[-1] == (750 - 750) / 3
