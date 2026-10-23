"""Price indicators used across the Kaufman labs.

Conventions:
- inputs and outputs are pandas Series aligned on the same index;
- a value at bar t uses only data up to and including bar t (no look-ahead);
- warm-up bars are NaN, never zero.
"""
import numpy as np
import pandas as pd


# --- Moving averages -------------------------------------------------------

def sma(series, n):
    return series.rolling(n).mean()


def ema(series, n):
    """Exponential MA with span n (alpha = 2/(n+1)), seeded from the first value."""
    return series.ewm(span=n, adjust=False).mean()


def wma(series, n):
    """Linearly weighted MA: weights 1..n, newest bar heaviest."""
    w = np.arange(1, n + 1)
    return series.rolling(n).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)


def triangular_weights(period):
    """Kaufman Ch 11: weights step up by 2/(P/2) to 2.0 at the centre, then down.

    An even period drops the oldest price so there is a centre (P = 10 -> 9 weights).
    """
    half = period // 2
    up = np.arange(1, half + 1) * (2.0 / half)
    return np.concatenate([up, up[-2::-1]])


def tma(series, period):
    w = triangular_weights(period)
    return series.rolling(len(w)).apply(lambda x: np.dot(x, w) / w.sum(), raw=True)


def triangular_macd(series, period):
    """TMA(P) - TMA(P/2): a smooth band-pass filter (Kaufman Ch 11)."""
    return tma(series, period) - tma(series, period // 2)


# --- Momentum and oscillators (Ch 9) ---------------------------------------

def momentum(series, n=20):
    return series - series.shift(n)


def rsi_wilder(series, n=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    avg_loss = loss.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(100).where(avg_gain.notna())


def stochastic_k(high, low, close, n=14):
    lowest = low.rolling(n).min()
    highest = high.rolling(n).max()
    denom = (highest - lowest).replace(0, np.nan)
    return 100 * (close - lowest) / denom


def macd(series, fast=12, slow=26, signal=9):
    line = ema(series, fast) - ema(series, slow)
    signal_line = ema(line, signal)
    return line, signal_line, line - signal_line


# --- Volatility and trend strength ------------------------------------------

def true_range(high, low, close):
    prev = close.shift(1)
    return pd.concat([high - low, (high - prev).abs(), (low - prev).abs()], axis=1).max(axis=1)


def atr(high, low, close, n=14):
    """Wilder's average true range."""
    return true_range(high, low, close).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def efficiency_ratio(series, n=10):
    """Kaufman's efficiency ratio: net change / sum of absolute bar changes, in [0, 1]."""
    direction = (series - series.shift(n)).abs()
    noise = series.diff().abs().rolling(n).sum()
    return direction / noise.replace(0, np.nan)


def adx(high, low, close, n=14):
    """Wilder's +DI, -DI and ADX. Returns a DataFrame with those three columns."""
    up = high.diff()
    down = -low.diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    smooth = lambda s: s.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    tr = smooth(true_range(high, low, close))
    plus_di = 100 * smooth(plus_dm) / tr
    minus_di = 100 * smooth(minus_dm) / tr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return pd.DataFrame({'plus_di': plus_di, 'minus_di': minus_di, 'adx': smooth(dx)})


# --- Cycle indicators (Ch 11) -----------------------------------------------

def cci(high, low, close, n):
    """Lambert's Commodity Channel Index. Uses the average (not the sum) for the mean."""
    x = (high + low + close) / 3
    mean = x.rolling(n).mean()
    mean_dev = x.rolling(n).apply(lambda w: np.abs(w - w.mean()).mean(), raw=True)
    return (x - mean) / (0.015 * mean_dev)


def fisher_transform(price, period=12):
    """Kaufman p. 519: smoothed channel position, then 0.5*ln((1+x)/(1-x))."""
    lo = price.rolling(period).min()
    hi = price.rolling(period).max()
    pos = ((price - lo) / (hi - lo).replace(0, np.nan) - 0.5).to_numpy()
    x = np.full(len(price), np.nan)
    prev = 0.0
    for i, v in enumerate(pos):
        if np.isnan(v):
            continue
        prev = np.clip(0.5 * 2 * v + 0.5 * prev, -0.999, 0.999)
        x[i] = prev
    return pd.Series(0.5 * np.log((1 + x) / (1 - x)), index=price.index)


def inverse_fisher_rsi(close, mom=10, rsi_period=20, wma_period=30):
    """Kaufman p. 520 (TradeStation code): bounded in [-100, 100]."""
    x2 = wma(0.1 * (rsi_wilder(close - close.shift(mom), rsi_period) - 50), wma_period)
    return 100 * (np.exp(2 * x2) - 1) / (np.exp(2 * x2) + 1)


def hilbert_phase(x, period):
    """Ehlers' 7-bar Hilbert transform phase angle in degrees, rising through each cycle.

    The input must be detrended. Q is scaled by Ehlers' gain correction (0.075*period + 0.54),
    which the book omits; `period` is the assumed cycle length.
    """
    x = pd.Series(x)
    gain_fix = 0.075 * period + 0.54
    Q = (0.0962 * x + 0.5769 * x.shift(2) - 0.5769 * x.shift(4) - 0.0962 * x.shift(6)) * gain_fix
    I = x.shift(3)
    return np.degrees(np.arctan2(I, Q)) % 360
