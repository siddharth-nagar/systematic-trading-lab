"""Causal implementations of the Kaufman Chapter 11, Part 4 tools (Maximum Entropy section).

Every function here produces a value at bar t using only bars <= t.
`tests_causality()` checks this by recomputing on truncated data.

Tools
-----
- highpass_detrend : Ehlers 2-pole high-pass + 4-bar WMA (causal detrending)
- hilbert_phase    : Kaufman p.516 Quadrature/InPhase, phase in Kaufman's convention
- mesa_burg        : rolling Burg (maximum entropy) spectrum -> dominant period, strength, forecast
- fisher           : Kaufman p.519 Fisher transform of channel position
- inverse_fisher_rsi : Kaufman p.520 inverse Fisher wrapped around RSI
"""
import numpy as np
import pandas as pd


# ---------------------------------------------------------------- detrending
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


# ---------------------------------------------------------------- Hilbert phase
def hilbert_phase(x):
    """Kaufman p.516 (Ehlers simplified Hilbert transform).

    Q = 0.0962 x_t + 0.5769 x_{t-2} - 0.5769 x_{t-4} - 0.0962 x_{t-6}
    I = x_{t-3}
    Returned phase uses Kaufman's convention: it rises 0 -> 360 through a cycle,
    trough ~ 90 degrees, peak ~ 270 degrees (Figure 11.19).
    """
    x = pd.Series(x)
    q = 0.0962 * x + 0.5769 * x.shift(2) - 0.5769 * x.shift(4) - 0.0962 * x.shift(6)
    i = x.shift(3)
    raw = np.degrees(np.arctan2(q, i))
    phase = (360 - raw) % 360
    dphase = (phase - phase.shift(1)) % 360          # forward advance per bar
    return pd.DataFrame({"Q": q, "I": i, "phase": phase, "dphase": dphase})


def cycle_mode(dphase, lookback=10, min_period=6, max_period=50, need=8):
    """Phase-regularity rule (Kaufman p.514: a regular sawtooth means a cycle is present).

    A bar is 'cycle-like' when the phase advanced by 360/max_period .. 360/min_period degrees.
    Cycle mode = at least `need` of the last `lookback` bars were cycle-like.
    """
    ok = dphase.between(360 / max_period, 360 / min_period)
    count = ok.rolling(lookback).sum()
    return (count >= need).where(count.notna())


# ---------------------------------------------------------------- MESA (Burg)
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


# ---------------------------------------------------------------- Fisher
def fisher(close, p=10, clip=0.999):
    """Kaufman p.519.
    X_t = 0.5*2*((P_t - MinL)/(MaxH - MinL) - 0.5) + 0.5*X_{t-1}
    y   = 0.5*ln((1+x)/(1-x));  trigger = y_{t-1}
    """
    c = np.asarray(close, dtype=float)
    hi = pd.Series(c).rolling(p).max().to_numpy()
    lo = pd.Series(c).rolling(p).min().to_numpy()
    X = np.zeros(len(c)); y = np.full(len(c), np.nan)
    for t in range(p - 1, len(c)):
        rng = hi[t] - lo[t]
        pos = (c[t] - lo[t]) / rng - 0.5 if rng > 0 else 0.0
        X[t] = np.clip(0.5 * 2 * pos + 0.5 * X[t - 1], -clip, clip)
        y[t] = 0.5 * np.log((1 + X[t]) / (1 - X[t]))
    y = pd.Series(y, index=getattr(close, "index", None))
    return pd.DataFrame({"fisher": y, "trigger": y.shift(1)})


# ---------------------------------------------------------------- Inverse Fisher on RSI
def rsi_wilder(series, n):
    d = series.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn)


def wma(series, n):
    w = np.arange(1, n + 1)
    return series.rolling(n).apply(lambda v: np.dot(v, w) / w.sum(), raw=True)


def inverse_fisher_rsi(close, mom=10, rsi_per=20, waper=30):
    """Kaufman p.520 (TradeStation code):
    series = close - close[mom]; x1 = 0.1*(RSI(series, rsi_per) - 50); x2 = WAVERAGE(x1, waper)
    invfisher = 100*(exp(2*x2) - 1)/(exp(2*x2) + 1)
    """
    s = close - close.shift(mom)
    x1 = 0.1 * (rsi_wilder(s, rsi_per) - 50)
    x2 = wma(x1, waper)
    return 100 * np.tanh(x2)          # identical to (e^(2x)-1)/(e^(2x)+1)


# ---------------------------------------------------------------- self-tests
def tests_causality(close, n_check=5):
    """Recompute every indicator on truncated data; values at the cut must match the full run."""
    full_hp = highpass_detrend(close)
    full = {
        "hp": full_hp,
        "phase": hilbert_phase(full_hp)["phase"],
        "fisher": fisher(close)["fisher"],
        "ifish": inverse_fisher_rsi(close),
    }
    rng = np.random.default_rng(0)
    for cut in rng.integers(500, len(close) - 50, n_check):
        c = close.iloc[:cut]
        hp = highpass_detrend(c)
        part = {"hp": hp, "phase": hilbert_phase(hp)["phase"],
                "fisher": fisher(c)["fisher"], "ifish": inverse_fisher_rsi(c)}
        for k in full:
            a, b = full[k].iloc[cut - 1], part[k].iloc[-1]
            assert (np.isnan(a) and np.isnan(b)) or abs(a - b) < 1e-9, (k, cut)
        m_full = mesa_burg(full_hp.iloc[cut - 80:cut + 20]).iloc[79]
        m_part = mesa_burg(hp.iloc[cut - 80:cut]).iloc[-1]
        assert np.allclose(m_full.to_numpy(), m_part.to_numpy(), equal_nan=True)
    return True


def tests_synthetic():
    t = np.arange(400)
    sine = pd.Series(10 * np.sin(2 * np.pi * t / 20))
    ph = hilbert_phase(sine)
    # phase must advance ~18 degrees/bar on average for a 20-bar cycle
    assert abs(ph["dphase"].iloc[50:].mean() - 18) < 0.5
    a, _ = burg(sine.to_numpy()[:60] - sine[:60].mean(), 10)
    m = mesa_burg(sine + np.random.default_rng(1).normal(0, 1, 400))
    assert abs(m["dom_period"].iloc[100:].median() - 20) <= 1
    f = fisher(pd.Series(100 + sine))
    assert np.isfinite(f["fisher"].dropna()).all()
    return True
