# Research 002 — Kaufman Ch.11 Part 4 cycle tools on NIFTY 50

**Question:** do the Maximum Entropy section tools (MESA, phase angle, Ehlers' lateral shift, Hilbert transform, Fisher, inverse Fisher) work on NIFTY daily data when used **without look-ahead** and with realistic execution?

**Status:** exploratory replication (Level 2). Parameters are the book's / Ehlers' defaults — nothing was optimised.

## Protocol (fixed before running)

| Item | Choice |
|---|---|
| Data | NIFTY 50 price index, daily OHLC, 2002-01 to 2026-03 ([provenance](data/DATA_PROVENANCE.md)) |
| Live test period | 2002-09 to 2026-03 (after indicator warm-up) |
| Signals | Computed from data up to the **close of day t** |
| Execution | Filled at the **open of day t+1** |
| Costs | 0.03% per side (futures-style: STT, fees, slippage); stress case 0.10% |
| Detrending | Causal Ehlers 2-pole high-pass (48 bars) + 4-bar WMA on 100·ln(price) |
| Stability | Two fixed halves: 2002–2013 and 2014–2026 |
| Not modelled | Dividends, futures roll/basis, margin, taxes |

Every indicator is checked by `cycle_tools.tests_causality()`: values recomputed on truncated data must equal the full-sample values.

## Results — Sharpe ratio (base costs)

| Strategy | 2002–2026 | 2002–2013 | 2014–2026 | CAGR % | MaxDD % |
|---|---:|---:|---:|---:|---:|
| Buy & hold | 0.75 | 0.79 | 0.74 | 14.5 | −59 |
| SMA50 trend long-only (Ch.8 reference) | **1.09** | 1.30 | 0.85 | 15.0 | −28 |
| MESA forecast L/S | −0.03 | −0.12 | 0.11 | −2.9 | −72 |
| Hilbert cycle L/S | −0.24 | −0.60 | 0.27 | −7.1 | −90 |
| Hilbert cycle long-only | 0.33 | 0.12 | 0.64 | 4.1 | −52 |
| Hilbert cycle L/S, cycle mode only | −0.47 | −0.71 | −0.15 | −6.0 | −82 |
| Fisher trigger cross L/S | 0.04 | 0.30 | −0.33 | −1.2 | −73 |
| Fisher after-extreme long-only | 0.41 | 0.38 | 0.49 | 5.4 | −52 |
| Inverse Fisher RSI long-only | 0.85 | 0.98 | 0.72 | 10.9 | −27 |
| Switch: Hilbert in cycle mode, SMA50 otherwise | 0.27 | 0.32 | 0.22 | 3.6 | −69 |
| **LOOK-AHEAD** Hilbert on full-sample FFT band-pass | 3.25 | 3.30 | 3.37 | 91.6 | −20 |

Full table with stress costs, volatility, t-stats, exposure and turnover: [`results/backtests.csv`](results/backtests.csv). Diagnostics: [`results/diagnostics.json`](results/diagnostics.json).

## Findings by tool

1. **MESA.** The dominant period sits at the longest allowed value (50) on 27% of days — the spectrum rises towards long periods (red noise), so the "dominant cycle" is often just the edge of the search range. The AR forecast predicts the *detrended filter* 67% of the time but predicts the *next 5 days of price* only 49% of the time, below the 56.5% you get by always guessing "up". It forecasts the smoothing, not the market.
2. **Phase angle.** NIFTY shows a regular sawtooth 38% of the time (Ehlers suggests ~20%), but cycle-mode episodes last a median of only **6 days**, with an implied period of ~14 days. The cycles are too brief to trade.
3. **Lateral shift.** Neither cycle detector predicts a choppier next 20 days (Hilbert t = 0.49, MESA t = −0.30). The SMA50 trend system did earn less when the phase was regular (6.2% vs 18.9% a year) but not significantly (t = −1.46), and the cycle system also earned less in cycle mode, so cycle mode did not identify where mean reversion works. Switching systems by regime lowered Sharpe from 0.66 to 0.27.
4. **Hilbert.** Average 10-day return after a "trough passed" buy signal is 0.55%, identical to the unconditional 0.56% (t = −0.01). Signals carry no turning-point information on NIFTY. Long-only results come from being long in a rising market about half the time.
5. **Fisher.** The transform works as described: channel position is U-shaped (55% of days in the two extreme bins) and Fisher output is bell-shaped. But trading the trigger cross means 174 position changes a year; at 0.10% per side CAGR falls to −12.6%. Filling at the signal-day close (Sharpe 0.37) instead of the next open (0.04) shows that most of the short-term edge is gone by the next morning's open.
6. **Inverse Fisher RSI.** Not bipolar on NIFTY daily data with Kaufman's parameters (|value| > 80 only 0.2% of the time). As a long/flat filter it reduced drawdown (−27% vs −59%) but did not beat a plain 50-day moving-average filter. It is a smoothed momentum indicator, not a cycle tool.
7. **Look-ahead trap.** The identical Hilbert rule on a zero-phase FFT band-pass of the full sample shows 91.6% CAGR and Sharpe 3.25. That filter uses future prices. This is why centred moving averages and full-sample spectral filters must never be used in a backtest.

## Interpretation and limits

- No cycle tool showed a tradable edge on daily NIFTY after costs with next-open execution.
- The only acceptable results came from trend/momentum filters, consistent with Ehlers' own view that a trader should prefer the dependability of the trend.
- One parameter set per tool; a different detrending cutoff or channel length could behave differently — but searching for it would be optimisation, which we deliberately avoid while reading the book.
- Secondary data source; 2002-09 one-week gap. Price index excludes dividends (~1–1.5%/yr), which understates buy-and-hold slightly.
- Several variants were tested: treat any single positive result as exploratory (multiple testing).

## Reproduce

```bash
pip install -r requirements.txt
cd 03_nifty_cycle_tools && python run_tests.py
```
