"""Volume, open interest and breadth indicators (Kaufman Ch 12, pp. 527-564).

Conventions as in lib/indicators.py: pandas Series in and out, no look-ahead, warm-up bars NaN.
Accumulating indices (OBV, A/D line, ...) start at 0 on the first bar; only their changes matter.
Where the book's printed formula is wrong or ambiguous, the docstring says which version is used.
"""
import numpy as np
import pandas as pd

from lib.indicators import ema


# --- Basic volume (pp. 535-537) ------------------------------------------------

def normalized_volume(volume, n=50):
    """100 * V_t / average volume over the last n days (p. 535)."""
    return 100 * volume / volume.rolling(n).mean()


def volume_momentum(volume, n):
    return volume - volume.shift(n)


def volume_pct_change(volume, n):
    return volume / volume.shift(n) - 1


def force_index(close, volume, smooth=None):
    """Elder: (C_t - C_{t-1}) * V_t, optionally EMA-smoothed (2 for timing, 13 for trend; p. 536)."""
    raw = close.diff() * volume
    return raw if smooth is None else ema(raw, smooth)


def volume_oscillator(volume, short=14, long=34, method='ratio'):
    """Method 1 'diff': short MA - long MA. Method 2 'ratio': short sum / long sum (p. 537)."""
    if method == 'diff':
        return volume.rolling(short).mean() - volume.rolling(long).mean()
    if method == 'ratio':
        return volume.rolling(short).sum() / volume.rolling(long).sum()
    raise ValueError("method must be 'diff' or 'ratio'")


# --- Accumulating volume indices (pp. 537-542) ----------------------------------

def _accumulate(step):
    return step.fillna(0).cumsum()


def obv(close, volume):
    """Granville's On-Balance Volume: add volume on up closes, subtract on down closes (p. 537)."""
    return _accumulate(np.sign(close.diff()) * volume)


def filtered_obv(close, volume, n=20, volume_sd=None, price_sd=None):
    """OBV that skips low-volume days and/or small price moves (pp. 563-564).

    volume_sd: ignore days with V < mean(V, n) - volume_sd * sd(V, n).
    price_sd: ignore days with |change| < mean(change, n) + price_sd * sd(change, n), as printed.
    Thresholds use the previous n days only.
    """
    step = np.sign(close.diff()) * volume
    keep = pd.Series(True, index=close.index)
    if volume_sd is not None:
        thr = volume.rolling(n).mean().shift(1) - volume_sd * volume.rolling(n).std().shift(1)
        keep &= ~(volume < thr)
    if price_sd is not None:
        chg = close.diff()
        thr = chg.rolling(n).mean().shift(1) + price_sd * chg.rolling(n).std().shift(1)
        keep &= ~(chg.abs() < thr)
    return _accumulate(step.where(keep, 0.0))


def money_flow_index(high, low, close, volume, n=14):
    """MFI = 100 - 100/(1 + positive flow / negative flow), flows = typical price x volume.

    The book (p. 540) accumulates the flows over all history with no period; that makes the
    ratio drift towards a constant. The usual n-day rolling sums are used here.
    """
    tp = (high + low + close) / 3
    flow = tp * volume
    pos = flow.where(tp > tp.shift(1), 0.0).rolling(n).sum()
    neg = flow.where(tp < tp.shift(1), 0.0).rolling(n).sum()
    mfi = 100 - 100 / (1 + pos / neg.replace(0, np.nan))
    return mfi.fillna(100).where(pos.notna())          # no negative flow -> 100, as for RSI


def volume_count_indicator(volume):
    """+1 when volume rises, -1 when it falls, accumulated (p. 540)."""
    return _accumulate(np.sign(volume.diff()))


def volume_accumulator(high, low, close, volume):
    """Chaikin: ((C - L)/(H - L) - 0.5) * 2 * V, accumulated; zero when H == L (p. 540)."""
    pos = (close - low) / (high - low).replace(0, np.nan)
    return _accumulate((pos - 0.5) * 2 * volume)


def accumulation_distribution(open_, high, low, close, volume):
    """Chaikin A/D: (C - O)/(H - L) * V, accumulated (p. 541). Use the previous close for O if needed."""
    return _accumulate((close - open_) / (high - low).replace(0, np.nan) * volume)


def intraday_intensity(high, low, close, volume):
    """((C - L) - (H - C))/(H - L) * V, accumulated (p. 541)."""
    return _accumulate(((close - low) - (high - close)) / (high - low).replace(0, np.nan) * volume)


def price_volume_trend(close, volume):
    """(C_t/C_{t-1} - 1) * V_t, accumulated (p. 541). Not for back-adjusted futures."""
    return _accumulate(close.pct_change() * volume)


def positive_negative_volume_index(close, volume, method='fosback'):
    """Returns DataFrame (pvi, nvi).

    method='close' (book variation 1, p. 542): PVI adds V on up closes, NVI adds V on down closes.
    method='fosback' (standard, Fosback's Stock Market Logic): both start at 100; PVI moves by the
    day's % price change when volume rises, NVI when volume falls. The book's variation 2,
    'PVI + (C_t/C_{t-1}) x V_t', mixes the two and is not used.
    """
    if method == 'close':
        chg = close.diff()
        return pd.DataFrame({'pvi': _accumulate(volume.where(chg > 0, 0.0)),
                             'nvi': _accumulate(volume.where(chg < 0, 0.0))})
    if method == 'fosback':
        ret = close.pct_change().fillna(0)
        dv = volume.diff()
        pvi = 100 * (1 + ret.where(dv > 0, 0.0)).cumprod()
        nvi = 100 * (1 + ret.where(dv < 0, 0.0)).cumprod()
        return pd.DataFrame({'pvi': pvi, 'nvi': nvi})
    raise ValueError("method must be 'close' or 'fosback'")


