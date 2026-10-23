"""Spectral and cycle-fitting tools (Kaufman Ch 11).

highpass_detrend, cycle_mode, burg and mesa_burg are copied unchanged from
research/002-nifty-cycle-tools/cycle_tools.py, where they were checked for causality.
"""
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


# --- Causal tools from Research 002 -----------------------------------------

def highpass_detrend(price, cutoff=48):
    """Remove trend causally. Input: price series. Output: detrended, lightly smoothed series.

    Uses 100*ln(price) so the scale is comparable in 2002 (~1,000) and 2026 (~25,000).
    Ehlers 2-pole high-pass: passes cycles shorter than ~`cutoff` bars, removes longer swings/trend.
    The 4-bar WMA (4,3,2,1)/10 removes 2-3 bar noise.
    """
    x = 100 * np.log(np.asarray(price, dtype=float))
    w = 0.707 * 2 * np.pi / cutoff
    a = (np.cos(w) + np.sin(w) - 1) / np.cos(w)
    hp = np.zeros_like(x)
    for t in range(2, len(x)):
        hp[t] = ((1 - a / 2) ** 2 * (x[t] - 2 * x[t - 1] + x[t - 2])
                 + 2 * (1 - a) * hp[t - 1] - (1 - a) ** 2 * hp[t - 2])
    sm = np.full_like(hp, np.nan)
    sm[3:] = (4 * hp[3:] + 3 * hp[2:-1] + 2 * hp[1:-2] + hp[:-3]) / 10
    out = pd.Series(sm, index=getattr(price, "index", None))
    out.iloc[:2 * cutoff] = np.nan          # filter warm-up
    return out


def cycle_mode(dphase, lookback=10, min_period=6, max_period=50, need=8):
    """Phase-regularity rule (Kaufman p.514: a regular sawtooth means a cycle is present).

    A bar is 'cycle-like' when the phase advanced by 360/max_period .. 360/min_period degrees.
    Cycle mode = at least `need` of the last `lookback` bars were cycle-like.
    """
    ok = dphase.between(360 / max_period, 360 / min_period)
    count = ok.rolling(lookback).sum()
    return (count >= need).where(count.notna())


def burg(x, order):
    """Burg's maximum-entropy AR fit. Returns a (a[0]=1) and residual power E.
    Model: x_t + a1 x_{t-1} + ... + ap x_{t-p} = e_t
    """
    x = np.asarray(x, dtype=float)
    f, b = x[1:].copy(), x[:-1].copy()
    a = np.array([1.0])
    E = np.dot(x, x) / len(x)
    for _ in range(order):
        k = -2 * np.dot(f, b) / (np.dot(f, f) + np.dot(b, b))
        a = np.concatenate([a, [0.0]])
        a = a + k * a[::-1]
        f, b = (f + k * b)[1:], (b + k * f)[:-1]
        E *= 1 - k * k
    return a, E


def mesa_burg(x, window=60, order=10, periods=np.arange(6, 51), horizon=5):
    """Rolling MESA on the detrended series. For each bar t uses x[t-window+1 .. t] only.

    Returns dominant period, strength (peak power / mean power across periods),
    and an AR forecast of the change in x over the next `horizon` bars.
    """
    x = pd.Series(x)
    vals = x.to_numpy()
    n = len(vals)
    dom = np.full(n, np.nan); strength = np.full(n, np.nan); fc = np.full(n, np.nan)
    k = np.arange(order + 1)
    E_mat = np.exp(-2j * np.pi * np.outer(1 / periods, k))      # (periods, order+1)
    for t in range(window - 1, n):
        w = vals[t - window + 1:t + 1]
        if np.isnan(w).any():
            continue
        w = w - w.mean()
        a, E = burg(w, order)
        spec = E / np.abs(E_mat @ a) ** 2
        j = int(np.argmax(spec))
        dom[t] = periods[j]
        strength[t] = spec[j] / spec.mean()
        hist = list(w[-order:])
        for _ in range(horizon):                                 # AR projection
            hist.append(-np.dot(a[1:], hist[::-1][:order]))
        fc[t] = hist[-1] - w[-1]
    return pd.DataFrame({"dom_period": dom, "strength": strength, "forecast_change": fc},
                        index=x.index)
