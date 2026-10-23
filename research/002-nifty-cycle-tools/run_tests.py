"""Research 002 — Kaufman Ch.11 Part 4 tools on NIFTY 50 daily data.

Protocol (fixed before running):
- Parameters are the book's / Ehlers' defaults. No optimisation.
- Signals use data up to the close of day t. Trades fill at the OPEN of day t+1.
- Costs: 0.03% per side base case (index futures: STT, exchange fees, slippage); 0.10% stress case.
- Report full period plus two fixed halves: 2002-2013 and 2014-2026.
- Price index only: no dividends, no futures roll/basis.

Run from this folder: python run_tests.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

import cycle_tools as ct

HERE = Path(__file__).resolve().parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
COST = 0.0003
COST_STRESS = 0.0010
HALVES = [("2002-2013", "2002-01-01", "2013-12-31"), ("2014-2026", "2014-01-01", "2026-12-31")]

df = pd.read_csv(HERE.parents[1] / "data" / "nifty50_daily_2002_2026.csv", parse_dates=["Date"], index_col="Date")
O, C = df["Open"], df["Close"]

# ------------------------------------------------------------------ indicators (all causal)
assert ct.tests_synthetic() and ct.tests_causality(C)
hp = ct.highpass_detrend(C)
hil = ct.hilbert_phase(hp)
cmode = ct.cycle_mode(hil["dphase"])
mesa = ct.mesa_burg(hp)
fis = ct.fisher(C)
ifish = ct.inverse_fisher_rsi(C)
sma50 = C.rolling(50).mean()

START = hp.first_valid_index() + pd.Timedelta(days=120)   # all warm-ups done
live = df.index >= START


# ------------------------------------------------------------------ backtest engine
def run(pos, cost=COST, fill="next_open"):
    """pos_t = position decided at the close of day t (+1 long, -1 short, 0 flat).

    next_open: old position earns close(t)->open(t+1); new position earns open(t+1)->close(t+1).
    same_close: new position earns close(t)->close(t+1) (needs a fill exactly at the signal close).
    """
    pos = pos.reindex(df.index).fillna(0).where(live, 0)
    if fill == "next_open":
        # Day t: overnight gap close(t-1)->open(t) is still carried by the position decided at close t-2;
        # at the open of t we switch to the position decided at close t-1.
        overnight = O / C.shift(1) - 1
        intraday = C / O - 1
        before_open = pos.shift(2).fillna(0)
        after_open = pos.shift(1).fillna(0)
        r = (1 + before_open * overnight) * (1 + after_open * intraday) - 1
        turnover = (after_open - before_open).abs()
    else:
        held = pos.shift(1).fillna(0)
        r = held * (C / C.shift(1) - 1)
        turnover = (held - pos.shift(2).fillna(0)).abs()
    r = r.fillna(0) - turnover * cost
    return r, pos, turnover


def stats(r, pos, turnover, mask=None):
    if mask is not None:
        r, pos, turnover = r[mask], pos[mask], turnover[mask]
    r = r[r.index >= START]
    pos, turnover = pos.loc[r.index], turnover.loc[r.index]
    yrs = len(r) / 252
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1
    vol = r.std() * np.sqrt(252)
    return {
        "CAGR %": round(100 * (eq.iloc[-1] ** (1 / yrs) - 1), 1),
        "Vol %": round(100 * vol, 1),
        "Sharpe": round(r.mean() * 252 / vol, 2) if vol > 0 else np.nan,
        "t-stat": round(r.mean() / r.std() * np.sqrt(len(r)), 2) if r.std() > 0 else np.nan,
        "MaxDD %": round(100 * dd.min(), 1),
        "Exposure %": round(100 * pos.abs().mean(), 0),
        "Turnover/yr": round(turnover.sum() / yrs, 1),
    }


def report(name, pos, results, curves=None):
    for label, cost in [("base", COST), ("stress", COST_STRESS)]:
        r, p, t = run(pos, cost)
        row = {"strategy": name, "costs": label, "period": "2002-2026", **stats(r, p, t)}
        results.append(row)
        if label == "base":
            for h, a, b in HALVES:
                results.append({"strategy": name, "costs": label, "period": h,
                                **stats(r, p, t, (r.index >= a) & (r.index <= b))})
            if curves is not None:
                curves[name] = (1 + r[r.index >= START]).cumprod()


def fwd_ret(h):
    """Return from the next open to the close h days later — what a trader acting on today's signal gets."""
    return C.shift(-h) / O.shift(-1) - 1


