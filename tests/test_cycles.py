import numpy as np

from lib import cycles


def test_periodogram_finds_planted_period():
    t = np.arange(500)
    spec = cycles.periodogram(np.sin(2 * np.pi * t / 25))
    assert spec.idxmax() == 25


def test_top_periods_of_three_waves():
    t = np.arange(1000)
    x = sum(a * np.sin(2 * np.pi * t / p) for a, p in [(1, 10), (2, 20), (4, 40)])
    assert sorted(cycles.top_periods(cycles.periodogram(x))) == [10, 20, 40]


def test_single_frequency_fit_recovers_period():
    t = np.arange(1, 161)
    f = cycles.single_frequency_fit(3 + 0.1 * t + 2 * np.sin(2 * np.pi * t / 16))
    assert abs(f['period'] - 16) < 0.5


def test_max_peak_test_detects_cycle_and_is_reproducible():
    rng = np.random.default_rng(3)
    x = np.sin(2 * np.pi * np.arange(400) / 20) + rng.normal(0, 0.5, 400)
    _, period, p, _ = cycles.max_peak_test(x, 4, 100, n_perm=200, seed=5)
    assert abs(period - 20) < 1 and p < 0.01
    assert cycles.max_peak_test(x, 4, 100, n_perm=200, seed=5)[2] == p


def test_turning_point_spacing_of_sine():
    x = np.sin(2 * np.pi * np.arange(200) / 20)
    assert np.all(cycles.turning_point_spacing(x) == 20)


def _price(n=900, seed=7):
    import pandas as pd
    rng = np.random.default_rng(seed)
    return pd.Series(1000 * np.exp(np.cumsum(rng.normal(0.0004, 0.01, n))))


def test_highpass_removes_a_steady_trend():
    import pandas as pd
    trend = pd.Series(np.exp(0.001 * np.arange(600)) * 100)
    out = cycles.highpass_detrend(trend).dropna()
    assert out.abs().max() < 1e-3


def test_research_002_tools_are_causal():
    price = _price()
    full = cycles.highpass_detrend(price)
    mesa_full = cycles.mesa_burg(full)
    for cut in (400, 650, 899):
        part = cycles.highpass_detrend(price.iloc[:cut])
        assert np.isclose(full.iloc[cut - 1], part.iloc[-1])
        mesa_part = cycles.mesa_burg(part)
        assert np.allclose(mesa_full.iloc[cut - 1].to_numpy(), mesa_part.iloc[-1].to_numpy(), equal_nan=True)


def test_mesa_finds_a_20_bar_cycle():
    import pandas as pd
    t = np.arange(400)
    x = pd.Series(np.sin(2 * np.pi * t / 20) + np.random.default_rng(1).normal(0, 0.3, 400))
    assert abs(cycles.mesa_burg(x)['dom_period'].iloc[100:].median() - 20) <= 1


def test_cycle_mode_on_sine_and_noise():
    import pandas as pd
    from lib.indicators import hilbert_phase
    t = np.arange(300)
    phase = hilbert_phase(np.sin(2 * np.pi * t / 20), 20)
    dphase = (phase - phase.shift(1)) % 360
    assert cycles.cycle_mode(dphase).iloc[50:].all()
    noise = hilbert_phase(np.random.default_rng(2).normal(0, 1, 300), 20)
    assert cycles.cycle_mode((noise - noise.shift(1)) % 360).iloc[50:].mean() < 0.5


def test_lib_copies_match_research_002():
    import importlib.util
    import pathlib
    path = pathlib.Path(__file__).parents[1] / 'research' / '002-nifty-cycle-tools' / 'cycle_tools.py'
    spec = importlib.util.spec_from_file_location('ct', path)
    ct = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ct)
    price = _price(500)
    assert np.allclose(cycles.highpass_detrend(price), ct.highpass_detrend(price), equal_nan=True)
    hp = cycles.highpass_detrend(price)
    assert np.allclose(cycles.mesa_burg(hp), ct.mesa_burg(hp), equal_nan=True)
