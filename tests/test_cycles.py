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