def ttest_mean(x):
    x = x.dropna()
    return round(x.mean() / x.std() * np.sqrt(len(x)), 2), len(x)


results, curves, diag = [], {}, {}

# ------------------------------------------------------------------ benchmarks
bh = pd.Series(1.0, index=df.index)
report("Buy & hold", bh, results, curves)
trend = np.sign(C - sma50).fillna(0)
report("SMA50 trend L/S (Ch.8 reference)", trend, results, curves)
report("SMA50 trend long-only (Ch.8 reference)", trend.clip(lower=0), results, curves)

# ------------------------------------------------------------------ 1. MESA
L = live & mesa["dom_period"].notna()
dp = mesa["dom_period"][L]
d = {}
d["share_at_longest_period_50"] = round(float((dp == 50).mean()), 3)
d["share_at_or_above_45"] = round(float((dp >= 45).mean()), 3)
d["median_dominant_period"] = float(dp.median())
d["median_abs_daily_change_in_period"] = float(dp.diff().abs().median())
d["share_days_period_jumps_gt5"] = round(float((dp.diff().abs() > 5).mean()), 3)
# Does the MESA forecast predict? compare forecast sign with what happened next.
real_hp = hp.shift(-5) - hp
fc = mesa["forecast_change"]
ok = L & real_hp.notna()
hit_hp = (np.sign(fc[ok]) == np.sign(real_hp[ok])).mean()
f5 = fwd_ret(5)
ok2 = L & f5.notna()
hit_px = (np.sign(fc[ok2]) == np.sign(f5[ok2])).mean()
up_base = (f5[ok2] > 0).mean()
strong = mesa["strength"] >= mesa["strength"].expanding(250).median()
ok3 = ok2 & strong
d["forecast_hit_rate_vs_detrended_next5"] = round(float(hit_hp), 3)
d["forecast_hit_rate_vs_price_next5"] = round(float(hit_px), 3)
d["forecast_hit_rate_vs_price_next5_strong_cycle_only"] = round(float((np.sign(fc[ok3]) == np.sign(f5[ok3])).mean()), 3)
d["base_rate_price_up_next5"] = round(float(up_base), 3)
# non-overlapping (every 5th day) significance of forecast-signed returns
signed = (np.sign(fc) * f5)[ok2].iloc[::5]
d["forecast_signed_return_tstat_nonoverlap"], d["n_nonoverlap"] = ttest_mean(signed)
diag["MESA"] = d
report("MESA forecast L/S", np.sign(fc).fillna(0), results, curves)
report("MESA forecast L/S, strong cycle only", (np.sign(fc) * strong).fillna(0), results)

# ------------------------------------------------------------------ 2. Phase angle
d = {}
cm = cmode[live].dropna()
d["share_time_cycle_mode"] = round(float(cm.mean()), 3)
dph = hil["dphase"][live]
d["share_bars_phase_moves_backwards_or_stalls"] = round(float(((dph > 180) | (dph < 1)).mean()), 3)
implied = (360 / dph[cmode[live] == 1]).replace(np.inf, np.nan)
d["median_implied_period_in_cycle_mode"] = round(float(implied.median()), 1)
# length of cycle-mode episodes
runs = (cm != cm.shift()).cumsum()
ep = cm.groupby(runs).agg(["first", "size"])
d["median_cycle_mode_episode_days"] = float(ep[ep["first"] == 1]["size"].median())
diag["Phase angle"] = d

# ------------------------------------------------------------------ 3. Ehlers lateral shift
er_fwd = (C.shift(-20) - C).abs() / C.diff().abs().rolling(20).sum().shift(-20)
er_past = (C - C.shift(20)).abs() / C.diff().abs().rolling(20).sum()
labels = {
    "Hilbert phase regular (cycle mode)": cmode == 1,
    "MESA strong cycle": strong,
    "Baseline: past ER20 below its median": er_past < er_past.expanding(250).median(),
}
lat = {}
for name, lab in labels.items():
    ok = live & lab.notna() & er_fwd.notna()
    a, b = er_fwd[ok & lab], er_fwd[ok & ~lab]
    # non-overlapping samples every 20 days
    s = pd.DataFrame({"er": er_fwd[ok], "lab": lab[ok]}).iloc[::20]
    diff = s[s.lab].er.mean() - s[~s.lab].er.mean()
    se = np.sqrt(s[s.lab].er.var() / s.lab.sum() + s[~s.lab].er.var() / (~s.lab).sum())
    lat[name] = {"share_of_time": round(float(lab[ok].mean()), 3),
                 "fwd_ER_when_cycle": round(float(a.mean()), 3),
                 "fwd_ER_otherwise": round(float(b.mean()), 3),
                 "difference": round(float(a.mean() - b.mean()), 3),
                 "t_nonoverlap": round(float(diff / se), 2)}