def demand_oscillator(high, low, close, volume):
    """Aspray (pp. 542-543): BP - SP, with the losing side's volume divided by K x |% change|.

    K = 3*C_t / (10-day average of max(H_t, H_{t-1}) - min(L_t, L_{t-1})).
    On a small move K x |%| < 1, so the scaled side outweighs the winning side: a small up day
    can give a negative value. Bars with no price change return NaN.
    """
    rng2 = pd.concat([high, high.shift(1)], axis=1).max(axis=1) - pd.concat([low, low.shift(1)], axis=1).min(axis=1)
    k = 3 * close / rng2.rolling(10).mean()
    pct = close.pct_change()
    scaled = volume / (k * pct.abs()).replace(0, np.nan)
    bp = volume.where(pct > 0, scaled)
    sp = volume.where(pct < 0, scaled)
    return (bp - sp).where(pct != 0)


def vwmacd(close, volume, fast=12, slow=26, signal=0.20):
    """Volume-weighted MACD (p. 544): VWMA(fast) - VWMA(slow); signal = EMA with smoothing 0.20."""
    vwma = lambda n: (close * volume).rolling(n).sum() / volume.rolling(n).sum()
    line = vwma(fast) - vwma(slow)
    return line, line.ewm(alpha=signal, adjust=False).mean()


def elastic_vwma(close, volume, shares_outstanding):
    """Fries' eVWMA (p. 545): ((OS - V) * eVWMA_{t-1} + V * C) / OS. OS should exceed max volume."""
    out = np.empty(len(close))
    c, v = close.to_numpy(float), volume.to_numpy(float)
    out[0] = c[0]
    for t in range(1, len(c)):
        out[t] = ((shares_outstanding - v[t]) * out[t - 1] + v[t] * c[t]) / shares_outstanding
    return pd.Series(out, index=close.index)


# --- Spikes and filters (pp. 554-557, 564) --------------------------------------

def volume_spike(volume, n=20, multiple=2.0, lag=5):
    """True when V_t > multiple x average volume of n days ending `lag` days ago (p. 555).

    Lagging the average keeps a 2-3 day build-up from raising its own threshold.
    """
    return volume > multiple * volume.shift(lag).rolling(n).mean()


def market_facilitation_index(high, low, volume):
    """Bill Williams: (H - L) / V (p. 564)."""
    return (high - low) / volume.replace(0, np.nan)


# --- Breadth (pp. 546-558) ---------------------------------------------------------

def ad_oscillator(advances, declines):
    return advances - declines


def ad_line(advances, declines):
    """Advance-decline index: previous value + (advances - declines).

    The book (p. 547) prints 'ADI_{t-1} - Advances_t - Declines_t'; the sign is a misprint.
    """
    return _accumulate(advances - declines)


def demand_index(adv_volume, dec_volume, n=10):
    """Sibbett: sum of upside volume / sum of downside volume over n days (p. 548; Merrill: n = 5)."""
    return adv_volume.rolling(n).sum() / dec_volume.rolling(n).sum()


def bolton_tremblay(advances, declines, unchanged):
    """BT = (A - D)/U; index adds sqrt(|BT|) with BT's sign. The book (p. 548) takes sqrt(BT) of a
    negative number; the magnitude is used here."""
    bt = (advances - declines) / unchanged.replace(0, np.nan)
    return _accumulate(np.sign(bt) * np.sqrt(bt.abs()))


def schultz(advances, total):
    """Advances as a percentage of all issues (p. 548). The book says 0-100 but omits the x100."""
    return 100 * advances / total


def mcclellan_oscillator(advances, declines, s1=0.10, s2=0.05):
    """EMA(0.10) - EMA(0.05) of net advances, i.e. 19- and 39-day (p. 549)."""
    na = advances - declines
    return na.ewm(alpha=s1, adjust=False).mean() - na.ewm(alpha=s2, adjust=False).mean()


def upside_downside_ratio(adv_volume, dec_volume):
    return adv_volume / dec_volume.replace(0, np.nan)


def trin(advances, declines, adv_volume, dec_volume):
    """Arms Index: (A/D) / (AV/DV) (p. 550). Below 1 = volume favours advancing stocks."""
    return (advances / declines.replace(0, np.nan)) / (adv_volume / dec_volume.replace(0, np.nan))


def thrust_oscillator(advances, declines, adv_volume, dec_volume):
    """Chande: 100 x (A*AV - D*DV) / (A*AV + D*DV), bounded +/-100 (p. 550)."""
    up, down = advances * adv_volume, declines * dec_volume
    return 100 * (up - down) / (up + down).replace(0, np.nan)


def high_low_index(new_highs, new_lows):
    """HLX_t = HLX_{t-1} + NH - NL (p. 551)."""
    return _accumulate(new_highs - new_lows)


def high_low_ratio(new_highs, new_lows, n=10):
    """Sum NH / sum (NH + NL) over n days (p. 551); Appel buys above ~0.80-0.90."""
    return new_highs.rolling(n).sum() / (new_highs + new_lows).rolling(n).sum().replace(0, np.nan)


def chadtp(advances, declines, n=5):
    """Connors-Hayward: (sum of advances - sum of declines over n days) / n (p. 557)."""
    return (advances.rolling(n).sum() - declines.rolling(n).sum()) / n
