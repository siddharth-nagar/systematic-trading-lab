# Research 003 — Kaufman Ch.12 volume, open interest and breadth on NIFTY: pre-registered protocol

**Written 2026-10-23, before any NSE volume, open interest or breadth data was downloaded.** The commit that adds this file is the proof. Nothing below may change after the data is seen. Corrections go in a dated "Amendments" section with the reason, and anything added later is labelled exploratory.

## Data (fixed)

| Item | Choice |
|---|---|
| Returns | NIFTY 50 index daily OHLC, `data/nifty50_daily_2002_2026.csv` (same as Research 002) |
| Volume / OI | `data/nifty_futures_daily.csv`: **total traded value** (₹) and **total open interest × front-month settle** (₹) over all NIFTY futures expiries. Value is used instead of contracts because NIFTY lot sizes changed. |
| Breadth | `data/nse_breadth_daily.csv`: EQ-series advances, declines, up/down volume, 52-week new highs/lows |
| Period | From the first date all inputs exist (expected 2002-01) to 2026-03; warm-up excluded |
| In-sample / out-of-sample | 2002–2019 / 2020-01 to 2026-03, both always reported |

If `data/downloads/nse/build_report.txt` shows a level break across 2024-07-08 that cannot be explained, the affected series is used only up to 2024-07-05 and this is recorded as an amendment.

## Execution and costs (fixed, as Research 002)

Signals use data up to the close of day t; fills at the **open of day t+1** (`lib.backtest.run(fill='next_open')`). Costs 0.03% per side; stress case 0.10%. Price index only: no dividends, no futures roll or basis.

## Hypotheses

All parameters are the book's. No parameter is searched.

**H1 — OBV versus price (pp. 537–540).** A long-only 40-day MA trend rule applied to **OBV** (OBV above its 40-day MA, OBV built from futures value) is compared with the same rule applied to **price**. H0: equal Sharpe ratios. Statistic: Sharpe difference, 95% interval from a stationary block bootstrap (mean block 20 days, 5,000 resamples, seed 1203).

**H2 — Volume filter (Saitta, p. 556).** Long-only 20-day MA price trend; a new entry is taken only if that day's futures value exceeds its 10-day average. Compared with the unfiltered rule. H0: equal Sharpe. Same bootstrap. Exposure and trades per year reported.

**H3 — Volume spikes mark the end of a move (pp. 530, 554–555).** Spike: futures value > 2 × its 20-day average ending 5 days earlier (`lib.volume.volume_spike`). H0: after a spike, the next 5-day return (next open to close of day 5) has the same mean as on all days, separately for spikes after a 5-day rise and after a 5-day fall. Non-overlapping events only; Welch t-test.

**H4 — Breadth as countertrend (Connors, p. 558).** Events: (a) declines > advances for at least 3 consecutive days; (b) declines ≥ 2 × advances. H0: the next 5-day NIFTY return after an event equals the unconditional 5-day return. Non-overlapping events; Welch t-test. The book's US figures (+0.50% and +0.60% a week) are the reference.

**H5 — Breadth confirms the trend (p. 547).** Long-only 40-day MA trend on NIFTY, taken only while the A/D line is above its own 40-day MA, compared with the unfiltered rule. H0: equal Sharpe; same bootstrap.

**H6 — Price, volume and open interest states (p. 533).** Each day is classified by the 20-day direction of price, futures value and open interest (8 states). H0: the next 20-day return is the same in all states. Kruskal-Wallis test on non-overlapping 20-day blocks; mean, median and count reported for every state, including those against the book.

## Multiple testing

Six hypotheses → Holm correction across H1–H6 at a 5% family-wise level. Unadjusted p-values are reported as well. A result counts as supported only if it survives Holm in-sample **and** has the same sign out-of-sample.

## Reporting rules

- Report every hypothesis, including nulls and wrong-sign results.
- Each rule runs once with the parameters above. Variations (other periods, thresholds or data) are labelled exploratory and kept separate.
- Log each run in `experiments/log.csv` with its commit hash.

## Amendments

None yet.
