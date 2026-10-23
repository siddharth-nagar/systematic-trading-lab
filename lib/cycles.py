"""Spectral and cycle-fitting tools (Kaufman Ch 11)."""
import numpy as np
import pandas as pd


def periodogram(x):
    """Power at each period (bars), from the FFT of the de-meaned series. Index = period."""
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    power = np.abs(np.fft.rfft(x)) ** 2 / n
    freq = np.fft.rfftfreq(n)
    keep = freq > 0
    return pd.Series(power[keep], index=1 / freq[keep], name='power').sort_index()


def top_periods(spec, k=3, min_period=2):
    """Periods of the k largest local peaks in a periodogram."""
    s = spec[spec.index >= min_period]
    peaks = s[(s > s.shift(1, fill_value=0)) & (s > s.shift(-1, fill_value=0))]
    return peaks.nlargest(k).index.to_numpy()


def single_frequency_fit(y):
    """Kaufman pp. 500-502: linear detrend, alpha = sum(cd)/sum(c^2), cos(w) = alpha/2,
    then least squares for a*cos(wt) + b*sin(wt). Angles are in degrees per bar."""
    y = np.asarray(y, float)
    x = np.arange(1, len(y) + 1)
    slope, intercept = np.polyfit(x, y, 1)
    r = y - (intercept + slope * x)
    c, d = r[1:-1], r[:-2] + r[2:]
    alpha = (c * d).sum() / (c * c).sum()
    omega = np.degrees(np.arccos(alpha / 2))
    X = np.column_stack([np.cos(np.radians(omega * x)), np.sin(np.radians(omega * x))])
    a, b = np.linalg.lstsq(X, r, rcond=None)[0]
    return dict(intercept=intercept, slope=slope, sum_c2=(c * c).sum(), sum_cd=(c * d).sum(),
                alpha=alpha, omega_deg=omega, period=360 / omega, a=a, b=b, x=x,
                trend=intercept + slope * x, fitted_cycle=X @ [a, b])


def max_peak_test(returns, min_period, max_period, n_perm=5000, seed=1101):
    """Permutation test for any cycle: largest periodogram value in the band vs shuffled returns.

    Returns (observed max power, its period, p-value, null maxima).
    """
    rng = np.random.default_rng(seed)
    r = np.asarray(returns, float)

    def stat(x):
        spec = periodogram(x)
        band = spec[(spec.index >= min_period) & (spec.index <= max_period)]
        return band.max(), band.idxmax()

    observed, at_period = stat(r)
    null = np.array([stat(rng.permutation(r))[0] for _ in range(n_perm)])
    p = ((null >= observed).sum() + 1) / (n_perm + 1)
    return observed, at_period, p, null


def turning_point_spacing(x):
    """Bars between successive local peaks."""
    s = np.sign(np.diff(np.asarray(x)))
    peaks = np.flatnonzero((s[:-1] > 0) & (s[1:] <= 0)) + 1
    return np.diff(peaks)