diag["Lateral shift (forward 20-day efficiency ratio; lower = choppier)"] = lat

# ------------------------------------------------------------------ 4. Hilbert cycle trades
ph = hil["phase"]
fwd_adv = (ph - ph.shift(1)) % 360
smooth = fwd_adv < 180
buy = (ph.shift(1) < 90) & (ph >= 90) & smooth          # trough passed
sell = (ph.shift(1) < 270) & (ph >= 270) & smooth       # peak passed
sig = pd.Series(np.nan, index=df.index)
sig[buy] = 1
sig[sell] = -1
hil_ls = sig.ffill().fillna(0)
report("Hilbert cycle L/S", hil_ls, results, curves)
report("Hilbert cycle long-only", hil_ls.clip(lower=0), results)
cyc_only = hil_ls.where(cmode == 1, 0).fillna(0)
report("Hilbert cycle L/S, cycle mode only", cyc_only, results)
f10 = fwd_ret(10)
d = {"n_buy_signals": int(buy[live].sum()), "n_sell_signals": int(sell[live].sum()),
     "fwd10_after_buy_%": round(100 * f10[buy & live].mean(), 2),
     "fwd10_after_sell_%": round(100 * f10[sell & live].mean(), 2),
     "fwd10_unconditional_%": round(100 * f10[live].mean(), 2)}
d["t_buy_minus_uncond"], _ = ttest_mean(f10[buy & live] - f10[live].mean())
d["t_sell_minus_uncond"], _ = ttest_mean(f10[sell & live] - f10[live].mean())
diag["Hilbert"] = d

# ------------------------------------------------------------------ 5. Fisher
F, T = fis["fisher"], fis["trigger"]
up = (F > T) & (F.shift(1) <= T.shift(1))
dn = (F < T) & (F.shift(1) >= T.shift(1))
plain = pd.Series(np.nan, index=df.index); plain[up] = 1; plain[dn] = -1
plain = plain.ffill().fillna(0)
report("Fisher trigger cross L/S", plain, results, curves)
ext_up = up & (F.shift(1) < -1)          # turning up just after an extreme low
ext_dn = dn & (F.shift(1) > 1)           # turning down just after an extreme high
ext = pd.Series(np.nan, index=df.index); ext[ext_up] = 1; ext[ext_dn] = -1
ext = ext.ffill().fillna(0)
report("Fisher after-extreme L/S", ext, results, curves)
report("Fisher after-extreme long-only", ext.clip(lower=0), results)
f5 = fwd_ret(5)
d = {}
x = fis["fisher"][live].dropna()
X_in = None
d["share_|fisher|>1.5"] = round(float((x.abs() > 1.5).mean()), 3)
d["n_after_extreme_buys"] = int(ext_up[live].sum())
d["n_after_extreme_sells"] = int(ext_dn[live].sum())
d["fwd5_after_extreme_buy_%"] = round(100 * f5[ext_up & live].mean(), 2)
d["fwd5_after_extreme_sell_%"] = round(100 * f5[ext_dn & live].mean(), 2)
d["fwd5_after_plain_up_cross_%"] = round(100 * f5[up & live].mean(), 2)
d["fwd5_unconditional_%"] = round(100 * f5[live].mean(), 2)
d["t_extreme_buy_minus_uncond"], _ = ttest_mean(f5[ext_up & live] - f5[live].mean())
d["t_extreme_sell_minus_uncond"], _ = ttest_mean(f5[ext_dn & live] - f5[live].mean())
diag["Fisher"] = d
# distribution before/after transform on real NIFTY data
hi10, lo10 = C.rolling(10).max(), C.rolling(10).min()
pos_raw = (2 * ((C - lo10) / (hi10 - lo10) - 0.5))[live].dropna()
hist_x = np.histogram(pos_raw, bins=np.linspace(-1, 1, 11))[0].tolist()
fz = x.clip(-2.5, 2.5)
hist_y = np.histogram(fz, bins=np.linspace(-2.5, 2.5, 11))[0].tolist()
diag["Fisher distribution"] = {"channel_position_bins": hist_x, "fisher_bins": hist_y}

