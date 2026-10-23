"""Research 002, Part 5 — CCI and Hurst phasing on NIFTY daily data (Kaufman pp. 520-526).

Same protocol as run_tests.py: signals at the close of t, fills at the open of t+1,
0.03% per side (0.10% stress), book parameters only, two fixed halves.

The Short Cycle Indicator (Lorca) is NOT tested: it was designed for intraday bars,
has many fixed constants, and its second form uses an undefined term (C^2).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
COST, COST_STRESS = 0.0003, 0.0010
HALVES = [("2002-2013", "2002-01-01", "2013-12-31"), ("2014-2026", "2014-01-01", "2026-12-31")]

df = pd.read_csv(HERE.parents[1] / "data" / "nifty50_daily_2002_2026.csv", parse_dates=["Date"], index_col="Date")
O, H, L, C = df["Open"], df["High"], df["Low"], df["Close"]
START = pd.Timestamp("2002-09-17")          # same live start as run_tests.py
live = df.index >= START


def run(pos, cost=COST):
    pos = pos.reindex(df.index).fillna(0).where(live, 0)
    before_open, after_open = pos.shift(2).fillna(0), pos.shift(1).fillna(0)
    r = (1 + before_open * (O / C.shift(1) - 1)) * (1 + after_open * (C / O - 1)) - 1
    turnover = (after_open - before_open).abs()
    return (r.fillna(0) - turnover * cost), pos, turnover


def stats(r, pos, turnover, mask=None):
    if mask is not None:
        r, pos, turnover = r[mask], pos[mask], turnover[mask]
    r = r[r.index >= START]
    pos, turnover = pos.loc[r.index], turnover.loc[r.index]
    yrs = len(r) / 252
    eq = (1 + r).cumprod()
    vol = r.std() * np.sqrt(252)
    return {"CAGR %": round(100 * (eq.iloc[-1] ** (1 / yrs) - 1), 1),
            "Sharpe": round(r.mean() * 252 / vol, 2) if vol > 0 else np.nan,
            "t-stat": round(r.mean() / r.std() * np.sqrt(len(r)), 2) if r.std() > 0 else np.nan,
            "MaxDD %": round(100 * (eq / eq.cummax() - 1).min(), 1),
            "Exposure %": round(100 * pos.abs().mean(), 0),
            "Turnover/yr": round(turnover.sum() / yrs, 1)}


results = []


def report(name, pos):
    r, p, t = run(pos)
    results.append({"strategy": name, "period": "2002-2026", "costs": "base", **stats(r, p, t)})
    for h, a, b in HALVES:
        results.append({"strategy": name, "period": h, "costs": "base",
                        **stats(r, p, t, (r.index >= a) & (r.index <= b))})
    r, p, t = run(pos, COST_STRESS)
    results.append({"strategy": name, "period": "2002-2026", "costs": "stress", **stats(r, p, t)})


def hold_between(enter_long, enter_short):
    s = pd.Series(np.nan, index=df.index)
    s[enter_long] = 1
    s[enter_short] = -1
    return s.ffill().fillna(0)


diag = {}
report("Buy & hold", pd.Series(1.0, index=df.index))

# ------------------------------------------------------------------ CCI (Lambert, p.521)
def cci(n):
    x = (H + L + C) / 3
    xbar = x.rolling(n).mean()
    md = x.rolling(n).apply(lambda v: np.mean(np.abs(v - v.mean())), raw=True)
    return (x - xbar) / (0.015 * md)


for n in (20, 8):
    c = cci(n)
    v = c[live].dropna()
    diag[f"CCI({n}) share within +/-100"] = round(float(v.between(-100, 100).mean()), 3)
    # Lambert: above +100 = cyclic turn UP (go with it); below -100 = turn DOWN
    lambert = pd.Series(np.where(c > 100, 1, np.where(c < -100, -1, 0)), index=df.index)
    report(f"CCI({n}) Lambert: with the turn L/S", lambert)
    report(f"CCI({n}) Lambert: with the turn long-only", lambert.clip(lower=0))
    # Popular 'overbought/oversold' reading: fade the extremes
    report(f"CCI({n}) fade extremes L/S", -lambert)
    report(f"CCI({n}) fade extremes long-only", (-lambert).clip(lower=0))
    f5 = C.shift(-5) / O.shift(-1) - 1
    up_x = (c > 100) & (c.shift(1) <= 100) & live
    dn_x = (c < -100) & (c.shift(1) >= -100) & live
    diag[f"CCI({n}) fwd5 % after cross above +100"] = round(100 * float(f5[up_x].mean()), 2)
    diag[f"CCI({n}) fwd5 % after cross below -100"] = round(100 * float(f5[dn_x].mean()), 2)
    diag[f"CCI({n}) fwd5 % unconditional"] = round(100 * float(f5[live].mean()), 2)

# ------------------------------------------------------------------ Hurst phasing (pp. 523-526)
F, HS = 40, 20                       # Kaufman's 40-day example; half-span = 20
trail = C.rolling(HS).mean()         # what you actually know at the close of t
centred = C.rolling(HS).mean().shift(-HS // 2)   # 'phased' half-span: uses 10 FUTURE days


def turns(ma):
    up = (ma > ma.shift(1)) & (ma.shift(1) <= ma.shift(2))
    dn = (ma < ma.shift(1)) & (ma.shift(1) >= ma.shift(2))
    return up, dn


u, d = turns(trail)
honest = hold_between(u, d)
report("Hurst: half-span turns, trailing MA (honest) L/S", honest)
report("Hurst: half-span turns, trailing MA (honest) long-only", honest.clip(lower=0))
u2, d2 = turns(centred)
cheat = hold_between(u2, d2)
report("LOOK-AHEAD Hurst: half-span turns, centred MA L/S", cheat)
diag["Hurst honest: median days between turns"] = float(pd.Series(np.flatnonzero((u | d)[live])).diff().median())

# how late is the honest turn versus the centred one?
lag = []
cen_turn_days = np.flatnonzero((u2 | d2).to_numpy())
hon_turn_days = np.flatnonzero((u | d).to_numpy())
for t0 in cen_turn_days:
    later = hon_turn_days[hon_turn_days >= t0]
    if len(later):
        lag.append(later[0] - t0)
diag["Hurst: median days the trailing turn appears after the centred turn"] = float(np.median(lag))

res = pd.DataFrame(results)
res.to_csv(OUT / "backtests_part5.csv", index=False)
(OUT / "diagnostics_part5.json").write_text(json.dumps(diag, indent=2))
win = df.loc["2023-01-01":"2023-07-31"]
pd.DataFrame({"close": C, "trailing_ma20": trail, "centred_ma20": centred}).loc[win.index].round(1) \
    .to_csv(OUT / "hurst_window_2023H1.csv")

pd.set_option("display.width", 220, "display.max_rows", 100)
print(res[res.costs == "base"].pivot_table(index="strategy", columns="period",
                                           values=["Sharpe", "CAGR %"], sort=False).to_string())
print(res[(res.period == "2002-2026")].to_string(index=False))
print(json.dumps(diag, indent=1))
