# Experiment Log

Use one entry per experiment. Keep experiments small while reading the book.

## Template

### Experiment ID
`YYYY-MM-DD-short-name`

### Question
What single question am I testing?

### Hypothesis
What market behaviour should make this work?

### Indicator / rule
Write the exact formula or rule.

### Data
Instrument, frequency, date range, source.

### Parameters
List them explicitly.

### Costs
Commission, spread, slippage assumptions.

### Result
Record only the metrics needed to answer the question.

### Failure modes
When or why did it fail?

### Decision
- [ ] Keep for later research
- [ ] Reject
- [ ] Needs more evidence
- [ ] Educational only

### Next action
One action only.

---

### Experiment ID
`2026-10-13-nifty-monthly-seasonality` (Research 001, recorded retrospectively)

### Question
Do NIFTY 50 calendar-month mean returns differ (Kaufman Ch.10)?

### Hypothesis
H0: all 12 calendar-month means are equal. H1: at least one differs.

### Indicator / rule
Monthly close-to-close returns; one-way F ratio; within-year permutation test (5,000 replicates, seed 7273).

### Data
NIFTY 50 price index, monthly, 2000–2025 (302 returns), secondary sources; six missing months in 2000–2001.

### Parameters
None optimised. Subperiods fixed: 2000–2012 and 2013–2025.

### Costs
Not applicable — descriptive/inferential, not a backtest.

### Result
F = 0.829, permutation p = 0.575. Do not reject equal means. See `02_nifty_seasonality/results/omnibus_report.md`.

### Failure modes
Low power with ~25 observations per month; unverified secondary data; regime changes over time.

### Decision
- [ ] Keep for later research
- [ ] Reject
- [x] Needs more evidence
- [ ] Educational only

### Next action
Reconcile missing months and conflicting closes against official NSE Indices data.

---

### Experiment ID
`2026-10-18-ch11-cycle-tools-nifty`

### Question
Do Kaufman's Ch.11 Maximum Entropy tools (MESA, phase angle, lateral shift, Hilbert, Fisher, inverse Fisher) give a tradable edge on NIFTY daily data without look-ahead?

### Hypothesis
Short-term cycles exist part of the time; when present, cycle tools time turns and mark sideways regimes (Ehlers: "if a short-term cycle exists, the market is not trending").

### Indicator / rule
Book/Ehlers formulas, causal high-pass detrend. Rules in `03_nifty_cycle_tools/run_tests.py`.

### Data
NIFTY 50 price index, daily OHLC, 2002-09 to 2026-03, secondary sources (see provenance).

### Parameters
Book defaults only: high-pass 48, MESA window 60 / order 10, Fisher channel 10, inverse Fisher 10/20/30, cycle mode 8 of 10 bars with period 6–50.

### Costs
0.03% per side; stress 0.10%. Fill at next open.

### Result
No cycle tool beat buy & hold or a 50-day MA filter. MESA price hit rate 49% vs 56.5% base rate. Hilbert buy signals: next-10-day return 0.55% vs 0.56% unconditional. Fisher cross: 174 changes/yr, destroyed by costs. Inverse Fisher long-only Sharpe 0.85 (vs SMA50 long-only 1.09). Look-ahead FFT version: Sharpe 3.25.

### Failure modes
Red-noise spectrum (dominant period at search edge), cycle episodes of ~6 days, overnight gaps remove short-term edges, costs on high-turnover rules.

### Decision
- [ ] Keep for later research
- [ ] Reject
- [ ] Needs more evidence
- [x] Educational only

### Next action
Continue Kaufman Ch.11 Part 5 (CCI, Short Cycle Indicator, Hurst phasing) — test phasing for the same look-ahead trap.

**Update 2026-10-19 (Part 5):** CCI (Lambert and fade readings, N = 20 and 8) gave no edge; CCI(20) inside ±100 only 54% of the time. Hurst phasing with a trailing MA20 = trend filter (long-only Sharpe 0.92); the centred-MA version shows Sharpe 2.88 — look-ahead. Chapter 11 complete; move to Chapter 12.

---

### Experiment ID
`2026-10-20-ch08-trend-systems-nifty` (lab: `01_kaufman/chapter_08_trend_systems/ch08_lab.ipynb`)

### Question
Do Kaufman's Chapter 8 trend-system findings hold on NIFTY daily data?

### Hypothesis
Fat-tailed runs make simple trend systems profitable; trendline signals beat price crosses; longer periods give better profit factors.

### Indicator / rule
Kaufman's systems (momentum, MA direction, exponential, N-day breakout, regression slope), price cross, Bollinger 20/2σ, Golden Cross 50/200.

### Data
NIFTY 50 price index, daily OHLC, 2002-10 to 2026-03 (`03_nifty_cycle_tools/data/`).

### Parameters
Kaufman's doubling set 5, 10, 20, 40, 80, 160 — whole profile reported, none selected.

### Costs
0.03% per side; default fill next open; Section 3 compares today's close / next open / next close.

### Result
Fat tail confirmed (runs ≥ 6 days: 5.1% vs 2.8% random; top 5 of 311 trades = 31% of gross profit). Profit factor rises with period up to 80 days. Price cross beat trendline on Sharpe at every period; same-day-close fills beat delayed fills. No long/short system beat buy & hold (Sharpe 0.76); long-only 40-day MA Sharpe 0.96, max DD −36% vs −59%.

### Failure modes
Shorting a strongly rising index; few trades at long periods (NDB-160 ≈ 16 trades); profit factor flattered by the long side.

### Decision
- [ ] Keep for later research
- [ ] Reject
- [ ] Needs more evidence
- [x] Educational only

### Next action
Chapter 12 (volume, open interest, breadth).