# ------------------------------------------------------------------ 6. Inverse Fisher RSI
ifs = np.sign(ifish).fillna(0)
report("Inverse Fisher RSI L/S", ifs, results, curves)
report("Inverse Fisher RSI long-only", ifs.clip(lower=0), results, curves)
v = ifish[live].dropna()
diag["Inverse Fisher"] = {"share_|ift|>80": round(float((v.abs() > 80).mean()), 3),
                          "share_|ift|<20": round(float((v.abs() < 20).mean()), 3),
                          "median_days_between_sign_flips": float(
                              pd.Series(np.flatnonzero(np.diff(np.sign(v.to_numpy())) != 0)).diff().median())}

# ------------------------------------------------------------------ Regime switching (lateral shift as a system)
mr = hil_ls
switch = mr.where(cmode == 1, trend).fillna(0)
report("Switch: Hilbert in cycle mode, SMA50 trend otherwise", switch, results, curves)
reg = {}
for sys_name, p in [("SMA50 trend", trend), ("Hilbert cycle", hil_ls)]:
    r, pp, t = run(p)
    lab = (cmode == 1).shift(1).reindex(r.index)       # regime known at the signal close
    ok = (r.index >= START) & lab.notna()
    a_, b_ = r[ok & (lab == True)], r[ok & (lab == False)]
    reg[sys_name] = {"ann_return_%_in_cycle_mode": round(100 * 252 * a_.mean(), 1),
                     "ann_return_%_otherwise": round(100 * 252 * b_.mean(), 1),
                     "t_difference": round(float((a_.mean() - b_.mean()) / np.sqrt(a_.var() / len(a_) + b_.var() / len(b_))), 2)}
diag["Systems by regime (base costs)"] = reg

# ------------------------------------------------------------------ Look-ahead demonstrations
# (a) zero-phase FFT band-pass over the FULL sample: uses future prices -> not tradable
logp = 100 * np.log(C.to_numpy())
lin = np.polyval(np.polyfit(np.arange(len(logp)), logp, 1), np.arange(len(logp)))
spec = np.fft.rfft(logp - lin)
freqs = np.fft.rfftfreq(len(logp))
spec[(freqs < 1 / 48) | (freqs > 1 / 10)] = 0
bp = pd.Series(np.fft.irfft(spec, n=len(logp)), index=df.index)
ph_la = ct.hilbert_phase(bp)["phase"]
adv = (ph_la - ph_la.shift(1)) % 360 < 180
s2 = pd.Series(np.nan, index=df.index)
s2[(ph_la.shift(1) < 90) & (ph_la >= 90) & adv] = 1
s2[(ph_la.shift(1) < 270) & (ph_la >= 270) & adv] = -1
report("LOOK-AHEAD: Hilbert on full-sample FFT band-pass", s2.ffill().fillna(0), results, curves)
# (b) fill timing: same rule, filled at the signal-day close instead of next open
r, p, t = run(hil_ls, COST, fill="same_close")
results.append({"strategy": "Hilbert cycle L/S, filled at signal close", "costs": "base",
                "period": "2002-2026", **stats(r, p, t)})
r, p, t = run(plain, COST, fill="same_close")
results.append({"strategy": "Fisher trigger cross L/S, filled at signal close", "costs": "base",
                "period": "2002-2026", **stats(r, p, t)})

# ------------------------------------------------------------------ save
res = pd.DataFrame(results)
res.to_csv(OUT / "backtests.csv", index=False)
(OUT / "diagnostics.json").write_text(json.dumps(diag, indent=2, default=float))
pd.DataFrame(curves).resample("ME").last().round(4).to_csv(OUT / "equity_monthly.csv")
ts = pd.DataFrame({"close": C, "hp": hp, "phase": hil["phase"], "dphase": hil["dphase"],
                   "cycle_mode": cmode, "mesa_period": mesa["dom_period"],
                   "mesa_strength": mesa["strength"], "fisher": fis["fisher"], "inv_fisher": ifish})
ts.round(4).to_csv(OUT / "indicators_daily.csv")

pd.set_option("display.width", 200, "display.max_rows", 200)
print(res[res.costs == "base"].pivot_table(index="strategy", columns="period", values=["Sharpe", "CAGR %"], sort=False).to_string())
print(res[(res.period == "2002-2026")].to_string(index=False))
print(json.dumps(diag, indent=1, default=float))
